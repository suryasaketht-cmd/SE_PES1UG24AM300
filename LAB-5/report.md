# Lab 5 Report — Static Code Analysis: Hostel Room Allocation

**Repo:** SETAPESU26/L5_60_hostel-room-allocation · **File:** `hostel_allocation.py`

## Results
| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.84/10 (31 messages) | **10.00/10** |
| Bandit | 5 issues (1 High, 2 Medium, 2 Low) | **0** |
| Flake8 | 20 issues | **0** |

Reports: `reports/before/` and `reports/after/` (`pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`).
Program output before/after: `reports/program_output_before.txt`, `reports/program_output_after.txt`.

## Commits
1. `fix(security): resolve all Bandit findings`
2. `style: fix all Flake8 issues`
3. `refactor: fix Pylint issues and logic bugs` (also adds reports, issues.md, reflection.md, report.md)

## Observed behaviour (before → after)
| Check | Before | After |
|-------|--------|-------|
| A1 occupants (capacity 2) | S1, S2, S3 | S1, S2 |
| Female student S4 | A2 (boys' block) | B1 (girls' block) |
| S1 requested twice | A2 (double allocated) | A1 (same room) |
| A1 after S2 vacates | S1, S2, S3 | S1 |
| Fee, 45 days | 4000 | 8000 (partial month billed as full) |
| Priority order | [1, 2, 4] | [4, 2, 1] |
| Vacant beds | 8 | 9 |

## Issue table and reflection
See `issues.md` (22 issues) and `reflection.md`.

## Assumptions to confirm
- Fees: a partial month is billed as a full month (ceil). Change `monthly_fee` if your instructor expects floor.
- Invalid `year` still returns `None` (not waitlisted), as in the original.
- Warden DB password comes from env var `WARDEN_DB_PASSWORD`; unset means "not connected".
