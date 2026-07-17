# Evidence Integrity Manifest (Canonical)

This file is the repository's canonical integrity index.  
All evidence verification starts here.

## 1) Verify this manifest index set

Run from repository root:

```bash
sha256sum -c checksum_manifest.txt
sha256sum -c mohave-judicial-audit/evidence_manifest.sha256
sha256sum -c Evidence/Clean_Exhibits/evidence_hashes.sha256
sha256sum -c Evidence/Clean_Exhibits/evidence_hashes_clean.sha256
sha256sum -c Evidence/Clean_Exhibits/court_exhibits.sha256
sha256sum -c audit_integrity.sha256
sha256sum -c evidence/audit_integrity.sha256
sha256sum -c enforcement_actions/finalized_manifest/INTEGRITY_SEAL.sha256
```

## 2) Manifest-of-manifests checksums

| File | SHA-256 |
|---|---|
| `checksum_manifest.txt` | `ed2f36ea420e84695190a53528a60302c461ae0545d747c1917e404b279d87ca` |
| `mohave-judicial-audit/evidence_manifest.sha256` | `d0006047d124479048f7874ba2920f49382c6a4c6e936a2235ef14180be0b0a1` |
| `Evidence/Clean_Exhibits/evidence_hashes.sha256` | `3064fb02ad30665626f43bb49d3520fbbbe5f512207c81171d38891bf839bdc7` |
| `Evidence/Clean_Exhibits/evidence_hashes_clean.sha256` | `91f46321329bb61c8d5adcdcc769195da2f14672f6a272cfb788908eb891d761` |
| `Evidence/Clean_Exhibits/court_exhibits.sha256` | `e18605cd75bf77e5238b7b157693275c057d510d5ba8eea82c6c516ea03e863b` |
| `audit_integrity.sha256` | `9f6b26d4bf92471050cdbbb8292e1ef7c9e7a144a809a8b182cead3415da79bb` |
| `evidence/audit_integrity.sha256` | `9f6b26d4bf92471050cdbbb8292e1ef7c9e7a144a809a8b182cead3415da79bb` |
| `enforcement_actions/finalized_manifest/INTEGRITY_SEAL.sha256` | `744f8439a06131f7a9d982cd6305835e2c12bde1dc15e7b3f5b426384311b4ec` |

## 3) Mohave County printer evidence (Node 031332)

Canonical artifact set:

- `mohave-judicial-audit/live_audit_031332.json`
- `mohave-judicial-audit/pre_notice_audit_031332.json`
- `mohave-judicial-audit/post_notice_audit_031332.json`
- `mohave-judicial-audit/evidence_manifest.sha256`

Expected hashes:

- `dd9abb0dff15a502f3a5c25dac40b3f9a62321403001db1d8a27bd8fa4ee2c35` — `live_audit_031332.json`
- `eabc64e61299fc98759974f622bbd6a301cfabe9c067eacdd8a992080c24f9c0` — `pre_notice_audit_031332.json`
- `f108ed9a70a042ffe552ea5c2a13865117b2435f0ebc91292a9609755603d49a` — `post_notice_audit_031332.json`
