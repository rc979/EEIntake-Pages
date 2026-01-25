
# EV Charging Site Project Plan

## Executive Summary

This document is the **master, traceable closeout deliverable** for an EV charging site electrical project. It presents a complete, phase-structured record of how an EV charging installation was engineered, reviewed, submitted, revised, and finalized, with every key decision tied back to its inputs and supporting evidence.

The plan is organized into **eight phases (Phase 1 through Phase 8)**. Within each phase, the document identifies the prerequisite inputs and how they were provided, establishes a stable evidence index (so files can be retrieved unambiguously), and summarizes how each deliverable was created (calculations, decision records, compilation/QA logs). It also preserves an audit trail of external review cycles—authority plan check and serving utility review—by capturing submission packages, receipts, comment logs, response letters, and approvals/finaled evidence.

The intent is not to restate every technical detail in prose, but to provide a defensible chain of custody: what information was relied on, how assumptions were verified and frozen, what artifacts were produced, and what evidence demonstrates acceptance at each checkpoint.

For readers who are not familiar with how electrical work is reviewed and validated in California, the **Introduction** section provides the operational context—how AHJs and utilities function as separate audit systems, why “written code” and “enforced code” diverge in practice, and why traceability and early risk characterization materially affect delivery outcomes.


## Table of Contents

