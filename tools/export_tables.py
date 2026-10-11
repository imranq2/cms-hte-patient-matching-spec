#!/usr/bin/env python3
"""Export the specification's matching tables as CSV and JSON.

Reads the same Google Docs API JSON that tools/convert_spec.py uses, so the files are generated
from the Doc, not retyped. Cell text is exactly what the Doc contains (formatting removed;
multiple paragraphs in one cell are joined with a space).

Usage (from the repository root):
  python3 tools/export_tables.py --json spec.json --out assets/data
"""
import argparse
import csv
import json
from pathlib import Path

SPEC_VERSION = "3.4.0"

# Position in the Doc's table order -> (file stem, title as printed or described in the Doc).
TABLES = {
    1: ("table-2-category-1", "Table 2: Approved matching combinations and conservative collision estimates (Category 1)"),
    2: ("table-2h-household", "Table 2-H: Household-tier threshold"),
    3: ("table-2i-individual", "Table 2-I: Individual within household"),
    4: ("category-2-combined", "Category 2: Combined probabilities of Household + Individual rules (section III.C.4)"),
    5: ("administrative-restrictions", "Administrative restrictions (section III.C.6)"),
    7: ("table-3-per-field-u", "Table 3: Conservative per-field u-probabilities"),
    8: ("table-4-sample-restrictions", "Table 4: Sample administrative restrictions on matching combinations"),
}


# Expected first header cell of each table, so that a table added to or removed from the Doc fails
# loudly instead of exporting the wrong table under a good name.
EXPECTED_HEADER = {1: "ID", 2: "ID", 3: "ID", 4: "Household leg", 5: "Candidate combination", 7: "Field", 8: "Candidate combination"}


def cell_text(cell: dict) -> str:
    parts = []
    for c in cell["content"]:
        if "paragraph" in c:
            t = "".join(e.get("textRun", {}).get("content", "") for e in c["paragraph"]["elements"])
            t = t.replace("\u000b", " ").strip()
            if t:
                parts.append(t)
    return " ".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    doc = json.load(open(args.json))
    revision = doc["content"]["revisionId"]
    tables = [el["table"] for el in doc["content"]["tabs"][0]["documentTab"]["body"]["content"] if "table" in el]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for pos, (stem, title) in TABLES.items():
        rows = [[cell_text(c) for c in r["tableCells"]] for r in tables[pos]["tableRows"]]
        header, body = rows[0], rows[1:]
        if header[0] != EXPECTED_HEADER[pos]:
            raise SystemExit(f"table {pos} header is {header[0]!r}, expected {EXPECTED_HEADER[pos]!r}: the Doc's table order changed")
        base = f"spec-v{SPEC_VERSION.replace('.', '-')}-{stem}"
        with open(out / f"{base}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(body)
        records = [dict(zip(header, r)) for r in body]
        payload = {
            "specification_version": SPEC_VERSION,
            "source_document_revision": revision,
            "table": title,
            "columns": header,
            "rows": records,
        }
        (out / f"{base}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        index.append((title, base, len(body)))
        print(f"{base}: {len(body)} rows")
    return None


if __name__ == "__main__":
    main()
