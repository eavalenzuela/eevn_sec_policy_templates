# eevn_sec_policy_templates

A reusable template-set for the **governance and policy layer** of an Information
Security Management System (ISMS) — the documented policies, procedures, standards,
and registers that frameworks like **HITRUST CSF**, HIPAA, SOC 2, and ISO 27001 are
assessed against.

This is the companion to `eevn_sec_test_templates`, which covers the *technical
application-security validation* layer (threat models, requirements, invariants,
findings). Where that repo answers *"did we build the app securely?"*, this repo
answers *"do we run a managed security program?"* The two are complementary inputs
to a HITRUST assessment.

The set is written **healthcare-first**: it assumes the organization is a HIPAA
Business Associate or Covered Entity handling PHI. HIPAA/healthcare-specific
documents live in `healthcare/`. The rest are general-purpose and apply to any
ISMS.

---

## Philosophy

- **Policy ≠ evidence.** A signed template scores poorly on its own. HITRUST r2
  grades each control on a maturity scale (Policy → Process → Implemented →
  Measured → Managed). These templates give you the *Policy* and *Process*
  layers; you still have to *operate* and *measure* them. Build early so controls
  have run-time before assessment.
- **Tailor, don't adopt blindly.** Every `[PLACEHOLDER]` is a decision you must
  make about *your* environment. A policy describing controls you don't actually
  perform is worse than no policy — it's a finding.
- **Living documents.** Every template carries a `Next Review` date (≤12 months)
  and a Version History. Auditors check that policies are reviewed, approved, and
  *followed*, not just that they exist.

---

## How to use

1. Copy the templates into the target project (a `docs/security/policies/` home is
   sensible, or keep this repo as the source of truth and publish rendered copies).
2. Read `_TEMPLATE.md.template` — it's the canonical skeleton every other document
   follows (metadata header, section order, framework-mapping table, version
   history). Don't break the structure; assessors rely on it.
3. Strip the `.template` suffix, fill the `[PLACEHOLDERS]`, and delete the
   `<!-- TEMPLATE: ... -->` guidance comments as you go.
4. Get each document **approved and signed** by the named approver, and record it
   in the Version History. Approval is itself an audit artifact.
5. Fill the **Framework Mapping** table once you map controls in HITRUST MyCSF —
   this turns the policy set into a navigable control library.

---

## Build order

Start with the **(P)** governance backbone, then risk, then operational policies.
Don't write all of them at once.

```
governance/   The program backbone — write these FIRST
risk/         Risk methodology + registers
asset-data/   Asset inventory, data classification, retention
access/        Access control, identity, JML, PAM, recertification
operations/   Change, SSDLC, vuln mgmt, crypto, logging, network, endpoint, backup
resilience/   Incident response, BCP, DR
vendor/       Third-party / supply-chain risk (BAA tracker lives with discovery artifacts)
people/        Awareness training, HR security, physical security
compliance/   Legal/regulatory register
healthcare/   HIPAA-specific: breach notification, NPP, minimum necessary,
              individual rights, de-identification, BAA management, sanctions
```

---

## Coverage index (document → HITRUST CSF mapping)

Every template carries a full Framework Mapping table (HITRUST CSF / HIPAA / SOC 2 / ISO 27001:2022) in its body. This index lists the primary **HITRUST CSF** control domains each document supports, so the set can be navigated as a control library. Refs are indicative starting points — confirm and complete them in MyCSF against your selected assessment scope.

### Governance (`governance/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-GOV-01 | Information Security Policy | 00 Info Security Mgmt Program; 04.a Policy Document |
| POL-GOV-02 | ISMS Scope Statement | 00 Info Security Mgmt Program; scoping/factor selection |
| POL-GOV-03 | Statement of Applicability (SoA) | All CSF domains (control selection traceability) |
| POL-GOV-04 | Roles & Responsibilities | 00 Mgmt Program; 02.a Roles and Responsibilities |
| POL-GOV-05 | Security Steering Committee Charter | 00 Mgmt Program; management commitment & oversight |
| POL-GOV-06 | Security Metrics & Objectives | 00 Mgmt Program; performance measurement |
| POL-GOV-07 | Management Review | 00 Mgmt Program; management review/evaluation |
| POL-GOV-08 | Internal Audit Program | 00 Mgmt Program; internal assessment |
| POL-GOV-09 | Corrective Action & POA&M | 00 Mgmt Program; corrective action plan |
| POL-GOV-10 | Document Control | 04.a Policy Document; 04.b Review of Policy |
| POL-GOV-11 | Exceptions & Waivers | 00 Mgmt Program; risk acceptance / exceptions |

