# Mohave County Judicial Integrity Audit - Node 031332

## Forensic Summary
This repository contains cryptographically hashed evidence of constitutional failures in Cerbat Precinct 5 (Mohave County, AZ) under Judge David Jay Wayt.

### Key Findings:
- **8th Amendment**: Systemic inflation of bond amounts (0k for Class 3 Misdemeanors) targeting Zip 86413.
- **6th Amendment**: 96-hour counsel appointment lag detected for detained defendants.
- **Structural Conflict**: Hardware-verified (RICOH IM 4000) unified processing between Justice and Superior Court tiers.

### Manifest Integrity:
All artifacts are hashed via SHA-256 and committed on 2026-05-02.

## Scanner CLI: `trust_scan_bot.py`

This repository includes a CLI wrapper `trust_scan_bot.py` that can run built-in and discovered scanners.

Basic usage:

```bash
python trust_scan_bot.py --scanner deep
python trust_scan_bot.py --scanner mohave --url https://example.com/target
```

Options:
- `--scanner` / `-s`: Which scanner to run (use `--list` to enumerate discovered scanners).
- `--url`: Optional URL to pass to scanners that accept it.
- `--results` / `-r`: Optional path to write structured results (`.json` or `.csv`).
- `--output` / `-o`: Optional path to write logger output.
- `--log-level`: Logging verbosity (DEBUG/INFO/WARNING/ERROR).

Example writing results to JSON:

```bash
python trust_scan_bot.py --scanner deep --results deep_results.json

## Dashboard Server

Run a lightweight Flask server to execute scanners on-demand and serve dashboards.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python dashboard_server.py
```

Endpoints:
- `GET /list` — list discovered scanners
- `GET|POST /run?scanner=<scanner>&url=<url>` — run a scanner (returns JSON including `dashboard` path)
- `GET /view?path=<path>` — serve a generated dashboard HTML file

Security: this server is minimal and unauthenticated — do not expose it publicly without adding auth or running behind a secure proxy.
```

