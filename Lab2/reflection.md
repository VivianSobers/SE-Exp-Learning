# Lab 2 — Agile Backlog Creation and Sprint Simulation in Jira

| Name | Vivian Sobers E |
| SRN | PES1UG24CS901 |
| Section |5 C |
| Course | Software Engineering, Semester 5 — Dept. of CSE, PES University |
| Problem Statement | #58 — Digital Art Commission & Watermarking Portal |
| Jira Project | DACWP (company-managed Scrum, board 68) |
| Simulation Period | 3 September 2026, 22:30 — 8 September 2026, 20:00 |

## 1. Epics and User Stories

I took the five functional requirements from Lab 1 and broke them into 4 Epics and 14 User Stories,
which came to 60 story points. I raised three more stories while the sprints were running,
taking the totals to 17 stories and 70 points. Every story is written in the
*As a [role], I want [goal], So that [benefit]* form, carries a priority of High, Medium or Low,
and is estimated on the Fibonacci scale. The backlog is ranked High, then Medium, then Low.

| Epic | User Stories (points) | Total | From Lab 1 |
| Epic 1: Commission Intake & Brief Management | DACWP-5 Create Creative Brief (5) DACWP-6 Submit Brief (3) DACWP-7 Accept Commission (3) | 11 | FR-002 (UC-01) |
| Epic 2: WIP Draft Delivery & IP Protection | DACWP-8 Upload WIP Draft (5) DACWP-9 Automatic Diagonal Watermarking (8) DACWP-10 View Watermarked Draft (3) DACWP-19 Re-watermark on Draft Replace (3) —  added mid-sprint | 19 | FR-003, FR-001 (UC-02) |
| Epic 3: Draft Review & Revision Cycle | DACWP-11 Approve Draft (3) DACWP-12 Request Revision (5) DACWP-13 Decision Notification (2) DACWP-21 Revision Comment Thread (5) —  added mid-sprint | 15 | FR-004 (UC-03) |
| Epic 4: Milestone Payment & Final Asset Release | DACWP-14 Pay Milestone via Gateway (8) DACWP-15 Unlock Final High-Res Asset (5) DACWP-16 Expiring Signed Download Link (5) DACWP-17 Apply Promo Code (2) DACWP-18 Handle Declined Payment (3) DACWP-20 Receipt Email (2) —  added mid-sprint | 25 | FR-005, NFR-001 (UC-04, UC-05) |

## 2. Sprint Results

Both sprints ran in parallel over the same window, 3 September 22:30 to 8 September 20:00.
Sprint 1 carried the intake, drafting and review work; Sprint 2 carried payment and asset release.

|  | Sprint 1 | Sprint 2 | Total |
| Stories committed | 9 | 8 | 17 |
| Points committed (incl. mid-sprint additions) | 38 | 32 | 70 |
| Points completed | 33 | 27 | 60 |
| Points carried to the next sprint | 5 | 5 | 10 |
| Completion | 87% | 84% | 86% |

Velocity was 33 points in Sprint 1 and 27 in Sprint 2, for 60 points in total.
The ten points still in progress at the close (DACWP-21 Revision Comment Thread and DACWP-16 Expiring
Signed Download Link) carry into the next sprint.

## 3. Screenshots

## 4. Reflection Questions

### 4.1 Did your estimations reflect the actual effort?

I think the estimates were fairly accurate. Since we didn't build the system, I mainly checked
whether the relative sizing made sense, and it did. I gave more points to the bigger jobs like
automatic watermarking and the payment gateway, since those involve real complexity and external
integrations, and fewer to things like basic screens or notifications. The stories I added
mid-sprint were more of a test, but they fit the existing scale without any adjustment, so the
sizing was at least consistent. Working in Fibonacci numbers helped too, because it stopped me
overthinking the exact values.

### 4.2 Was your backlog well-prioritized?

Yes, I think so. I ordered it around the user's journey, from submitting a brief through to
receiving the final file, so the core flow of the system got built first. Splitting the stories into
High, Medium and Low priority made the ordering easier to defend, and when new work came up
mid-sprint I could slot it in without reshuffling everything around it. Most of what went unfinished
came from those later additions, so carrying them into the next sprint seems reasonable.

### 4.3 How did your simulated sprint align with your plan?

It followed the plan fairly closely. Both sprints started with the same number of points, and even
with the extra stories added partway through, most of that work still got finished. 60 out of 70
points felt like a solid result. Running the two sprints in parallel worked better than I expected,
mainly because they covered different parts of the system, so neither one sat waiting on the other.
I didn't have to drop anything from scope, and only ten points carried over.

### 4.4 What insights did the burndown chart give about your team's capacity?

Both sprints landed close to each other, 33 points and 27, so somewhere around 30 points a sprint
looks like a realistic capacity to plan against. The shape of the line was useful as well. It sat
flat on the days I closed nothing and stepped down as stories moved to Done, and it ticked upward
whenever I added a story mid-sprint, which made the cost of a scope change hard to miss. As a record
of what actually happened in the sprint, that beats going by my own impression of it.