### Risk (`risk/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-RSK-01 | Risk Management Methodology | 03.a Risk Mgmt Program; 03.b Performing Risk Assessments |
| REG-RSK-01 | Risk Register | 03.b Performing Risk Assessments; 03.c Risk Mitigation; 03.d Risk Evaluation |
| POL-RSK-02 | Risk Treatment Plan | 03.c Risk Mitigation; 03.d Risk Evaluation |
| POL-RSK-03 | Risk Acceptance | 03.c Risk Mitigation; 03.d Risk Evaluation; 05.h Authorization Process |

### Asset & Data (`asset-data/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-DAT-01 | Asset Management Policy | 07.a Inventory; 07.b Ownership; 07.c Acceptable Use; 07.d Classification |
| POL-DAT-02 | Data Classification & Handling | 07.d Classification; 06.d Data Protection & Privacy |
| POL-DAT-03 | Data Retention & Disposal | 06.c Records Retention; 09.p Disposal of Media |
| POL-DAT-04 | Acceptable Use Policy | 07.c Acceptable Use of Assets |

### Access (`access/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-AC-01 | Access Control Policy | 01.a Access Control Policy; 01.b/01.c; 01.v Information Access Restriction |
| POL-AC-02 | Identity & Authentication Policy | 01.d Password Mgmt; 01.q Identification & Authentication |
| POL-AC-03 | Joiner / Mover / Leaver Procedure | 01.b Registration/De-registration; 02.i Removal of Access Rights |
| POL-AC-04 | Privileged Access Management | 01.c Privilege Mgmt; 09.aa Audit Logging |
| POL-AC-05 | Access Recertification Procedure | 01.e Review of User Access Rights |
| POL-AC-06 | Remote Access Policy | 01.j External Connections; 01.y Teleworking; 09.m Network Controls |

### Operations (`operations/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-OPS-01 | Change Management Policy | 09.b Change Mgmt; 10.k Change Control Procedures |
| POL-OPS-02 | Secure SDLC Policy | 10.b Input Validation; 10.k Change Control; 10.m Vulnerability Mgmt |
| POL-OPS-03 | Vulnerability & Patch Management | 10.m Control of Technical Vulnerabilities; 09.b Change Mgmt |
| POL-OPS-04 | Configuration & Hardening Standard | 09 Comms & Ops Mgmt; 10.h Control of Operational Software |
| POL-OPS-05 | Cryptography & Key Management | 06.d Data Protection; 10.f Cryptographic Controls; 10.g Key Mgmt |
| POL-OPS-06 | Logging & Monitoring Policy | 09.aa Audit Logging; 09.ab Monitoring; 09.ac Protection of Logs |
| POL-OPS-07 | Network Security Policy | 01.m Segregation in Networks; 01.n Connection Control; 09.m Network Controls |
| POL-OPS-08 | Endpoint Security Policy | 08.j Mobile Computing; 09.j Controls Against Malicious Code |
| POL-OPS-09 | Backup Policy | 09.l Back-up; 12.c Continuity Plans |

### Resilience (`resilience/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-RES-01 | Incident Response Plan | 11.a–11.d Information Security Incident Management |
| POL-RES-02 | Business Continuity Plan | 12.a/12.b/12.c/12.e Business Continuity Management |
| POL-RES-03 | Disaster Recovery Plan | 12.c/12.d/12.e Continuity Plans; 09.l Back-up |

### Vendor (`vendor/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-VEN-01 | Third-Party Risk Management | 05.i External Party Risks; 05.k Third-Party Agreements; 09.e/09.f Service Delivery & Monitoring |

