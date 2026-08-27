# Use-Case Flow Specification

**Problem #58 — Digital Art Commission & Watermarking Portal**

## Use Case: UC-04 — Make Milestone Payment

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-04 |
| **Primary Actor** | Client Buyer |
| **Supporting Actor** | Payment Gateway |
| **Traces to** | FR-005 |
| **Included** | *Process Payment* («include») |
| **Extended by** | *Apply Promo Code* («extend») |
| **Description** | The client pays the milestone for an approved draft. On successful authorization the system marks the milestone *Paid* and unlocks the final high-resolution, watermark-free source file, which the client then retrieves in **UC-05 Download Final Asset**. |

### Preconditions
1. The Client Buyer is authenticated and viewing an active commission.
2. The Digital Artist has submitted a draft that the client has **approved** (UC-03).
3. The milestone linked to the approved draft has status **Pending Payment**.

### Postconditions
- **On success:** The milestone status is **Paid**, a payment receipt is issued, and the final high-res source file is marked **unlocked** for that client — making UC-05 available.
- **On failure:** The milestone remains **Pending Payment**, no receipt is issued, and the final asset stays locked.

### Main Success Scenario
1. The Client Buyer selects **"Pay Milestone"** on the approved draft. The system displays the milestone amount and payment summary.
2. The Client Buyer selects a payment method (credit/debit card or wallet) and confirms.
3. The system validates the payment details and connects to the **Payment Gateway** *(«include» Process Payment)*.
4. The Payment Gateway authorizes the payment and returns an authorization reference.
5. The system records the transaction against the milestone and sets its status to **Paid**.
6. The system unlocks the final high-resolution, watermark-free source file for this client (FR-005).
7. The system displays a payment confirmation and emails the receipt.
8. The use case ends successfully. The client may now invoke **UC-05 Download Final Asset**, which generates an expiring signed S3 URL valid for 60 minutes (NFR-001).

### Alternate Flow

**4a. Payment Declined**
- 4a1. The Payment Gateway returns a *declined* / authorization-failure response.
- 4a2. The system displays a "Payment failed" message and keeps the milestone as **Pending Payment**.
- 4a3. The Client Buyer is prompted to retry with another payment method.
- 4a4. If payment fails again after **2 attempts**, the system cancels the current payment session, notifies the client, and leaves the final asset locked. The client may restart UC-04 later.

### Alternate Flow (optional extension)

**2a. Apply Promo Code** *(«extend»)*
- 2a1. Before confirming, the Client Buyer enters a valid promo code.
- 2a2. The system validates the code and reduces the milestone amount before proceeding to step 3.
