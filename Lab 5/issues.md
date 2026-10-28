# Lab 5: Issue table

File: `loan_calculator.py` from [SETAPESU26/L5_57_loan-eligibility](https://github.com/SETAPESU26/L5_57_loan-eligibility).
Line numbers refer to the original file (the reports in [`before/`](before/)).

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.17/10 | 10.00/10 |
| Bandit | 8 issues (2 High, 1 Medium, 5 Low) | No issues |
| Flake8 | 22 issues | None |

## Issues found by the tools

High and medium severity first.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Plain-text FTP (Bandit B402, B321, High) | Security | 3, 68-71 | `uploadToBureau` sent credit reports and the login over unencrypted FTP | Replaced `ftplib` with an HTTPS `PUT` using `http.client.HTTPSConnection` and `ssl.create_default_context()`, so the certificate is checked |
| 2 | Unsafe deserialization with `marshal` (Bandit B302, Medium) | Security | 4, 57, 64 | The loan book was saved and loaded with `marshal`, which isn't safe for data read back from disk | Saved and loaded the book as JSON (`loans.json`) |
| 3 | Hardcoded password (Bandit B107) | Security | 67 | The bureau password `Bureau#2024` was a default argument in the source | Removed the parameter; the password is read from the `BUREAU_PASSWORD` environment variable, and the upload refuses to run without it |
| 4 | Shelling out to `mail` (Bandit B404, B603, B607; Pylint W1510) | Security | 6, 74 | `notifyApplicant` ran the `mail` program by partial path with an email address from user input, and didn't check the result | Sent the email with `smtplib` and `EmailMessage` over STARTTLS instead of starting a process |
| 5 | Predictable application IDs (Bandit B311) | Security | 51 | IDs came from `random.randint`, which is guessable | Used `secrets.randbelow`, keeping the `LN-` plus 8 digits format |
| 6 | Mutable default argument (Pylint W0102) | Bug | 20-21 | `history=[]` was created once and shared across every call to `checkEligibility`, so it kept growing. Nothing ever read it | Removed the unused parameter. That also fixed too-many-arguments (R0913, R0917) |
| 7 | Unused argument, unused variable, redefined built-in (Pylint W0613, W0612, W0622) | Bug | 33-38 | `maxLoanAmount` ignored `annual_rate`, looped with an unused `month` and shadowed `sum`. The warnings pointed at a real bug (row 16) | Replaced the loop with the present-value formula (see row 16) |
| 8 | `global` statement (Pylint W0603) | Quality | 62 | `loadApplications` rebound the module-level dict | Cleared and updated the existing dict in place |
| 9 | Files opened without `with` (Pylint R1732) | Quality | 56, 63, 70 | A crash between `open` and `close` would leave the file open | Used `with open(...)` everywhere |
| 10 | No `__main__` guard | Quality | 106 | `main()` ran, and wrote `loans.bin`, whenever the module was imported | Wrapped the call in `if __name__ == "__main__":` |
| 11 | camelCase function names, missing docstrings (Pylint C0103, C0114, C0116) | Style | 1-93 | Function names didn't follow PEP 8, and nothing was documented | Renamed every function to snake_case and added a module docstring and one per function |
| 12 | Needless `else`/`elif` after `return`, chained `==`, extra parentheses (Pylint R1705, R1714, R1703, C0325) | Style | 28-31, 79, 82-91 | Branching was longer than it needed to be | Used `not in LOAN_TYPES`, flat `if` blocks and a plain `return` |
| 13 | Unused import (Flake8 F401, Pylint W0611) | Style | 2 | `math` was imported and never used | Removed it |
| 14 | Formatting (Flake8 E302, E305, E501, F541; Pylint C0301) | Style | 14-106 | Missing blank lines between functions, lines over 79 characters, and an f-string with no placeholders | Added two blank lines between top-level definitions, wrapped long lines and made the f-string a plain string |

## Bugs no tool flagged

The README warned that some problems only show up in the output. Each of these is fixed in commit `fix: correct loan calculation bugs`.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 15 | Rate passed as a percentage | Bug | 94 | The demo passed `9` instead of `0.09`, so the EMI on 5 lakh came out as 375,000 a month | Passed `0.09`, which gives 10,379.18 |
| 16 | Maximum loan ignored interest | Bug | 33-38 | The affordable EMI was multiplied by the number of months, giving 900,000 | Divided the affordable EMI by the EMI of a 1-rupee loan (the present value of the payments): 722,600.60 |
| 17 | Eligibility shortcut | Bug | 24-25 | A credit score over 750 or income over 25,000 returned `True` before the FOIR and loan-type checks, so an 80% FOIR applicant and a "crypto" loan were both approved | Checked the loan type and FOIR first, then applied the score/income condition last. Both demo cases now return `False` |
| 18 | Risk band accepted impossible scores | Bug | 81-91 | Credit scores run from 300 to 900, but 950 came back as `LOW` | Anything above 900 or below 300 returns `INVALID` |
| 19 | Interest saved included the prepaid principal | Bug | 76-79 | The 50,000 prepayment itself was counted as interest saved (62,275.07) | Subtracted the prepayment: 12,275.07 |
| 20 | Crashes on edge inputs | Bug | 15-17, 26, 63 | A 0% rate or zero income caused division by zero, and loading a missing file crashed | A 0% rate gives principal / months, zero income is ineligible, and a missing file gives an empty loan book |

I checked these fixes with 25 pytest tests kept outside the repo. Where I could, the tests use outside reference values: the EMI of 1 lakh at 12% for 1 year is 8,884.88. Other tests check one function against another. For example, the EMI of the maximum loan must equal the affordable EMI, and the interest saved must match the difference in total schedule interest.