### People (`people/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-HR-01 | Security Awareness & Training | 02.e Awareness, Education, and Training |
| POL-HR-02 | HR Security Policy | 02.a/02.b/02.c/02.f/02.g Human Resources Security |
| POL-HR-03 | Physical & Environmental Security | 08.a/08.b/08.d Physical Security; 08.l Secure Disposal |

### Compliance (`compliance/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-CMP-01 | Legal & Regulatory Compliance | 06.a Compliance with Legal Requirements; 13 Privacy Practices |

### Healthcare / HIPAA (`healthcare/`)
| ID | Document | Primary HITRUST CSF refs |
|---|---|---|
| POL-HIP-01 | HIPAA Breach Notification Procedure | 11.a Reporting Events; 12 Privacy/breach controls |
| POL-HIP-02 | Notice of Privacy Practices & PHI Policy | 13 Privacy Practices, Notice & Consent; 19.a Notice |
| POL-HIP-03 | Minimum Necessary Standard | 13 Minimum Necessary; 01.b/01.c Access & Privilege Mgmt |
| POL-HIP-04 | Individual Rights Procedure | 19 Individual Participation & Access; 13 Privacy Practices |
| POL-HIP-05 | De-Identification & Limited Data Set | 13 De-identification of PHI; 06.d Data Protection |
| POL-HIP-06 | BAA Management Procedure | 05.i Third-Party Risks; 09.e/09.f Service Delivery & Monitoring |
| POL-HIP-07 | HIPAA Workforce Sanctions Policy | 02.f Disciplinary Process; 00 Mgmt Program |

> **Note on `00`:** HITRUST historically expressed governance under control category 0.0 / "Information Security Management Program." If your MyCSF object uses the newer numeric control IDs, re-map the governance rows accordingly during scoping.

---

## Document ID convention (lift verbatim)

| Domain | Prefix | Example |
|---|---|---|
| Governance | `POL-GOV-` | `POL-GOV-01` Information Security Policy |
| Risk | `POL-RSK-` | `POL-RSK-01` Risk Management Methodology |
| Asset & Data | `POL-DAT-` | `POL-DAT-02` Data Classification |
| Access | `POL-AC-` | `POL-AC-01` Access Control Policy |
| Operations | `POL-OPS-` | `POL-OPS-03` Vulnerability Management |
| Resilience | `POL-RES-` | `POL-RES-01` Incident Response Plan |
| Vendor | `POL-VEN-` | `POL-VEN-01` Third-Party Risk Management |
| People | `POL-HR-` | `POL-HR-01` Security Awareness Training |
| Compliance | `POL-CMP-` | `POL-CMP-01` Legal & Regulatory Compliance |
| Healthcare/HIPAA | `POL-HIP-` | `POL-HIP-01` Breach Notification Procedure |
| Procedures | `...-PROC-` | use where a doc is a procedure, not a policy |
| Registers/Logs | `REG-` | `REG-RSK-01` Risk Register |

---

## Document types

- **Policy** — "the organization shall…" Durable statements of intent and requirement.
- **Procedure** — step-by-step "how." Changes more often than the parent policy.
- **Standard** — specific technical baselines (e.g., hardening, crypto algorithms).
- **Register / Log** — living records (risk register, exceptions log, BAA tracker).
  These are templates for *structure*; the content is operational data.

---

## What this is not

- **Not legal advice.** The HIPAA documents reflect the regulations' structure but
  must be reviewed by counsel before use. Breach-notification timelines and state
  law overlays in particular need legal sign-off.
- **Not a HITRUST assessment.** These templates feed an assessment performed in
  MyCSF with an Authorized External Assessor; they don't replace it.
- **Not auto-compliant.** Filling in a template doesn't implement the control.
  The control must actually operate, and you must be able to evidence it.

---

## Origin

Built to complement `eevn_sec_test_templates` for a healthcare SaaS ISMS program
(AWS + Snowflake + GitHub stack). The control set is harmonized so that one policy
set maps cleanly across HITRUST CSF, HIPAA, SOC 2, and ISO 27001.
