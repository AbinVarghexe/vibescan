# VibeScan Code Explanation

VibeScan is structured as a standard Python package. Below is a code-by-code breakdown of how the application is built and functions.

## 1. Entry Point & CLI Configuration (`setup.py` & `vibescan/cli.py`)

### `setup.py`
This file makes VibeScan installable via `pip`. It handles the metadata, requires minimum dependencies (`requests`, `colorama`, `packaging`), and most importantly, defines the `console_scripts` entry point:
```python
    entry_points={
        "console_scripts": [
            "vibescan=vibescan.cli:main",
        ],
    },
```
This maps the shell command `vibescan` to the `main()` function in `cli.py`.

### `vibescan/cli.py`
This is the main orchestrator of the tool.
- **Argument Parsing:** Uses `argparse` to take an optional directory path parameter and a `--debug` flag.
- **File Discovery:** Checks for the presence of `package.json` and `requirements.txt` in the specified target path.
- **Data Flow Process:**
  - Passes the paths to the parser functions (`parse_package_json`, `parse_requirements_txt`) in `parsers.py` to get a list of dependency dictionaries.
  - Iterates through the list of dependencies. For each dependency, it calls `check_typosquatting` and either `check_npm_package` or `check_pypi_package` depending on the ecosystem.
  - Feeds the returned dictionary data into `calculate_risk` from `scorer.py` to get a numeric score and a list of risk reasons.
  - Compiles the final results and passes them to `report_results` in `reporter.py`.
- **Exit Codes:** Uses `sys.exit(1)` if `report_results` returns `False` (indicating critical risks) to fail CI pipelines.

## 2. Dependency File Parsing (`vibescan/parsers.py`)

This file is responsible for reading and extracting dependencies from manifest files.
- `parse_package_json(path)`: Uses the standard library `json` module to load the file. It checks both the `dependencies` and `devDependencies` keys and returns a list of dictionaries where each specifies the package `name`, `version`, and `ecosystem` (`npm`).
- `parse_requirements_txt(path)`: Uses standard file reading and the `re` module. It skips comments and edge case URLs (like Git links). It parses the package name and version using a regex split (`re.split(r'[=><!~]+', line)`) and strips out extras (e.g. turning `package[security]` into `package`). Ecosystem is set to `pypi`.

## 3. Remote Registry Checkers (`vibescan/checkers/registry_checker.py`)

The tool makes HTTP GET requests strictly to public APIs to gather safety indicators.

- `check_npm_package(name)`:
  - Hits `https://registry.npmjs.org/{name}`. A `404` directly signifies that the package doesn't exist, heavily flagging the package as a hallucination.
  - Parses the `time.created` string into a Python `datetime` object.
  - Hits `https://api.npmjs.org/downloads/point/last-month/{name}` to pull recent download counts, which is a strong proxy for package legitimacy.
  
- `check_pypi_package(name)`:
  - Hits `https://pypi.org/pypi/{name}/json`. A `404` signifies hallucination.
  - Parses the first `upload_time` inside the `releases` dictionary to figure out the package creation date.

Both functions gracefully handle timeouts and network disconnects, returning `None` for existence instead of failing outright.

## 4. Risk Scoring Engine (`vibescan/scorer.py`)

The `calculate_risk(registry_data, typo_data)` function applies heuristic rules to generate a final risk score (0 to 100).

1. **Existence (Hallucinations):** If `registry_data['exists']` is `False`, it adds `100` points (immediate critical risk), as the AI has generated a package that isn't real.
2. **Typosquatting:** If the typo checker flagged it, and it's suspiciously close to a popular package, it adds `60` points.
3. **Creation Age:** Compares the package `created` date to the current `datetime.now(timezone.utc)`. Packages newer than 7 days get `+40` points, packages newer than 30 days get `+10` points.
4. **Popularity:** For ecosystems where download metadata is readily accessible (like NPM), fewer than 100 downloads in the last month adds `+20` points; fewer than 1000 adds `+5` points.

The score is artificially capped at 100 before being returned with an array of text reasons.

## 5. UI and Reporting (`vibescan/reporter.py`)

This handles outputting the findings nicely to the terminal.
- Uses `colorama` to provide color-coded text (`Fore.GREEN`, `Fore.YELLOW`, `Fore.RED`) regardless of the operating system.
- `report_results(results)`: Buckets all the scrutinized dependencies into Safe (`<10`), Suspicious (`10` to `59`), and Critical (`>=60`).
- Iterates over the suspicious and critical lists, explicitly listing the package name, ecosystem, specific score, and bullet points of reasons why it was flagged.
- Returns `False` if there are any critical dependencies, causing the main function to trigger an exit code `1`. Otherwise returns `True`.
