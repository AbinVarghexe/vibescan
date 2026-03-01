# VibeScan (Node.js Wrapper)

A Node.js wrapper for VibeScan - the AI dependency security scanner.

## Installation

```bash
npm install -g vibescan-js
```

**Prerequisites**: This package requires Python 3.7+ and the VibeScan Python package to be installed:

```bash
pip install vibescan
```

## Usage

Once installed, you can use the `vibescan` command from any Node.js project:

```bash
vibescan
```

Scan a specific directory:

```bash
vibescan ./my-project
```

Enable debug output:

```bash
vibescan --debug
```

## How It Works

This is a lightweight Node.js wrapper that calls the VibeScan Python CLI. It allows Node.js developers to easily integrate VibeScan into their workflow without leaving the npm ecosystem.

## Features

- Detects AI hallucinated dependencies
- Identifies typosquatting attempts
- Scans package.json files
- Cross-platform support (Windows, macOS, Linux)
- Fast and efficient
- No data sent to external servers

## Requirements

- Node.js 12.0.0 or higher
- Python 3.7 or higher
- VibeScan Python package (`pip install vibescan`)

## Related Packages

- **vibescan** (Python): The core scanning engine
- **vibescan-web**: Web interface for VibeScan

## License

MIT

## Contributing

Contributions are welcome! Please visit the main repository at https://github.com/yourusername/vibescan

## Support

For issues and questions, please visit: https://github.com/yourusername/vibescan/issues