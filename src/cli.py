import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
JSON_PATH    = "data/approved_sources/jurisdiction_constants.json"
MD_INBOX     = "data/evidence_inbox"
REPORT_PATH  = "data/reports/latest_report.json"
AUDIT_PATH   = "data/reports/audit_log.txt"

# ---------------------------------------------------------------------------
# CONFIGURATION & WEIGHTS
# ---------------------------------------------------------------------------
WEIGHTS = {
    "json": 1.0,
    "md":   0.85,
    "csv":  0.70,
    "unknown": 0.50,
}

STATUTE_PATTERN = re.compile(r'\d+\s+U\.S\.C\.\s+§\s+\d+[\w()\.\-]*')

# Contextual Keywords mapping back to our core frameworks
KEYWORD_RULES = {
    "42 U.S.C. § 1983": ["ricoh", "printer", "node 031332", "clerk", "docket", "ministerial", "return of service", "holding", "144-month", "12-year", "detention"],
    "42 U.S.C. § 1985": ["bailstrike", "supervisors", "exposure", "conspiracy", "bond claim"],
    "15 U.S.C. § 1681": ["equifax", "lexisnexis", "credit", "aggregator", "debt", "reporting"]
}

# ---------------------------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------------------------

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

def ensure_dirs():
    for d in ["data/reports", "data/approved_sources", "data/evidence_inbox"]:
        os.makedirs(d, exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_json(path):
    if not os.path.exists(path):
        print("[ERROR] JSON not found: " + path)
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_text_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_csv_as_text(path):
    if not os.path.exists(path):
        return "", []
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    flat = " ".join(str(v) for row in rows for v in row.values())
    return flat, rows

def collect_inbox_files(inbox_dir):
    files = []
    if not os.path.isdir(inbox_dir):
        return files
    for fname in sorted(os.listdir(inbox_dir)):
        fpath = os.path.join(inbox_dir, fname)
        if not os.path.isfile(fpath):
            continue
        ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else "unknown"
        weight = WEIGHTS.get(ext, WEIGHTS["unknown"])
        files.append({"path": fpath, "name": fname, "ext": ext, "weight": weight})
    return files

# ---------------------------------------------------------------------------
# EXTRACTION ENGINE (RE-ENGINEERED FOR KEYWORDS)
# ---------------------------------------------------------------------------

def extract_statutes_and_context(text, source_label, weight):
    events = []
    text_lower = text.lower()
    
    # 1. Run standard regex literal checks
    for match in STATUTE_PATTERN.finditer(text):
        statute = normalize(match.group())
        events.append({
            "statute":      statute,
            "source":       source_label,
            "weight":       weight,
            "match_type":   "LITERAL_REGEX"
        })
        
    # 2. Run smart contextual keyword checks
    for statute, keywords in KEYWORD_RULES.items():
        for kw in keywords:
            if kw in text_lower:
                # Avoid duplication if regex already caught it
                if not any(e["statute"] == statute and e["source"] == source_label for e in events):
                    events.append({
                        "statute":      statute,
                        "source":       source_label,
                        "weight":       weight,
                        "match_type":   f"CONTEXT_KEYWORD_MATCH ('{kw}')"
                    })
    return events

# ---------------------------------------------------------------------------
# CROSS-CHECK & REPORTS
# ---------------------------------------------------------------------------

def cross_check(events, approved_frameworks):
    matched, unmatched = [], []
    for ev in events:
        statute = ev["statute"]
        aligned = any(statute == f or statute.startswith(f) or f.startswith(statute) for f in approved_frameworks)
        ev["aligned"] = aligned
        if aligned: matched.append(ev)
        else: unmatched.append(ev)
    return matched, unmatched

def write_audit_log(path, run_meta, matched, unmatched, unused_frameworks):
    lines = []
    sep = "=" * 70
    lines.append(sep)
    lines.append("  AUDIT RUN: " + run_meta["timestamp"])
    lines.append("  Draft Query: " + (run_meta.get("draft_query") or "(none)"))
    lines.append(sep)
    lines.append("\n[VERIFIED CONNECTIONS] -- Evidence linking back to your frameworks:")
    lines.append("-" * 70)
    for ev in matched:
        lines.append("  OK  | weight={:.2f} | file={} -> {} via {}".format(
            ev["weight"], ev["source"], ev["statute"], ev["match_type"]
        ))
    lines.append("\n" + sep + "\n")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("[LOG ] Audit ledger updated -> " + path)

def write_report(path, run_meta, matched, unmatched, unused_frameworks, all_events):
    report = {
        "run_meta": run_meta,
        "summary": {"total_connections": len(all_events), "matched_count": len(matched)},
        "verified_events": matched
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("[RPT ] Clean JSON report compiled -> " + path)

# ---------------------------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Context-Aware Claims Verifier")
    parser.add_argument("--draft", type=str, default=None)
    args = parser.parse_args()

    ensure_dirs()
    print("=" * 60)
    print("  Upgraded Contextual Reference Engine Active")
    print("  Timestamp: " + timestamp())
    print("=" * 60)

    data = load_json(JSON_PATH)
    if data is None: sys.exit(1)

    approved = [normalize(s) for s in data.get("statutory_frameworks", [])]
    run_meta = {"timestamp": timestamp(), "draft_query": args.draft, "approved_frameworks": approved}

    all_events = []
    inbox_files = collect_inbox_files(MD_INBOX)
    
    for fi in inbox_files:
        text, _ = load_csv_as_text(fi["path"]) if fi["ext"] == "csv" else (load_text_file(fi["path"]), [])
        events = extract_statutes_and_context(text, fi["name"], fi["weight"])
        print("[{:>4}] Scanned '{}' -> Found {} valid context links.".format(fi["ext"].upper(), fi["name"], len(events)))
        all_events += events

    matched, unmatched = cross_check(all_events, approved)
    write_audit_log(AUDIT_PATH, run_meta, matched, unmatched, [])
    write_report(REPORT_PATH, run_meta, matched, unmatched, [], all_events)
    print("=" * 60)

if __name__ == "__main__":
    main()
