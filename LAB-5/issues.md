# Issues found and fixed — `hostel_allocation.py`

Baseline: Pylint 5.84/10 · Bandit 5 findings (1 High, 2 Medium, 2 Low) · Flake8 20 findings.
Final: Pylint 10.00/10 · Bandit 0 · Flake8 0.

| # | Issue | Type | Line(s) (original) | Description | Fix Approach |
|---|-------|------|--------------------|-------------|--------------|
| 1 | Flask `debug=True` (B201, **High**) | Security | 80 | Werkzeug debugger exposes remote code execution | `app.run(host="127.0.0.1", debug=False)` |
| 2 | Unsafe `yaml.load` (B506, Medium) | Security | 21 | `yaml.Loader` can instantiate arbitrary Python objects | Use `yaml.safe_load` |
| 3 | `logging.config.listen` (B612, Medium) | Security | 72 | Opens a socket that accepts config and executes code; function unused | Removed the function and import |
| 4 | Hardcoded password (B106, Low) | Security | 66 | `"Hostel@123"` committed in source | Read from `WARDEN_DB_PASSWORD` env var |
| 5 | `random.sample` (B311, Low) | Security | 56 | Predictable PRNG for a lottery | `random.SystemRandom().sample` |
| 6 | Reflected XSS in `/room` | Security (not flagged by tools) | 77 | `id` query param concatenated into HTML; also crashes with `TypeError` if `id` is missing | `markupsafe.escape`, default `""` |
| 7 | Room over-allocation | Bug | 34 | `>` should be `>=`; A1 (capacity 2) held 3 students | Use `>=` |
| 8 | Gender ignored | Bug / W0613 | 29, 34 | Female student placed in the boys' block; `gender` argument unused | Skip rooms whose block gender differs |
| 9 | Duplicate allocation | Bug | 29 | Same student allocated twice (S1 in A1 and A2) | Return existing room if already allocated |
| 10 | Mutable default arg (W0102) | Bug | 29 | `preferred=[]` shared across calls; unknown preferred room → `KeyError` | Default `None`; skip unknown rooms |
| 11 | `vacateRoom` leaves bed occupied | Bug | 41-45 | Removed from `allocations` but not from `room["occupants"]`; dead `else: pass` | `pop` + remove from occupants |
| 12 | Priority order reversed | Bug | 53 | Docs say seniors first, sorted ascending | `reverse=True` |
| 13 | `vacantBeds` wrong | Bug | 58-63 | Only counted completely empty rooms (printed 8) | `sum(capacity - occupants)` |
| 14 | Fee rounding / crash | Bug | 47-50 | 45 days billed as 1 month; `KeyError` if student not allocated | Ceil to whole months; clear `ValueError` |
| 15 | `main()` runs on import | Design (E305) | 101 | Importing the module executes the demo | `if __name__ == "__main__":` |
| 16 | `type(x) != int` (E721/C0123) | Style | 30 | Unidiomatic type check | `isinstance` (also excludes `bool`) |
| 17 | Unused imports `os`, `sys` (F401/W0611) | Style | 1-2 | Dead imports | Removed `sys`; `os` is now used |
| 18 | Blank lines / long lines (E302, E305, E501, C0301) | Style | many | PEP 8 formatting | Reformatted, wrapped lines |
| 19 | camelCase names (C0103) | Style | 11 funcs | Not snake_case | Renamed all to snake_case |
| 20 | Missing docstrings (C0114/C0116) | Style | all | No module/function docs | Added docstrings |
| 21 | Dict iteration (C0206) | Style | 60 | Index into dict inside loop | `.values()` / `.items()` |
| 22 | Inconsistent return (implicit `None`) | Bug | 39 | `allocateRoom` fell off the end | Explicit `return None`; no duplicate waitlist entries |
