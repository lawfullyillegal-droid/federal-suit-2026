# Contributing to Federal Suit 2026: Evidentiary Archive

## Status: CLOSED — READ-ONLY EVIDENTIARY ARCHIVE

This repository is **not an open-source project**. It is a **sealed evidentiary archive** maintained in support of an active federal civil rights action.

---

## Who May Contribute

Only the **primary custodian** (`lawfullyillegal-droid`) may commit changes to this repository.

External pull requests, forks for contribution purposes, and unsolicited modifications **will not be accepted**.

---

## Why This Repository Is Read-Only to the Public

This archive contains:
- Forensic audit outputs with SHA-256 integrity hashes
- Timestamped evidence packets and exhibits
- Legal filings, notices, and correspondence
- Prover9 logic proofs and audit manifests

Unauthorized modification of any file in this archive would constitute **tampering with evidence** and may carry civil and criminal liability under applicable federal law.

---

## How Corrections Are Handled

If you identify an error in a document that has already been published:
- **Do not** open a pull request or issue that edits the original file.
- Original files are **never deleted or overwritten** once committed. They are preserved as part of the immutable record.
- Corrections are added as **versioned addenda** (e.g., `EXHIBIT_A_v2.md`) alongside the original, with a clear notation of what changed and why.

---

## Reporting Concerns

If you believe content in this archive contains information that is factually wrong, contact the custodian via the email address listed in `README.md`. Do not open a public issue that discloses sensitive case details.

---

## Archive Integrity

Every batch of evidence is hashed and recorded in `MANIFEST.md`. The repository uses signed commits where available. Any unauthorized modification to a committed file will be detectable via the Git history and hash mismatch.

---

*This file is part of the Federal Suit 2026 Evidentiary Archive maintained by lawfullyillegal-droid. Last updated: 2026-06-02.*
