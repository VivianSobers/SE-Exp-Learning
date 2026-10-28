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


def calculateEMI(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return emi


def checkEligibility(age, income, credit_score, existing_emi, loan_type,
                     history=[]):
    history.append(loan_type)
    if age < 21 or age > 60:
        return False
    if loan_type not in ("home", "car", "personal"):
        return False
    if income <= 0 or existing_emi / income > MAX_FOIR:
        return False
    return credit_score > 750 or income > 25000


def maxLoanAmount(income, existing_emi, annual_rate, years):
    available = income * MAX_FOIR - existing_emi
    if available <= 0:
        return 0
    # Largest principal whose EMI equals the affordable amount
    return available / calculateEMI(1, annual_rate, years)


def amortisationSchedule(principal, annual_rate, years):
    emi = calculateEMI(principal, annual_rate, years)
    balance = principal
    rows = []
    for month in range(1, years * 12 + 1):
        interest = balance * annual_rate / 12
        balance = balance - (emi - interest)
        rows.append((month, round(interest, 2), round(balance, 2)))
    return rows


def applicationId():
    return "LN-" + str(10000000 + secrets.randbelow(90000000))


def saveApplication(name, amount, file="loans.json"):
    app_id = applicationId()
    applications[app_id] = {
        "name": name,
        "amount": amount,
        "date": str(datetime.now()),
    }
    f = open(file, "w", encoding="utf-8")
    json.dump(applications, f, indent=2)
    f.close()
    return app_id


def loadApplications(file="loans.json"):
    global applications
    if not os.path.exists(file):
        applications = {}
        return
    f = open(file, "r", encoding="utf-8")
    applications = json.load(f)
    f.close()


def uploadToBureau(report_path, user="loanops"):
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


def notifyApplicant(email, status):
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


def interestSaved(principal, annual_rate, years, prepayment):
    original = calculateEMI(principal, annual_rate, years) * years * 12
    prepayment = min(prepayment, principal)
    reduced = (calculateEMI(principal - prepayment, annual_rate, years)
               * years * 12)
    # The prepaid principal is not interest, so take it out of the saving
    return (original - reduced - prepayment)


def riskBand(credit_score):
    if credit_score > 900:
        return "INVALID"
    if credit_score >= 800:
        return "LOW"
    elif credit_score >= 700:
        return "MEDIUM"
    elif credit_score >= 600:
        return "HIGH"
    elif credit_score >= 300:
        return "VERY HIGH"
    else:
        return "INVALID"


def main():
    print("EMI for 5L @ 9% for 5 years:", calculateEMI(500000, 0.09, 5))
    print("Eligible (score 760, income 15000, EMIs 12000):",
          checkEligibility(35, 15000, 760, 12000, "personal"))
    print("Eligible (unknown loan type 'crypto'):",
          checkEligibility(30, 80000, 650, 0, "crypto"))
    print("Max loan for income 40000:", maxLoanAmount(40000, 5000, 0.09, 5))
    print("Last schedule row:", amortisationSchedule(100000, 0.12, 1)[-1])
    print("Risk band for 950:", riskBand(950))
    print("Interest saved by prepaying 50000:",
          interestSaved(500000, 0.09, 5, 50000))
    print("Saved as:", saveApplication("Anil", 500000))
    loadApplications()
    print("Applications on file:", len(applications))
    print("Upload to bureau skipped (no network)")


main()
