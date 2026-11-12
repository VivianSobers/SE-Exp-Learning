# Lab 7: Fuzzing for Input Validation Bugs (Income Tax Parser)

Assigned repo: [SETAPESU26/L6_L7_57_income_tax](https://github.com/SETAPESU26/L6_L7_57_income_tax) (`LAB7` folder).

| File | What it is |
|------|------------|
| [`income_tax_parser.py`](income_tax_parser.py) | Fixed module. None of the three functions raises for any input; invalid input returns `None` |
| [`test_income_tax_parser.py`](test_income_tax_parser.py) | 7 Hypothesis tests: a no-crash test per function, a valid-input test per function, and one for non-ASCII PAN letters |
| [`PES1UG24CS901_VivianSobers_LAB7.pdf`](PES1UG24CS901_VivianSobers_LAB7.pdf) | Screenshots SS1 to SS4 and the list of bugs fixed |
| [`screenshots/`](screenshots/) | The same four screenshots as PNG files |

| Run | Result |
|-----|--------|
| SS1: `python income_tax_parser.py`, buggy | Crashes with `ValueError` on the amount `Rs 12.5 lakh` |
| SS2: `python -m pytest test_income_tax_parser.py`, buggy | 4 failed, 3 passed |
| SS3: `python income_tax_parser.py`, fixed | Prints `Invalid amount` and `Invalid tax slab` and finishes |
| SS4: `python -m pytest test_income_tax_parser.py`, fixed | 7 passed |

To rerun, from this folder:

```bash
pip install hypothesis pytest
python income_tax_parser.py
python -m pytest test_income_tax_parser.py
```
