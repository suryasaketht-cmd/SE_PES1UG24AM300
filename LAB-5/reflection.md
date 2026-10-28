# Reflection

> The handout text I had did not list the four reflection questions explicitly, so these cover the standard ones for this lab. Re-label to match your handout if the wording differs.

**1. Which issues were the easiest and hardest to fix?**
Easiest: Flake8 style issues and Bandit's `yaml.safe_load` / `debug=False`, which are one-line changes. Hardest: the logic bugs (over-capacity, gender, duplicates, vacate, vacant beds) because no tool flags them. I only found them by reading the program output critically.

**2. Did the tools report any false positives?**
Mostly no, but severity needs judgment. Bandit B311 (`random`) is Low and only matters if the lottery has security stakes; I still switched to `SystemRandom` because it is free. B106 flagged a real hardcoded secret. Pylint's `unused-argument` for `gender` was a true positive that pointed at a real bug.

**3. How would you integrate static analysis into a workflow?**
Run Flake8 and Pylint as pre-commit hooks, and run Bandit plus a Pylint score threshold (e.g. `--fail-under=9.5`) in CI on every pull request, blocking merges on High/Medium Bandit findings.

**4. What improvements in quality, readability and security did you see?**
Pylint went from 5.84 to 10.00, Flake8 from 20 findings to 0, and Bandit from 5 to 0. The code now has docstrings and consistent naming, no hardcoded credentials, no remote-code-execution surfaces, and escapes user input. Also: static analysis is necessary but not sufficient; the most damaging bugs here were invisible to all three tools.
