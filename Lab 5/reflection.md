# Lab 5: Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The Flake8 issues were the easiest. Missing blank lines, long lines, an unused import and an f-string with nothing in it are all mechanical, and the report gives the exact line and column. Most of Pylint's naming and docstring warnings were the same kind of work, just more of it.

The Bandit findings took the most thought, because removing the flagged call wasn't enough. The program still had to upload reports to the bureau and email applicants. So I had to choose a safe replacement: HTTPS with certificate checking instead of FTP, `smtplib` with STARTTLS instead of running `mail`, JSON instead of `marshal`, and an environment variable instead of a password in the code.

The hardest bugs were the ones no tool reported. The maximum loan, the eligibility shortcut and the interest saved figure all ran without errors and printed believable numbers. I only caught them by checking the output against what the numbers should be. Then I wrote tests that compare one function with another, for example that the EMI on the maximum loan equals the EMI the applicant can afford.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Nothing was completely wrong, but some findings were weaker than their wording suggests. Bandit's B404 fires just because `subprocess` is imported, before looking at how it's used. The call here passed a fixed argument list and no shell, so the import alone wasn't a vulnerability. The real issues on that line were the partial path to `mail` and the unchecked result, which B607 and Pylint's W1510 also reported.

Pylint's too-many-arguments warning on `checkEligibility` is borderline too. Five or six inputs is normal for an eligibility check. It went away here only because one of the arguments, the mutable `history` list, was unused anyway.

It worked the other way as well. Pylint's "unused argument `annual_rate`" in `maxLoanAmount` looked like a style complaint, but it was the only tool output pointing at a real calculation bug: the function ignored interest completely.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I'd run them in two places. Locally, Flake8 and Pylint would run in a pre-commit hook, so style problems get fixed before a commit exists. They're fast enough that this costs nothing. In CI, all three would run on every pull request. Bandit would fail the build on any medium or high finding, and Pylint would fail it below an agreed score, for example 9.5. Each tool's config would be committed to the repo so every developer gets the same rules. When a finding is accepted on purpose, it would be marked with an inline `# nosec` or `# pylint: disable=` comment that gives the reason, so the decision can be reviewed. And because no tool caught the calculation bugs in this lab, unit tests would run in the same pipeline.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The numbers changed: Pylint went from 5.17 to 10.00, Bandit from 8 issues to none, and Flake8 from 22 to none. In practice:

- The password is no longer in the source, and data leaving the program is encrypted.
- The loan book is stored as readable JSON, which is also safe to load.
- Function names and docstrings now say what each function does and which units it expects. Unclear units were exactly how the 9 versus 0.09 rate bug happened.
- Files are always closed, and importing the module no longer runs the demo and writes a file.
- The demo output is now correct: an EMI of 10,379.18 instead of 375,000, a maximum loan of 722,600.60 instead of 900,000, interest saved of 12,275.07 instead of 62,275.07, and both bad applications rejected.
- Edge cases such as a 0% rate, zero income or a missing file no longer crash the program.
