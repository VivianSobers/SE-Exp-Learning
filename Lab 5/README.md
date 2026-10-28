# Lab 5: Static Code Analysis (Loan Eligibility and EMI Calculator)

Assigned repo: [SETAPESU26/L5_57_loan-eligibility](https://github.com/SETAPESU26/L5_57_loan-eligibility).

| File | What it is |
|------|------------|
| [`loan_calculator.py`](loan_calculator.py) | Cleaned script |
| [`before/`](before/) | Pylint, Bandit and Flake8 reports on the original script |
| [`after/`](after/) | The same reports on the final script. `flake8_report.txt` is empty because Flake8 prints nothing when it finds no issues |
| [`issues.md`](issues.md) | Issue table |

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.17/10 | 10.00/10 |
| Bandit | 8 issues | No issues |
| Flake8 | 22 issues | None |

Commits, in order:

1. `docs: add Lab5 baseline reports`: the original script and the before reports
2. `fix: correct loan calculation bugs`: wrong output that no tool flagged
3. `fix: resolve bandit security issues`
4. `fix: clean flake8 style issues`
5. `fix: raise pylint score to 10`

To rerun, from this folder:

```bash
python -m pip install pylint bandit flake8
python loan_calculator.py
python -m pylint loan_calculator.py
python -m bandit -r loan_calculator.py
python -m flake8 loan_calculator.py
```

Tools used: Pylint 4.1.3, Bandit 1.9.4 and Flake8 7.4.1 on Python 3.14.5.
