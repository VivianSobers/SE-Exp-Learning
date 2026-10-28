"""Loan eligibility and EMI calculator.

Calculates EMIs, checks eligibility, works out the maximum affordable loan,
builds amortisation schedules, assigns risk bands and stores applications.
"""
import os
import base64
import http.client
import json
import secrets
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage

# Global loan book
applications = {}
MAX_FOIR = 0.5
BUREAU_HOST = "upload.creditbureau.example"
LOAN_TYPES = {"home", "car", "personal"}


def calculate_emi(principal, annual_rate, years):
    """Return the monthly EMI for a loan; annual_rate is a decimal (0.09)."""
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def check_eligibility(age, income, credit_score, existing_emi, loan_type):
    """Return True if the applicant qualifies for the given loan type."""
    if age < 21 or age > 60:
        return False
    if loan_type not in LOAN_TYPES:
        return False
    if income <= 0 or existing_emi / income > MAX_FOIR:
        return False
    return credit_score > 750 or income > 25000


def max_loan_amount(income, existing_emi, annual_rate, years):
    """Return the largest principal whose EMI fits within the FOIR limit."""
    available = income * MAX_FOIR - existing_emi
    if available <= 0:
        return 0
    return available / calculate_emi(1, annual_rate, years)


def amortisation_schedule(principal, annual_rate, years):
    """Return (month, interest, closing balance) rows for the whole loan."""
    emi = calculate_emi(principal, annual_rate, years)
    balance = principal
    rows = []
    for month in range(1, years * 12 + 1):
        interest = balance * annual_rate / 12
        balance = balance - (emi - interest)
        rows.append((month, round(interest, 2), round(balance, 2)))
    return rows


def application_id():
    """Return a new random application ID such as LN-12345678."""
    return "LN-" + str(10000000 + secrets.randbelow(90000000))


def save_application(name, amount, file="loans.json"):
    """Add an application to the loan book, save it as JSON, return its ID."""
    app_id = application_id()
    applications[app_id] = {
        "name": name,
        "amount": amount,
        "date": str(datetime.now()),
    }
    with open(file, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2)
    return app_id


def load_applications(file="loans.json"):
    """Replace the loan book with the one saved in file (empty if missing)."""
    applications.clear()
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            applications.update(json.load(f))


def upload_to_bureau(report_path, user="loanops"):
    """Upload a report to the credit bureau over HTTPS."""
    # Credentials come from the environment, never from the source code
    password = os.environ.get("BUREAU_PASSWORD")
    if not password:
        raise RuntimeError("Set BUREAU_PASSWORD to upload to the bureau")
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    with open(report_path, "rb") as report:
        body = report.read()
    # HTTPS with certificate checks instead of plain-text FTP
    conn = http.client.HTTPSConnection(
        BUREAU_HOST, timeout=30, context=ssl.create_default_context()
    )
    try:
        conn.request(
            "PUT",
            "/reports/" + os.path.basename(report_path),
            body=body,
            headers={"Authorization": "Basic " + token},
        )
        status = conn.getresponse().status
    finally:
        conn.close()
    if status >= 300:
        raise RuntimeError(f"Bureau upload failed with HTTP {status}")


def notify_applicant(email, status):
    """Email the applicant their application status."""
    # Send through SMTP with STARTTLS instead of shelling out to `mail`
    message = EmailMessage()
    message["Subject"] = "Loan " + status
    message["From"] = os.environ.get("LOAN_MAIL_FROM", "loans@bank.example")
    message["To"] = email
    message.set_content(f"Your loan application status: {status}")
    smtp_host = os.environ.get("SMTP_HOST", "localhost")
    with smtplib.SMTP(smtp_host, 587, timeout=30) as smtp:
        smtp.starttls(context=ssl.create_default_context())
        smtp.send_message(message)


def interest_saved(principal, annual_rate, years, prepayment):
    """Return the interest saved by prepaying part of the principal upfront."""
    original = calculate_emi(principal, annual_rate, years) * years * 12
    prepayment = min(prepayment, principal)
    reduced = (calculate_emi(principal - prepayment, annual_rate, years)
               * years * 12)
    # The prepaid principal is not interest, so take it out of the saving
    return original - reduced - prepayment


def risk_band(credit_score):
    """Map a credit score (300-900) to a risk band."""
    if credit_score > 900 or credit_score < 300:
        return "INVALID"
    if credit_score >= 800:
        return "LOW"
    if credit_score >= 700:
        return "MEDIUM"
    if credit_score >= 600:
        return "HIGH"
    return "VERY HIGH"


def main():
    """Run the built-in demo."""
    print("EMI for 5L @ 9% for 5 years:", calculate_emi(500000, 0.09, 5))
    print("Eligible (score 760, income 15000, EMIs 12000):",
          check_eligibility(35, 15000, 760, 12000, "personal"))
    print("Eligible (unknown loan type 'crypto'):",
          check_eligibility(30, 80000, 650, 0, "crypto"))
    print("Max loan for income 40000:", max_loan_amount(40000, 5000, 0.09, 5))
    print("Last schedule row:", amortisation_schedule(100000, 0.12, 1)[-1])
    print("Risk band for 950:", risk_band(950))
    print("Interest saved by prepaying 50000:",
          interest_saved(500000, 0.09, 5, 50000))
    print("Saved as:", save_application("Anil", 500000))
    load_applications()
    print("Applications on file:", len(applications))
    print("Upload to bureau skipped (no network)")


if __name__ == "__main__":
    main()
