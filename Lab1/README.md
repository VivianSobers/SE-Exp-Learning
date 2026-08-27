# SE Experiential Learning — Lab 1

**Course:** Software Engineering (Semester 5) · Dept. of CSE, PES University
**Lab 1:** Requirements Engineering & UML Use-Case Modelling
**Problem Statement #58 — Media, Events & Community:** *Digital Art Commission & Watermarking Portal*

## Problem Context

An art commission platform where **clients** submit visual creative briefs, **artists**
upload watermarked work-in-progress (WIP) drafts, and final high-resolution source files
unlock only upon confirmed milestone payment.

## Deliverables

| # | Deliverable | File |
|---|-------------|------|
| 1 | Requirements Table (5 FRs + 2 NFRs, with traceability to use cases) | [`requirements-table.md`](requirements-table.md) |
| 2 | UML Use-Case Diagram (draw.io source + exported renderings) | [`use-case-diagram.drawio`](use-case-diagram.drawio) · [`use-case-diagram.pdf`](use-case-diagram.pdf) · [`use-case-diagram.png`](use-case-diagram.png) · [`use-case-diagram.svg`](use-case-diagram.svg) |
| 3 | Use-Case Flow Specification (one page) | [`use-case-flow.pdf`](use-case-flow.pdf) · [`use-case-flow.md`](use-case-flow.md) |

## Actors

- **Client Buyer** — commissions artwork, reviews and approves drafts, pays milestones, downloads finals.
- **Digital Artist** — accepts commissions, uploads WIP drafts, delivers final source files.
- **Payment Gateway** *(supporting/secondary actor)* — authorizes milestone payments.

## Use cases

| ID | Use case | Actor | Relationships |
|----|----------|-------|---------------|
| UC-01 | Submit Creative Brief | Client Buyer | — |
| UC-02 | Upload WIP Draft | Digital Artist | «include» *Apply Diagonal Watermark* |
| UC-03 | Review / Approve Draft | Client Buyer | «extend» *Request Revision* |
| UC-04 | Make Milestone Payment | Client Buyer, Payment Gateway | «include» *Process Payment* · «extend» *Apply Promo Code* |
| UC-05 | Download Final Asset | Client Buyer | «include» *Generate Signed Download URL* |

The one-page flow specification documents **UC-04 Make Milestone Payment**.

## Reference material

The instructor-provided [problem statement](58_SE_Lab1_SE_Problem_Statements.pdf) is kept
alongside the deliverables. The lab handout is not tracked in this repo.

## How to edit / regenerate the diagram

The diagram is authored in **draw.io** (`use-case-diagram.drawio`) — open it at
[app.diagrams.net](https://app.diagrams.net) or in the draw.io desktop app to edit, then
**File → Export as → PDF / PNG / SVG**. The committed `.pdf`, `.png` and `.svg` are
renderings of that source and should be re-exported whenever the source changes.