- [Overview (includes Phase Overview)](#overview)
- [Introduction](#introduction)
- [Phase 1: Project Initiation and Feasibility](#phase-1)
- [Phase 2: Data Collection and Site Analysis](#phase-2)
- [Phase 3: System Design and Load Calculation](#phase-3)
- [Phase 4: Preliminary Drawing Set Production](#phase-4)
- [Phase 5: Permitting Submission](#phase-5)
- [Phase 6: Authority Review and Drawing Revision](#phase-6)
- [Phase 7: Utility Coordination](#phase-7)
- [Phase 8: Electrical Closeout and Handover](#phase-8)
- [Addendum A: Stable Filename Index (by Phase)](#addendum-a)
- [Addendum B: Party Directory (Roles + Contacts)](#addendum-b)

<a id="overview"></a>

## Overview
<a id="phase-overview"></a>

### Phase Overview (Deliverables by Phase)
#### Phase 1: Project Initiation and Feasibility

This phase establishes the foundational viability of the project.

* **Phase 1 Project Technical Intake Record**: Captures project identifiers, technical constraints, stakeholders/roles, and approvers. 
* **Phase 1 Feasibility Memo / Go–No-Go (Screening-Level)**: Uses Phase 1 inputs to determine preliminary electrical viability and define conditions to proceed. 
* **Phase 1 Input Register + Evidence Index**: Lists every prerequisite input with provenance (who/when/how provided), versioning, verification method, and evidence pointers. 
* **Phase 1 Assumption + Exclusion Register**: Records Phase 1 assumptions (with owners to validate) and explicit exclusions (including civil/constructability and business/cost/schedule). 
* **Phase 1 Preliminary Electrical Basis of Design (BOD)**: Freezes the Phase 1 “technical truth” set (or explicitly flags TBDs) used to seed later deliverables. 
* **Phase 1 Forward Traceability Map**: Shows how Phase 1 inputs/assumptions flow into deliverables in Phases 2–8.

#### Phase 2: Data Collection and Site Analysis

This phase involves gathering and standardizing all necessary information about the existing site.

* **Phase 2 Intake Checklist – Complete**: Requires Site plans (Owner/Architect), Panel schedules (Electrician), Photos (Installer), Charger SKUs (Installer/Vendor), and AHJ (Address). 
* **Phase 2 Normalized Site Data Package**: Requires Raw plans (Phase 2), Photos (Phase 2), and Schedules (Phase 2).

#### Phase 3: System Design and Load Calculation

The focus of this phase is on determining the site's electrical capacity and selecting the appropriate EV charging system architecture.

* **Phase 3 NEC Load Calculation**: Requires Panel schedules (Electrician), EVSE ratings (Manufacturer), and NEC methods (Code). 
* **Phase 3 EV System Architecture Decision**: Requires Load results (EE, Phase 3), Charger mix (Installer/Owner), and Site constraints (Phase 2).

#### Phase 4: Preliminary Drawing Set Production

This phase produces the necessary detailed **electrical** drawings required for permitting review.

* **Phase 4 Preliminary One-Line Diagram**: Requires Architecture decision (Phase 3), Service info (Utility bill/As-builts), and Charger specs (Manufacturer). 
* **Phase 4 Site Plan w/ EVSE Locations**: Requires Base site plan (Owner/Architect) and Parking layout (Owner). 
* **Phase 4 Conduit & Trenching Details**: Requires Routing assumptions (Installer) and Site conditions (Photos, Phase 2). 
* **Phase 4 Updated Panel Schedules**: Requires Existing schedules (Electrician) and New EV loads (EE, Phase 3). 
* **Phase 4 Electrical Notes & Code Sheets**: Requires Jurisdiction (Address) and Standard templates (Internal). 
* **Phase 4 Permit Drawing Set – Unstamped**: Requires One-line (Phase 4), Site plan (Phase 4), Details (Phase 4), Schedules (Phase 4), and Notes (Phase 4).

#### Phase 5: Permitting Submission

This phase focuses on the formal submission of documents required to obtain construction permits.

* **Phase 5 Stamped Permit Drawings**: Requires Unstamped drawing set (Phase 4). 
* **Phase 5 Permit Application Package**: Requires Stamped plans (Phase 5), Permit forms (AHJ), and Project metadata (Phase 2 / Phase 4).

#### Phase 6: Authority Review and Drawing Revision

This phase addresses any feedback or comments received from the AHJ and ensures that all drawing revisions are complete.

* **Phase 6 AHJ Comment Log – Parsed**: Requires Plan check comments (AHJ). 
* **Phase 6 Revised Drawings – Post-Comments**: Requires Comment log (Phase 6) and Prior drawings (Phase 4 / Phase 5). 
* **Phase 6 Comment Response Letter**: Requires AHJ comments (AHJ) and Revised drawings (Phase 6).

#### Phase 7: Utility Coordination

This phase handles all necessary applications and coordination with the local electrical utility company.

* **Phase 7 Utility Load Letter / Single-Line**: Requires Load calc (Phase 3) and Service info (Utility bill/As-builts). 
* **Phase 7 Utility Application Forms**: Requires Utility requirements (Utility portal) and Project data (Phase 3 / Phase 4).

#### Phase 8: Electrical Closeout and Handover

The final phase involves documenting the completed site and providing necessary support for final inspections and system activation.

* **Phase 8 As-Built Drawings**: Requires Field redlines (Electrician/Installer) and Inspector notes (AHJ). 
* **Phase 8 Inspection Support Responses**: Requires Inspector feedback (AHJ).

<a id="introduction"></a>

## Introduction

In California, electrical engineering work is validated externally by two independent authorities: the Authority Having Jurisdiction (AHJ) and the serving electrical utility. AHJs enforce the adopted California Electrical Code and local amendments through plan check and inspection. Utilities are not code enforcers; they manage grid and asset risk, reviewing added load, service impacts, fault duty, and—in EV projects—the credibility of any claimed load-management scheme. These entities do not coordinate with each other and do not participate in design. They review finished artifacts only.

In the San Francisco Bay Area, the AHJ is typically the city or county building department responsible for electrical permits. A multifamily EV project in Palo Alto, for example, is reviewed by the City of Palo Alto – Building Division, while a similar project nearby may face a different department with different amendments, reviewer expectations, and enforcement thresholds. The serving utility runs a parallel review with different criteria and timelines. Same written code, materially different enforcement outcomes.

Both AHJs and utilities operate as audit systems. They do not accept undocumented reasoning, verbal explanations, or implied engineering intent. Anything not written, indexed, and traceable is treated as nonexistent. Most comments and deficiencies are not about incorrect calculations but about failure to demonstrate how inputs flowed into outputs and whether assumptions were verified, frozen, and consistently applied. This is why written code ≠ enforced code in practice, and why designing purely to the most conservative interpretation everywhere results in systematic over-engineering.

Over-engineering is not a neutral safety margin in California; it is economically destructive. The state faces a chronic scarcity of licensed EEs and especially PEs, which drives very high labor costs. Every unnecessary design iteration, oversizing decision, or avoidable service upgrade consumes scarce senior hours that cannot be amortized. When firms respond to regulatory uncertainty with blanket conservatism, they burn the most expensive resource they have and compress margins without meaningfully reducing approval risk.

Modeling each AHJ—what they actually enforce, what they routinely question, and where they allow judgment—is therefore critical. Precise alignment to enforcement reality allows designs that are code-compliant, defensible, and no more complex than necessary. This reduces PE touch time, limits redesign cycles, and keeps projects within a labor envelope that is survivable given market scarcity.

Utilities must be modeled with the same rigor. Written utility standards, handbooks, or greenbooks do not reflect how load increases, EMS claims, or service constraints are actually reviewed in practice. Utilities differ materially in what they flag, what they defer, what they require upfront, and what they reopen later in the process. Treating utilities as deterministic rule engines leads to the same failure mode as over-interpreting code: unnecessary conservatism, late surprises, and unplanned rework. Capturing utility behavior—what documentation they demand, how they evaluate managed load, and where they apply discretion—is essential to avoiding service upgrades and uncontrolled scope growth.

Profitability depends on this discipline starting early. Correctly characterizing a project’s regulatory and utility risk at intake—based on service conditions, load posture, AHJ enforcement behavior, and utility sensitivity—and fitting it into a canonical, repeatable form is what enables accurate pricing. When risk is explicitly classified rather than discovered midstream, fees can reflect true exposure, delivery plans can be matched to risk class, and engineers can execute with confidence that the work is achievable within tolerable margins. In California EE practice, traceability, AHJ and utility modeling, and early risk canonicalization are prerequisites for operating profitably under scarcity and scrutiny.

The two comparison tables below make these claims concrete by showing how differences in grid/permit governance and liability structure can force additional phases, rework loops, or evidence requirements (relative to California).

### Comparative regulatory context (California vs. EU vs. Costa Rica)

| Category | California (USA) | European Union (EU) | Costa Rica | Phase Impact (EU/CR vs. CA) |
|:---|:---|:---|:---|:---|
| Grid Contract Status | Standard Customer: You request a utility service/meter upgrade (e.g., Taylor Nguyen). | Market Participant: You sign a bilateral GCA (Grid Connection Agreement) as an active grid asset. | Public Service User: You apply for a “Public Service Connection” from the state monopoly (ICE/CNFL). | Add Phase (EU): GCA Legal Negotiation & Signing. |
| GCA Throttling | Passive/Local: System is capped internally to protect building breakers. | Active/Remote: GCA legally permits the DSO to remotely throttle your load during grid stress. | Regulated Limit: Strict “Hosting Capacity” limits (often 15%) on local distribution circuits. | Add Phase (EU): DSO Signal Integration & Testing. |
| Market Operations | Open/Deregulated: Any business can sell energy by kWh/minute. Focus on uptime. | Harmonized (AFIR): Mandated ad-hoc payment, price transparency, and open roaming. | State Monopoly: Law 9518 restricts resale to utilities; private sites often offer “Free Amenity”. | Add Phase (EU): MSP/Roaming Integration. Modify (CR): Legal Resale Review. |
| Project Steward | CPO-Focused: The software vendor often “pilots” the project to ensure operational ROI. | DSO-Focused: The regulated Grid Operator is the gatekeeper of timelines and capacity terms. | EE/Consultor-Led: The licensed engineer is the steward, navigating the CFIA and ICE. | Shift: Stewardship moves from vendor to grid authority or engineer. |
| Technical Steward | EE Firm: Licensed PE (Priya Shah) stewards NEC 625.42 and the “Right to a Permit”. | EE Firm: Technical executor ensuring design meets both IEC and DSO-specific GCA signals. | EE Firm: Responsible for the Bitácora Digital (mandatory legal project log). | Add Task (CR): Continuous Bitácora Logging (Phase 3–7). |
| EMS Architecture | EE-Led: Design must be “fail-safe” to satisfy the AHJ and avoid $50k utility upgrades. | CPO-Driven: Software logic often dictates the load profile to match volatile energy markets. | EE-Led: Must prove site stability to prevent local transformer failure in residential zones. | Neutral: Responsibility shift within Phase 2. |
| Permit Authority | Ministerial (AHJ): Cities must approve per AB 1236 if health/safety codes are met. | Discretionary: Local municipalities often have “Urban Design” or “Public Realm” veto power. | APC (CFIA): Centralized digital platform where plans are validated by the National College of Engineers. | Add Phase (EU): Public Design Review. Consolidate (CR): Single APC track. |
| Compliance Check | PE Seal + AHJ: PE stamps plans; City Inspector performs the final field walk. | Independent Audit: Often requires a third-party certificate (e.g., TÜV, Consuel) before turn-on. | CFIA Validation: Final project “Seal of Approval” is issued via the digital Bitácora platform. | Add Phase (EU): Independent Regulatory Audit. |
| Significant Constraint | ADA Accessibility: Strict prescriptive design for van-spaces and accessible paths. | Grid Congestion: High-speed DC rollouts are often limited by local grid “waitlists”. | Environmental (SETENA): Coastal or protected zone projects require a lengthy environmental track. | Add Phase (CR): SETENA Environmental Screening. |

**Acronyms used above (not defined earlier in this document):**

- **AB 1236**: California Assembly Bill 1236 (EV charging “streamlined permitting” requirements for jurisdictions).
- **ADA**: Americans with Disabilities Act (accessibility requirements).
- **AFIR**: Alternative Fuels Infrastructure Regulation (EU).
- **CPO**: Charge Point Operator.
- **Consuel**: Comité National pour la Sécurité des Usagers de l’Électricité (France; common third‑party electrical conformity body).
- **DSO**: Distribution System Operator (EU).
- **GCA**: Grid Connection Agreement (EU).
- **IEC**: International Electrotechnical Commission (standards family widely used in the EU context).
- **MSP**: Mobility Service Provider (roaming/payment operator in EU charging ecosystems).
- **NEC**: National Electrical Code (US); in California this is adopted/amended via the California Electrical Code.

### Comparative liability context (California vs. Germany vs. Costa Rica)

| Category | California (USA) | Germany (EU) | Costa Rica |
|:---|:---|:---|:---|
| Primary Liability Basis | Tort & Negligence: Focus on “Duty of Care” and unlimited potential for indirect damages (loss of profit). | Statutory/Contractual: Governed by the BGB (Civil Code) and VOB; focus is on “Direct Damage” only. | Professional Responsibility: Governed by Law 3663 and CFIA; linked to the “Bitácora Digital” logs. |
| Personal vs. Corporate | Individual Signature: The PE who stamps the plans carries “Responsible Charge” and personal liability. | Corporate Focused: Liability typically sits with the firm (GmbH) as the contracting party under the BGB. | Personal & Solidary: The signing engineer and the firm are jointly liable for the 10-year stability. |
| Duration of Liability | 10 Years: Statute of repose for latent defects (California Code of Civil Procedure 337.15). | 5 Years: Standard warranty period for construction works under § 634a BGB. | 10 Years: Civil liability for structural/safety defects (Article 1185 of the Civil Code). |
| Damages Scope | Unlimited: Includes punitive and indirect damages if negligence is proven. | Capped/Direct: Usually limited to the cost of repair; “indirect damages” are excluded unless specifically in the contract. | Direct & Rectification: Focus on the legal obligation to fix the defect at the engineer’s expense. |
| Insurance Reality | High Premium: Professional Liability (E&O) is expensive and critical for risk mitigation. | Standardized: Coverage is often tied to the HOAI fee structure and is a market standard for firms. | The “Garantía”: Engineers often rely on a mandatory CFIA-backed guarantee or professional bond. |

<a id="phase-1"></a>

## Phase 1: Project Initiation and Feasibility
### Phase 1 Purpose and Boundaries 

Phase 1 exists to produce a **traceable, evidence-backed, screening-level** feasibility determination for the project’s electrical viability and to define the prerequisite inputs needed to complete later phases. 

**Phase 1 is NOT permit-grade engineering**. Any screening calculations in Phase 1 are explicitly **superseded by Phase 3 (NEC Load Calculation)** and must not be reused for permit submittals.

**NOTE:** The Phase 1 register fields below are filled with **example data** to demonstrate a “completed” deliverable package. Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 1.2 Project Technical Intake Record

| Field | Value |
|:---- |:---- |
| Project name | EV Charging Site Project |
| Site address | Place (Palo Alto, CA) |
| Building type | Multifamily residential (common-area charging) |
| Applicable code basis (prelim) | 2022 California Electrical Code (CEC) (confirm in Phase 2) |
| Electrical constraint | Use existing service; avoid service upgrade **unless unavoidable for code compliance** |
| Intended EVSE deployment (prelim) | 8 ports, Level 2 (confirm by cut sheets) |
| Primary stakeholders | Owner, Installer, Electrician, Engineer-of-Record, Project Manager |
| Technical approvers | Engineer-of-Record (final), Owner (program intent), Installer (equipment selection) |

### 1.3 Input Register + Evidence Index (Prerequisite Inputs)

This register is the authoritative list of Phase 1 inputs and **how they were provided**.

| Input ID | Input | Provenance (who / how / when) | Evidence reference ID(s) | Verification + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 1-I01 | Utility bills / usage history (≥12 months) | Nora Patel (Owner Rep)<br>Owner email + shared drive link<br>Received: 2026-01-08 (v1.0) | 1-I01 | Verify: service address + meter/account match; 12-month coverage<br>Used in: Phase 1, Phase 1, Phase 3, Phase 7 |
| 1-I02 | Service characteristics (rating, voltage/phase) | Luis Romero (Electrician) + utility portal export<br>Electrician upload + portal capture PDF<br>Received: 2026-01-09 (v1.1) | 1-I02 | Verify: nameplate vs utility letter; voltage/phase match<br>Used in: Phase 1, Phase 1, Phase 3, Phase 4, Phase 7 |
| 1-I03 | EVSE intent (make/model) | Mia Chen (Installer PM)<br>Installer email (PDF cut sheet)<br>Received: 2026-01-10 (v1.0) | 1-I03 | Verify: cut sheet ratings + OCPD guidance<br>Used in: Phase 1, Phase 1, Phase 2, Phase 3, Phase 3, Phase 4 |
| 1-I04 | Site photos (electrical gear + context) | Mia Chen (Installer PM)<br>Installer upload (photo set)<br>Received: 2026-01-10 (v1.0) | 1-I04 | Verify: readable ratings/labels + gear context<br>Used in: Phase 1, Phase 1, Phase 2 |

### 1.4 Assumption + Exclusion Register

#### 1.4.1 Exclusions (Scope Guardrails)

This master deliverable intentionally excludes:

- **Civil / constructability** topics (trenching, routing, demolition, means-and-methods, etc.)

#### 1.4.2 Assumptions

| Assumption ID | Assumption | Rationale + risk | Validation (owner + when) |
|:---- |:---- |:---- |:---- |
| 1-A01 | EV charging loads treated as continuous per applicable code | Rationale: standard EVSE treatment<br>Risk: under/over-sizing; feasibility error | Owner: Engineer-of-Record<br>Validate by: Phase 3 |
| 1-A02 | Service rating and voltage/phase match evidence | Rationale: screening requires best-available verified data<br>Risk: Phase 1 conclusions invalid | Owner: Electrician / EOR<br>Validate by: Phase 2 + Phase 3 |
| 1-A03 | EVSE may be provisional in Phase 1; frozen in Phase 2 | Rationale: SKU selection often finalizes after feasibility<br>Risk: Phase 1 estimates diverge materially | Owner: Installer<br>Validate by: Phase 2 |

### 1.5 Preliminary Electrical Basis of Design (BOD)

This BOD is the **single source of truth for Phase 1** and is the seed for later deliverables. Any “TBD” items must be closed in Phase 2.

| BOD Item | Value | Evidence (Input ID) | Status |
|:---- |:---- |:---- |:---- |
| Service rating | 800A | 1-I02 | Verified (nameplate + utility letter) |
| Service voltage/phase | 208Y/120V, 3-phase | 1-I02 | Verified (nameplate + utility letter) |
| EVSE quantity (ports) | 8 | 1-I03 | Verified (installer intent + cut sheet basis) |
| EVSE electrical characteristics | 208V, 3-phase; 32A continuous per port; 40A OCPD recommended | 1-I03 | Verified (cut sheet revA) |
| Load management posture | Required (aggregate cap to ≤250A service headroom) | 1-I01 + 1-I03 | Screening-level: confirm method/justification in Phase 3/Phase 3 |

### 1.6 Feasibility Memo / Go–No-Go (Screening-Level)

#### 1.6.1 Project Intent and Goal

The goal of this project is to deploy shared, common-area Level-2 EV charging for a multifamily residential building. The deployment must utilize existing electrical infrastructure without triggering a service upgrade, while preserving operational headroom and future expandability.

#### 1.6.2 Project Scope

* Install 8 Level-2 EVSE (approximately 7.6 kW each) in the garage common area. 
* Serve all EV loads from a dedicated EV subpanel fed from the existing 800A service. 
* Size all electrical infrastructure per NEC continuous-load requirements.

#### 1.6.3 Required Inputs Checklist (Phase 1)

The Phase 1 inputs are controlled by the **Phase 1 Input Register + Evidence Index** above. This memo references those inputs by ID to maintain provenance and traceability.

#### 1.6.4 Input Summaries and Analysis

#### 1.6.5 Utility Bills Summary (Owner)

The provided utility bills/usage history were analyzed to estimate existing service utilization. This is a screening-level assessment and must be cross-checked using the formal NEC methodology in Phase 3 (), using verified panel schedules and EVSE ratings.

| Key Metric | Value |
|:---- |:---- |
| Main Service Size | 800 Amps @ 208Y/120V |
| Peak Demand (Past 12 Mo.) | 550 Amps |
| Average Demand (Past 12 Mo.) | 380 Amps |
| Service Capacity Utilization (Peak) | 68.75% |
| Available Headroom (Peak) | 250 Amps |

The existing service has a **250 Amp** capacity margin based on the historical peak demand of 550 Amps (out of 800 Amps total).

#### 1.6.6 Service Size (Utility Bill)

The existing service is confirmed to be an **800 Amp, 208Y/120V, 3-Phase** service. This matches the data used in the utility bill analysis.

#### 1.6.7 Charger Intent (Installer/Owner)

The project intent is the installation of **8 Level-2 EVSE ports**. At Phase 1, the EVSE electrical characteristics may be provisional until manufacturer cut sheets are provided and frozen in Phase 2 ().

**Phase 1 screening approach:** to avoid false certainty, Phase 1 uses a bounded estimate based on available intent data and clearly states the conditions under which the result changes.

#### 1.6.8 Feasibility Memo / Go–No-Go

**Date:** 2026-01-12

**To:** Project Stakeholders (Owner, Installer, Electrician, Engineering)

**From:** Jordan Lee, Project Manager

**Subject:** Feasibility and Recommendation for Multifamily EV Charging Project

Based on the preliminary data collection and analysis (Phase 1.1), this memo assesses the viability of the proposed scope against the project goal of deploying 8 Level-2 EVSE without a service upgrade.

#### 1.6.9 Screening Calculation Basis (Not Permit-Grade)

Per applicable code requirements, EV charging loads are typically treated as continuous for feeder and equipment sizing. The **formal** load calculation methodology, demand factors (if applicable), and any load management justification must be documented in **Phase 3 ()** using verified inputs.

#### 1.6.10 Inputs used (by ID)
- Utility usage history: **1-I01**
- Service characteristics: **1-I02**
- EVSE intent (provisional): **1-I03**

#### 1.6.11 Method
Phase 1 computes a screening current envelope using best-available intent data and applies a continuous-load factor where appropriate. If EVSE cut sheets later show a higher continuous current than assumed here, Phase 1 conclusions must be revisited and may require load management or other architecture changes (Phase 3).

| Parameter | Calculation | Result |
|:---- |:---- |:---- |
| EVSE cut sheet continuous current (per port) | Per manufacturer cut sheet (revA) | 32 A |
| Unmanaged continuous feeder current (8 ports) | 8 \* (32 A \* 125%) | 320 A |
| Target managed aggregate cap | Service headroom basis (see below) | 250 A (cap) |

#### 1.6.12 Existing Service Headroom Analysis

| Parameter | Value (Amps) |
|:---- |:---- |
| Existing Service Size | 800 A |
| Historical Peak Demand | 550 A |
| Available Headroom | 250 A |
| Unmanaged EV load (continuous) | 320 A |
| Headroom deficit (unmanaged) | -70 A |
| Feasible path | Load management to cap EV demand at ≤250 A |

#### 1.6.13 Go/No-Go Criteria (Phase 1)

**GO** is valid only if all conditions below remain true after Phase 2 validation:

- Verified service characteristics (1-I02) match the screening basis (rating and voltage/phase).
- Verified EVSE cut sheets (1-I03 → frozen in Phase 2) do not materially increase the continuous current beyond the screening assumptions.
- Formal NEC/CEC load calculation (Phase 3) confirms compliance; if unmanaged loading exceeds headroom, a compliant load-management architecture must be adopted (Phase 3).

#### 1.6.14 Conclusion and Recommendation

**GO (Conditional – Managed Load Required)**

Based on screening-level inputs **1-I01 / 1-I02 / 1-I03**, the unmanaged code-continuous EV load for 8 ports is **320 A**, which exceeds the estimated **250 A** historical service headroom by **70 A**.

This is a **conditional GO** that requires a compliant **load management / EMS** approach in Phase 3 (/Phase 3) to cap aggregate EV demand at or below the available headroom, or an alternate approach (e.g., fewer ports or different EVSE ratings) to be validated by the Engineer-of-Record.

### 1.7 Next Steps

Proceed to **Phase 2: Data Collection and Site Analysis** to (a) freeze EVSE cut sheets and electrical characteristics in the intake package (Phase 2) and (b) verify service/gear data. Then proceed to **Phase 3** to complete the formal load calculation (Phase 3) and system architecture decision (Phase 3).

### 1.8 Forward Traceability Map (Phase 1 → Later Deliverables)

This map explains how Phase 1 inputs are used to craft deliverables in later phases.

| Later deliverable | Crafted from Phase 1 items | Notes |
|:---- |:---- |:---- |
| Phase 2 Intake Checklist – Complete | Phase 1 (Input Register) | Phase 1 defines required evidence and provenance fields that Phase 2 must complete/verify. |
| Phase 2 Normalized Site Data Package | Phase 1 (BOD) + Phase 1 (Assumptions) | Phase 1 sets the “truth set” that Phase 2 must confirm and normalize. |
| Phase 3 NEC Load Calculation | 1-I02 + 1-I03 + Phase 1 | Phase 3 supersedes Phase 1 screening; Phase 1 documents what was assumed and what must be validated. |
| Phase 3 EV System Architecture Decision | Phase 1 (criteria) + Phase 3 results | Phase 1 defines the decision constraint (use existing service unless unavoidable) and conditions that trigger load management. |
| Phase 4 Preliminary One-Line Diagram | 1-I02 + Phase 1 | Phase 1 establishes service basis and initial BOD identifiers; Phase 4 depicts the engineered architecture selected in Phase 3. |
| Phase 7 Utility Load Letter / Single-Line | 1-I01 + 1-I02 | Phase 1 records usage history and service basis; Phase 7 uses the validated versions. |


<a id="phase-2"></a>

## Phase 2: Data Collection and Site Analysis
This section documents the completion of **Phase 2: Data Collection and Site Analysis** for the Electric Vehicle (EV) Charging Project. Phase 2 gathers, verifies, and normalizes the **electrical design prerequisites** into a controlled package suitable for engineering (Phase 3).

**NOTE:** The Phase 2 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, evidence pointers, and logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 2.1 Phase 2 Boundaries (Electrical-Only)

Phase 2 captures information required to perform electrical engineering and code compliance tasks. It intentionally excludes:

- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)

### 2.2 Intake Checklist – Complete

This checklist confirms the acquisition of required Phase 2 inputs and links each item to an evidence record in **Phase 2**. Acceptance criteria are included to make “Complete” auditable.

| Input ID | Input | Source | Status | Acceptance criteria (electrical-only) | Verified by | Date |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 2-I01 | Site plans (electrical context excerpts) | Owner/Architect | Complete | Includes service room location and electrical-room plan excerpts; revision/date visible | Priya Shah (Project Engineer) | 2026-01-18 |
| 2-I02 | Panel schedules (MDP + relevant subpanels) | Electrician | Complete | Legible; identifies main breaker rating, bus rating, voltage/phase, spare spaces; latest revision noted | Priya Shah (Project Engineer) | 2026-01-18 |
| 2-I03 | Photo set (service gear + nameplates + breaker labels) | Installer | Complete | Nameplates readable; includes context + closeups; photos indexed/annotated | Priya Shah (Project Engineer) | 2026-01-18 |
| 2-I04 | EVSE cut sheets (final for design basis) | Installer/Vendor | Complete | Includes electrical ratings, continuous current, OCPD guidance; revision identified; matches program intent | Priya Shah (Project Engineer) | 2026-01-18 |
| 2-I05 | AHJ + adopted electrical code edition | Owner/Address + AHJ website | Complete | Electrical permitting authority identified; code edition and amendments source recorded | Jordan Lee (Project Manager) | 2026-01-18 |

### 2.3 Input Register + Evidence Index (Stable Filenames)

This register records **how inputs were provided** and where they are stored. File names are stable and referenced throughout the master deliverable.

| Input ID | Input | Provenance (who / how / when) | Evidence reference ID(s) | Verification + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 2-I01 | Site plans (electrical context excerpts) | Nora Patel (Owner Rep)<br>Owner email + shared drive link<br>Received: 2026-01-15 (v2.0) | 2-I01 | Verify: revision/date + title block + electrical-room location<br>Derived from: 1-I04 (context)<br>Used in: Phase 2, Phase 2, Phase 4 |
| 2-I02 | Panel schedules (MDP + relevant subpanels) | Luis Romero (Electrician)<br>Electrician upload (PDF)<br>Received: 2026-01-16 (v1.0) | 2-I02 | Verify: cross-check MDP ratings vs 1-I02; legibility; spare spaces<br>Derived from: 1-I02<br>Used in: Phase 2, Phase 2, Phase 3, Phase 4 |
| 2-I03 | Photo set (service gear + nameplates + labels) | Mia Chen (Installer PM)<br>Installer upload (photo set + index)<br>Received: 2026-01-16 (v1.0) | 2-I03 | Verify: nameplates readable; photos correspond to MDP + meter/service gear<br>Derived from: 1-I02 + 1-I04<br>Used in: Phase 2, Phase 2, Phase 4 |
| 2-I04 | EVSE cut sheets (final for design basis) | Mia Chen (Installer PM)<br>Installer email (PDF)<br>Received: 2026-01-16 (revA) | 2-I04 | Verify: voltage/phase + continuous current + OCPD; matches Phase 1 intent<br>Derived from: 1-I03<br>Used in: Phase 2, Phase 2, Phase 3, Phase 3, Phase 4 |
| 2-I05 | AHJ + code basis evidence | Jordan Lee (PM)<br>AHJ website capture + notes<br>Received: 2026-01-17 (v1.0) | 2-I05 | Verify: AHJ name + adopted code edition + capture metadata<br>Derived from: N/A<br>Used in: Phase 2, Phase 2, Phase 4, Phase 5 |

### 2.4 Key Excerpts (Electrical-Only)

To satisfy master-deliverable traceability, the following excerpts capture the **minimum critical information** needed to proceed. Full documents remain indexed in **Phase 2**.

#### 2.4.1 Site Plans – Electrical Context Excerpts (2-I01)

**Excerpted findings (from plan title block and electrical-room plan excerpt):**

- Building address and revision/date shown on drawings (Rev 2, 2026-01-15).
- Electrical service room identified on plan (label: “Electrical Room / Main Switchgear”).
- Service entry point and main electrical gear room boundary shown for reference (no routing/constructability assumptions made here).

#### 2.4.2 Panel Schedules – MDP Excerpt (2-I02)

**Excerpted data (MDP schedule header and key fields):**

- Panel designation: **MDP**
- Main device: **800A main**
- Bus rating: **800A**
- System: **208Y/120V, 3-phase**
- Available spaces: **4 (3-pole)**

#### 2.4.3 Photo Set – Nameplate/Label Verification Excerpts (2-I03)

**Excerpted verifications (from annotated photo index):**

- MDP nameplate confirms **800A**, **208Y/120V**, **3-phase**.
- Meter/service labeling matches the service characteristics used in Phase 1.
- Breaker labeling is legible for engineering validation of schedules (no field-modification assumptions made).

#### 2.4.4 EVSE Cut Sheet – Electrical Rating Excerpt (2-I04)

**Excerpted electrical basis (from cut sheet revA):**

- Model: **ElectriCharge L2-7.6-G**
- Supply: **208V, 3-phase**
- Continuous current: **32A**
- Recommended OCPD: **40A**

#### 2.4.5 AHJ / Code Basis – Evidence Excerpt (2-I05)

**Excerpted jurisdiction basis:**

- Electrical permitting authority (AHJ): **City of Palo Alto – Building Division (Electrical Permits)** (as documented in evidence capture)
- Adopted code basis: **2022 California Electrical Code (CEC)** (source captured in 2-I05)

### 2.5 Required Input Details

#### 2.5.1 Site Plans

The site plans confirm the location of the primary service/electrical room and provide electrical-context plan excerpts for engineering reference. Phase 2 does not assert installation routing, trenching, or constructability.

#### 2.5.2 Panel Schedules (Electrician)

The schedules below are for the Main Distribution Panel (MDP), confirming the service details and available space.

* **Panel Designation:** MDP 
* **Main Service:** 800A Main 
* **Bus Rating:** 800A 
* **Service Voltage:** 208Y/120V, 3-Phase 
* **Connected Load:** 550A 
* **Available Spaces:** 4 (Three-Pole)

#### 2.5.3 Photos (Installer)

Photos were taken to document the existing main service gear and the physical conditions of the proposed installation location.

#### 2.5.4 Charger SKUs (Installer/Vendor)

The selected EVSE model specifications are detailed below.

| Parameter | Value |
|:---- |:---- |
| Model Name | ElectriCharge L2-7.6-G |
| Output Power | 7.6 kW (Nominal) |
| Voltage | 208V, 3-Phase |
| Continuous Current Draw | 32A @ 208V |
| Required OCPD Size | 40A |

#### 2.5.5 Authority Having Jurisdiction (AHJ)

The electrical permitting jurisdiction and adopted code basis are confirmed (see 2-I05 evidence capture).

| Data Point | Value |
|:---- |:---- |
| Jurisdiction (Electrical) | City of Palo Alto – Building Division (Electrical Permits) |
| Site Address | Place (Palo Alto, CA) |
| Applicable Code | 2022 California Electrical Code (CEC) |

### 2.6 Normalized Site Data Package

The raw inputs from **Phase 2/Phase 2** have been processed, cross-referenced, and standardized into a controlled package for engineering use. This ensures all teams reference consistent, verified figures and stable filenames.

### 2.7 Normalization Rules (Document Control)

The following rules were applied to create a consistent engineering package:

- **File naming**: `P1.2_<Category>_<Descriptor>_<YYYY-MM-DD>.<ext>`
- **PDF standard**: all PDFs normalized to portrait orientation where feasible, searchable text (OCR applied when needed), and bookmarks added for long sets
- **Redactions**: personal information removed where present (non-technical)
- **Revisions**: latest revision is used; superseded versions retained but marked “Superseded” in filenames
- **Extraction**: key electrical data extracted into tables for engineering use; extraction sources are cited back to `Phase 2` evidence pointers

### 2.8 Normalization / Validation Log (Raw → Normalized)

| Log ID | Raw → Normalized (evidence IDs) | Transformation performed | Validated (by/date) |
|:---- |:---- |:---- |:---- |
| P1-N01 | Raw: 2-I01 → Out: Phase 2 Electrical-context plan excerpts | Extracted electrical-room/service-context sheets; bookmarks; OCR verified | Priya Shah / 2026-01-18 |
| P1-N02 | Raw: 2-I02 → Out: Phase 2 Normalized panel schedules | Cleaned scan; OCR; standardized order; header callouts | Priya Shah / 2026-01-18 |
| P1-N03 | Raw: 2-I03 → Out: Phase 2 Annotated photo index | Selected nameplate/label photos; annotated; created index | Priya Shah / 2026-01-18 |
| P1-N04 | Raw: 2-I04 → Out: Phase 2 EVSE cut sheet (frozen for design) | Marked “Frozen for design basis”; extracted ratings summary | Priya Shah / 2026-01-18 |
| P1-N05 | Raw: 2-I05 → Out: Phase 2 AHJ/code basis evidence | Verified AHJ naming; standardized capture; recorded metadata | Jordan Lee / 2026-01-18 |

The following table summarizes standardized data points derived from Phase 2 inputs and their normalized outputs.

| Data Element | Standardized Value | Notes |
|:---- |:---- |:---- |
| Electrical context plan excerpts | `P1.2_SitePlans_ElectricalContext_Excerpts_2026-01-18.pdf` | Electrical-room/service context only; no routing assumptions. |
| Panel schedule package (MDP + relevant) | `P1.2_PanelSchedules_Normalized_MDP_Subpanels_2026-01-18.pdf` | Used for Phase 3 load calc and Phase 4 schedule updates. |
| EVSE design-basis cut sheet | `P1.2_EVSE_CutSheet_FrozenForDesign_revA_2026-01-18.pdf` | Frozen for Phase 3 design basis. |
| AHJ/code basis evidence | `P1.2_AHJ_CodeBasis_Normalized_2026-01-18.pdf` | Supports code sheets and permit application package. |
| Service gear photo index | `P1.2_Photos_Annotated_Index_2026-01-18.pdf` | Confirms ratings/labels used in Phases 1, 3, and 4. |
| Utility coordination contact (technical) | Utility account rep: Taylor Nguyen  | Technical point of contact for Phase 7 coordination. |

### 2.9 Data Standardization Certification

The data package is formally certified for completeness and integrity.

| Certification Point | Status | Certified By | Date |
| ----- | ----- | ----- | ----- |
| Data Integrity | Certified | Priya Shah (Project Engineer) | 2026-01-18 |
| File Format Standardization | Certified | Ethan Brooks (Document Control) | 2026-01-18 |
| Completeness Check | Certified | Jordan Lee (Project Manager) | 2026-01-18 |

### 2.10 Next Steps

Phase 2 is complete. The **Normalized Site Data Package (Phase 2)** is finalized and is the required input for all subsequent design and engineering activities.

The project proceeds to **Phase 3: System Design and Load Calculation**, using the certified data package (Phase 2) to perform the NEC Load Calculation (Phase 3) and determine the final EV System Architecture (Phase 3).


<a id="phase-3"></a>

## Phase 3: System Design and Load Calculation
#### 3.1.1 EV Charging Project Plan: Phase 3 Documentation

This section formalizes the outputs of **Phase 3: System Design and Load Calculation** for the Electric Vehicle (EV) Charging Site Project. Phase 3 uses the controlled Phase 2 package (Phase 2) to produce a **permit-relevant electrical load calculation** and an **architecture decision record** suitable to seed the drawing set in Phase 4.

**NOTE:** The Phase 3 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, stable evidence pointers, and decision logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 3.2 Phase 3 Boundaries (Electrical-Only)

Phase 3 captures information required to perform electrical engineering and code compliance tasks. It intentionally excludes:

- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)

The goal of Phase 3 is to confirm that the proposed EV charging system is electrically viable and compliant with the applicable code basis (CEC/NEC as adopted by the AHJ), and to select a compliant system architecture that satisfies the project’s electrical constraint of avoiding a service upgrade unless unavoidable.

### 3.3 Phase 3 Evidence Index + Engineering Work Products

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 3-W01 | Load calculation workbook + summary | Priya Shah, PE <br>Spreadsheet + PDF export<br>Date: 2026-01-22 (v1.0) | [`phases/P2/Outputs/P2.1_LoadCalc_Workbook_2026-01-22.xlsx`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.1_LoadCalc_Workbook_2026-01-22.xlsx.html)<br>[`phases/P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf) | Inputs: Phase 2 panel schedules + EVSE cut sheet + AHJ/code basis<br>Used in: Phase 3, Phase 4, Phase 5, Phase 7 |
| 3-W02 | Independent load calc check memo | Alex Kim, EE <br>Redline review + sign-off<br>Date: 2026-01-22 (v1.0) | [`phases/P2/Outputs/P2.1_LoadCalc_CheckMemo_2026-01-22.pdf`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.1_LoadCalc_CheckMemo_2026-01-22.pdf) | Inputs: 3-W01<br>Used in: Phase 3 |
| 3-W03 | Architecture decision record | Priya Shah, PE <br>Engineering memo + diagram<br>Date: 2026-01-22 (v1.0) | [`phases/P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf) | Inputs: 3-W01 + Phase 2 evidence<br>Used in: Phase 3, Phase 4, Phase 4, Phase 4 |
| 3-W04 | EMS technical brief | Mia Chen (Installer PM)<br>Vendor PDF<br>Date: 2026-01-21 (revB) | [`phases/P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf`](https://rc979.github.io/EEIntake/phases/P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf) | Inputs: N/A<br>Used in: Phase 3, Phase 4, Phase 4 |

### 3.4 Key Excerpts (Electrical-Only)

#### 3.4.1 Load Calc Summary Excerpt (3-W01)

**Excerpted results:**

- EVSE continuous current basis: **32A per port** (from Phase 2 EVSE cut sheet)
- Continuous load factor applied per code basis: **125%**
- Aggregate unmanaged EV continuous load: **320A**
- Available historical headroom basis (screening, from Phase 1): **250A**
- Outcome: unmanaged load **exceeds headroom**; a compliant load-management method is required to avoid service upgrade

#### 3.4.2 Independent Check Excerpt (3-W02)

**Excerpted check outcome:** “Calculation logic and arithmetic verified; inputs align to Phase 2 evidence pointers; conclusions supported.”

#### 3.4.3 Architecture Decision Excerpt (3-W03)

**Excerpted decision:** “Proceed with a 400A bus-rated EV subpanel with feeder sized for the full unmanaged continuous load, combined with a listed EMS/load management method to cap aggregate demand to ≤250A.”

### 3.5 NEC Load Calculation

The NEC Load Calculation confirms the exact electrical capacity required for the new EV charging infrastructure. This calculation is mandatory for permitting (Phase 5) and utility coordination (Phase 7).

| Input | Source (evidence ID) |
|:---- |:---- |
| Panel schedules | 2-I02 (normalized in Phase 2) |
| EVSE ratings | 2-I04 (frozen for design in Phase 2) |
| AHJ/code basis | 2-I05 (normalized in Phase 2) |

#### 3.5.1 Load Calculation Summary (NEC 625.42 \- Continuous Load)

Based on the required 8 Level-2 EVSE and the NEC 625.42 requirement for 125% continuous loading:

| Parameter | Calculation | Result |
|:---- |:---- |:---- |
| Single EVSE Continuous Load | 32A \* 125% | 40 A |
| Total New Connected Load | 8 EVSE \* 40 A | 320 A |
| Required Subpanel Bus Rating | 320 A | **400 A** |
| Required Subpanel Feeder Breaker | 320 A | **350 A** |

**Conclusion:** The total NEC continuous load is **320 Amps**. This confirms that the previously available **250 Amps** of service headroom (Phase 1) is *insufficient* to support the full, unmanaged, NEC-mandated continuous load.

#### 3.5.2 Service Headroom Re-Evaluation

Phase 1 () established that an unmanaged, code-continuous EV load for 8 ports would exceed the available historical headroom and therefore requires a managed load approach. The formal Phase 3 calculation confirms **320 Amps** unmanaged continuous load versus **250 Amps** available headroom, necessitating an **Energy Management System (EMS)** (or another compliant demand/management method) per NEC 625.42(A)(2).

| Parameter | Value (Amps) |
|:---- |:---- |
| Existing Service Size | 800 A |
| Historical Peak Demand | 550 A |
| Available Headroom (Unmanaged) | 250 A |
| Required New EV Load (Unmanaged) | 320 A |
| Load Deficit (Triggering Service Upgrade) | \-70 A |

The project must proceed with an EMS, or the core project goal of avoiding a service upgrade (Phase 1) is invalid.

### 3.6 EV System Architecture Decision

This phase selects the system components and architecture to manage the required 320A load within the 250A service headroom using a Load Management System.

| Input | Source |
|:---- |:---- |
| Load results | EE (Phase 3) |
| Charger mix | Installer/Owner (Phase 2 EVSE basis) |
| Existing electrical conditions | Phase 2 (panel schedules + photos) |
| Load management technical basis | 3-W04 (EMS technical brief) |

#### 3.6.1 System Architecture Proposal

To reconcile the 320A required load with the 250A available headroom, the system must incorporate an EMS that limits the total current draw of the EV subpanel to **250 Amps**.

| Element | Specification | Rationale |
|:---- |:---- |:---- |
| **Subpanel Feeder** | 350A feeder OCPD (3-pole) | Sized for the full 320A continuous load per NEC. |
| **EV Subpanel Bus** | 400A Rated | Sized for the full 320A continuous load per NEC. |
| **EMS System** | Integrated Panel-level EMS | Limits total current draw to **250 Amps** to fit within service headroom. |
| **Charger Count** | 8 Level-2 EVSE | No change to the original project scope. |
| **Charger Circuits** | 40A OCPD, 8 circuits | Individual circuits are sized per the NEC for each charger's continuous load. |

#### 3.6.2 Decision

**EV System Architecture Decision: Managed Load System (Go)**

The project will utilize a 400A bus-rated EV subpanel fed by a 350A breaker, integrated with an EMS to dynamically limit the total demand to **250 Amps**. This meets all requirements: NEC compliance (via subpanel rating) and project goal (via EMS management to avoid service upgrade).

### 3.7 Phase 3 Engineering Certification

| Certification Point | Status | Certified By | Date |
|:---- |:---- |:---- |:---- |
| Load calculation prepared | Certified | Priya Shah, PE  | 2026-01-22 |
| Independent check completed | Certified | Alex Kim, EE  | 2026-01-22 |
| Architecture decision documented | Certified | Priya Shah, PE  | 2026-01-22 |
| Inputs traceable to Phase 2 evidence pointers | Certified | Ethan Brooks (Document Control) | 2026-01-22 |

### 3.8 Next Steps

Phase 3 is complete. The system architecture and exact load requirements are confirmed.

The project proceeds to **Phase 4: Preliminary Drawing Set Production**. The outputs of Phase 3, including the Phase 3 Load Calculation and the Phase 3 Architecture Decision, are the mandatory inputs for all drawings in Phase 4\.


<a id="phase-4"></a>

## Phase 4: Preliminary Drawing Set Production
#### 4.1.1 EV Charging Project Plan: Phase 4 Documentation

This section formalizes the outputs of **Phase 4: Preliminary Drawing Set Production** for the Electric Vehicle (EV) Charging Site Project. Phase 4 translates the approved system design (Phase 3\) into an **unstamped electrical permit drawing set** suitable for engineering stamp (Phase 5) and AHJ electrical review.

**NOTE:** The Phase 4 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and compilation logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 4.2 Phase 4 Boundaries (Electrical-Only)

Phase 4 captures permit-drawing content required for electrical engineering and code compliance. It intentionally excludes:

- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)

The goal of Phase 4 is to produce the **unstamped electrical permit drawing set** that incorporates the electrical design and code requirements confirmed in Phases 1 and 2\.

### 4.3 Evidence Index + Drawing Work Products (Stable Filenames)

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 4-W01 | Preliminary one-line diagram (sheet) | Sam Ortega (CAD Tech, ) + Priya Shah, PE <br>CAD + PDF export<br>Date: 2026-01-26 (v1.0) | [`phases/P3/Outputs/P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf) | Inputs: Phase 3 decision; Phase 2 schedules; Phase 2 EVSE; Phase 2 code basis<br>Used in: Phase 4, Phase 4 |
| 4-W02 | Site plan w/ EVSE locations (electrical-impacting) | Sam Ortega (CAD Tech, )<br>CAD + PDF export<br>Date: 2026-01-26 (v1.0) | [`phases/P3/Outputs/P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf) | Inputs: base site plan (owner/architect) + parking layout (owner) + Phase 2 context<br>Used in: Phase 4, Phase 4 |
| 4-W03 | Conduit & trenching details (electrical-impacting) | Priya Shah, PE  + Sam Ortega (CAD Tech, )<br>CAD notes + PDF export<br>Date: 2026-01-26 (v1.0) | [`phases/P3/Outputs/P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf) | Inputs: routing assumptions (installer) + Phase 2 photos + code basis<br>Used in: Phase 4, Phase 4 |
| 4-W04 | Updated panel schedules (MDP + EVSP-1) | Priya Shah, PE <br>Spreadsheet + PDF export<br>Date: 2026-01-26 (v1.0) | [`phases/P3/Outputs/P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf) | Inputs: Phase 2 schedules + Phase 3 + Phase 3<br>Used in: Phase 4, Phase 4 |
| 4-W05 | Electrical notes & code sheets | Priya Shah, PE <br>Template + PDF export<br>Date: 2026-01-26 (v1.0) | [`phases/P3/Outputs/P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf) | Inputs: Phase 2 code basis + P2 decision + EMS brief<br>Used in: Phase 4, Phase 4 |
| 4-W06 | Permit drawing set (unstamped, compiled) | Ethan Brooks (Document Control)<br>PDF compilation<br>Date: 2026-01-26 (v1.0) | [`phases/P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf) | Inputs: 4-W01..4-W05<br>Used in: Phase 4, Phase 5 |

### 4.4 Key Excerpts (Electrical-Only)

#### 4.4.1 One-Line Diagram Excerpt (4-W01)

**Excerpted design basis:**

- Existing service: **800A, 208Y/120V, 3Φ** (Phase 2 evidence)
- New EV subpanel: **400A bus**; feeder OCPD: **350A, 3-pole**
- EVSE branch circuits: **8 circuits**, each **40A OCPD** for **32A continuous** ports
- Load management: **EMS caps aggregate EV demand to ≤250A** per Phase 3 decision

#### 4.4.2 Site Plan w/ EVSE Locations Excerpt (4-W02)

**Excerpted content:** EVSE locations are shown based on owner/parking layout inputs, along with electrical equipment identifiers. Only items that affect electrical design are called out (equipment locations, electrical room reference, and design-relevant constraints).

#### 4.4.3 Conduit & Trenching Details Excerpt (4-W03)

**Excerpted content:** Electrical-impacting routing assumptions and site-condition constraints are documented for engineering use (e.g., feeder length basis for voltage drop/derating), without specifying construction means-and-methods.

#### 4.4.4 Drawing Set Compilation Excerpt (4-W06)

**Excerpted compilation rule:** “Phase 4 includes Phase 4–Phase 4 in the sheet order defined below; filenames and sheet titles must match the evidence pointers exactly.”

### 4.5 Preliminary One-Line Diagram

This one-line diagram depicts the complete electrical system from the utility source to the EV charging equipment. It defines major equipment, ratings, overcurrent protection, grounding intent, and the Energy Management System (EMS) used to manage aggregate EV load.

#### 4.5.1 Inputs (traceable)

- Architecture Decision: 3-W03 (see Addendum A for filenames)

- Service / MDP information: 2-I02 + 2-I03 (see Addendum A for filenames)

- EVSE cut sheet (design basis): 2-I04 (see Addendum A for filenames)

#### 4.5.2 System Description (summary)

The one-line diagram shows a new **400A, 120/208V, 3-phase EV subpanel** connected to the existing **800A MDP** via a **350A, 3-pole feeder OCPD**. A listed **Energy Management System (EMS)** is shown controlling aggregate EV demand to **≤250A** in accordance with the managed-load approach documented in Phase 3.

#### 4.5.3 Technical Specifications Shown on the Diagram (excerpt list)

#### 4.5.4 Utility Source and Fault Data ( design inputs)

- Utility transformer identifier: TX-485-A

- Available fault current at MDP bus: 42 kA (utility-provided short-circuit data)

- Calculated available fault current at EV subpanel bus: 38 kA (based on feeder impedance)

#### 4.5.5 Panel and Protection Ratings

- MDP bus rating: 800 A

- EV subpanel bus rating: 400 A

- EV feeder OCPD: 350 A, 3-pole

- Breaker interrupting rating: 65 kAIC minimum at 120/208 V

#### 4.5.6 Feeder Conductors (design basis)

- Phase conductors: three (3) parallel sets per phase of 250 kcmil copper, THHN/THWN-2 (design basis)

- Neutral conductor: not required (EVSE loads are line-to-line only)

- Equipment grounding conductor: one (1) 4/0 AWG copper (design basis)

- Ampacity basis: sized at 75°C terminal rating per applicable code requirements; final conductor sizing to be confirmed in stamped set

#### 4.5.7 Wiring Method (electrical-only)

- Wiring method is specified as a code-compliant raceway system sized per NEC Chapter 9 and applicable articles. **No routing/trenching/constructability means-and-methods are specified in this master deliverable.**

#### 4.5.8 Grounding and Bonding (intent)

- Equipment grounding conductor routed with feeder conductors in all raceways

- Bonding jumpers provided where required by wiring method and transitions

- EV subpanel grounding bar bonded to the building grounding electrode system (referenced on details sheet)

#### 4.5.9 Energy Management System (EMS)

- EMS device identified on the diagram as “Schlage / ChargePoint EMS Unit” 

- Dedicated EMS symbol legend included

- Control interface shown between EMS and EV feeder/EVSE branch circuits

- Fail-safe behavior note: on EMS fault/loss of comms, system defaults to a safe state that prevents EV feeder demand from exceeding the configured cap

#### 4.5.10 Coordination and Selectivity

- Coordination note: verify time-current coordination between feeder OCPD and downstream branch OCPD in final stamped set

This one-line diagram is intended to be code-complete for permit review, subject to final PE stamp and any jurisdiction-specific refinements identified during Phase 5\.



### 4.6 Site Plan w/ EVSE Locations

This plan overlays EVSE and electrical equipment identifiers onto the base plan to show EVSE locations provided by the owner/parking layout inputs and to capture any **site placement constraints that affect electrical design** (equipment adjacency, electrical-room reference, and plan-check clarity). It intentionally does **not** provide constructability means-and-methods.

| Input | Source |
|:---- |:---- |
| Base site plan | 2-I01 (normalized in Phase 2) |
| Parking layout | P3-PARK (see Addendum A) |
| Photo context (verification) | 2-I03 (normalized in Phase 2) |

Electrical-impacting plan outputs (excerpt):

- EVSE locations labeled **EVSE-01** through **EVSE-08** per owner parking layout input
- EV subpanel identified as **EVSP-1** relative to the existing **MDP** room (reference only)
- Notes call out placement constraints that affect electrical design only (e.g., maximum assumed feeder path length basis for voltage drop checks; any “no-penetration” zones that constrain electrical routing)

### 4.7 Conduit & Trenching Details (Electrical-Impacting)

This detail sheet documents **routing assumptions** and **site-condition constraints** that affect electrical design outcomes (feeder length basis, voltage drop basis, conductor derating basis, separation requirements, and transition points), using installer-provided assumptions and Phase 2 site photos. It intentionally avoids non-electrical constructability means-and-methods.

| Input | Source |
|:---- |:---- |
| Routing assumptions | 4-I03 (see Addendum A) |
| Site conditions | 2-I03 (normalized in Phase 2) |
| Code basis (separation/wiring method references) | 2-I05 (normalized in Phase 2) |

Electrical-impacting detail content (excerpt):

- **Feeder length basis:** 165 ft electrical path length used for voltage-drop checks and fault/impedance assumptions (final field-verified)
- **Wiring method basis:** raceway system sized per NEC Chapter 9 and applicable articles; conductor temperature/termination basis 75°C unless equipment requires otherwise
- **Derating basis:** parallel conductors and conduit fill assumptions documented for engineering sizing; final installation must comply with applicable adjustment factors
- **Separation:** power/communications separation and grounding/bonding intent documented for electrical compliance (final routing by installer)
- **Transitions/constraints:** identifies electrical-impacting transition points (e.g., “MDP room exit point” and “EVSP-1 entry point”) and any photo-identified constraints impacting electrical routing decisions

### 4.8 Updated Panel Schedules

The existing panel schedule for the MDP is updated to reflect the new downstream load (the 350A breaker for the EV subpanel), and a new schedule for the EV subpanel is created.

| Input | Source |
|:---- |:---- |
| Existing schedules | 2-I02 (normalized in Phase 2) |
| New EV loads (calc + decision) | 3-W01 + 3-W03 |

The updated MDP schedule shows:

| Slot | Breaker | Load | Amps | Notes |
|:---- |:---- |:---- |:---- |:---- |
| 40, 42, 44 | 3-Pole, 350A | EV Subpanel | 250A Managed | Connection to New EV Subpanel |

The New EV Subpanel schedule shows:

| Slot | Breaker | Load | Amps | Notes |
|:---- |:---- |:---- |:---- |:---- |
| 1, 3, 5 | 3-Pole, 40A | EVSE \#1 | 40A | Dedicated Circuit for Continuous Load |
| 7, 9, 11 | 3-Pole, 40A | EVSE \#2 | 40A | Dedicated Circuit for Continuous Load |
| 13, 15, 17 | 3-Pole, 40A | EVSE \#3 | 40A | Dedicated Circuit for Continuous Load |
| 19, 21, 23 | 3-Pole, 40A | EVSE \#4 | 40A | Dedicated Circuit for Continuous Load |
| 25, 27, 29 | 3-Pole, 40A | EVSE \#5 | 40A | Dedicated Circuit for Continuous Load |
| 31, 33, 35 | 3-Pole, 40A | EVSE \#6 | 40A | Dedicated Circuit for Continuous Load |
| 37, 39, 41 | 3-Pole, 40A | EVSE \#7 | 40A | Dedicated Circuit for Continuous Load |
| 43, 45, 47 | 3-Pole, 40A | EVSE \#8 | 40A | Dedicated Circuit for Continuous Load |

### 4.9 Electrical Notes & Code Sheets

This document compiles the necessary general and project-specific notes, ensuring the construction documents clearly articulate the applicable codes, standards, and installation methods.

| Input | Source |
|:---- |:---- |
| AHJ/code basis | 2-I05 (normalized in Phase 2) |
| Architecture decision | 3-W03 |
| Standard templates | Internal |

The notes sheet explicitly references the **2022 California Electrical Code (CEC)** and the use of the **NEC 625.42(A)(2)** method (EMS) to justify the 250A managed load. Key notes include:

* **A. Load Management:** The EV subpanel utilizes a listed Energy Management System (EMS) to cap the maximum aggregate demand at 250 Amps to prevent exceeding the available service headroom. 
* **B. Continuous Loads:** All EV loads are calculated at 125% demand factor per NEC 625.42. 
* **C. Wiring:** All conductors shall be sized per NEC 310 and rated for 75°C minimum.

### 4.10 Permit Drawing Set – Unstamped

This deliverable is the compiled **electrical permit drawing set** (unstamped), finalized and ready for the engineer of record's final stamp.

| Input | Source |
|:---- |:---- |
| One-line | Phase 4 |
| Site plan | Phase 4 |
| Details | Phase 4 |
| Schedules | Phase 4 |
| Notes | Phase 4 |

This complete set, reserved as a File, is the primary output of Phase 4 and serves as the input for Phase 5\.

### 4.11 Compilation / QA Log

| QA Item | Check performed | Result | Checked by | Date |
|:---- |:---- |:---- |:---- |:---- |
| Sheet inclusion | Phase 4–Phase 4 present in compiled PDF | Pass | Ethan Brooks (Document Control) | 2026-01-26 |
| Stable filenames | Output filenames match Phase 4 evidence pointers | Pass | Ethan Brooks (Document Control) | 2026-01-26 |
| Title block consistency | Sheet titles/IDs consistent across set | Pass | Sam Ortega (CAD Tech, ) | 2026-01-26 |
| Cross-references | Notes reference correct sheet IDs | Pass | Priya Shah, PE  | 2026-01-26 |

### 4.12 Phase 4 Drawing Package Certification

| Certification Point | Status | Certified By | Date |
|:---- |:---- |:---- |:---- |
| Drawing set compiled (unstamped) | Certified | Ethan Brooks (Document Control) | 2026-01-26 |
| Electrical content aligns to Phase 3 decision | Certified | Priya Shah, PE  | 2026-01-26 |
| Inputs traceable to Phase 2 evidence pointers | Certified | Priya Shah, PE  | 2026-01-26 |

### 4.13 Next Steps

Phase 4 is complete. The **Unstamped Permit Drawing Set (Phase 4)** is finalized.

The project proceeds to **Phase 5: Permitting Submission** to obtain the **Stamped Permit Drawings (Phase 5)** and assemble the permit application package (Phase 5).


<a id="phase-5"></a>

## Phase 5: Permitting Submission
### 5.1 Phase 5 Purpose

Phase 5 documents the formal submission of the electrical permit package to the AHJ, including the stamped drawing set, required forms, and submission receipts/tracking.

**NOTE:** The Phase 5 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and submission logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 5.2 Phase 5 Boundaries (Electrical-Only)

Phase 5 captures the electrical permitting submission artifacts. It intentionally excludes:

- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)

### 5.3 Evidence Index + Submission Work Products (Stable Filenames)

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 5-W01 | Stamped permit drawings (electrical set) | Priya Shah, PE (EOR)<br>Stamp + PDF<br>Date: 2026-01-29 (v1.0) | [`phases/P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf) | Inputs: Phase 4 unstamped set<br>Used in: Phase 5, Phase 5 |
| 5-W02 | AHJ permit application form(s) | Jordan Lee (PM)<br>AHJ portal form + PDF export<br>Date: 2026-01-29 (v1.0) | [`phases/P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf) | Inputs: AHJ requirements + project metadata<br>Used in: Phase 5 |
| 5-W03 | Permit application package (compiled) | Ethan Brooks (Document Control)<br>PDF compilation<br>Date: 2026-01-29 (v1.0) | [`phases/P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf) | Inputs: Phase 5 + 5-W02 + supporting attachments<br>Used in: Phase 5, Phase 6 |
| 5-W04 | Supporting attachments bundle (electrical) | Ethan Brooks (Document Control)<br>PDF compilation<br>Date: 2026-01-29 (v1.0) | [`phases/P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf) | Inputs: Phase 3 + Phase 3 + EVSE/EMS + code basis<br>Used in: Phase 5 |
| 5-W05 | AHJ submission receipt / confirmation | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-01-29 (v1.0) | [`phases/P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf) | Inputs: portal submission<br>Used in: Phase 5, Phase 6 |
| 5-W06 | Permit tracking log (submission metadata) | Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-01-29 (v1.0) | [`phases/P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx.html) | Inputs: portal submission data<br>Used in: Phase 6 |

### 5.4 Key Excerpts (Electrical-Only)

#### 5.4.1 Submission Confirmation Excerpt (5-W05)

**Excerpted receipt fields:**

- AHJ: City of Palo Alto – Building Division (Electrical Permits)
- Submission method: Online portal upload
- Permit application number: **EL-2026-01472** 
- Submission date/time: **2026-01-29 14:18 PT**
- Submitted by: **Jordan Lee (PM)** 

#### 5.4.2 Stamped Set Excerpt (5-W01)

**Excerpted stamp fields:**

- Engineer-of-Record: **Priya Shah, PE**
- Stamp date: **2026-01-29**
- Set: **P4.1_PermitSet_Stamped_2026-01-29.pdf** derived from **Phase 4** with no content changes other than stamp block and any required administrative cover sheet

### 5.5 Stamped Permit Drawings

This deliverable is the Phase 4 compiled set (Phase 4) reviewed and stamped by the Engineer-of-Record for submission to the AHJ.

| Input | Source |
|:---- |:---- |
| Unstamped permit set | 4-W06 |
| EOR review notes  | P4-EOR (see Addendum A) |

**Output (reference ID):** 5-W01

### 5.6 Permit Application Package

This deliverable is the complete electrical permit submission package as provided to the AHJ, including forms, stamped drawings, and electrical support documents commonly required for plan check.

#### 5.6.1 Package contents (electrical-only)
- **Stamped drawings**: 5-W01
- **AHJ application forms**: 5-W02
- **Supporting attachments (electrical)**: 5-W04
  - Load calculation summary (Phase 3): 3-W01
  - Architecture decision record (Phase 3): 3-W03
  - EVSE cut sheet (design basis): 2-I04
  - EMS technical brief: 3-W04
  - AHJ/code basis evidence: 2-I05

**Output (reference ID):** 5-W03

### 5.7 P4 Submission / QA Log

| QA Item | Check performed | Result | Checked by | Date |
|:---- |:---- |:---- |:---- |:---- |
| Stamped set included | Phase 5 stamped drawings included in package | Pass | Ethan Brooks (Document Control) | 2026-01-29 |
| Stable filenames | Package references match evidence pointers | Pass | Ethan Brooks (Document Control) | 2026-01-29 |
| Attachment completeness | Load calc, EVSE, EMS, and code basis included | Pass | Jordan Lee (PM) | 2026-01-29 |
| Portal upload verification | Receipt downloaded; application number captured | Pass | Jordan Lee (PM) | 2026-01-29 |

### 5.8 Phase 5 Certification

| Certification Point | Status | Certified By | Date |
|:---- |:---- |:---- |:---- |
| Stamped drawings issued (Phase 5) | Certified | Priya Shah, PE  | 2026-01-29 |
| Permit application package submitted (Phase 5) | Certified | Jordan Lee (PM) | 2026-01-29 |
| Submission receipt archived and traceable | Certified | Ethan Brooks (Document Control) | 2026-01-29 |

### 5.9 Phase 5 Closeout Confirmation (Completed)

Phase 5 is considered **complete** and closed out because all submission artifacts are archived under stable filenames:

- **Stamped drawing set issued**: [`phases/P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf)
- **Permit forms archived**: [`phases/P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf)
- **Supporting attachments bundle archived**: [`phases/P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf)
- **Compiled submission package archived (as-submitted)**: [`phases/P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf)
- **Submission receipt archived**: [`phases/P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf)
- **Permit tracking log started**: [`phases/P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx.html)


<a id="phase-6"></a>

## Phase 6: Authority Review and Drawing Revision
### 6.1 Phase 6 Purpose

Phase 6 documents the AHJ plan check review, parses all AHJ comments into an auditable log, produces revised drawings addressing those comments, and records responses in a formal comment response letter. It explicitly captures the **rework loop caused by AHJ pushback** (comment intake → disposition → drawing changes → resubmission → approval evidence) so the revision path is traceable and defensible.

**NOTE:** The Phase 6 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and revision logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 6.2 Phase 6 Boundaries (Electrical-Only)

Phase 6 captures electrical plan-check comments and electrical drawing revisions. It intentionally excludes:

- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)

### 6.3 Evidence Index + Review/Revision Work Products (Stable Filenames)

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 6-W01 | AHJ plan check comments (raw) | AHJ<br>Portal download<br>Date: 2026-02-06 (v1.0) | [`phases/P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf`](https://rc979.github.io/EEIntake/phases/P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf) | Inputs: AHJ portal<br>Used in: Phase 6 |
| 6-W02 | AHJ comment log (parsed + tracked) | Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-02-06 (v1.0) | [`phases/P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx.html) | Inputs: 6-W01<br>Used in: Phase 6, Phase 6, Phase 6 |
| 6-W03 | Revised drawings (post-comments, stamped) | Priya Shah, PE (EOR)<br>CAD update + stamp + PDF<br>Date: 2026-02-12 (Rev 1) | [`phases/P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf) | Inputs: Phase 5 stamped set + 6-W02<br>Used in: Phase 6, Phase 6 |
| 6-W04 | Redline set (internal review) | Priya Shah, PE (EOR)<br>PDF markups<br>Date: 2026-02-10 (v1.0) | [`phases/P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf) | Inputs: Phase 5 stamped set + 6-W02<br>Used in: Phase 6 |
| 6-W05 | Comment response letter | Priya Shah, PE (EOR)<br>Letter PDF<br>Date: 2026-02-12 (Rev 1) | [`phases/P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf) | Inputs: 6-W02 + 6-W03<br>Used in: Phase 6 |
| 6-W06 | Resubmission receipt / confirmation | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-02-12 (v1.0) | [`phases/P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf) | Inputs: AHJ portal<br>Used in: Phase 6 closeout |
| 6-W07 | AHJ approval / permit issuance confirmation | AHJ<br>Portal download<br>Date: 2026-02-19 (v1.0) | [`phases/P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf) | Inputs: AHJ portal<br>Used in: Phase 6, Phase 6 closeout |

### 6.4 Key Excerpts (Electrical-Only)

#### 6.4.1 AHJ Comment Themes Excerpt (6-W01)

**Excerpted themes:**

- Request clarification of **EMS/load management method** and fail-safe behavior.
- Request confirmation of **available fault current / AIC** selection basis.
- Request additional **code notes** (EVSE continuous load, labeling, disconnecting means references as applicable).

#### 6.4.2 Revision Summary Excerpt (6-W03)

**Excerpted revision summary:**

- Updated one-line notes to clarify EMS cap logic and fail-safe state.
- Added fault current basis note and verified minimum AIC rating statement.
- Updated notes sheet with explicit NEC/CEC references and labeling notes.

#### 6.4.3 AHJ Approval Excerpt (6-W07)

**Excerpted approval fields:**

- Status: **Approved**
- Permit application number: **EL-2026-01472** 
- Approval date/time: **2026-02-19 10:07 PT**

### 6.5 AHJ Comment Log – Parsed

This deliverable converts the AHJ’s raw plan-check comments into a structured, trackable log with owners, dispositions, and references to revised sheets.

| Input | Source |
|:---- |:---- |
| AHJ comments (raw) | 6-W01 |
| Prior submitted set | 5-W01 |

**Output (reference ID):** 6-W02

**Parsed comment log (excerpt):**

| AHJ Comment ID | Location + comment | Required action + owner | Resolution |
|:---- |:---- |:---- |:---- |
| C-01 | E-001 (One-Line): Clarify EMS method/fail-safe; cite code basis | Add EMS control note + fail-safe statement + code ref<br>Owner: Priya Shah, PE | Disposition: Accepted<br>Revised in: Rev 1<br>Response: Phase 6 §2.1 |
| C-02 | E-001 (One-Line): Provide fault current basis; confirm OCPD AIC | Add short-circuit basis note + minimum AIC statement<br>Owner: Priya Shah, PE | Disposition: Accepted<br>Revised in: Rev 1<br>Response: Phase 6 §2.2 |
| C-03 | E-003 (Notes): Add EVSE continuous-load factor + labeling requirement | Expand notes with NEC/CEC refs + labeling language<br>Owner: Priya Shah, PE | Disposition: Accepted<br>Revised in: Rev 1<br>Response: Phase 6 §2.3 |
| C-04 | General: Confirm EV subpanel designation and schedule consistency | Standardize nomenclature “EVSP-1” across set<br>Owner: Sam Ortega (CAD) | Disposition: Accepted<br>Revised in: Rev 1<br>Response: Phase 6 §2.4 |

### 6.6 Revised Drawings – Post-Comments

This deliverable is the revised electrical permit set addressing AHJ comments. Revisions are tracked by revision number and traceable back to comment IDs.

| Input | Source |
|:---- |:---- |
| Comment log (parsed) | 6-W02 |
| Prior stamped set | 5-W01 |
| Internal redlines (optional) | 6-W04 |

**Output (reference ID):** 6-W03

#### 6.6.1 Revision log

| Revision | Date | Summary | Addressed comments |
|:---- |:---- |:---- |:---- |
| Rev 1 | 2026-02-12 | EMS notes clarified; fault-current/AIC basis added; notes expanded; nomenclature normalized | C-01, C-02, C-03, C-04 |

#### 6.6.2 How changes were crafted (traceable mapping)

| Change ID | From (prior set) | To (revised set) | Change description | Driven by AHJ comment |
|:---- |:---- |:---- |:---- |:---- |
| CH-01 | E-001 | E-001 | Added EMS cap statement + fail-safe note + code reference | C-01 |
| CH-02 | E-001 | E-001 | Added available fault current basis note; confirmed minimum AIC | C-02 |
| CH-03 | E-003 | E-003 | Added explicit EVSE continuous load and labeling notes | C-03 |
| CH-04 | E-002/E-004 | E-002/E-004 | Standardized equipment ID “EVSP-1” across plan and schedules | C-04 |

### 6.7 Comment Response Letter

This deliverable provides point-by-point responses to each AHJ comment and cross-references the revised sheets where changes were made.

| Input | Source |
|:---- |:---- |
| Comment log (parsed) | 6-W02 |
| Revised stamped set | 6-W03 |

**Output (reference ID):** 6-W05

**Response letter (excerpt):**

- **C-01 (EMS clarification):** Added EMS control narrative and fail-safe behavior note on Sheet E-001; see Rev 1 clouded note “EMS-1.”
- **C-02 (fault current / AIC):** Added fault-current basis statement and confirmed minimum breaker AIC on Sheet E-001.
- **C-03 (notes/labeling):** Updated Sheet E-003 to explicitly state EVSE continuous load treatment (125%) and labeling notes.
- **C-04 (nomenclature):** Standardized EV subpanel designation to “EVSP-1” across all sheets and schedules.

### 6.8 Phase 6 Resubmission Log

| Field | Value |
|:---- |:---- |
| Resubmission date/time | 2026-02-12 16:42 PT |
| Submitted by | Jordan Lee (PM) |
| Permit application number | EL-2026-01472  |
| Receipt evidence | 6-W06 |

### 6.9 AHJ Acceptance / Approval Confirmation (100% Closeout)

This deliverable records that the AHJ has accepted all comments and has approved the revised electrical permit set (or issued the permit). Phase 6 is not considered complete until this evidence is archived.

| Input | Source |
|:---- |:---- |
| Resubmission receipt | 6-W06 |
| Revised stamped set | 6-W03 |
| AHJ approval notice / permit issuance | 6-W07 |

**Closeout criteria:**

- All AHJ comments in `P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx` have disposition **Accepted/Resolved**
- AHJ status is **Approved** (or **Permit Issued**) as evidenced by `P5.4_AHJ_Approval_Notice_2026-02-19.pdf`

### 6.10 Phase 6 Certification

| Certification Point | Status | Certified By | Date |
|:---- |:---- |:---- |:---- |
| AHJ comments parsed and tracked (Phase 6) | Certified | Jordan Lee (PM) | 2026-02-06 |
| Revised set addresses all comments (Phase 6) | Certified | Priya Shah, PE  | 2026-02-12 |
| Comment response letter issued (Phase 6) | Certified | Priya Shah, PE  | 2026-02-12 |
| Resubmission receipt archived | Certified | Ethan Brooks (Document Control) | 2026-02-12 |
| AHJ approval / permit issuance archived (Phase 6) | Certified | Ethan Brooks (Document Control) | 2026-02-19 |

### 6.11 Phase 6 Closeout Confirmation (Completed)

Phase 6 is considered **complete** and closed out because AHJ comments are resolved and approval evidence is archived:

- **Raw plan check comments archived**: [`phases/P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf`](https://rc979.github.io/EEIntake/phases/P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf)
- **Parsed comment log archived**: [`phases/P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx.html) (all items dispositioned **Accepted/Resolved**)
- **Internal redlines archived**: [`phases/P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf)
- **Revised stamped set issued (Rev 1)**: [`phases/P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf)
- **Point-by-point response letter issued**: [`phases/P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf)
- **Resubmission receipt archived**: [`phases/P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf)
- **AHJ approval/permit issuance archived**: [`phases/P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf)


<a id="phase-7"></a>

## Phase 7: Utility Coordination
### 7.1 Phase 7 Purpose

Phase 7 documents coordination with the local electrical utility to communicate the planned EV load addition and any load-management method, submit required utility application forms, and archive all utility correspondence/receipts. It also records the **utility-driven rework cycle** when the initial submission receives pushback (deficiency notice → rework package → resubmission → final acknowledgment) so utility concerns and responses remain auditable.

**NOTE:** The Phase 7 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and coordination logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 7.2 Phase 7 Boundaries (Electrical-Only)

Phase 7 captures technical utility coordination artifacts (load letters, single-line/one-line as requested by the utility, and utility portal forms). It intentionally excludes:

- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)

### 7.3 Evidence Index + Utility Coordination Work Products (Stable Filenames)

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 7-W01 | Utility requirements capture | Jordan Lee (PM)<br>Utility portal capture + PDF<br>Date: 2026-02-20 (v1.0) | [`phases/P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf`](https://rc979.github.io/EEIntake/phases/P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf) | Inputs: utility portal<br>Used in: Phase 7 |
| 7-W02 | Utility load letter + single-line | Priya Shah, PE (EOR)<br>Letter + PDF<br>Date: 2026-02-21 (v1.0) | [`phases/P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf) | Inputs: Phase 3 + Phase 3 + service info (+ stamped set if required)<br>Used in: Phase 7, Phase 7 |
| 7-W03 | Utility application forms (completed) | Jordan Lee (PM)<br>Portal form + PDF export<br>Date: 2026-02-21 (v1.0) | [`phases/P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf) | Inputs: 7-W01 + project technical metadata<br>Used in: Phase 7 |
| 7-W04 | Utility submission receipt | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-02-21 (v1.0) | [`phases/P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf) | Inputs: portal submission<br>Used in: Phase 7 closeout |
| 7-W05 | Utility correspondence log | Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-02-24 (v1.0) | [`phases/P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx.html) | Inputs: utility comms<br>Used in: Phase 7 closeout |
| 7-W06 | Utility deficiency / additional info required | Utility<br>Portal message + PDF<br>Date: 2026-02-25 (v1.0) | [`phases/P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf`](https://rc979.github.io/EEIntake/phases/P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf) | Inputs: utility review of initial submission<br>Used in: Phase 7 |
| 7-W07 | Utility rework package | Priya Shah, PE  + Jordan Lee (PM)<br>PDF compilation<br>Date: 2026-02-27 (v1.0) | [`phases/P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf) | Inputs: 7-W06 + evidence from Phases 2, 3, and 4 + EMS brief<br>Used in: Phase 7 |
| 7-W08 | Utility resubmission receipt | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-02-27 (v1.0) | [`phases/P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf) | Inputs: portal resubmission<br>Used in: Phase 7 closeout |
| 7-W09 | Utility approval / acknowledgment (final) | Utility<br>Email/portal letter<br>Date: 2026-03-03 (v1.0) | [`phases/P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf) | Inputs: utility review<br>Used in: Phase 7 closeout |

### 7.4 Key Excerpts (Electrical-Only)

#### 7.4.1 Utility Load Letter Excerpt (7-W02)

**Excerpted technical content:**

- Service: **800A, 208Y/120V, 3Φ** (verified in Phase 2)
- EVSE: **8 ports**, **32A continuous** each (design basis)
- Unmanaged continuous EV load: **320A**
- Load management: **EMS caps aggregate EV demand to ≤250A**
- Reference documents included: Phase 3 load calc summary + architecture decision record

#### 7.4.2 Utility Submission Receipt Excerpt (7-W04)

**Excerpted receipt fields:**

- Submission method: Utility online portal
- Application/reference number: **UTIL-EV-2026-00831** 
- Submitted by: **Jordan Lee (PM)** 
- Submission date/time: **2026-02-21 11:05 PT**

#### 7.4.3 Utility Deficiency Notice Excerpt (7-W06)

**Excerpted status:**

- Status: **Incomplete / Additional Information Required**
- Reason: EMS documentation insufficient for utility review; request clarification of monitoring point and fail-safe cap behavior
- Response due: N/A (utility queue-based)

### 7.5 Utility Load Letter / Single-Line

This deliverable packages the technical load information for the utility, including a single-line/one-line diagram excerpt as required by the utility and a narrative describing any load-management method (EMS) used to limit service impact.

| Input | Source |
|:---- |:---- |
| Load calculation summary | 3-W01 |
| Architecture decision record | 3-W03 |
| Service characteristics evidence | 2-I02 + 2-I03 |
| EVSE cut sheet (design basis) | 2-I04 |
| EMS technical brief | 3-W04 |

**Output (reference ID):** 7-W02

### 7.6 Utility Application Forms

This deliverable captures the completed utility application forms and any required attachments. The submission receipt and correspondence log are archived to preserve full traceability.

| Input | Source |
|:---- |:---- |
| Utility requirements | 7-W01 |
| Utility load letter/single-line | 7-W02 |
| Stamped permit drawings (if requested by utility) | 5-W01 |

**Output (reference ID):** 7-W03

### 7.7 Utility Deficiency Response / Rework + Resubmission

This deliverable documents the utility’s “incomplete/additional info required” outcome and the technical rework performed to satisfy the utility’s request, followed by resubmission and approval.

#### 7.7.1 Deficiency received

| Input | Source |
|:---- |:---- |
| Utility deficiency notice | 7-W06 |

#### 7.7.2 Rework package (electrical-only)

| Rework component | Evidence pointer |
|:---- |:---- |
| EMS clarification memo (monitoring point + cap + fail-safe) | 7-W07 (Section 1) |
| EMS technical brief (revB) | 3-W04 |
| Load calc summary (Phase 3) | 3-W01 |
| Architecture decision record (Phase 3) | 3-W03 |
| Stamped permit set (reference, if requested) | 5-W01 |

#### 7.7.3 Resubmission + approval

| Field | Value |
|:---- |:---- |
| Utility application/reference number | UTIL-EV-2026-00831  |
| Resubmission date/time | 2026-02-27 09:22 PT |
| Resubmission receipt | 7-W08 |
| Utility approval/acknowledgment | 7-W09 |

### 7.8 Phase 7 Coordination Log

| Date | Activity | Evidence (reference ID) |
|:---- |:---- |:---- |
| 2026-02-20 | Confirm required attachments for EV load add (email w/ utility rep) | 7-W01 |
| 2026-02-21 | Submit application + load letter (utility portal) | 7-W04 |
| 2026-02-24 | EMS clarification requested (call, pre-review) | 7-W05 |
| 2026-02-25 | Deficiency issued: “Additional Info Required” (utility portal) | 7-W06 |
| 2026-02-27 | Resubmit rework package (utility portal) | 7-W08 |
| 2026-03-03 | Approval/acknowledgment issued (utility portal letter) | 7-W09 |

### 7.9 Phase 7 Closeout Criteria

Phase 7 is considered complete when:

- Utility application submission receipt is archived (**7-W04**)
- Correspondence log is complete (**7-W05**)
- Utility deficiency notice (if issued) is archived and dispositioned (**7-W06**)
- Utility approval/acknowledgment is archived (**7-W09**) or documented as “not applicable/none issued” in the correspondence log

### 7.10 Phase 7 Certification

| Certification Point | Status | Certified By | Date |
|:---- |:---- |:---- |:---- |
| Utility load letter/single-line issued (Phase 7) | Certified | Priya Shah, PE  | 2026-02-21 |
| Utility application submitted (Phase 7) | Certified | Jordan Lee (PM) | 2026-02-21 |
| Submission receipt archived | Certified | Ethan Brooks (Document Control) | 2026-02-21 |
| Utility deficiency addressed and resubmitted (Phase 7) | Certified | Jordan Lee (PM) | 2026-02-27 |
| Utility approval/acknowledgment archived (final) | Certified | Ethan Brooks (Document Control) | 2026-03-03 |

### 7.11 Phase 7 Closeout Confirmation (Completed)

Phase 7 is considered **complete** and closed out because the utility coordination cycle is fully evidenced end-to-end:

- **Utility requirements captured**: [`phases/P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf`](https://rc979.github.io/EEIntake/phases/P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf)
- **Load letter + one-line issued**: [`phases/P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf)
- **Utility application forms archived**: [`phases/P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf)
- **Submission receipt archived**: [`phases/P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf)
- **Correspondence log archived**: [`phases/P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx.html)
- **Deficiency notice archived**: [`phases/P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf`](https://rc979.github.io/EEIntake/phases/P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf)
- **Rework package archived**: [`phases/P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf)
- **Resubmission receipt archived**: [`phases/P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf)
- **Final utility acknowledgment archived**: [`phases/P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf)


<a id="phase-8"></a>

## Phase 8: Electrical Closeout and Handover
### 8.1 Phase 8 Purpose

Phase 8 captures the final electrical closeout artifacts: **as-built electrical drawings**, responses supporting final inspection, and evidence that the AHJ finaled the electrical permit/inspection (where applicable).

**NOTE:** The Phase 8 fields below are filled with **example data** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and closeout logs). Replace all names, dates, and evidence pointers with real project records before using this document externally.

### 8.2 Phase 8 Boundaries (Electrical-Only)

Phase 8 captures electrical closeout documentation. It intentionally excludes:

- **Civil / constructability** topics (installation means-and-methods, trenching execution details, routing procedures, etc.)

### 8.3 Evidence Index + Closeout Work Products (Stable Filenames)

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
|:---- |:---- |:---- |:---- |:---- |
| 8-W01 | Field redlines (electrical) | Luis Romero (Electrician) + Mia Chen (Installer PM)<br>Markups + photo references<br>Date: 2026-03-18 (v1.0) | [`phases/P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf`](https://rc979.github.io/EEIntake/phases/P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf) | Inputs: field observations + installed labels<br>Used in: Phase 8 |
| 8-W02 | As-built electrical drawing set | Sam Ortega (CAD Tech, ) + Priya Shah, PE <br>CAD update + PDF export<br>Date: 2026-03-22 (As-Built v1) | [`phases/P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf) | Inputs: Phase 6 revised stamped set + 8-W01 + inspection notes<br>Used in: Phase 8 |
| 8-W03 | AHJ final inspection / permit finaled confirmation | AHJ<br>Portal download<br>Date: 2026-03-26 (v1.0) | [`phases/P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf) | Inputs: AHJ portal<br>Used in: Phase 8 |
| 8-W04 | Inspector notes / correction notice (if any) | AHJ<br>Field note + portal upload<br>Date: 2026-03-24 (v1.0) | [`phases/P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf`](https://rc979.github.io/EEIntake/phases/P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf) | Inputs: field inspection<br>Used in: Phase 8, Phase 8 |
| 8-W05 | Inspection support Q&A log | Priya Shah, PE  + Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-03-26 (v1.0) | [`phases/P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx.html) | Inputs: AHJ questions + responses<br>Used in: Phase 8 |
| 8-W06 | EMS configuration summary (as-installed) | Mia Chen (Installer PM)<br>Vendor export + PDF<br>Date: 2026-03-21 (v1.0) | [`phases/P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf) | Inputs: EMS system<br>Used in: Phase 8, Phase 8 |

### 8.4 Key Excerpts (Electrical-Only)

#### 8.4.1 As-Built Summary Excerpt (8-W02)

**Excerpted as-built outcomes:**

- EV subpanel designation standardized as **EVSP-1** (matches permit set)
- EMS aggregate cap configured to **250A** (as-installed), with documented fail-safe behavior
- One-line and schedules updated to reflect installed breaker/labeling differences found in field redlines (no change to the approved load-management intent)

#### 8.4.2 Final Inspection Excerpt (8-W03)

**Excerpted AHJ status:**

- Final inspection result: **Pass**
- Permit status: **Finaled/Closed**
- Permit application number: **EL-2026-01472** 
- Final date/time: **2026-03-26 09:40 PT**

### 8.5 As-Built Drawings

This deliverable is the as-built electrical drawing set prepared from field redlines and any AHJ inspector notes. The as-built set is intended to be the authoritative record of the installed electrical scope.

| Input | Source |
|:---- |:---- |
| Prior approved/revised permit set | 6-W03 |
| Field redlines (electrical) | 8-W01 |
| AHJ inspector notes (if any) | 8-W04 |
| EMS as-installed config summary | 8-W06 |

**Output (reference ID):** 8-W02

#### 8.5.1 As-built change log

| Change ID | Sheet | Change description | Source evidence |
|:---- |:---- |:---- |:---- |
| AB-01 | One-line | Updated EMS note to match as-installed cap value and monitoring point label | 8-W06 + 8-W01 |
| AB-02 | Panel schedules | Updated EVSP-1 schedule to reflect installed breaker spaces/labeling | 8-W01 |
| AB-03 | Notes | Added “as-built” cover note and clarified labeling applied in field | 8-W01 + 8-W04 |

### 8.6 Inspection Support Responses

This deliverable documents responses provided to the AHJ/inspector during final inspection or closeout, including clarifications, supplemental documentation, and confirmation of corrected items.

| Input | Source |
|:---- |:---- |
| Inspector notes / questions | 8-W04 |
| As-built set (draft/final) | 8-W02 |
| EMS configuration summary | 8-W06 |

**Output (reference ID):** 8-W05

**Inspection support log (excerpt):**

| Item | Question/Issue | Response provided | Evidence pointer | Status |
|:---- |:---- |:---- |:---- |:---- |
| IS-01 | Provide EMS cap confirmation for plan-check intent | Provided EMS config export showing cap set to 250A and fail-safe mode | 8-W06 | Closed |
| IS-02 | Confirm panel labeling and circuit IDs match drawings | Provided updated as-built schedule page and photo references | 8-W02 | Closed |

### 8.7 AHJ Final Acceptance / Permit Closeout Confirmation

This deliverable archives proof that the AHJ finaled/closed the electrical permit/inspection, marking the end of the AHJ process for this scope.

| Input | Source |
|:---- |:---- |
| Final inspection / permit status evidence | 8-W03 |

### 8.8 Phase 8 Closeout Criteria

Phase 8 is considered complete when:

- As-built electrical drawings are issued and archived (**8-W02**)
- Inspection support log is complete (**8-W05**)
- AHJ final acceptance/permit closeout evidence is archived (**8-W03**)

### 8.9 Phase 8 Certification

| Certification Point | Status | Certified By | Date |
|:---- |:---- |:---- |:---- |
| As-built electrical set issued (Phase 8) | Certified | Priya Shah, PE  | 2026-03-22 |
| Inspection support documentation complete (Phase 8) | Certified | Jordan Lee (PM) | 2026-03-26 |
| AHJ final acceptance archived (Phase 8) | Certified | Ethan Brooks (Document Control) | 2026-03-26 |

### 8.10 Phase 8 Closeout Confirmation (Completed / Project Electrical Scope Closed)

Phase 8 is considered **complete** and the overall electrical project is **closed out** because final inspection/permit close evidence and as-built records are archived:

- **Field redlines archived**: [`phases/P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf`](https://rc979.github.io/EEIntake/phases/P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf)
- **EMS as-installed configuration summary archived**: [`phases/P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf)
- **As-built electrical record set issued**: [`phases/P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf)
- **Inspector notes archived (if any)**: [`phases/P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf`](https://rc979.github.io/EEIntake/phases/P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf)
- **Inspection support log archived**: [`phases/P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx.html)
- **AHJ final/permit finaled confirmation archived**: [`phases/P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf)


<a id="addendum-a"></a>

## 12 Addendum A: Stable Filename Index (by Phase)

This addendum is a consolidated index of all **stable evidence pointers** referenced in this document, grouped by phase and section/deliverable.

### 12.1 Phase 1 — Project Initiation and Feasibility

- **P0 inputs**
  - [`phases/P0/Inputs/P0-I01_Utility_Bills_2025-01_to_2025-12.pdf`](https://rc979.github.io/EEIntake/phases/P0/Inputs/P0-I01_Utility_Bills_2025-01_to_2025-12.pdf)
  - [`phases/P0/Inputs/P0-I01_GreenButton_IntervalData_2025.csv`](https://rc979.github.io/EEIntake/phases/P0/Inputs/P0-I01_GreenButton_IntervalData_2025.csv.html)
  - [`phases/P0/Inputs/P0-I02_MDP_Nameplate_Photos.zip`](https://rc979.github.io/EEIntake/galleries/p0-i02_mdp_nameplate_photos/index.html)
  - [`phases/P0/Inputs/P0-I02_Utility_Service_Info_Letter.pdf`](https://rc979.github.io/EEIntake/phases/P0/Inputs/P0-I02_Utility_Service_Info_Letter.pdf)
  - [`phases/P0/Inputs/P0-I03_ElectriCharge_L2-7.6-G_CutSheet_revA.pdf`](https://rc979.github.io/EEIntake/phases/P0/Inputs/P0-I03_ElectriCharge_L2-7.6-G_CutSheet_revA.pdf)
  - [`phases/P0/Inputs/P0-I04_PhotoSet_ExistingGear_and_GarageArea.zip`](https://rc979.github.io/EEIntake/galleries/p0-i04_photoset_existinggear_and_garagearea/index.html)
  - [`phases/P0/Inputs/P0-I04_PhotoIndex_Annotated.pdf`](https://rc979.github.io/EEIntake/phases/P0/Inputs/P0-I04_PhotoIndex_Annotated.pdf)

### 12.2 Phase 2 — Data Collection and Site Analysis

- **P1 inputs**
  - [`phases/P1/Inputs/P1-I01_SitePlans_Arch_Set_rev2_2026-01-15.pdf`](https://rc979.github.io/EEIntake/phases/P1/Inputs/P1-I01_SitePlans_Arch_Set_rev2_2026-01-15.pdf)
  - [`phases/P1/Inputs/P1-I02_PanelSchedules_MDP_and_Subpanels_2026-01-16.pdf`](https://rc979.github.io/EEIntake/phases/P1/Inputs/P1-I02_PanelSchedules_MDP_and_Subpanels_2026-01-16.pdf)
  - [`phases/P1/Inputs/P1-I03_PhotoSet_ServiceGear_Nameplates_2026-01-16.zip`](https://rc979.github.io/EEIntake/galleries/p1-i03_photoset_servicegear_nameplates_2026-01-16/index.html)
  - [`phases/P1/Inputs/P1-I03_PhotoIndex_Annotated_2026-01-16.pdf`](https://rc979.github.io/EEIntake/phases/P1/Inputs/P1-I03_PhotoIndex_Annotated_2026-01-16.pdf)
  - [`phases/P1/Inputs/P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf`](https://rc979.github.io/EEIntake/phases/P1/Inputs/P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf)
  - [`phases/P1/Inputs/P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf`](https://rc979.github.io/EEIntake/phases/P1/Inputs/P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf)

- **P1 normalized outputs (Phase 2)**
  - [`phases/P1/Outputs/P1.2_SitePlans_ElectricalContext_Excerpts_2026-01-18.pdf`](https://rc979.github.io/EEIntake/phases/P1/Outputs/P1.2_SitePlans_ElectricalContext_Excerpts_2026-01-18.pdf)
  - [`phases/P1/Outputs/P1.2_PanelSchedules_Normalized_MDP_Subpanels_2026-01-18.pdf`](https://rc979.github.io/EEIntake/phases/P1/Outputs/P1.2_PanelSchedules_Normalized_MDP_Subpanels_2026-01-18.pdf)
  - [`phases/P1/Outputs/P1.2_Photos_Annotated_Index_2026-01-18.pdf`](https://rc979.github.io/EEIntake/phases/P1/Outputs/P1.2_Photos_Annotated_Index_2026-01-18.pdf)
  - [`phases/P1/Outputs/P1.2_EVSE_CutSheet_FrozenForDesign_revA_2026-01-18.pdf`](https://rc979.github.io/EEIntake/phases/P1/Outputs/P1.2_EVSE_CutSheet_FrozenForDesign_revA_2026-01-18.pdf)
  - [`phases/P1/Outputs/P1.2_AHJ_CodeBasis_Normalized_2026-01-18.pdf`](https://rc979.github.io/EEIntake/phases/P1/Outputs/P1.2_AHJ_CodeBasis_Normalized_2026-01-18.pdf)

### 12.3 Phase 3 — System Design and Load Calculation

- **P2 engineering work products**
  - [`phases/P2/Outputs/P2.1_LoadCalc_Workbook_2026-01-22.xlsx`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.1_LoadCalc_Workbook_2026-01-22.xlsx.html)
  - [`phases/P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf)
  - [`phases/P2/Outputs/P2.1_LoadCalc_CheckMemo_2026-01-22.pdf`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.1_LoadCalc_CheckMemo_2026-01-22.pdf)
  - [`phases/P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf`](https://rc979.github.io/EEIntake/phases/P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf)
  - [`phases/P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf`](https://rc979.github.io/EEIntake/phases/P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf)

### 12.4 Phase 4 — Preliminary Drawing Set Production

- **P3 inputs**
  - [`phases/P3/Inputs/P3-PARK_ParkingLayout_OwnerProvided_2026-01-20.pdf`](https://rc979.github.io/EEIntake/phases/P3/Inputs/P3-PARK_ParkingLayout_OwnerProvided_2026-01-20.pdf)
  - [`phases/P3/Inputs/P3-I03_RoutingAssumptions_InstallerMemo_2026-01-20.pdf`](https://rc979.github.io/EEIntake/phases/P3/Inputs/P3-I03_RoutingAssumptions_InstallerMemo_2026-01-20.pdf)

- **P3 drawing work products**
  - [`phases/P3/Outputs/P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf)
  - [`phases/P3/Outputs/P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf)
  - [`phases/P3/Outputs/P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf)
  - [`phases/P3/Outputs/P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf)
  - [`phases/P3/Outputs/P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf)
  - [`phases/P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf`](https://rc979.github.io/EEIntake/phases/P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf)

### 12.5 Phase 5 — Permitting Submission (AHJ)

- **P4 inputs**
  - [`phases/P4/Inputs/P4-EOR_ReviewNotes_2026-01-28.pdf`](https://rc979.github.io/EEIntake/phases/P4/Inputs/P4-EOR_ReviewNotes_2026-01-28.pdf)

- **P4 submission outputs**
  - [`phases/P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf)
  - [`phases/P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf)
  - [`phases/P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf)
  - [`phases/P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf)
  - [`phases/P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf)
  - [`phases/P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx`](https://rc979.github.io/EEIntake/phases/P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx.html)

### 12.6 Phase 6 — Authority Review and Drawing Revision (AHJ)

- **P5 inputs**
  - [`phases/P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf`](https://rc979.github.io/EEIntake/phases/P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf)

- **P5 review/revision outputs**
  - [`phases/P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx.html)
  - [`phases/P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf)
  - [`phases/P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf)
  - [`phases/P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf)
  - [`phases/P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf)
  - [`phases/P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf`](https://rc979.github.io/EEIntake/phases/P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf)

### 12.7 Phase 7 — Utility Coordination

- **P6 inputs**
  - [`phases/P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf`](https://rc979.github.io/EEIntake/phases/P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf)
  - [`phases/P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf`](https://rc979.github.io/EEIntake/phases/P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf)

- **P6 coordination outputs**
  - [`phases/P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf)
  - [`phases/P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf)
  - [`phases/P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf)
  - [`phases/P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx.html)
  - [`phases/P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf)
  - [`phases/P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf)
  - [`phases/P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf`](https://rc979.github.io/EEIntake/phases/P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf)

### 12.8 Phase 8 — Electrical Closeout and Handover

- **P7 inputs**
  - [`phases/P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf`](https://rc979.github.io/EEIntake/phases/P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf)
  - [`phases/P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf`](https://rc979.github.io/EEIntake/phases/P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf)

- **P7 closeout outputs**
  - [`phases/P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf)
  - [`phases/P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf)
  - [`phases/P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx.html)
  - [`phases/P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf`](https://rc979.github.io/EEIntake/phases/P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf)


<a id="addendum-b"></a>

## 13 Addendum B: Party Directory (Roles + Contacts)

This addendum lists all parties referenced in this document. **Contact details are example placeholders** and must be replaced with real information.

| Party | Works for | Role | Email | Phone |
|:---- |:---- |:---- |:---- |:---- |
| Owner (Entity) | Place Property Ownership | Project owner / applicant | ev-projects@owner.example | +1-650-555-0120 |
| Owner/Architect (Entity) | ABC Architects | Plan source / record drawings provider | projects@architect.example | +1-650-555-0121 |
| Installer (Entity) | EV Install Services | Installation contractor / field coordination | pm@installer.example | +1-650-555-0122 |
| Electrical Contractor (Entity) | Romero Electric | Electrical contractor | service@electric.example | +1-650-555-0123 |
| Nora Patel | Owner | Owner representative | nora.patel@owner.example | +1-650-555-0101 |
| Mia Chen | Installer | Installer PM | mia.chen@installer.example | +1-650-555-0102 |
| Luis Romero | Electrical Contractor | Electrician / field lead | luis.romero@electric.example | +1-650-555-0103 |
| Priya Shah, PE | Engineer-of-Record | Electrical engineer (EOR) | priya.shah@eor.example | +1-650-555-0104 |
| Alex Kim, EE | Independent Reviewer | Electrical engineer (independent check) | alex.kim@review.example | +1-650-555-0105 |
| Sam Ortega | Design/CAD | CAD technician | sam.ortega@cad.example | +1-650-555-0106 |
| Ethan Brooks | Document Control | Document control | ethan.brooks@docs.example | +1-650-555-0107 |
| Jordan Lee | Project Management | Project manager | jordan.lee@pm.example | +1-650-555-0108 |
| Taylor Nguyen | Utility | Utility account rep (technical) | taylor.nguyen@utility.example | +1-650-555-0109 |
| EVSE Manufacturer (Entity) | ElectriCharge | EVSE cut sheet issuer | support@electricharge.example | +1-800-555-0124 |
| EMS Vendor (Entity) | Schlage / ChargePoint | Load management / EMS tech source | ems-support@emsvendor.example | +1-800-555-0125 |
| City of Palo Alto – Building Division (Electrical Permits) | AHJ | Electrical permitting authority / plan check | permits@paloalto.example | +1-650-555-0110 |
| Local Electrical Utility (Portal) | Utility | Utility interconnection/load review | evprogram@utility.example | +1-800-555-0111 |
