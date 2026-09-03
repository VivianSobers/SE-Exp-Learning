# Lab 2 — Agile Backlog Creation & Sprint Simulation in Jira

**Problem #58 — Digital Art Commission & Watermarking Portal**
Jira project **DACWP** · board 35 · company-managed Scrum

## Backlog summary

Lab 1's five functional requirements were decomposed into **4 Epics** and **14 User Stories**
totalling **60 story points** (Fibonacci: 2, 3, 5, 8).

| Epic | Stories | Points | Traces to |
|------|---------|--------|-----------|
| Epic 1: Commission Intake & Brief Management | DACWP-5, 6, 7 | 11 | FR-002 |
| Epic 2: WIP Draft Delivery & IP Protection | DACWP-8, 9, 10 | 16 | FR-003, FR-001 |
| Epic 3: Draft Review & Revision Cycle | DACWP-11, 12, 13 | 10 | FR-004 |
| Epic 4: Milestone Payment & Final Asset Release | DACWP-14 … 18 | 23 | FR-005, NFR-001 |

## Sprint results

| | Sprint 1 | Sprint 2 |
|---|---|---|
| Stories | 5 | 6 |
| Committed points | 24 | 26 |
| Completed points | 24 | 26 |
| Completion | 100% | 100% |

**Velocity:** 24 then 26 points — an average of **25 points per sprint**.
**Not delivered:** DACWP-16 (5, High), DACWP-18 (3, Medium), DACWP-17 (2, Low) — **10 points** left in the backlog.

## Reflection Questions

### 1. Did your estimations reflect the actual effort?

Only partly, and the honest answer is that this simulation could not fully test them. No code
was written, so "actual effort" was never measured against the estimates — what the exercise
does validate is whether the *relative* sizing was coherent.

On that measure the estimates hold up. The two 8-point stories — DACWP-9 (automatic diagonal
watermarking) and DACWP-14 (milestone payment via gateway) — are the only two that depend on
something outside the application: an image-processing pipeline and a third-party payment
gateway. Sizing them above everything else was right. The 2- and 3-point stories are all
single-screen CRUD or notification work, which is genuinely small.

Where I would revise: DACWP-14 at 8 points is probably still under-estimated. Payment gateway
integration carries error handling, idempotency and reconciliation work that isn't visible from
the user story. Under planning poker, an argument for 13 would have been reasonable.

### 2. Was your backlog well-prioritized?

Mostly, with one clear miss. The ordering put the commission-to-payment critical path first,
so the two sprints delivered a coherent end-to-end slice: a client can submit a brief, an artist
can upload a watermarked draft, the client can review and approve it, pay the milestone, and have
the final asset unlocked. That is a demonstrable product increment, which is the real test of
prioritization.

The miss is **DACWP-16 (Expiring Signed Download Link, 5 points, High priority)**. It carries
NFR-001 — the 60-minute signed URL that stops paid deliverables leaking — and it was ranked High
yet did not make either sprint. Delivering "unlock the final asset" (DACWP-15) *without* the
expiring link means the sprint output has a security gap. Either DACWP-16 should have displaced
a Medium story in Sprint 2, or it should have been merged into DACWP-15 as one story, since
neither is really shippable alone.

The two items left behind deliberately — the promo code (Low) and declined-payment retry
(Medium) — are the right things to defer.

### 3. How did your simulated sprint align with your plan?

Exactly, which is itself the finding worth reporting. Both sprints committed to a fixed set of
stories and completed 100% of them, because a simulation has none of the things that actually
derail sprints: no blockers, no review feedback, no scope added mid-sprint, no story turning out
harder than it looked, no dependency on another team.

A real sprint that closes at 100% twice running is usually a signal of under-commitment rather
than good execution. So the alignment here reflects the absence of uncertainty, not the accuracy
of planning. The plan I would trust is the one that survives a sprint where something goes wrong.

### 4. What insights did the burndown chart give about your team's capacity?

Two useful ones and one caveat.

**Capacity looks like roughly 25 points per sprint**, consistent across both. If that held, the
10 remaining points would need only about half a sprint, so a third sprint would be significantly
under-filled — the sensible response is to pull more scope in rather than run a near-empty sprint.

**The step pattern shows work completing one story at a time** rather than everything landing at
the end, which is the healthier shape: it means value was being delivered continuously instead of
piling up against the deadline.

The caveat: both sprints were configured with the handout's 1-week duration but executed in about
40 minutes of wall-clock time. The burndown therefore drops far more steeply than the guideline
line, and the gap between the two lines is an artifact of the compressed simulation, not evidence
that the team ran ahead of schedule. In a real sprint that same gap would be the most useful
signal on the chart.
