# Lab 6: Code and Branch Coverage (Income Tax Calculator)

Assigned repo: [SETAPESU26/L6_L7_57_income_tax](https://github.com/SETAPESU26/L6_L7_57_income_tax) (`LAB6` folder).

| File | What it is |
|------|------------|
| [`income_tax.py`](income_tax.py) | Module under test, unchanged |
| [`test_income_tax.py`](test_income_tax.py) | Starter tests from the repo, unchanged |
| [`CodeCoverageTest_PES1UG24CS901_income_tax.py`](CodeCoverageTest_PES1UG24CS901_income_tax.py) | 15 tests for line coverage |
| [`BranchCoverageTest_PES1UG24CS901_income_tax.py`](BranchCoverageTest_PES1UG24CS901_income_tax.py) | 21 tests for branch coverage |
| [`screenshots/`](screenshots/) | Terminal output of both coverage runs for each test file |

Coverage of `income_tax.py`:

| Tests | Line coverage | Branch coverage |
|-------|---------------|-----------------|
| Starter `test_income_tax.py` | 38% | 33% |
| `CodeCoverageTest_...` | 100% | 99% (misses `7->9`) |
| `BranchCoverageTest_...` | 100% | 100% |

The code coverage tests run every line but never try the old regime with investments of 150,000 or less, so the `if investments > 150000` check is never false. That missing branch (`7->9`) is why line coverage reads 100% while branch coverage doesn't. The branch coverage tests add that case plus boundary values: investments of exactly 150,000, taxable income of exactly 0, ages 59, 60, 79 and 80, taxable income equal to the exemption, a slab of exactly 250,000, and tax paid equal to tax due.

To rerun, from this folder:

```bash
pip install coverage pytest
coverage run -m pytest CodeCoverageTest_PES1UG24CS901_income_tax.py && coverage report -m
coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS901_income_tax.py && coverage report -m
```
