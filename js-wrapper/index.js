#!/usr/bin/env node

const { spawn } = require("child_process");
const path = require("path");

// This wrapper assumes the Python `vibescan` package is installed globally
// or accessible in the correct environment (e.g. built alongside).
// For a true production approach, this might download a precompiled bin
// or bundle a small Python environment using something like PyInstaller.

const args = process.argv.slice(2);

// Check if Python executable 'vibescan' works
const vibescanProcess = spawn("vibescan", args, {
  stdio: "inherit",
  shell: true,
});

vibescanProcess.on("error", (err) => {
  console.error("\\n[VibeScan Error] Cannot find the `vibescan` Python CLI.");
  console.error(
    "Please ensure the Python package is installed: `pip install vibescan`\\n",
  );
  process.exit(1);
});

vibescanProcess.on("close", (code) => {
  process.exit(code);
});