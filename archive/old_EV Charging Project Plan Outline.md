## Main

![Realistic image of multiple electric vehicles charging at a commercial site][image1]

## EV Charging Site Project Plan

This document outlines the phased plan for the development and installation of an Electric Vehicle (EV) charging site, detailing the deliverables and their required inputs across seven distinct phases.


## Executive Summary

This document is the **master, traceable closeout deliverable** for an EV charging site electrical project. It is structured by phases (0–7) and, for each phase, records:
- The **prerequisite inputs** required (and how they were provided), via evidence indexes with stable filenames
- How phase deliverables were **crafted** (calculation logs, decision records, compilation/QA logs)
- The chain of custody through **submissions, rework cycles, and approvals** (AHJ + utility), using receipts and acceptance artifacts

**Scope boundaries:** This master deliverable is intentionally **electrical-only**. It excludes **civil/constructability** topics and all **business/cost/schedule** content.

**Print/layout note (portrait letter):** The main document uses **reference IDs** (e.g., `P3-W06`, `P5-W07`) to keep tables readable when printed. Filenames are consolidated in **Addendum A**.



<a id="table-of-contents"></a>
## Table of Contents

- [Phase Overview (Deliverables by Phase)](#phase-overview)
- [Phase 0: Project Initiation and Feasibility](#phase-0)
- [Phase 1: Data Collection and Site Analysis](#phase-1)
- [Phase 2: System Design and Load Calculation](#phase-2)
- [Phase 3: Preliminary Drawing Set Production](#phase-3)
- [Phase 4: Permitting Submission](#phase-4)
- [Phase 5: Authority Review and Drawing Revision](#phase-5)
- [Phase 6: Utility Coordination](#phase-6)
- [Phase 7: Electrical Closeout and Handover](#phase-7)
- [Addendum A: Stable Filename Index (by Phase)](#addendum-a)
- [Addendum B: Party Directory (Roles + Contacts)](#addendum-b)

<a id="phase-overview"></a>
## Phase Overview (Deliverables by Phase)

### Phase 0: Project Initiation and Feasibility

This phase establishes the foundational viability of the project.

* **P0.0 Project Technical Intake Record**: Captures project identifiers, technical constraints, stakeholders/roles, and approvers.  
* **P0.1 Feasibility Memo / Go–No-Go (Screening-Level)**: Uses Phase 0 inputs to determine preliminary electrical viability and define conditions to proceed.  
* **P0.2 Input Register + Evidence Index**: Lists every prerequisite input with provenance (who/when/how provided), versioning, verification method, and evidence pointers.  
* **P0.3 Assumption + Exclusion Register**: Records Phase 0 assumptions (with owners to validate) and explicit exclusions (including civil/constructability and business/cost/schedule).  
* **P0.4 Preliminary Electrical Basis of Design (BOD)**: Freezes the Phase 0 “technical truth” set (or explicitly flags TBDs) used to seed later deliverables.  
* **P0.5 Forward Traceability Map**: Shows how Phase 0 inputs/assumptions flow into deliverables in Phases 1–7.

### Phase 1: Data Collection and Site Analysis

This phase involves gathering and standardizing all necessary information about the existing site.

* **P1.1 Intake Checklist – Complete**: Requires Site plans (Owner/Architect), Panel schedules (Electrician), Photos (Installer), Charger SKUs (Installer/Vendor), and AHJ (Address).  
* **P1.2 Normalized Site Data Package**: Requires Raw plans (P1.1), Photos (P1.1), and Schedules (P1.1).

### Phase 2: System Design and Load Calculation

The focus of this phase is on determining the site's electrical capacity and selecting the appropriate EV charging system architecture.

* **P2.1 NEC Load Calculation**: Requires Panel schedules (Electrician), EVSE ratings (Manufacturer), and NEC methods (Code).  
* **P2.2 EV System Architecture Decision**: Requires Load results (EE, P2.1), Charger mix (Installer/Owner), and Site constraints (P1.2).

### Phase 3: Preliminary Drawing Set Production

This phase produces the necessary detailed **electrical** drawings required for permitting review.

* **P3.1 Preliminary One-Line Diagram**: Requires Architecture decision (P2.2), Service info (Utility bill/As-builts), and Charger specs (Manufacturer).  
* **P3.2 Site Plan w/ EVSE Locations**: Requires Base site plan (Owner/Architect) and Parking layout (Owner).  
* **P3.3 Conduit & Trenching Details**: Requires Routing assumptions (Installer) and Site conditions (Photos, P1.2).  
* **P3.4 Updated Panel Schedules**: Requires Existing schedules (Electrician) and New EV loads (EE, P2.1).  
* **P3.5 Electrical Notes & Code Sheets**: Requires Jurisdiction (Address) and Standard templates (Internal).  
* **P3.6 Permit Drawing Set – Unstamped**: Requires One-line (P3.1), Site plan (P3.2), Details (P3.3), Schedules (P3.4), and Notes (P3.5).

### Phase 4: Permitting Submission

This phase focuses on the formal submission of documents required to obtain construction permits.

* **P4.1 Stamped Permit Drawings**: Requires Unstamped drawing set (P3.6).  
* **P4.2 Permit Application Package**: Requires Stamped plans (P4.1), Permit forms (AHJ), and Project metadata (P1.2 / P3.6).

### Phase 5: Authority Review and Drawing Revision

This phase addresses any feedback or comments received from the AHJ and ensures that all drawing revisions are complete.

* **P5.1 AHJ Comment Log – Parsed**: Requires Plan check comments (AHJ).  
* **P5.2 Revised Drawings – Post-Comments**: Requires Comment log (P5.1) and Prior drawings (P3.6 / P4.1).  
* **P5.3 Comment Response Letter**: Requires AHJ comments (AHJ) and Revised drawings (P5.2).

### Phase 6: Utility Coordination

This phase handles all necessary applications and coordination with the local electrical utility company.

* **P6.1 Utility Load Letter / Single-Line**: Requires Load calc (P2.1) and Service info (Utility bill/As-builts).  
* **P6.2 Utility Application Forms**: Requires Utility requirements (Utility portal) and Project data (P2.1 / P3.6).

### Phase 7: Electrical Closeout and Handover

The final phase involves documenting the completed site and providing necessary support for final inspections and system activation.

* **P7.1 As-Built Drawings**: Requires Field redlines (Electrician/Installer) and Inspector notes (AHJ).  
* **P7.2 Inspection Support Responses**: Requires Inspector feedback (AHJ).

# 

<a id="phase-0"></a>
# **Phase 0: Project Initiation and Feasibility**

## **IMPORTANT: Phase 0 Purpose and Boundaries (Read First)**

Phase 0 exists to produce a **traceable, evidence-backed, screening-level** feasibility determination for the project’s electrical viability and to define the prerequisite inputs needed to complete later phases.  

**Phase 0 is NOT permit-grade engineering**. Any screening calculations in Phase 0 are explicitly **superseded by Phase 2 (P2.1 NEC Load Calculation)** and must not be reused for permit submittals.

**NOTE:** The Phase 0 register fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” deliverable package. Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **P0.0 Project Technical Intake Record**

| Field | Value |
| :---- | :---- |
| Project name | EV Charging Site Project |
| Site address | Place (Palo Alto, CA) |
| Building type | Multifamily residential (common-area charging) |
| Applicable code basis (prelim) | 2022 California Electrical Code (CEC) (confirm in Phase 1 / P1.1) |
| Electrical constraint | Use existing service; avoid service upgrade **unless unavoidable for code compliance** |
| Intended EVSE deployment (prelim) | 8 ports, Level 2 (confirm by cut sheets) |
| Primary stakeholders | Owner, Installer, Electrician, Engineer-of-Record, Project Manager |
| Technical approvers | Engineer-of-Record (final), Owner (program intent), Installer (equipment selection) |

## **P0.2 Input Register + Evidence Index (Prerequisite Inputs)**

This register is the authoritative list of Phase 0 inputs and **how they were provided**.

| Input ID | Input | Provenance (who / how / when) | Evidence reference ID(s) | Verification + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P0-I01 | Utility bills / usage history (≥12 months) | Nora Patel (Owner Rep)<br>Owner email + shared drive link<br>Received: 2026-01-08 (v1.0) | P0-I01 | Verify: service address + meter/account match; 12-month coverage<br>Used in: P0.1, P0.4, P2.1, P6.1 |
| P0-I02 | Service characteristics (rating, voltage/phase) | Luis Romero (Electrician) + utility portal export<br>Electrician upload + portal capture PDF<br>Received: 2026-01-09 (v1.1) | P0-I02 | Verify: nameplate vs utility letter; voltage/phase match<br>Used in: P0.1, P0.4, P2.1, P3.1, P6.1 |
| P0-I03 | EVSE intent (make/model) | Mia Chen (Installer PM)<br>Installer email (PDF cut sheet)<br>Received: 2026-01-10 (v1.0) | P0-I03 | Verify: cut sheet ratings + OCPD guidance<br>Used in: P0.1, P0.4, P1.1, P2.1, P2.2, P3.1 |
| P0-I04 | Site photos (electrical gear + context) | Mia Chen (Installer PM)<br>Installer upload (photo set)<br>Received: 2026-01-10 (v1.0) | P0-I04 | Verify: readable ratings/labels + gear context<br>Used in: P0.1, P0.4, P1.1 |

## **P0.3 Assumption + Exclusion Register**

### **Exclusions (Scope Guardrails)**

This master deliverable intentionally excludes:
- **Civil / constructability** topics (trenching, routing, demolition, means-and-methods, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

### **Assumptions**

| Assumption ID | Assumption | Rationale + risk | Validation (owner + when) |
| :---- | :---- | :---- | :---- |
| P0-A01 | EV charging loads treated as continuous per applicable code | Rationale: standard EVSE treatment<br>Risk: under/over-sizing; feasibility error | Owner: Engineer-of-Record<br>Validate by: Phase 2 / P2.1 |
| P0-A02 | Service rating and voltage/phase match evidence | Rationale: screening requires best-available verified data<br>Risk: Phase 0 conclusions invalid | Owner: Electrician / EOR<br>Validate by: Phase 1 / P1.1 + Phase 2 / P2.1 |
| P0-A03 | EVSE may be provisional in Phase 0; frozen in Phase 1 | Rationale: SKU selection often finalizes after feasibility<br>Risk: Phase 0 estimates diverge materially | Owner: Installer<br>Validate by: Phase 1 / P1.1 |

## **P0.4 Preliminary Electrical Basis of Design (BOD)**

This BOD is the **single source of truth for Phase 0** and is the seed for later deliverables. Any “TBD” items must be closed in Phase 1.

| BOD Item | Value | Evidence (Input ID) | Status |
| :---- | :---- | :---- | :---- |
| Service rating | 800A | P0-I02 | Verified (nameplate + utility letter) |
| Service voltage/phase | 208Y/120V, 3-phase | P0-I02 | Verified (nameplate + utility letter) |
| EVSE quantity (ports) | 8 | P0-I03 | Verified (installer intent + cut sheet basis) |
| EVSE electrical characteristics | 208V, 3-phase; 32A continuous per port; 40A OCPD recommended | P0-I03 | Verified (cut sheet revA) |
| Load management posture | Required (aggregate cap to ≤250A service headroom) | P0-I01 + P0-I03 | Screening-level: confirm method/justification in P2.1/P2.2 |

## **P0.1 Feasibility Memo / Go–No-Go (Screening-Level)**

# **Project Intent and Goal**

The goal of this project is to deploy shared, common-area Level-2 EV charging for a multifamily residential building. The deployment must utilize existing electrical infrastructure without triggering a service upgrade, while preserving operational headroom and future expandability.

# **Project Scope**

* Install 8 Level-2 EVSE (approximately 7.6 kW each) in the garage common area.  
* Serve all EV loads from a dedicated EV subpanel fed from the existing 800A service.  
* Size all electrical infrastructure per NEC continuous-load requirements.

# **Required Inputs Checklist (Phase 0)**

The Phase 0 inputs are controlled by the **P0.2 Input Register + Evidence Index** above. This memo references those inputs by ID to maintain provenance and traceability.

# **Input Summaries and Analysis**

## **Utility Bills Summary (Owner)**

The provided utility bills/usage history were analyzed to estimate existing service utilization. This is a screening-level assessment and must be cross-checked using the formal NEC methodology in Phase 2 (P2.1), using verified panel schedules and EVSE ratings.

| Key Metric | Value |
| :---- | :---- |
| Main Service Size | 800 Amps @ 208Y/120V |
| Peak Demand (Past 12 Mo.) | 550 Amps |
| Average Demand (Past 12 Mo.) | 380 Amps |
| Service Capacity Utilization (Peak) | 68.75% |
| Available Headroom (Peak) | 250 Amps |

The existing service has a **250 Amp** capacity margin based on the historical peak demand of 550 Amps (out of 800 Amps total).

## **Service Size (Utility Bill)**

The existing service is confirmed to be an **800 Amp, 208Y/120V, 3-Phase** service. This matches the data used in the utility bill analysis.

## **Charger Intent (Installer/Owner)**

The project intent is the installation of **8 Level-2 EVSE ports**. At Phase 0, the EVSE electrical characteristics may be provisional until manufacturer cut sheets are provided and frozen in Phase 1 (P1.1).

**Phase 0 screening approach:** to avoid false certainty, Phase 0 uses a bounded estimate based on available intent data and clearly states the conditions under which the result changes.

# **Feasibility Memo / Go–No-Go**

**Date:** 2026-01-12

**To:** Project Stakeholders (Owner, Installer, Electrician, Engineering)

**From:** Jordan Lee, Project Manager

**Subject:** Feasibility and Recommendation for Multifamily EV Charging Project

Based on the preliminary data collection and analysis (Phase 0.1), this memo assesses the viability of the proposed scope against the project goal of deploying 8 Level-2 EVSE without a service upgrade.

## **Screening Calculation Basis (Not Permit-Grade)**

Per applicable code requirements, EV charging loads are typically treated as continuous for feeder and equipment sizing. The **formal** load calculation methodology, demand factors (if applicable), and any load management justification must be documented in **Phase 2 (P2.1)** using verified inputs.

### **Inputs used (by ID)**
- Utility usage history: **P0-I01**
- Service characteristics: **P0-I02**
- EVSE intent (provisional): **P0-I03**

### **Method**
Phase 0 computes a screening current envelope using best-available intent data and applies a continuous-load factor where appropriate. If EVSE cut sheets later show a higher continuous current than assumed here, Phase 0 conclusions must be revisited and may require load management or other architecture changes (Phase 2).

| Parameter | Calculation | Result |
| :---- | :---- | :---- |
| EVSE cut sheet continuous current (per port) | Per manufacturer cut sheet (revA) | 32 A |
| Unmanaged continuous feeder current (8 ports) | 8 \* (32 A \* 125%) | 320 A |
| Target managed aggregate cap | Service headroom basis (see below) | 250 A (cap) |

## **Existing Service Headroom Analysis**

| Parameter | Value (Amps) |
| :---- | :---- |
| Existing Service Size | 800 A |
| Historical Peak Demand | 550 A |
| Available Headroom | 250 A |
| Unmanaged EV load (continuous) | 320 A |
| Headroom deficit (unmanaged) | -70 A |
| Feasible path | Load management to cap EV demand at ≤250 A |

## **Go/No-Go Criteria (Phase 0)**

**GO** is valid only if all conditions below remain true after Phase 1/2 validation:
- Verified service characteristics (P0-I02) match the screening basis (rating and voltage/phase).
- Verified EVSE cut sheets (P0-I03 → frozen in P1.1) do not materially increase the continuous current beyond the screening assumptions.
- Formal NEC/CEC load calculation (P2.1) confirms compliance; if unmanaged loading exceeds headroom, a compliant load-management architecture must be adopted (P2.2).

## **Conclusion and Recommendation**

**GO (Conditional – Managed Load Required)**

Based on screening-level inputs **P0-I01 / P0-I02 / P0-I03**, the unmanaged code-continuous EV load for 8 ports is **320 A**, which exceeds the estimated **250 A** historical service headroom by **70 A**.

This is a **conditional GO** that requires a compliant **load management / EMS** approach in Phase 2 (P2.1/P2.2) to cap aggregate EV demand at or below the available headroom, or an alternate approach (e.g., fewer ports or different EVSE ratings) to be validated by the Engineer-of-Record.

## **Next Steps**

Proceed to **Phase 1: Data Collection and Site Analysis** to (a) freeze EVSE cut sheets and electrical characteristics in the intake package (P1.1) and (b) verify service/gear data. Then proceed to **Phase 2** to complete the formal load calculation (P2.1) and system architecture decision (P2.2).

## **P0.5 Forward Traceability Map (Phase 0 → Later Deliverables)**

This map explains how Phase 0 inputs are used to craft deliverables in later phases.

| Later deliverable | Crafted from Phase 0 items | Notes |
| :---- | :---- | :---- |
| P1.1 Intake Checklist – Complete | P0.2 (Input Register) | Phase 0 defines required evidence and provenance fields that Phase 1 must complete/verify. |
| P1.2 Normalized Site Data Package | P0.4 (BOD) + P0.3 (Assumptions) | Phase 0 sets the “truth set” that Phase 1 must confirm and normalize. |
| P2.1 NEC Load Calculation | P0-I02 + P0-I03 + P0.3 | Phase 2 supersedes Phase 0 screening; Phase 0 documents what was assumed and what must be validated. |
| P2.2 EV System Architecture Decision | P0.1 (criteria) + P2.1 results | Phase 0 defines the decision constraint (use existing service unless unavoidable) and conditions that trigger load management. |
| P3.1 Preliminary One-Line Diagram | P0-I02 + P0.4 | Phase 0 establishes service basis and initial BOD identifiers; Phase 3 depicts the engineered architecture selected in Phase 2. |
| P6.1 Utility Load Letter / Single-Line | P0-I01 + P0-I02 | Phase 0 records usage history and service basis; Phase 6 uses the validated versions. |

![An image depicting a multifamily residential building garage area with new electric vehicle charging stations installed.][image2]

<a id="phase-1"></a>
# **Phase 1: Data Collection and Site Analysis**

![A collection of technical documents, architectural blueprints, and electrical diagrams spread out on a table, representing the site analysis and data collection for an EV charging project][image3]

# **Phase 1: Data Collection and Site Analysis**

This section documents the completion of **Phase 1: Data Collection and Site Analysis** for the Electric Vehicle (EV) Charging Project. Phase 1 gathers, verifies, and normalizes the **electrical design prerequisites** into a controlled package suitable for engineering (Phase 2).

**NOTE:** The Phase 1 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, evidence pointers, and logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 1 Boundaries (Electrical-Only)**

Phase 1 captures information required to perform electrical engineering and code compliance tasks. It intentionally excludes:
- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

# **P1.1 Intake Checklist – Complete**

This checklist confirms the acquisition of required Phase 1 inputs and links each item to an evidence record in **P1.0**. Acceptance criteria are included to make “Complete” auditable.

| Input ID | Input | Source | Status | Acceptance criteria (electrical-only) | Verified by | Date |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| P1-I01 | Site plans (electrical context excerpts) | Owner/Architect | Complete | Includes service room location and electrical-room plan excerpts; revision/date visible | Priya Shah (Project Engineer) | 2026-01-18 |
| P1-I02 | Panel schedules (MDP + relevant subpanels) | Electrician | Complete | Legible; identifies main breaker rating, bus rating, voltage/phase, spare spaces; latest revision noted | Priya Shah (Project Engineer) | 2026-01-18 |
| P1-I03 | Photo set (service gear + nameplates + breaker labels) | Installer | Complete | Nameplates readable; includes context + closeups; photos indexed/annotated | Priya Shah (Project Engineer) | 2026-01-18 |
| P1-I04 | EVSE cut sheets (final for design basis) | Installer/Vendor | Complete | Includes electrical ratings, continuous current, OCPD guidance; revision identified; matches program intent | Priya Shah (Project Engineer) | 2026-01-18 |
| P1-I05 | AHJ + adopted electrical code edition | Owner/Address + AHJ website | Complete | Electrical permitting authority identified; code edition and amendments source recorded | Jordan Lee (Project Manager) | 2026-01-18 |

## **P1.0 Input Register + Evidence Index (Stable Filenames)**

This register records **how inputs were provided** and where they are stored. File names are stable and referenced throughout the master deliverable.

| Input ID | Input | Provenance (who / how / when) | Evidence reference ID(s) | Verification + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P1-I01 | Site plans (electrical context excerpts) | Nora Patel (Owner Rep)<br>Owner email + shared drive link<br>Received: 2026-01-15 (v2.0) | P1-I01 | Verify: revision/date + title block + electrical-room location<br>Derived from: P0-I04 (context)<br>Used in: P1.1, P1.2, P3.1 |
| P1-I02 | Panel schedules (MDP + relevant subpanels) | Luis Romero (Electrician)<br>Electrician upload (PDF)<br>Received: 2026-01-16 (v1.0) | P1-I02 | Verify: cross-check MDP ratings vs P0-I02; legibility; spare spaces<br>Derived from: P0-I02<br>Used in: P1.1, P1.2, P2.1, P3.4 |
| P1-I03 | Photo set (service gear + nameplates + labels) | Mia Chen (Installer PM)<br>Installer upload (photo set + index)<br>Received: 2026-01-16 (v1.0) | P1-I03 | Verify: nameplates readable; photos correspond to MDP + meter/service gear<br>Derived from: P0-I02 + P0-I04<br>Used in: P1.1, P1.2, P3.1 |
| P1-I04 | EVSE cut sheets (final for design basis) | Mia Chen (Installer PM)<br>Installer email (PDF)<br>Received: 2026-01-16 (revA) | P1-I04 | Verify: voltage/phase + continuous current + OCPD; matches Phase 0 intent<br>Derived from: P0-I03<br>Used in: P1.1, P1.2, P2.1, P2.2, P3.1 |
| P1-I05 | AHJ + code basis evidence | Jordan Lee (PM)<br>AHJ website capture + notes<br>Received: 2026-01-17 (v1.0) | P1-I05 | Verify: AHJ name + adopted code edition + capture metadata<br>Derived from: N/A<br>Used in: P1.1, P1.2, P3.5, P4.2 |

## **Key Excerpts (Electrical-Only)**

To satisfy master-deliverable traceability, the following excerpts capture the **minimum critical information** needed to proceed. Full documents remain indexed in **P1.0**.

### **Site Plans – Electrical Context Excerpts (P1-I01)**

**Excerpted findings (from plan title block and electrical-room plan excerpt):**
- Building address and revision/date shown on drawings (Rev 2, 2026-01-15).
- Electrical service room identified on plan (label: “Electrical Room / Main Switchgear”).
- Service entry point and main electrical gear room boundary shown for reference (no routing/constructability assumptions made here).

### **Panel Schedules – MDP Excerpt (P1-I02)**

**Excerpted data (MDP schedule header and key fields):**
- Panel designation: **MDP**
- Main device: **800A main**
- Bus rating: **800A**
- System: **208Y/120V, 3-phase**
- Available spaces: **4 (3-pole)**

### **Photo Set – Nameplate/Label Verification Excerpts (P1-I03)**

**Excerpted verifications (from annotated photo index):**
- MDP nameplate confirms **800A**, **208Y/120V**, **3-phase**.
- Meter/service labeling matches the service characteristics used in Phase 0.
- Breaker labeling is legible for engineering validation of schedules (no field-modification assumptions made).

### **EVSE Cut Sheet – Electrical Rating Excerpt (P1-I04)**

**Excerpted electrical basis (from cut sheet revA):**
- Model: **ElectriCharge L2-7.6-G**
- Supply: **208V, 3-phase**
- Continuous current: **32A**
- Recommended OCPD: **40A**

### **AHJ / Code Basis – Evidence Excerpt (P1-I05)**

**Excerpted jurisdiction basis:**
- Electrical permitting authority (AHJ): **City of Palo Alto – Building Division (Electrical Permits)** (as documented in evidence capture)
- Adopted code basis: **2022 California Electrical Code (CEC)** (source captured in P1-I05)

## **Required Input Details**

### **Site Plans**

The site plans confirm the location of the primary service/electrical room and provide electrical-context plan excerpts for engineering reference. Phase 1 does not assert installation routing, trenching, or constructability.

![Architectural floor plan showing the layout of a multi-family residential garage with a designated area for new electric vehicle charging stations][image4]

### **Panel Schedules (Electrician)**

The schedules below are for the Main Distribution Panel (MDP), confirming the service details and available space.

* **Panel Designation:** MDP  
* **Main Service:** 800A Main  
* **Bus Rating:** 800A  
* **Service Voltage:** 208Y/120V, 3-Phase  
* **Connected Load:** 550A  
* **Available Spaces:** 4 (Three-Pole)

### **Photos (Installer)**

Photos were taken to document the existing main service gear and the physical conditions of the proposed installation location.

![Close-up photograph of a large commercial electrical main distribution panel and utility meter in a service room][image5]

![Photograph of a concrete parking garage area, showing the proximity to the electrical room and the proposed location for the EV charging stations][image6]

### **Charger SKUs (Installer/Vendor)**

The selected EVSE model specifications are detailed below.

| Parameter | Value |
| :---- | :---- |
| Model Name | ElectriCharge L2-7.6-G |
| Output Power | 7.6 kW (Nominal) |
| Voltage | 208V, 3-Phase |
| Continuous Current Draw | 32A @ 208V |
| Required OCPD Size | 40A |

### **Authority Having Jurisdiction (AHJ)**

The electrical permitting jurisdiction and adopted code basis are confirmed (see P1-I05 evidence capture).

| Data Point | Value |
| :---- | :---- |
| Jurisdiction (Electrical) | City of Palo Alto – Building Division (Electrical Permits) |
| Site Address | Place (Palo Alto, CA) |
| Applicable Code | 2022 California Electrical Code (CEC) |

# **P1.2 Normalized Site Data Package**

The raw inputs from **P1.0/P1.1** have been processed, cross-referenced, and standardized into a controlled package for engineering use. This ensures all teams reference consistent, verified figures and stable filenames.

## **P1.2 Normalization Rules (Document Control)**

The following rules were applied to create a consistent engineering package:
- **File naming**: `P1.2_<Category>_<Descriptor>_<YYYY-MM-DD>.<ext>`
- **PDF standard**: all PDFs normalized to portrait orientation where feasible, searchable text (OCR applied when needed), and bookmarks added for long sets
- **Redactions**: personal information removed where present (non-technical)
- **Revisions**: latest revision is used; superseded versions retained but marked “Superseded” in filenames
- **Extraction**: key electrical data extracted into tables for engineering use; extraction sources are cited back to `P1.0` evidence pointers

## **P1.2 Normalization / Validation Log (Raw → Normalized)**

| Log ID | Raw → Normalized (evidence IDs) | Transformation performed | Validated (by/date) |
| :---- | :---- | :---- | :---- |
| P1-N01 | Raw: P1-I01 → Out: P1.2 Electrical-context plan excerpts | Extracted electrical-room/service-context sheets; bookmarks; OCR verified | Priya Shah / 2026-01-18 |
| P1-N02 | Raw: P1-I02 → Out: P1.2 Normalized panel schedules | Cleaned scan; OCR; standardized order; header callouts | Priya Shah / 2026-01-18 |
| P1-N03 | Raw: P1-I03 → Out: P1.2 Annotated photo index | Selected nameplate/label photos; annotated; created index | Priya Shah / 2026-01-18 |
| P1-N04 | Raw: P1-I04 → Out: P1.2 EVSE cut sheet (frozen for design) | Marked “Frozen for design basis”; extracted ratings summary | Priya Shah / 2026-01-18 |
| P1-N05 | Raw: P1-I05 → Out: P1.2 AHJ/code basis evidence | Verified AHJ naming; standardized capture; recorded metadata | Jordan Lee / 2026-01-18 |

The following table summarizes standardized data points derived from Phase 1 inputs and their normalized outputs.

| Data Element | Standardized Value | Notes |
| :---- | :---- | :---- |
| Electrical context plan excerpts | `P1.2_SitePlans_ElectricalContext_Excerpts_2026-01-18.pdf` | Electrical-room/service context only; no routing assumptions. |
| Panel schedule package (MDP + relevant) | `P1.2_PanelSchedules_Normalized_MDP_Subpanels_2026-01-18.pdf` | Used for Phase 2 load calc and Phase 3 schedule updates. |
| EVSE design-basis cut sheet | `P1.2_EVSE_CutSheet_FrozenForDesign_revA_2026-01-18.pdf` | Frozen for Phase 2/3 design basis. |
| AHJ/code basis evidence | `P1.2_AHJ_CodeBasis_Normalized_2026-01-18.pdf` | Supports code sheets and permit application package. |
| Service gear photo index | `P1.2_Photos_Annotated_Index_2026-01-18.pdf` | Confirms ratings/labels used in Phase 0/2/3. |
| Utility coordination contact (technical) | Utility account rep: Taylor Nguyen (mock) | Technical point of contact for Phase 6 coordination. |

## **Data Standardization Certification**

The data package is formally certified for completeness and integrity.

# 

| Certification Point | Status | Certified By | Date |
| ----- | ----- | ----- | ----- |
| Data Integrity | Certified | Priya Shah (Project Engineer) | 2026-01-18 |
| File Format Standardization | Certified | Ethan Brooks (Document Control) | 2026-01-18 |
| Completeness Check | Certified | Jordan Lee (Project Manager) | 2026-01-18 |

# **Next Steps**

Phase 1 is complete. The **Normalized Site Data Package (P1.2)** is finalized and is the required input for all subsequent design and engineering activities.

The project proceeds to **Phase 2: System Design and Load Calculation**, using the certified data package (P1.2) to perform the NEC Load Calculation (P2.1) and determine the final EV System Architecture (P2.2).

<a id="phase-2"></a>
# **Phase 2: System Design and Load Calculation**

![close-up image of electrical schematics and blueprints being reviewed by an engineer][image9]

# **EV Charging Project Plan: Phase 2 Documentation**

This section formalizes the outputs of **Phase 2: System Design and Load Calculation** for the Electric Vehicle (EV) Charging Site Project. Phase 2 uses the controlled Phase 1 package (P1.2) to produce a **permit-relevant electrical load calculation** and an **architecture decision record** suitable to seed the drawing set in Phase 3.

# **Phase 2: System Design and Load Calculation**

**NOTE:** The Phase 2 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, stable evidence pointers, and decision logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 2 Boundaries (Electrical-Only)**

Phase 2 captures information required to perform electrical engineering and code compliance tasks. It intentionally excludes:
- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

The goal of Phase 2 is to confirm that the proposed EV charging system is electrically viable and compliant with the applicable code basis (CEC/NEC as adopted by the AHJ), and to select a compliant system architecture that satisfies the project’s electrical constraint of avoiding a service upgrade unless unavoidable.

## **P2.0 Phase 2 Evidence Index + Engineering Work Products**

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P2-W01 | Load calculation workbook + summary | Priya Shah, PE (mock)<br>Spreadsheet + PDF export<br>Date: 2026-01-22 (v1.0) | P2/Outputs/P2.1_LoadCalc_Workbook_2026-01-22.xlsx<br>P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf | Inputs: P1.2 panel schedules + EVSE cut sheet + AHJ/code basis<br>Used in: P2.1, P3.4, P4.2, P6.1 |
| P2-W02 | Independent load calc check memo | Alex Kim, EE (mock)<br>Redline review + sign-off<br>Date: 2026-01-22 (v1.0) | P2/Outputs/P2.1_LoadCalc_CheckMemo_2026-01-22.pdf | Inputs: P2-W01<br>Used in: P2.1 |
| P2-W03 | Architecture decision record | Priya Shah, PE (mock)<br>Engineering memo + diagram<br>Date: 2026-01-22 (v1.0) | P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf | Inputs: P2-W01 + P1.2 evidence<br>Used in: P2.2, P3.1, P3.4, P3.5 |
| P2-W04 | EMS technical brief | Mia Chen (Installer PM)<br>Vendor PDF<br>Date: 2026-01-21 (revB) | P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf | Inputs: N/A<br>Used in: P2.2, P3.1, P3.5 |

## **Key Excerpts (Electrical-Only)**

### **Load Calc Summary Excerpt (P2-W01)**

**Excerpted results:**
- EVSE continuous current basis: **32A per port** (from P1.2 EVSE cut sheet)
- Continuous load factor applied per code basis: **125%**
- Aggregate unmanaged EV continuous load: **320A**
- Available historical headroom basis (screening, from Phase 0): **250A**
- Outcome: unmanaged load **exceeds headroom**; a compliant load-management method is required to avoid service upgrade

### **Independent Check Excerpt (P2-W02)**

**Excerpted check outcome:** “Calculation logic and arithmetic verified; inputs align to Phase 1 evidence pointers; conclusions supported.”

### **Architecture Decision Excerpt (P2-W03)**

**Excerpted decision:** “Proceed with a 400A bus-rated EV subpanel with feeder sized for the full unmanaged continuous load, combined with a listed EMS/load management method to cap aggregate demand to ≤250A.”

## **P2.1 NEC Load Calculation**

The NEC Load Calculation confirms the exact electrical capacity required for the new EV charging infrastructure. This calculation is mandatory for permitting (P4.2) and utility coordination (P6.1).

| Input | Source (evidence ID) |
| :---- | :---- |
| Panel schedules | P1-I02 (normalized in P1.2) |
| EVSE ratings | P1-I04 (frozen for design in P1.2) |
| AHJ/code basis | P1-I05 (normalized in P1.2) |

### **Load Calculation Summary (NEC 625.42 \- Continuous Load)**

Based on the required 8 Level-2 EVSE and the NEC 625.42 requirement for 125% continuous loading:

| Parameter | Calculation | Result |
| :---- | :---- | :---- |
| Single EVSE Continuous Load | 32A \* 125% | 40 A |
| Total New Connected Load | 8 EVSE \* 40 A | 320 A |
| Required Subpanel Bus Rating | 320 A | **400 A** |
| Required Subpanel Feeder Breaker | 320 A | **350 A** |

**Conclusion:** The total NEC continuous load is **320 Amps**. This confirms that the previously available **250 Amps** of service headroom (P0.1) is *insufficient* to support the full, unmanaged, NEC-mandated continuous load.

### **Service Headroom Re-Evaluation**

Phase 0 (P0.1) established that an unmanaged, code-continuous EV load for 8 ports would exceed the available historical headroom and therefore requires a managed load approach. The formal P2.1 calculation confirms **320 Amps** unmanaged continuous load versus **250 Amps** available headroom, necessitating an **Energy Management System (EMS)** (or another compliant demand/management method) per NEC 625.42(A)(2).

| Parameter | Value (Amps) |
| :---- | :---- |
| Existing Service Size | 800 A |
| Historical Peak Demand | 550 A |
| Available Headroom (Unmanaged) | 250 A |
| Required New EV Load (Unmanaged) | 320 A |
| Load Deficit (Triggering Service Upgrade) | \-70 A |

The project must proceed with an EMS, or the core project goal of avoiding a service upgrade (P0.1) is invalid.

![close-up of a circuit board and wires, representing an electrical system][image10]

## **P2.2 EV System Architecture Decision**

This phase selects the system components and architecture to manage the required 320A load within the 250A service headroom using a Load Management System.

| Input | Source |
| :---- | :---- |
| Load results | EE (P2.1) |
| Charger mix | Installer/Owner (P1.2 EVSE basis) |
| Existing electrical conditions | P1.2 (panel schedules + photos) |
| Load management technical basis | P2-W04 (EMS technical brief) |

### **System Architecture Proposal**

To reconcile the 320A required load with the 250A available headroom, the system must incorporate an EMS that limits the total current draw of the EV subpanel to **250 Amps**.

| Element | Specification | Rationale |
| :---- | :---- | :---- |
| **Subpanel Feeder** | 350A feeder OCPD (3-pole) | Sized for the full 320A continuous load per NEC. |
| **EV Subpanel Bus** | 400A Rated | Sized for the full 320A continuous load per NEC. |
| **EMS System** | Integrated Panel-level EMS | Limits total current draw to **250 Amps** to fit within service headroom. |
| **Charger Count** | 8 Level-2 EVSE | No change to the original project scope. |
| **Charger Circuits** | 40A OCPD, 8 circuits | Individual circuits are sized per the NEC for each charger's continuous load. |

### **Decision**

**EV System Architecture Decision: Managed Load System (Go)**

The project will utilize a 400A bus-rated EV subpanel fed by a 350A breaker, integrated with an EMS to dynamically limit the total demand to **250 Amps**. This meets all requirements: NEC compliance (via subpanel rating) and project goal (via EMS management to avoid service upgrade).

## **Phase 2 Engineering Certification (Mock)**

| Certification Point | Status | Certified By | Date |
| :---- | :---- | :---- | :---- |
| Load calculation prepared | Certified | Priya Shah, PE (mock) | 2026-01-22 |
| Independent check completed | Certified | Alex Kim, EE (mock) | 2026-01-22 |
| Architecture decision documented | Certified | Priya Shah, PE (mock) | 2026-01-22 |
| Inputs traceable to Phase 1 evidence pointers | Certified | Ethan Brooks (Document Control) | 2026-01-22 |

# **Next Steps**

Phase 2 is complete. The system architecture and exact load requirements are confirmed.

The project proceeds to **Phase 3: Preliminary Drawing Set Production**. The outputs of Phase 2, including the P2.1 Load Calculation and the P2.2 Architecture Decision, are the mandatory inputs for all drawings in Phase 3\.

<a id="phase-3"></a>
# **Phase 3: Preliminary Drawing Set Production**

![A blueprint-style architectural drawing with lines and symbols representing an electric vehicle charging station layout, overlaid with electrical schematic lines.][image11]

# **EV Charging Project Plan: Phase 3 Documentation**

This section formalizes the outputs of **Phase 3: Preliminary Drawing Set Production** for the Electric Vehicle (EV) Charging Site Project. Phase 3 translates the approved system design (Phase 2\) into an **unstamped electrical permit drawing set** suitable for engineering stamp (Phase 4) and AHJ electrical review.

# **Phase 3: Preliminary Drawing Set Production**

**NOTE:** The Phase 3 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and compilation logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 3 Boundaries (Electrical-Only)**

Phase 3 captures permit-drawing content required for electrical engineering and code compliance. It intentionally excludes:
- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

The goal of Phase 3 is to produce the **unstamped electrical permit drawing set** that incorporates the electrical design and code requirements confirmed in Phases 1 and 2\.

## **P3.0 Evidence Index + Drawing Work Products (Stable Filenames)**

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P3-W01 | Preliminary one-line diagram (sheet) | Sam Ortega (CAD Tech, mock) + Priya Shah, PE (mock)<br>CAD + PDF export<br>Date: 2026-01-26 (v1.0) | P3/Outputs/P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf | Inputs: P2.2 decision; P1.2 schedules; P1.2 EVSE; P1.2 code basis<br>Used in: P3.1, P3.6 |
| P3-W02 | Site plan w/ EVSE locations (electrical-impacting) | Sam Ortega (CAD Tech, mock)<br>CAD + PDF export<br>Date: 2026-01-26 (v1.0) | P3/Outputs/P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf | Inputs: base site plan (owner/architect) + parking layout (owner) + P1.2 context<br>Used in: P3.2, P3.6 |
| P3-W03 | Conduit & trenching details (electrical-impacting) | Priya Shah, PE (mock) + Sam Ortega (CAD Tech, mock)<br>CAD notes + PDF export<br>Date: 2026-01-26 (v1.0) | P3/Outputs/P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf | Inputs: routing assumptions (installer) + P1.2 photos + code basis<br>Used in: P3.3, P3.6 |
| P3-W04 | Updated panel schedules (MDP + EVSP-1) | Priya Shah, PE (mock)<br>Spreadsheet + PDF export<br>Date: 2026-01-26 (v1.0) | P3/Outputs/P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf | Inputs: P1.2 schedules + P2.1 + P2.2<br>Used in: P3.4, P3.6 |
| P3-W05 | Electrical notes & code sheets | Priya Shah, PE (mock)<br>Template + PDF export<br>Date: 2026-01-26 (v1.0) | P3/Outputs/P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf | Inputs: P1.2 code basis + P2 decision + EMS brief<br>Used in: P3.5, P3.6 |
| P3-W06 | Permit drawing set (unstamped, compiled) | Ethan Brooks (Document Control)<br>PDF compilation<br>Date: 2026-01-26 (v1.0) | P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf | Inputs: P3-W01..P3-W05<br>Used in: P3.6, P4.1 |

## **Key Excerpts (Electrical-Only)**

### **One-Line Diagram Excerpt (P3-W01)**

**Excerpted design basis:**
- Existing service: **800A, 208Y/120V, 3Φ** (Phase 1 evidence)
- New EV subpanel: **400A bus**; feeder OCPD: **350A, 3-pole**
- EVSE branch circuits: **8 circuits**, each **40A OCPD** for **32A continuous** ports
- Load management: **EMS caps aggregate EV demand to ≤250A** per Phase 2 decision

### **Site Plan w/ EVSE Locations Excerpt (P3-W02)**

**Excerpted content:** EVSE locations are shown based on owner/parking layout inputs, along with electrical equipment identifiers. Only items that affect electrical design are called out (equipment locations, electrical room reference, and design-relevant constraints).

### **Conduit & Trenching Details Excerpt (P3-W03)**

**Excerpted content:** Electrical-impacting routing assumptions and site-condition constraints are documented for engineering use (e.g., feeder length basis for voltage drop/derating), without specifying construction means-and-methods.

### **Drawing Set Compilation Excerpt (P3-W06)**

**Excerpted compilation rule:** “P3.6 includes P3.1–P3.5 in the sheet order defined below; filenames and sheet titles must match the evidence pointers exactly.”

# **P3.1 Preliminary One-Line Diagram**

This one-line diagram depicts the complete electrical system from the utility source to the EV charging equipment. It defines major equipment, ratings, overcurrent protection, grounding intent, and the Energy Management System (EMS) used to manage aggregate EV load.

## **Inputs (traceable)**

 - Architecture Decision: P2-W03 (see Addendum A for filenames)

 - Service / MDP information: P1-I02 + P1-I03 (see Addendum A for filenames)

 - EVSE cut sheet (design basis): P1-I04 (see Addendum A for filenames)

## **System Description (summary)**

The one-line diagram shows a new **400A, 120/208V, 3-phase EV subpanel** connected to the existing **800A MDP** via a **350A, 3-pole feeder OCPD**. A listed **Energy Management System (EMS)** is shown controlling aggregate EV demand to **≤250A** in accordance with the managed-load approach documented in Phase 2.

## **Technical Specifications Shown on the Diagram (excerpt list)**

### **Utility Source and Fault Data (mock design inputs)**

 - Utility transformer identifier: TX-485-A

 - Available fault current at MDP bus: 42 kA (utility-provided short-circuit data)

 - Calculated available fault current at EV subpanel bus: 38 kA (based on feeder impedance)

### **Panel and Protection Ratings**

 - MDP bus rating: 800 A

 - EV subpanel bus rating: 400 A

 - EV feeder OCPD: 350 A, 3-pole

 - Breaker interrupting rating: 65 kAIC minimum at 120/208 V

### **Feeder Conductors (design basis)**

 - Phase conductors: three (3) parallel sets per phase of 250 kcmil copper, THHN/THWN-2 (design basis)

 - Neutral conductor: not required (EVSE loads are line-to-line only)

 - Equipment grounding conductor: one (1) 4/0 AWG copper (design basis)

 - Ampacity basis: sized at 75°C terminal rating per applicable code requirements; final conductor sizing to be confirmed in stamped set

### **Wiring Method (electrical-only)**

 - Wiring method is specified as a code-compliant raceway system sized per NEC Chapter 9 and applicable articles. **No routing/trenching/constructability means-and-methods are specified in this master deliverable.**

### **Grounding and Bonding (intent)**

 - Equipment grounding conductor routed with feeder conductors in all raceways

 - Bonding jumpers provided where required by wiring method and transitions

 - EV subpanel grounding bar bonded to the building grounding electrode system (referenced on details sheet)

### **Energy Management System (EMS)**

 - EMS device identified on the diagram as “Schlage / ChargePoint EMS Unit” (mock)

 - Dedicated EMS symbol legend included

 - Control interface shown between EMS and EV feeder/EVSE branch circuits

 - Fail-safe behavior note: on EMS fault/loss of comms, system defaults to a safe state that prevents EV feeder demand from exceeding the configured cap

### **Coordination and Selectivity**

 - Coordination note: verify time-current coordination between feeder OCPD and downstream branch OCPD in final stamped set

This one-line diagram is intended to be code-complete for permit review, subject to final PE stamp and any jurisdiction-specific refinements identified during Phase 4\.

# 

# 

# **P3.2 Site Plan w/ EVSE Locations**

This plan overlays EVSE and electrical equipment identifiers onto the base plan to show EVSE locations provided by the owner/parking layout inputs and to capture any **site placement constraints that affect electrical design** (equipment adjacency, electrical-room reference, and plan-check clarity). It intentionally does **not** provide constructability means-and-methods.

| Input | Source |
| :---- | :---- |
| Base site plan | P1-I01 (normalized in P1.2) |
| Parking layout | P3-PARK (see Addendum A) |
| Photo context (verification) | P1-I03 (normalized in P1.2) |

Electrical-impacting plan outputs (excerpt):
- EVSE locations labeled **EVSE-01** through **EVSE-08** per owner parking layout input
- EV subpanel identified as **EVSP-1** relative to the existing **MDP** room (reference only)
- Notes call out placement constraints that affect electrical design only (e.g., maximum assumed feeder path length basis for voltage drop checks; any “no-penetration” zones that constrain electrical routing)

![Electrical layout plan excerpt showing EVSE labels (EVSE-01 through EVSE-08), EV subpanel (EVSP-1), and reference to existing MDP room for electrical plan-check clarity.][image12]

# **P3.3 Conduit & Trenching Details (Electrical-Impacting)**

This detail sheet documents **routing assumptions** and **site-condition constraints** that affect electrical design outcomes (feeder length basis, voltage drop basis, conductor derating basis, separation requirements, and transition points), using installer-provided assumptions and Phase 1 site photos. It intentionally avoids non-electrical constructability means-and-methods.

| Input | Source |
| :---- | :---- |
| Routing assumptions | P3-I03 (see Addendum A) |
| Site conditions | P1-I03 (normalized in P1.2) |
| Code basis (separation/wiring method references) | P1-I05 (normalized in P1.2) |

Electrical-impacting detail content (excerpt):
- **Feeder length basis (mock):** 165 ft electrical path length used for voltage-drop checks and fault/impedance assumptions (final field-verified)
- **Wiring method basis:** raceway system sized per NEC Chapter 9 and applicable articles; conductor temperature/termination basis 75°C unless equipment requires otherwise
- **Derating basis:** parallel conductors and conduit fill assumptions documented for engineering sizing; final installation must comply with applicable adjustment factors
- **Separation:** power/communications separation and grounding/bonding intent documented for electrical compliance (final routing by installer)
- **Transitions/constraints:** identifies electrical-impacting transition points (e.g., “MDP room exit point” and “EVSP-1 entry point”) and any photo-identified constraints impacting electrical routing decisions

# **P3.4 Updated Panel Schedules**

The existing panel schedule for the MDP is updated to reflect the new downstream load (the 350A breaker for the EV subpanel), and a new schedule for the EV subpanel is created.

| Input | Source |
| :---- | :---- |
| Existing schedules | P1-I02 (normalized in P1.2) |
| New EV loads (calc + decision) | P2-W01 + P2-W03 |

The updated MDP schedule shows:

| Slot | Breaker | Load | Amps | Notes |
| :---- | :---- | :---- | :---- | :---- |
| 40, 42, 44 | 3-Pole, 350A | EV Subpanel | 250A Managed | Connection to New EV Subpanel |

The New EV Subpanel schedule shows:

| Slot | Breaker | Load | Amps | Notes |
| :---- | :---- | :---- | :---- | :---- |
| 1, 3, 5 | 3-Pole, 40A | EVSE \#1 | 40A | Dedicated Circuit for Continuous Load |
| 7, 9, 11 | 3-Pole, 40A | EVSE \#2 | 40A | Dedicated Circuit for Continuous Load |
| 13, 15, 17 | 3-Pole, 40A | EVSE \#3 | 40A | Dedicated Circuit for Continuous Load |
| 19, 21, 23 | 3-Pole, 40A | EVSE \#4 | 40A | Dedicated Circuit for Continuous Load |
| 25, 27, 29 | 3-Pole, 40A | EVSE \#5 | 40A | Dedicated Circuit for Continuous Load |
| 31, 33, 35 | 3-Pole, 40A | EVSE \#6 | 40A | Dedicated Circuit for Continuous Load |
| 37, 39, 41 | 3-Pole, 40A | EVSE \#7 | 40A | Dedicated Circuit for Continuous Load |
| 43, 45, 47 | 3-Pole, 40A | EVSE \#8 | 40A | Dedicated Circuit for Continuous Load |

# **P3.5 Electrical Notes & Code Sheets**

This document compiles the necessary general and project-specific notes, ensuring the construction documents clearly articulate the applicable codes, standards, and installation methods.

| Input | Source |
| :---- | :---- |
| AHJ/code basis | P1-I05 (normalized in P1.2) |
| Architecture decision | P2-W03 |
| Standard templates | Internal |

The notes sheet explicitly references the **2022 California Electrical Code (CEC)** and the use of the **NEC 625.42(A)(2)** method (EMS) to justify the 250A managed load. Key notes include:

* **A. Load Management:** The EV subpanel utilizes a listed Energy Management System (EMS) to cap the maximum aggregate demand at 250 Amps to prevent exceeding the available service headroom.  
* **B. Continuous Loads:** All EV loads are calculated at 125% demand factor per NEC 625.42.  
* **C. Wiring:** All conductors shall be sized per NEC 310 and rated for 75°C minimum.

# **P3.6 Permit Drawing Set – Unstamped**

This deliverable is the compiled **electrical permit drawing set** (unstamped), finalized and ready for the engineer of record's final stamp.

| Input | Source |
| :---- | :---- |
| One-line | P3.1 |
| Site plan | P3.2 |
| Details | P3.3 |
| Schedules | P3.4 |
| Notes | P3.5 |

This complete set, reserved as a File, is the primary output of Phase 3 and serves as the input for Phase 4\.

## **P3.6 Compilation / QA Log (Mock)**

| QA Item | Check performed | Result | Checked by | Date |
| :---- | :---- | :---- | :---- | :---- |
| Sheet inclusion | P3.1–P3.5 present in compiled PDF | Pass | Ethan Brooks (Document Control) | 2026-01-26 |
| Stable filenames | Output filenames match P3.0 evidence pointers | Pass | Ethan Brooks (Document Control) | 2026-01-26 |
| Title block consistency | Sheet titles/IDs consistent across set | Pass | Sam Ortega (CAD Tech, mock) | 2026-01-26 |
| Cross-references | Notes reference correct sheet IDs | Pass | Priya Shah, PE (mock) | 2026-01-26 |

## **Phase 3 Drawing Package Certification (Mock)**

| Certification Point | Status | Certified By | Date |
| :---- | :---- | :---- | :---- |
| Drawing set compiled (unstamped) | Certified | Ethan Brooks (Document Control) | 2026-01-26 |
| Electrical content aligns to Phase 2 decision | Certified | Priya Shah, PE (mock) | 2026-01-26 |
| Inputs traceable to Phase 1 evidence pointers | Certified | Priya Shah, PE (mock) | 2026-01-26 |

# **Next Steps**

Phase 3 is complete. The **Unstamped Permit Drawing Set (P3.6)** is finalized.

The project proceeds to **Phase 4: Permitting Submission** to obtain the **Stamped Permit Drawings (P4.1)** and assemble the permit application package (P4.2).

<a id="phase-4"></a>
# **Phase 4: Permitting Submission**

## **Phase 4 Purpose**

Phase 4 documents the formal submission of the electrical permit package to the AHJ, including the stamped drawing set, required forms, and submission receipts/tracking.

**NOTE:** The Phase 4 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and submission logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 4 Boundaries (Electrical-Only)**

Phase 4 captures the electrical permitting submission artifacts. It intentionally excludes:
- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

## **P4.0 Evidence Index + Submission Work Products (Stable Filenames)**

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P4-W01 | Stamped permit drawings (electrical set) | Priya Shah, PE (mock EOR)<br>Stamp + PDF<br>Date: 2026-01-29 (v1.0) | P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf | Inputs: P3.6 unstamped set<br>Used in: P4.1, P4.2 |
| P4-W02 | AHJ permit application form(s) | Jordan Lee (PM)<br>AHJ portal form + PDF export<br>Date: 2026-01-29 (v1.0) | P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf | Inputs: AHJ requirements + project metadata<br>Used in: P4.2 |
| P4-W03 | Permit application package (compiled) | Ethan Brooks (Document Control)<br>PDF compilation<br>Date: 2026-01-29 (v1.0) | P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf | Inputs: P4.1 + P4-W02 + supporting attachments<br>Used in: P4.2, P5.1 |
| P4-W04 | Supporting attachments bundle (electrical) | Ethan Brooks (Document Control)<br>PDF compilation<br>Date: 2026-01-29 (v1.0) | P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf | Inputs: P2.1 + P2.2 + EVSE/EMS + code basis<br>Used in: P4.2 |
| P4-W05 | AHJ submission receipt / confirmation | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-01-29 (v1.0) | P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf | Inputs: portal submission<br>Used in: P4.2, P5.1 |
| P4-W06 | Permit tracking log (submission metadata) | Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-01-29 (v1.0) | P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx | Inputs: portal submission data<br>Used in: Phase 5 |

## **Key Excerpts (Electrical-Only)**

### **Submission Confirmation Excerpt (P4-W05)**

**Excerpted receipt fields (mock):**
- AHJ: City of Palo Alto – Building Division (Electrical Permits)
- Submission method: Online portal upload
- Permit application number: **EL-2026-01472** (mock)
- Submission date/time: **2026-01-29 14:18 PT**
- Submitted by: **Jordan Lee (PM)** (mock)

### **Stamped Set Excerpt (P4-W01)**

**Excerpted stamp fields (mock):**
- Engineer-of-Record: **Priya Shah, PE**
- Stamp date: **2026-01-29**
- Set: **P4.1_PermitSet_Stamped_2026-01-29.pdf** derived from **P3.6** with no content changes other than stamp block and any required administrative cover sheet

## **P4.1 Stamped Permit Drawings**

This deliverable is the Phase 3 compiled set (P3.6) reviewed and stamped by the Engineer-of-Record for submission to the AHJ.

| Input | Source |
| :---- | :---- |
| Unstamped permit set | P3-W06 |
| EOR review notes (mock) | P4-EOR (see Addendum A) |

**Output (reference ID):** P4-W01

## **P4.2 Permit Application Package**

This deliverable is the complete electrical permit submission package as provided to the AHJ, including forms, stamped drawings, and electrical support documents commonly required for plan check.

### **Package contents (electrical-only)**
- **Stamped drawings**: P4-W01
- **AHJ application forms**: P4-W02
- **Supporting attachments (electrical)**: P4-W04
  - Load calculation summary (Phase 2): P2-W01
  - Architecture decision record (Phase 2): P2-W03
  - EVSE cut sheet (design basis): P1-I04
  - EMS technical brief: P2-W04
  - AHJ/code basis evidence: P1-I05

**Output (reference ID):** P4-W03

## **P4 Submission / QA Log (Mock)**

| QA Item | Check performed | Result | Checked by | Date |
| :---- | :---- | :---- | :---- | :---- |
| Stamped set included | P4.1 stamped drawings included in package | Pass | Ethan Brooks (Document Control) | 2026-01-29 |
| Stable filenames | Package references match evidence pointers | Pass | Ethan Brooks (Document Control) | 2026-01-29 |
| Attachment completeness | Load calc, EVSE, EMS, and code basis included | Pass | Jordan Lee (PM) | 2026-01-29 |
| Portal upload verification | Receipt downloaded; application number captured | Pass | Jordan Lee (PM) | 2026-01-29 |

## **Phase 4 Certification (Mock)**

| Certification Point | Status | Certified By | Date |
| :---- | :---- | :---- | :---- |
| Stamped drawings issued (P4.1) | Certified | Priya Shah, PE (mock) | 2026-01-29 |
| Permit application package submitted (P4.2) | Certified | Jordan Lee (PM) | 2026-01-29 |
| Submission receipt archived and traceable | Certified | Ethan Brooks (Document Control) | 2026-01-29 |

<a id="phase-5"></a>
# **Phase 5: Authority Review and Drawing Revision**

## **Phase 5 Purpose**

Phase 5 documents the AHJ plan check review, parses all AHJ comments into an auditable log, produces revised drawings addressing those comments, and records responses in a formal comment response letter.

**NOTE:** The Phase 5 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and revision logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 5 Boundaries (Electrical-Only)**

Phase 5 captures electrical plan-check comments and electrical drawing revisions. It intentionally excludes:
- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

## **P5.0 Evidence Index + Review/Revision Work Products (Stable Filenames)**

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P5-W01 | AHJ plan check comments (raw) | AHJ<br>Portal download<br>Date: 2026-02-06 (v1.0) | P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf | Inputs: AHJ portal<br>Used in: P5.1 |
| P5-W02 | AHJ comment log (parsed + tracked) | Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-02-06 (v1.0) | P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx | Inputs: P5-W01<br>Used in: P5.1, P5.2, P5.3 |
| P5-W03 | Revised drawings (post-comments, stamped) | Priya Shah, PE (mock EOR)<br>CAD update + stamp + PDF<br>Date: 2026-02-12 (Rev 1) | P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf | Inputs: P4.1 stamped set + P5-W02<br>Used in: P5.2, P5.3 |
| P5-W04 | Redline set (internal review) | Priya Shah, PE (mock EOR)<br>PDF markups<br>Date: 2026-02-10 (v1.0) | P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf | Inputs: P4.1 stamped set + P5-W02<br>Used in: P5.2 |
| P5-W05 | Comment response letter | Priya Shah, PE (mock EOR)<br>Letter PDF<br>Date: 2026-02-12 (Rev 1) | P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf | Inputs: P5-W02 + P5-W03<br>Used in: P5.3 |
| P5-W06 | Resubmission receipt / confirmation | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-02-12 (v1.0) | P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf | Inputs: AHJ portal<br>Used in: Phase 5 closeout |
| P5-W07 | AHJ approval / permit issuance confirmation | AHJ<br>Portal download<br>Date: 2026-02-19 (v1.0) | P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf | Inputs: AHJ portal<br>Used in: P5.4, Phase 5 closeout |

## **Key Excerpts (Electrical-Only)**

### **AHJ Comment Themes Excerpt (P5-W01)**

**Excerpted themes (mock):**
- Request clarification of **EMS/load management method** and fail-safe behavior.
- Request confirmation of **available fault current / AIC** selection basis.
- Request additional **code notes** (EVSE continuous load, labeling, disconnecting means references as applicable).

### **Revision Summary Excerpt (P5-W03)**

**Excerpted revision summary (mock):**
- Updated one-line notes to clarify EMS cap logic and fail-safe state.
- Added fault current basis note and verified minimum AIC rating statement.
- Updated notes sheet with explicit NEC/CEC references and labeling notes.

### **AHJ Approval Excerpt (P5-W07)**

**Excerpted approval fields (mock):**
- Status: **Approved**
- Permit application number: **EL-2026-01472** (mock)
- Approval date/time: **2026-02-19 10:07 PT**

## **P5.1 AHJ Comment Log – Parsed**

This deliverable converts the AHJ’s raw plan-check comments into a structured, trackable log with owners, dispositions, and references to revised sheets.

| Input | Source |
| :---- | :---- |
| AHJ comments (raw) | P5-W01 |
| Prior submitted set | P4-W01 |

**Output (reference ID):** P5-W02

**Parsed comment log (mock excerpt):**

| AHJ Comment ID | Location + comment | Required action + owner | Resolution |
| :---- | :---- | :---- | :---- |
| C-01 | E-001 (One-Line): Clarify EMS method/fail-safe; cite code basis | Add EMS control note + fail-safe statement + code ref<br>Owner: Priya Shah, PE | Disposition: Accepted<br>Revised in: Rev 1<br>Response: P5.3 §2.1 |
| C-02 | E-001 (One-Line): Provide fault current basis; confirm OCPD AIC | Add short-circuit basis note + minimum AIC statement<br>Owner: Priya Shah, PE | Disposition: Accepted<br>Revised in: Rev 1<br>Response: P5.3 §2.2 |
| C-03 | E-003 (Notes): Add EVSE continuous-load factor + labeling requirement | Expand notes with NEC/CEC refs + labeling language<br>Owner: Priya Shah, PE | Disposition: Accepted<br>Revised in: Rev 1<br>Response: P5.3 §2.3 |
| C-04 | General: Confirm EV subpanel designation and schedule consistency | Standardize nomenclature “EVSP-1” across set<br>Owner: Sam Ortega (CAD) | Disposition: Accepted<br>Revised in: Rev 1<br>Response: P5.3 §2.4 |

## **P5.2 Revised Drawings – Post-Comments**

This deliverable is the revised electrical permit set addressing AHJ comments. Revisions are tracked by revision number and traceable back to comment IDs.

| Input | Source |
| :---- | :---- |
| Comment log (parsed) | P5-W02 |
| Prior stamped set | P4-W01 |
| Internal redlines (optional) | P5-W04 |

**Output (reference ID):** P5-W03

### **Revision log (mock)**

| Revision | Date | Summary | Addressed comments |
| :---- | :---- | :---- | :---- |
| Rev 1 | 2026-02-12 | EMS notes clarified; fault-current/AIC basis added; notes expanded; nomenclature normalized | C-01, C-02, C-03, C-04 |

### **How changes were crafted (traceable mapping)**

| Change ID | From (prior set) | To (revised set) | Change description | Driven by AHJ comment |
| :---- | :---- | :---- | :---- | :---- |
| CH-01 | E-001 | E-001 | Added EMS cap statement + fail-safe note + code reference | C-01 |
| CH-02 | E-001 | E-001 | Added available fault current basis note; confirmed minimum AIC | C-02 |
| CH-03 | E-003 | E-003 | Added explicit EVSE continuous load and labeling notes | C-03 |
| CH-04 | E-002/E-004 | E-002/E-004 | Standardized equipment ID “EVSP-1” across plan and schedules | C-04 |

## **P5.3 Comment Response Letter**

This deliverable provides point-by-point responses to each AHJ comment and cross-references the revised sheets where changes were made.

| Input | Source |
| :---- | :---- |
| Comment log (parsed) | P5-W02 |
| Revised stamped set | P5-W03 |

**Output (reference ID):** P5-W05

**Response letter (mock excerpt):**
- **C-01 (EMS clarification):** Added EMS control narrative and fail-safe behavior note on Sheet E-001; see Rev 1 clouded note “EMS-1.”
- **C-02 (fault current / AIC):** Added fault-current basis statement and confirmed minimum breaker AIC on Sheet E-001.
- **C-03 (notes/labeling):** Updated Sheet E-003 to explicitly state EVSE continuous load treatment (125%) and labeling notes.
- **C-04 (nomenclature):** Standardized EV subpanel designation to “EVSP-1” across all sheets and schedules.

## **Phase 5 Resubmission Log (Mock)**

| Field | Value |
| :---- | :---- |
| Resubmission date/time | 2026-02-12 16:42 PT |
| Submitted by | Jordan Lee (PM) |
| Permit application number | EL-2026-01472 (mock) |
| Receipt evidence | P5-W06 |

## **P5.4 AHJ Acceptance / Approval Confirmation (100% Closeout)**

This deliverable records that the AHJ has accepted all comments and has approved the revised electrical permit set (or issued the permit). Phase 5 is not considered complete until this evidence is archived.

| Input | Source |
| :---- | :---- |
| Resubmission receipt | P5-W06 |
| Revised stamped set | P5-W03 |
| AHJ approval notice / permit issuance | P5-W07 |

**Closeout criteria (mock):**
- All AHJ comments in `P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx` have disposition **Accepted/Resolved**
- AHJ status is **Approved** (or **Permit Issued**) as evidenced by `P5.4_AHJ_Approval_Notice_2026-02-19.pdf`

## **Phase 5 Certification (Mock)**

| Certification Point | Status | Certified By | Date |
| :---- | :---- | :---- | :---- |
| AHJ comments parsed and tracked (P5.1) | Certified | Jordan Lee (PM) | 2026-02-06 |
| Revised set addresses all comments (P5.2) | Certified | Priya Shah, PE (mock) | 2026-02-12 |
| Comment response letter issued (P5.3) | Certified | Priya Shah, PE (mock) | 2026-02-12 |
| Resubmission receipt archived | Certified | Ethan Brooks (Document Control) | 2026-02-12 |
| AHJ approval / permit issuance archived (P5.4) | Certified | Ethan Brooks (Document Control) | 2026-02-19 |

<a id="phase-6"></a>
# **Phase 6: Utility Coordination**

## **Phase 6 Purpose**

Phase 6 documents coordination with the local electrical utility to communicate the planned EV load addition and any load-management method, submit required utility application forms, and archive all utility correspondence/receipts.

**NOTE:** The Phase 6 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and coordination logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 6 Boundaries (Electrical-Only)**

Phase 6 captures technical utility coordination artifacts (load letters, single-line/one-line as requested by the utility, and utility portal forms). It intentionally excludes:
- **Civil / constructability** topics (routing/trenching/means-and-methods, installation sequencing, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

## **P6.0 Evidence Index + Utility Coordination Work Products (Stable Filenames)**

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P6-W01 | Utility requirements capture | Jordan Lee (PM)<br>Utility portal capture + PDF<br>Date: 2026-02-20 (v1.0) | P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf | Inputs: utility portal<br>Used in: P6.2 |
| P6-W02 | Utility load letter + single-line | Priya Shah, PE (mock EOR)<br>Letter + PDF<br>Date: 2026-02-21 (v1.0) | P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf | Inputs: P2.1 + P2.2 + service info (+ stamped set if required)<br>Used in: P6.1, P6.2 |
| P6-W03 | Utility application forms (completed) | Jordan Lee (PM)<br>Portal form + PDF export<br>Date: 2026-02-21 (v1.0) | P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf | Inputs: P6-W01 + project technical metadata<br>Used in: P6.2 |
| P6-W04 | Utility submission receipt | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-02-21 (v1.0) | P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf | Inputs: portal submission<br>Used in: Phase 6 closeout |
| P6-W05 | Utility correspondence log | Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-02-24 (v1.0) | P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx | Inputs: utility comms<br>Used in: Phase 6 closeout |
| P6-W06 | Utility deficiency / additional info required | Utility<br>Portal message + PDF<br>Date: 2026-02-25 (v1.0) | P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf | Inputs: utility review of initial submission<br>Used in: P6.3 |
| P6-W07 | Utility rework package | Priya Shah, PE (mock) + Jordan Lee (PM)<br>PDF compilation<br>Date: 2026-02-27 (v1.0) | P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf | Inputs: P6-W06 + Phase 1/2/4 evidence + EMS brief<br>Used in: P6.3 |
| P6-W08 | Utility resubmission receipt | Jordan Lee (PM)<br>Portal download + screenshot PDF<br>Date: 2026-02-27 (v1.0) | P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf | Inputs: portal resubmission<br>Used in: Phase 6 closeout |
| P6-W09 | Utility approval / acknowledgment (final) | Utility<br>Email/portal letter<br>Date: 2026-03-03 (v1.0) | P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf | Inputs: utility review<br>Used in: Phase 6 closeout |

## **Key Excerpts (Electrical-Only)**

### **Utility Load Letter Excerpt (P6-W02)**

**Excerpted technical content (mock):**
- Service: **800A, 208Y/120V, 3Φ** (verified in Phase 1)
- EVSE: **8 ports**, **32A continuous** each (design basis)
- Unmanaged continuous EV load: **320A**
- Load management: **EMS caps aggregate EV demand to ≤250A**
- Reference documents included: Phase 2 load calc summary + architecture decision record

### **Utility Submission Receipt Excerpt (P6-W04)**

**Excerpted receipt fields (mock):**
- Submission method: Utility online portal
- Application/reference number: **UTIL-EV-2026-00831** (mock)
- Submitted by: **Jordan Lee (PM)** (mock)
- Submission date/time: **2026-02-21 11:05 PT**

### **Utility Deficiency Notice Excerpt (P6-W06)**

**Excerpted status (mock):**
- Status: **Incomplete / Additional Information Required**
- Reason: EMS documentation insufficient for utility review; request clarification of monitoring point and fail-safe cap behavior
- Response due: N/A (utility queue-based)

## **P6.1 Utility Load Letter / Single-Line**

This deliverable packages the technical load information for the utility, including a single-line/one-line diagram excerpt as required by the utility and a narrative describing any load-management method (EMS) used to limit service impact.

| Input | Source |
| :---- | :---- |
| Load calculation summary | P2-W01 |
| Architecture decision record | P2-W03 |
| Service characteristics evidence | P1-I02 + P1-I03 |
| EVSE cut sheet (design basis) | P1-I04 |
| EMS technical brief | P2-W04 |

**Output (reference ID):** P6-W02

## **P6.2 Utility Application Forms**

This deliverable captures the completed utility application forms and any required attachments. The submission receipt and correspondence log are archived to preserve full traceability.

| Input | Source |
| :---- | :---- |
| Utility requirements | P6-W01 |
| Utility load letter/single-line | P6-W02 |
| Stamped permit drawings (if requested by utility) | P4-W01 |

**Output (reference ID):** P6-W03

## **P6.3 Utility Deficiency Response / Rework + Resubmission**

This deliverable documents the utility’s “incomplete/additional info required” outcome and the technical rework performed to satisfy the utility’s request, followed by resubmission and approval.

### **Deficiency received**

| Input | Source |
| :---- | :---- |
| Utility deficiency notice | P6-W06 |

### **Rework package (electrical-only)**

| Rework component | Evidence pointer |
| :---- | :---- |
| EMS clarification memo (monitoring point + cap + fail-safe) | P6-W07 (Section 1) |
| EMS technical brief (revB) | P2-W04 |
| Load calc summary (Phase 2) | P2-W01 |
| Architecture decision record (Phase 2) | P2-W03 |
| Stamped permit set (reference, if requested) | P4-W01 |

### **Resubmission + approval**

| Field | Value |
| :---- | :---- |
| Utility application/reference number | UTIL-EV-2026-00831 (mock) |
| Resubmission date/time | 2026-02-27 09:22 PT |
| Resubmission receipt | P6-W08 |
| Utility approval/acknowledgment | P6-W09 |

## **Phase 6 Coordination Log (Mock)**

| Date | Activity | Evidence (reference ID) |
| :---- | :---- | :---- |
| 2026-02-20 | Confirm required attachments for EV load add (email w/ utility rep) | P6-W01 |
| 2026-02-21 | Submit application + load letter (utility portal) | P6-W04 |
| 2026-02-24 | EMS clarification requested (call, pre-review) | P6-W05 |
| 2026-02-25 | Deficiency issued: “Additional Info Required” (utility portal) | P6-W06 |
| 2026-02-27 | Resubmit rework package (utility portal) | P6-W08 |
| 2026-03-03 | Approval/acknowledgment issued (utility portal letter) | P6-W09 |

## **Phase 6 Closeout Criteria**

Phase 6 is considered complete when:
- Utility application submission receipt is archived (**P6-W04**)
- Correspondence log is complete (**P6-W05**)
- Utility deficiency notice (if issued) is archived and dispositioned (**P6-W06**)
- Utility approval/acknowledgment is archived (**P6-W09**) or documented as “not applicable/none issued” in the correspondence log

## **Phase 6 Certification (Mock)**

| Certification Point | Status | Certified By | Date |
| :---- | :---- | :---- | :---- |
| Utility load letter/single-line issued (P6.1) | Certified | Priya Shah, PE (mock) | 2026-02-21 |
| Utility application submitted (P6.2) | Certified | Jordan Lee (PM) | 2026-02-21 |
| Submission receipt archived | Certified | Ethan Brooks (Document Control) | 2026-02-21 |
| Utility deficiency addressed and resubmitted (P6.3) | Certified | Jordan Lee (PM) | 2026-02-27 |
| Utility approval/acknowledgment archived (final) | Certified | Ethan Brooks (Document Control) | 2026-03-03 |

<a id="phase-7"></a>
# **Phase 7: Electrical Closeout and Handover**

## **Phase 7 Purpose**

Phase 7 captures the final electrical closeout artifacts: **as-built electrical drawings**, responses supporting final inspection, and evidence that the AHJ finaled the electrical permit/inspection (where applicable).

**NOTE:** The Phase 7 fields below are filled with **MOCK / EXAMPLE DATA** to demonstrate a “completed” master deliverable package (provenance, stable filenames, and closeout logs). Replace all mock names, dates, and evidence pointers with real project records before using this document externally.

## **Phase 7 Boundaries (Electrical-Only)**

Phase 7 captures electrical closeout documentation. It intentionally excludes:
- **Civil / constructability** topics (installation means-and-methods, trenching execution details, routing procedures, etc.)
- **Business aspects** including **cost, schedule, procurement, commercial terms**, and financial analysis

## **P7.0 Evidence Index + Closeout Work Products (Stable Filenames)**

| Item ID | Work product | Provenance (who / how / when) | Evidence reference ID(s) | Inputs + downstream use |
| :---- | :---- | :---- | :---- | :---- |
| P7-W01 | Field redlines (electrical) | Luis Romero (Electrician) + Mia Chen (Installer PM)<br>Markups + photo references<br>Date: 2026-03-18 (v1.0) | P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf | Inputs: field observations + installed labels<br>Used in: P7.1 |
| P7-W02 | As-built electrical drawing set | Sam Ortega (CAD Tech, mock) + Priya Shah, PE (mock)<br>CAD update + PDF export<br>Date: 2026-03-22 (As-Built v1) | P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf | Inputs: P5.2 revised stamped set + P7-W01 + inspection notes<br>Used in: P7.1 |
| P7-W03 | AHJ final inspection / permit finaled confirmation | AHJ<br>Portal download<br>Date: 2026-03-26 (v1.0) | P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf | Inputs: AHJ portal<br>Used in: P7.3 |
| P7-W04 | Inspector notes / correction notice (if any) | AHJ<br>Field note + portal upload<br>Date: 2026-03-24 (v1.0) | P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf | Inputs: field inspection<br>Used in: P7.2, P7.1 |
| P7-W05 | Inspection support Q&A log | Priya Shah, PE (mock) + Jordan Lee (PM)<br>Spreadsheet<br>Date: 2026-03-26 (v1.0) | P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx | Inputs: AHJ questions + responses<br>Used in: P7.2 |
| P7-W06 | EMS configuration summary (as-installed) | Mia Chen (Installer PM)<br>Vendor export + PDF<br>Date: 2026-03-21 (v1.0) | P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf | Inputs: EMS system<br>Used in: P7.1, P7.2 |

## **Key Excerpts (Electrical-Only)**

### **As-Built Summary Excerpt (P7-W02)**

**Excerpted as-built outcomes (mock):**
- EV subpanel designation standardized as **EVSP-1** (matches permit set)
- EMS aggregate cap configured to **250A** (as-installed), with documented fail-safe behavior
- One-line and schedules updated to reflect installed breaker/labeling differences found in field redlines (no change to the approved load-management intent)

### **Final Inspection Excerpt (P7-W03)**

**Excerpted AHJ status (mock):**
- Final inspection result: **Pass**
- Permit status: **Finaled/Closed**
- Permit application number: **EL-2026-01472** (mock)
- Final date/time: **2026-03-26 09:40 PT**

## **P7.1 As-Built Drawings**

This deliverable is the as-built electrical drawing set prepared from field redlines and any AHJ inspector notes. The as-built set is intended to be the authoritative record of the installed electrical scope.

| Input | Source |
| :---- | :---- |
| Prior approved/revised permit set | P5-W03 |
| Field redlines (electrical) | P7-W01 |
| AHJ inspector notes (if any) | P7-W04 |
| EMS as-installed config summary | P7-W06 |

**Output (reference ID):** P7-W02

### **As-built change log (mock)**

| Change ID | Sheet | Change description | Source evidence |
| :---- | :---- | :---- | :---- |
| AB-01 | One-line | Updated EMS note to match as-installed cap value and monitoring point label | P7-W06 + P7-W01 |
| AB-02 | Panel schedules | Updated EVSP-1 schedule to reflect installed breaker spaces/labeling | P7-W01 |
| AB-03 | Notes | Added “as-built” cover note and clarified labeling applied in field | P7-W01 + P7-W04 |

## **P7.2 Inspection Support Responses**

This deliverable documents responses provided to the AHJ/inspector during final inspection or closeout, including clarifications, supplemental documentation, and confirmation of corrected items.

| Input | Source |
| :---- | :---- |
| Inspector notes / questions | P7-W04 |
| As-built set (draft/final) | P7-W02 |
| EMS configuration summary | P7-W06 |

**Output (reference ID):** P7-W05

**Inspection support log (mock excerpt):**

| Item | Question/Issue | Response provided | Evidence pointer | Status |
| :---- | :---- | :---- | :---- | :---- |
| IS-01 | Provide EMS cap confirmation for plan-check intent | Provided EMS config export showing cap set to 250A and fail-safe mode | P7-W06 | Closed |
| IS-02 | Confirm panel labeling and circuit IDs match drawings | Provided updated as-built schedule page and photo references | P7-W02 | Closed |

## **P7.3 AHJ Final Acceptance / Permit Closeout Confirmation**

This deliverable archives proof that the AHJ finaled/closed the electrical permit/inspection, marking the end of the AHJ process for this scope.

| Input | Source |
| :---- | :---- |
| Final inspection / permit status evidence | P7-W03 |

## **Phase 7 Closeout Criteria**

Phase 7 is considered complete when:
- As-built electrical drawings are issued and archived (**P7-W02**)
- Inspection support log is complete (**P7-W05**)
- AHJ final acceptance/permit closeout evidence is archived (**P7-W03**)

## **Phase 7 Certification (Mock)**

| Certification Point | Status | Certified By | Date |
| :---- | :---- | :---- | :---- |
| As-built electrical set issued (P7.1) | Certified | Priya Shah, PE (mock) | 2026-03-22 |
| Inspection support documentation complete (P7.2) | Certified | Jordan Lee (PM) | 2026-03-26 |
| AHJ final acceptance archived (P7.3) | Certified | Ethan Brooks (Document Control) | 2026-03-26 |

<a id="addendum-a"></a>
## Addendum A: Stable Filename Index (by Phase)

This addendum is a consolidated index of all **stable evidence pointers** referenced in this document, grouped by phase and section/deliverable.

### Phase 0 (P0) — Project Initiation and Feasibility

- **P0 inputs**
  - P0/Inputs/P0-I01_Utility_Bills_2025-01_to_2025-12.pdf
  - P0/Inputs/P0-I01_GreenButton_IntervalData_2025.csv
  - P0/Inputs/P0-I02_MDP_Nameplate_Photos.zip
  - P0/Inputs/P0-I02_Utility_Service_Info_Letter.pdf
  - P0/Inputs/P0-I03_ElectriCharge_L2-7.6-G_CutSheet_revA.pdf
  - P0/Inputs/P0-I04_PhotoSet_ExistingGear_and_GarageArea.zip
  - P0/Inputs/P0-I04_PhotoIndex_Annotated.pdf

### Phase 1 (P1) — Data Collection and Site Analysis

- **P1 inputs**
  - P1/Inputs/P1-I01_SitePlans_Arch_Set_rev2_2026-01-15.pdf
  - P1/Inputs/P1-I02_PanelSchedules_MDP_and_Subpanels_2026-01-16.pdf
  - P1/Inputs/P1-I03_PhotoSet_ServiceGear_Nameplates_2026-01-16.zip
  - P1/Inputs/P1-I03_PhotoIndex_Annotated_2026-01-16.pdf
  - P1/Inputs/P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf
  - P1/Inputs/P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf

- **P1 normalized outputs (P1.2)**
  - P1/Outputs/P1.2_SitePlans_ElectricalContext_Excerpts_2026-01-18.pdf
  - P1/Outputs/P1.2_PanelSchedules_Normalized_MDP_Subpanels_2026-01-18.pdf
  - P1/Outputs/P1.2_Photos_Annotated_Index_2026-01-18.pdf
  - P1/Outputs/P1.2_EVSE_CutSheet_FrozenForDesign_revA_2026-01-18.pdf
  - P1/Outputs/P1.2_AHJ_CodeBasis_Normalized_2026-01-18.pdf

### Phase 2 (P2) — System Design and Load Calculation

- **P2 engineering work products**
  - P2/Outputs/P2.1_LoadCalc_Workbook_2026-01-22.xlsx
  - P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf
  - P2/Outputs/P2.1_LoadCalc_CheckMemo_2026-01-22.pdf
  - P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf
  - P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf

### Phase 3 (P3) — Preliminary Drawing Set Production

- **P3 inputs**
  - P3/Inputs/P3-PARK_ParkingLayout_OwnerProvided_2026-01-20.pdf
  - P3/Inputs/P3-I03_RoutingAssumptions_InstallerMemo_2026-01-20.pdf

- **P3 drawing work products**
  - P3/Outputs/P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf
  - P3/Outputs/P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf
  - P3/Outputs/P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf
  - P3/Outputs/P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf
  - P3/Outputs/P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf
  - P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf

### Phase 4 (P4) — Permitting Submission (AHJ)

- **P4 inputs**
  - P4/Inputs/P4-EOR_ReviewNotes_2026-01-28.pdf

- **P4 submission outputs**
  - P4/Outputs/P4.1_PermitSet_Stamped_2026-01-29.pdf
  - P4/Outputs/P4.2_AHJ_ApplicationForms_2026-01-29.pdf
  - P4/Outputs/P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf
  - P4/Outputs/P4.SupportingAttachments_Electrical_2026-01-29.pdf
  - P4/Outputs/P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf
  - P4/Outputs/P4.PermitTrackingLog_2026-01-29.xlsx

### Phase 5 (P5) — Authority Review and Drawing Revision (AHJ)

- **P5 inputs**
  - P5/Inputs/P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf

- **P5 review/revision outputs**
  - P5/Outputs/P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx
  - P5/Outputs/P5.Redlines_InternalReview_2026-02-10.pdf
  - P5/Outputs/P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf
  - P5/Outputs/P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf
  - P5/Outputs/P5.ResubmissionReceipt_AHJ_2026-02-12.pdf
  - P5/Outputs/P5.4_AHJ_Approval_Notice_2026-02-19.pdf

### Phase 6 (P6) — Utility Coordination

- **P6 inputs**
  - P6/Inputs/P6.UtilityRequirements_Capture_2026-02-20.pdf
  - P6/Inputs/P6.Utility_DeficiencyNotice_2026-02-25.pdf

- **P6 coordination outputs**
  - P6/Outputs/P6.1_UtilityLoadLetter_SingleLine_2026-02-21.pdf
  - P6/Outputs/P6.2_UtilityApplicationForms_Completed_2026-02-21.pdf
  - P6/Outputs/P6.SubmissionReceipt_Utility_2026-02-21.pdf
  - P6/Outputs/P6.CorrespondenceLog_2026-02-24.xlsx
  - P6/Outputs/P6.3_Utility_ReworkPackage_2026-02-27.pdf
  - P6/Outputs/P6.ResubmissionReceipt_Utility_2026-02-27.pdf
  - P6/Outputs/P6.Utility_Approval_Acknowledgment_2026-03-03.pdf

### Phase 7 (P7) — Electrical Closeout and Handover

- **P7 inputs**
  - P7/Inputs/P7.FieldRedlines_Electrical_2026-03-18.pdf
  - P7/Inputs/P7.AHJ_InspectorNotes_2026-03-24.pdf

- **P7 closeout outputs**
  - P7/Outputs/P7.EMS_ConfigSummary_AsInstalled_2026-03-21.pdf
  - P7/Outputs/P7.1_AsBuilt_ElectricalPermitSet_2026-03-22.pdf
  - P7/Outputs/P7.2_InspectionSupport_Log_2026-03-26.xlsx
  - P7/Outputs/P7.AHJ_FinalInspection_PermitFinaled_2026-03-26.pdf

<a id="addendum-b"></a>
## Addendum B: Party Directory (Roles + Contacts)

This addendum lists all parties referenced in this document. **Contact details are MOCK/EXAMPLE placeholders** and must be replaced with real information.

| Party | Works for | Role | Email | Phone |
| :---- | :---- | :---- | :---- | :---- |
| Owner (Entity) | Place Property Ownership (mock) | Project owner / applicant | `ev-projects@owner.example` | `+1 (650) 555-0120` |
| Owner/Architect (Entity) | ABC Architects (mock) | Plan source / record drawings provider | `projects@architect.example` | `+1 (650) 555-0121` |
| Installer (Entity) | EV Install Services (mock) | Installation contractor / field coordination | `pm@installer.example` | `+1 (650) 555-0122` |
| Electrical Contractor (Entity) | Romero Electric (mock) | Electrical contractor | `service@electric.example` | `+1 (650) 555-0123` |
| Nora Patel | Owner (mock) | Owner Representative | `nora.patel@owner.example` | `+1 (650) 555-0101` |
| Mia Chen | Installer (mock) | Installer Project Manager | `mia.chen@installer.example` | `+1 (650) 555-0102` |
| Luis Romero | Electrical Contractor (mock) | Electrician / Field Lead | `luis.romero@electric.example` | `+1 (650) 555-0103` |
| Priya Shah, PE | Engineer-of-Record (mock) | Electrical Engineer / EOR | `priya.shah@eor.example` | `+1 (650) 555-0104` |
| Alex Kim, EE | Independent Reviewer (mock) | Electrical Engineer (independent check) | `alex.kim@review.example` | `+1 (650) 555-0105` |
| Sam Ortega | Design/CAD (mock) | CAD Technician | `sam.ortega@cad.example` | `+1 (650) 555-0106` |
| Ethan Brooks | Document Control (mock) | Document Control | `ethan.brooks@docs.example` | `+1 (650) 555-0107` |
| Jordan Lee | Project Management (mock) | Project Manager | `jordan.lee@pm.example` | `+1 (650) 555-0108` |
| Taylor Nguyen | Utility (mock) | Utility Account Representative (technical) | `taylor.nguyen@utility.example` | `+1 (650) 555-0109` |
| EVSE Manufacturer (Entity) | ElectriCharge (mock) | EVSE cut sheet issuer | `support@electricharge.example` | `+1 (800) 555-0124` |
| EMS Vendor (Entity) | Schlage / ChargePoint (mock) | Load management / EMS technical source | `ems-support@emsvendor.example` | `+1 (800) 555-0125` |
| City of Palo Alto – Building Division (Electrical Permits) | AHJ | Electrical permitting authority / plan check | `electricalpermits@paloalto.example` | `+1 (650) 555-0110` |
| Local Electrical Utility (Portal) | Utility | Utility interconnection/load review | `evprogram@utility.example` | `+1 (800) 555-0111` |

