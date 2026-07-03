#!/usr/bin/env python3
"""Instantiate the policy template set into a target directory.

Copies every ``<domain>/<name>.md.template`` to ``<out>/<domain>/<name>.md``,
substituting ``[PLACEHOLDER]`` values from a config file, optionally stripping
the ``<!-- TEMPLATE: ... -->`` guidance comments, and rewriting backticked
cross-references from ``*.md.template`` to the rendered ``*.md`` names so the
instantiated set links to itself. Finishes with a per-file count of remaining
placeholders — your tailoring worklist.

Config format (see ``tools/example.conf``): one substitution per line,
``KEY = value``, where KEY is the placeholder text without its brackets, e.g.::

    COMPANY = Acme Health, Inc.
    Security Officer / CISO = CISO
    CTO = VP Engineering

``#`` comments and blank lines are ignored. Keys are matched literally and
case-sensitively against the bracketed text. Placeholders you don't map are
left in place and reported.

Stdlib only. Examples:

    python3 tools/render.py --out ../myorg-policies --config myorg.conf
    python3 tools/render.py --out /tmp/preview --strip-comments
    python3 tools/render.py --out ../p --include governance --include risk
"""

import argparse
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAINS = [
    "governance",
    "risk",
    "asset-data",
    "access",
    "operations",
    "resilience",
    "vendor",
    "people",
    "compliance",
    "healthcare",
]

COMMENT_RE = re.compile(r"<!--.*?-->\n?", re.S)
XREF_RE = re.compile(r"`([^`\n]*?)\.md\.template`")
# a placeholder is a bracketed span that is not a markdown link's text
PLACEHOLDER_RE = re.compile(r"\[([^\[\]\n]+)\](?!\()")


def load_config(path):
    subs = {}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise SystemExit(f"{path}:{lineno}: expected 'KEY = value', got: {line}")
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if not key:
                raise SystemExit(f"{path}:{lineno}: empty key")
            subs[key] = value
    return subs


def render_text(text, subs, strip_comments):
    if strip_comments:
        text = COMMENT_RE.sub("", text)
        text = text.lstrip("\n")
    for key, value in subs.items():
        text = text.replace(f"[{key}]", value)
    text = XREF_RE.sub(lambda m: f"`{m.group(1)}.md`", text)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, help="target directory for the rendered set")
    parser.add_argument("--config", help="placeholder substitution file (KEY = value per line)")
    parser.add_argument(
        "--strip-comments",
        action="store_true",
        help="remove <!-- TEMPLATE: ... --> guidance comments from the output",
    )
    parser.add_argument(
        "--include",
        action="append",
        metavar="DOMAIN",
        choices=DOMAINS,
        help="render only these domain directories (repeatable; default: all)",
    )
    parser.add_argument(
        "--force", action="store_true", help="overwrite existing files in the target directory"
    )
    args = parser.parse_args()

    subs = load_config(args.config) if args.config else {}
    domains = args.include or DOMAINS

    out_root = os.path.abspath(args.out)
    if os.path.abspath(REPO_ROOT) == out_root:
        raise SystemExit("refusing to render into the template repo itself")

    rendered = []
    for domain in domains:
        src_dir = os.path.join(REPO_ROOT, domain)
        if not os.path.isdir(src_dir):
            continue
        for name in sorted(os.listdir(src_dir)):
            if not name.endswith(".md.template"):
                continue
            dst_dir = os.path.join(out_root, domain)
            dst = os.path.join(dst_dir, name[: -len(".template")])
            if os.path.exists(dst) and not args.force:
                raise SystemExit(f"{dst} exists (use --force to overwrite)")
            text = open(os.path.join(src_dir, name), encoding="utf-8").read()
            text = render_text(text, subs, args.strip_comments)
            os.makedirs(dst_dir, exist_ok=True)
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(text)
            rendered.append((os.path.relpath(dst, out_root), text))

    if not rendered:
        raise SystemExit("nothing rendered — check --include values")

    # include the canonical skeleton so `../_TEMPLATE.md` references resolve
    # in the rendered set (it is itself a controlled document per POL-GOV-10)
    skeleton_src = os.path.join(REPO_ROOT, "_TEMPLATE.md.template")
    skeleton_dst = os.path.join(out_root, "_TEMPLATE.md")
    if os.path.isfile(skeleton_src) and (args.force or not os.path.exists(skeleton_dst)):
        text = render_text(open(skeleton_src, encoding="utf-8").read(), subs, args.strip_comments)
        with open(skeleton_dst, "w", encoding="utf-8") as fh:
            fh.write(text)
        rendered.append(("_TEMPLATE.md", text))

    print(f"rendered {len(rendered)} documents to {out_root}\n")
    print("remaining placeholders to fill (tailoring worklist):")
    total = 0
    for rel, text in rendered:
        count = len(PLACEHOLDER_RE.findall(text))
        total += count
        print(f"  {count:4d}  {rel}")
    print(f"  {total:4d}  total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
