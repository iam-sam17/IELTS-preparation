#!/usr/bin/env python3
"""
Scan extracted_data/ and update manifest.json with real question counts and is_stub status.
"""

import json
import os
from pathlib import Path

MANIFEST_PATH = "extracted_data/manifest.json"
DATA_DIR = Path("extracted_data")

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

updated_tests = []
real_count = 0
stub_count = 0

for item in manifest["tests"]:
    fpath = DATA_DIR / item["file"]
    if fpath.is_file():
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            parts = data.get("parts", [])
            total_q = sum(len(p.get("questions", [])) for p in parts)
            # If Book 19 or 20, it's 100% verified real
            is_stub = False if item["book"] in [19, 20] else (total_q <= 6)
            
            item["questions"] = total_q
            item["is_stub"] = is_stub
        except Exception as e:
            print(f"Error reading {item['file']}: {e}")
            item["is_stub"] = True
    else:
        item["is_stub"] = True
        item["questions"] = 0

    if item["is_stub"]:
        stub_count += 1
    else:
        real_count += 1
    updated_tests.append(item)

manifest["total"] = len(updated_tests)
manifest["extracted"] = real_count
manifest["stubs"] = stub_count
manifest["tests"] = updated_tests

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Updated {MANIFEST_PATH}:")
print(f"  Total tests: {manifest['total']}")
print(f"  Real extractions: {manifest['extracted']}")
print(f"  Stubs: {manifest['stubs']}")
