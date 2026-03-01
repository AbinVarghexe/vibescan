# Product Requirements Document (PRD): VibeScan

## 1. Executive Summary
**VibeScan** is a cross-platform, pre-publish security analysis tool built for the modern AI-assisted development era. As developers increasingly rely on LLM code generators (e.g., "vibe coding"), the risk of introducing **hallucinated dependencies**, typosquatting ("slopsquatting"), and vulnerable libraries into the software supply chain has skyrocketed. VibeScan bridges this gap by acting as a fast, developer-friendly safeguard for Python (PyPI) and Node.js (npm) ecosystems.

## 2. Problem Statement
AI coding assistants often generate functionally plausible but physically non-existent packages, or suggest insecure, outdated dependencies. Malicious actors monitor for these AI hallucinations to register fake packages (slopsquatting), waiting for developers to blindly copy-paste install commands. Traditional SCA (Software Composition Analysis) tools often focus on *known* vulnerabilities (CVEs) but may miss contextless AI hallucinations or brand-new malicious packages before they are published or pushed to production.

## 3. Target Audience
*   **Developers & AI-Assisted Coders**: Looking for rapid, frictionless safety checks before committing code.
*   **DevSecOps & AppSec Teams**: Needing to enforce supply-chain hygiene in CI/CD pipelines.
*   **Open Source Maintainers**: Verifying external contributions don't introduce malicious/hallucinated dependencies.

## 4. Product Goals
*   **Shift-Left Security**: Catch risky dependencies at the pre-commit or pre-publish stage.
*   **Cross-Ecosystem**: Support both Python (`requirements.txt`, `pyproject.toml`) and Node.js (`package.json`).
*   **AI-Specific Defenses**: Explicitly target hallucinated packages, unusual API usages, and slopsquatting.
*   **High Performance**: Run locally within seconds to avoid disrupting developer flow.

## 5. Core Features

### 5.1. Dependency Hallucination Detection
*   **Live Registry Verification**: Quickly ping the npm registry and PyPI to verify that the specified packages and versions actually exist.
*   **Age & Popularity Heuristics**: Flag packages that are unusually new (e.g., created in the last 24 hours), have suspiciously low download counts, or lack a clear maintainer history.

### 5.2. Typosquatting & Slopsquatting Defense
*   **Name Distance Algorithms**: Use Levenshtein distance and known typosquatting patterns to detect names misleadingly similar to popular packages (e.g., `reqeusts` or `react-domm`).
*   **AI Hallucination Pattern Matching**: Cross-reference dependency names against a database/heuristics of known syntax errors or common LLM hallucination naming conventions (e.g., `crypto-secure-hash`).

### 5.3. Machine-Learning Risk Scoring
*   **Risk Rubric**: Combine multiple signals (registry existence, typosquatting indicators, package age, metadata completeness) into an explainable **Risk Score (0-100)**.
*   **Explainable Output**: Instead of just blocking a build, explain *why* it was blocked (e.g., *"Package 'foo-bar' is only 2 hours old and has 0 downloads, typical of a newly hallucinated slopsquatting package."*).

### 5.4. Static Code Analysis (AST)
*   **Unusual Import Detection**: Scan local Python (using AST) and JavaScript (using Babel/AST) files to see if the code imports non-existent inner modules of a real package, which is a common AI hallucination.
*   **Insecure Invocation**: Identify known insecure installations or command executions (e.g., direct OS command execution combined with unverified downloads).

## 6. Integrations & User Workflow

*   **CLI Utility**: A standalone tool that developers can run locally: `vibescan check ./my-project`
*   **Pre-commit Hook**: Automatically scan newly added dependencies before a developer can run `git commit`. 
*   **CI/CD Pipeline Step**: Easy integration into GitHub Actions, GitLab CI, etc., to block PRs that contain high-risk dependencies.

## 7. Non-Functional Requirements
*   **Extensibility**: The tool must be built such that adding a new package manager (e.g., Rust's `cargo`, Go's `go modules`) in the future is straightforward.
*   **Privacy-first**: The tool should analyze code and local manifests locally without sending proprietary source code to a remote server. Only lightweight metadata/package names should be queried against public registries.
*   **Performance**: Should execute in under 2 seconds for a standard project size to not break "the vibe" of rapid coding.

## 8. Success Metrics
*   **Adoption**: Number of CLI downloads and CI/CD workflow integrations.
*   **True Positive Rate**: Accurate detection of hallucinated packages injected intentionally into test projects.
*   **False Positive Rate**: Minimal interference with legitimate dependencies (developers shouldn't have to bypass the tool often).