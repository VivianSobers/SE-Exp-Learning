# Requirements Table — Problem #58: Digital Art Commission & Watermarking Portal

**Actors:** Client Buyer, Digital Artist, Payment Gateway (supporting)

## Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria (measurable pass/fail) | Rationale |
|--------|------|-------------|----------|--------------------------------------------|-----------|
| **FR-001** | Functional | The system shall apply a dynamic diagonal overlay watermark to every draft illustration uploaded by an artist before it is displayed to the client. | High | **Pass:** Every draft rendered in the client portal shows the diagonal watermark. **Fail:** Any unwatermarked high-res draft image is exposed to the client before final payment. | Core IP protection — prevents clients from using drafts without paying. *(Given)* |
| **FR-002** | Functional | The system shall allow a Client Buyer to create and submit a visual creative brief specifying title, description, reference images, budget and deadline. | High | **Pass:** A submitted brief with all mandatory fields is stored and made visible to the assigned artist within 5 s. **Fail:** A brief is accepted with a mandatory field left blank. | Entry point of the commission workflow — nothing can proceed without a brief. |
| **FR-003** | Functional | The system shall allow a Digital Artist to upload a WIP draft file against a commission the artist has accepted. | High | **Pass:** An upload against an accepted commission is stored and listed as the commission's latest draft. **Fail:** An upload is accepted against a commission the uploading artist has not accepted. | Enables the iterative feedback loop; the watermarking obligation on that draft is governed by FR-001. |
| **FR-004** | Functional | The system shall allow a Client Buyer to record an explicit **Approve** or **Request Revision** decision on a watermarked draft. | High | **Pass:** The draft's status changes to *Approved* or *Revision Requested* and the artist is notified within 5 s of the decision. **Fail:** A draft remains in *Pending Review* after a decision is submitted, or a milestone becomes payable without an *Approved* draft. | Approval is the gate between drafting and payment — it is the precondition of UC-04 and the trigger for the revision cycle. |
| **FR-005** | Functional | The system shall allow a Client Buyer to pay a milestone through the Payment Gateway and shall make the final high-resolution, watermark-free source file downloadable **if and only if** that milestone payment has been authorized by the gateway. | High | **Pass:** The final high-res file is downloadable exactly when a gateway authorization reference exists for its milestone. **Fail:** The file is downloadable with no authorization reference on record, **or** stays locked after one has been recorded. | The headline rule of the platform: the artist is paid before the client receives a usable deliverable. |

## Non-Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria (measurable pass/fail) | Rationale |
|--------|------|-------------|----------|--------------------------------------------|-----------|
| **NFR-001** | Non-Functional — Performance & Security | The system shall serve final high-resolution asset downloads exclusively through expiring signed S3 URLs valid for 60 minutes only. | High | **Pass:** Under simulated peak load, a generated download URL serves the asset throughout its 60-minute window and returns HTTP 403 for every request after it. **Fail:** Any download URL is still usable more than 60 minutes after issue. | Prevents link sharing/leakage of paid deliverables while keeping downloads fast. *(Given)* |
| **NFR-002** | Non-Functional — Performance | The system shall render and make an uploaded draft available in watermarked form in the client portal within 5 seconds of upload for at least 95% of uploads under peak load. | Medium | **Pass:** Load test shows 95th-percentile watermark-render-to-display time ≤ 5 s under peak concurrency. **Fail:** More than 5% of uploads exceed 5 s to appear watermarked. | Keeps the review loop responsive so the watermarking step never feels like a bottleneck. |

---

### Traceability (requirement → use case)

| Requirement | Use case(s) in the UML diagram |
|-------------|--------------------------------|
| FR-001 | *Apply Diagonal Watermark* («include» of UC-02) |
| FR-002 | UC-01 Submit Creative Brief |
| FR-003 | UC-02 Upload WIP Draft |
| FR-004 | UC-03 Review / Approve Draft, *Request Revision* («extend») |
| FR-005 | UC-04 Make Milestone Payment (+ *Process Payment*), UC-05 Download Final Asset |
| NFR-001 | *Generate Signed Download URL* («include» of UC-05) |
| NFR-002 | *Apply Diagonal Watermark* (timing constraint on UC-02) |

### Notes
- Exactly **5 Functional Requirements** (FR-001 → FR-005) and **2 Non-Functional Requirements** (NFR-001, NFR-002) as required.
- FR-001 and NFR-001 are the instructor-provided samples; FR-002–FR-005 and NFR-002 are original.
- Every requirement is phrased as a testable *"The system shall…"* statement with a single measurable pass/fail criterion, and every use case in the diagram traces back to a requirement.
