# Running VibeScan

VibeScan is a command-line interface (CLI) tool designed to detect AI-hallucinated dependencies and slopsquatting/typosquatting attempts in your projects. It analyzes your dependency files (`package.json` for npm and `requirements.txt` for PyPI) and assigns a risk score to each dependency.

## Prerequisites

- Python 3.7 or higher
- `pip` (Python package manager)

## Installation

You can install VibeScan directly from the source code.

1. Clone or download the repository to your local machine:
   ```bash
   git clone https://github.com/AbinVarghexe/vibescan.git
   cd vibescan
   ```

2. Install the package in editable mode (or normally):
   ```bash
   pip install -e .
   ```
   This command installs the required dependencies (`requests`, `colorama`, `packaging`) and sets up the `vibescan` global CLI command.

## Usage

Once installed, you can scan any directory containing a `package.json` or `requirements.txt` file.

### Basic Scan
To scan the current directory:
```bash
vibescan
```

To scan a specific directory:
```bash
vibescan /path/to/your/project
```

### Debug Mode
If you want to see more verbose output (e.g., to confirm which dependency files were found), use the `--debug` flag:
```bash
vibescan --debug /path/to/your/project
```

## How It Works During Execution

1. **Discovery:** The tool looks for `package.json` and `requirements.txt` in the target directory.
2. **Parsing:** It extracts all the specified dependencies from these files.
3. **Analysis:** For each dependency, it queries the respective registry (npm or PyPI) to check if the package legitimately exists, how old it is, and its download counts. It also checks against known typosquatting patterns.
4. **Scoring:** The tool calculates a risk score from 0 to 100 based on the gathered data.
5. **Reporting:** It prints out a final report categorizing dependencies into Safe, Suspicious, or Critical. If any critical risks are detected, the tool exits with a non-zero exit code (`1`), which is useful for failing CI/CD pipelines.
