#!/usr/bin/env python3
"""Structural linter for the eevn_sec_policy_templates set.

Validates every ``<domain>/<name>.md.template`` against the conventions the
README and ``_TEMPLATE.md.template`` promise assessors:

* metadata header table with all required fields
* exactly one H1 title and a ``> **Status:**`` line
* required sections (Purpose, Scope, Roles, Exceptions, Framework Mapping,
  Related Documents, Version History)
* well-formed, unique Document IDs whose domain code matches the directory
* every backticked ``*.md.template`` cross-reference resolves on disk
* no nested HTML comments (an inner ``-->`` truncates the guidance block and
  leaks template instructions into the rendered document)
* the README coverage index and the templates on disk agree 1:1

Stdlib only. Exit code 0 = clean, 1 = findings. Run from anywhere:

    python3 tools/check_templates.py
"""

import argparse
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_CODES = {
    "governance": "GOV",
    "risk": "RSK",
    "asset-data": "DAT",
    "access": "AC",
    "operations": "OPS",
    "resilience": "RES",
    "vendor": "VEN",
    "people": "HR",
    "compliance": "CMP",
    "healthcare": "HIP",
}

REQUIRED_META = [
    "Document ID",
    "Version",
    "Classification",
    "Owner",
    "Approver",
    "Effective Date",
    "Last Reviewed",
    "Next Review",
    "Applies To",
]

REQUIRED_SECTIONS = [
    "Purpose",
    "Scope",
    "Roles & Responsibilities",
    "Exceptions",
    "Framework Mapping",
    "Related Documents",
    "Version History",
]

DOC_ID_RE = re.compile(r"^(POL|REG)-(GOV|RSK|DAT|AC|OPS|RES|VEN|HR|CMP|HIP)-\d{2}$")
XREF_RE = re.compile(r"`([^`\n]*?\.md\.template)`")
H1_RE = re.compile(r"^# (?!#)(.+)$", re.M)
SECTION_RE = re.compile(r"^## +(?:\d+\.|N(?:\+\d+)?\.)? *(.+?)\s*$", re.M)


def find_templates():
    """Yield repo-relative paths of all domain templates, sorted."""
    out = []
    for d in sorted(DIR_CODES):
        full = os.path.join(REPO_ROOT, d)
        if not os.path.isdir(full):
            continue
        for name in sorted(os.listdir(full)):
            if name.endswith(".md.template"):
                out.append(os.path.join(d, name))
    return out


def check_nested_comments(rel, text, problems):
    i = text.find("<!--")
    while i != -1:
        j = text.find("-->", i + 4)
        body = text[i + 4 : j] if j != -1 else text[i + 4 :]
        if "<!--" in body:
            problems.append(f"{rel}: nested '<!--' inside a comment block (breaks rendering)")
        if j == -1:
            problems.append(f"{rel}: unterminated HTML comment")
            break
        i = text.find("<!--", j + 3)


def check_xrefs(rel, text, problems):
    base = os.path.dirname(rel)
    for m in XREF_RE.finditer(text):
        # skip [`...`] placeholder examples — they are decisions, not links
        if text[max(m.start() - 1, 0)] == "[" and text[m.end() : m.end() + 1] == "]":
            continue
        ref = m.group(1)
        target = os.path.normpath(os.path.join(REPO_ROOT, base, ref))
        if not os.path.isfile(target):
            problems.append(f"{rel}: broken cross-reference `{ref}`")


def check_template(rel, ids, problems):
    text = open(os.path.join(REPO_ROOT, rel), encoding="utf-8").read()

    check_nested_comments(rel, text, problems)
    check_xrefs(rel, text, problems)

    h1s = H1_RE.findall(text)
    if len(h1s) != 1:
        problems.append(f"{rel}: expected exactly one H1 title, found {len(h1s)}")

    if "> **Status:**" not in text:
        problems.append(f"{rel}: missing '> **Status:**' line")

    for field in REQUIRED_META:
        if f"| {field} |" not in text:
            problems.append(f"{rel}: metadata table missing '{field}'")

    sections = SECTION_RE.findall(text)
    for required in REQUIRED_SECTIONS:
        candidates = [required]
        if required == "Roles & Responsibilities":
            # the roles document itself defines roles rather than referencing them
            candidates.append("Role Definitions")
        if not any(s == c or s.startswith(c) for s in sections for c in candidates):
            problems.append(f"{rel}: missing required section '{required}'")

    m = re.search(r"^\| Document ID \| (.+?) \|$", text, re.M)
    if not m:
        return None
    doc_id = m.group(1).strip()
    if not DOC_ID_RE.match(doc_id):
        problems.append(f"{rel}: malformed Document ID '{doc_id}'")
        return None
    domain = rel.split(os.sep, 1)[0]
    if doc_id.split("-")[1] != DIR_CODES[domain]:
        problems.append(
            f"{rel}: Document ID '{doc_id}' domain code does not match directory "
            f"'{domain}/' (expected -{DIR_CODES[domain]}-)"
        )
    if doc_id in ids:
        problems.append(f"{rel}: duplicate Document ID '{doc_id}' (also in {ids[doc_id]})")
    else:
        ids[doc_id] = rel
    return doc_id


def check_readme_index(ids, problems):
    """Reconcile the README coverage index with the templates on disk."""
    readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.isfile(readme_path):
        problems.append("README.md: missing")
        return
    text = open(readme_path, encoding="utf-8").read()

    section_re = re.compile(r"^### .+?\(`([a-z-]+)/`\)$", re.M)
    row_re = re.compile(r"^\| ((?:POL|REG)-[A-Z]+-\d{2}) \|", re.M)

    # map each index row to the directory of the section it sits under
    sections = [(m.start(), m.group(1)) for m in section_re.finditer(text)]
    listed = {}
    for m in row_re.finditer(text):
        doc_id = m.group(1)
        row_dir = None
        for start, d in sections:
            if start < m.start():
                row_dir = d
            else:
                break
        if doc_id in listed:
            problems.append(f"README.md: '{doc_id}' listed more than once in the coverage index")
            continue
        listed[doc_id] = row_dir

    for doc_id, rel in sorted(ids.items()):
        if doc_id not in listed:
            problems.append(f"README.md: '{doc_id}' ({rel}) missing from the coverage index")
        elif listed[doc_id] != rel.split(os.sep, 1)[0]:
            problems.append(
                f"README.md: '{doc_id}' listed under '{listed[doc_id]}/' but lives in "
                f"'{rel.split(os.sep, 1)[0]}/'"
            )
    for doc_id in sorted(listed):
        if doc_id not in ids:
            problems.append(f"README.md: coverage index lists '{doc_id}' but no template carries it")


def check_root_skeleton(problems):
    """The canonical skeleton only gets the rendering/link checks (its fields are placeholders)."""
    rel = "_TEMPLATE.md.template"
    path = os.path.join(REPO_ROOT, rel)
    if not os.path.isfile(path):
        problems.append(f"{rel}: missing")
        return
    text = open(path, encoding="utf-8").read()
    check_nested_comments(rel, text, problems)
    check_xrefs(rel, text, problems)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-q", "--quiet", action="store_true", help="only print findings, no summary")
    args = parser.parse_args()

    problems = []
    ids = {}
    templates = find_templates()
    for rel in templates:
        check_template(rel, ids, problems)
    check_root_skeleton(problems)
    check_readme_index(ids, problems)

    for p in problems:
        print(f"FAIL: {p}")
    if not args.quiet:
        print(
            f"checked {len(templates)} templates + _TEMPLATE.md.template + README index: "
            f"{len(problems)} problem(s)"
        )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
