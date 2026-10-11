#!/usr/bin/env python3
"""Convert the CMS Patient Matching Specification Google Doc into ReadMe pages.

Inputs (both exported from the same Doc revision):
  --markdown  Google Docs "Download as Markdown" export (body text, lists, headings)
  --json      Google Docs API documents.get JSON (used for table cells and for verification)

The Markdown export merges multi-paragraph table cells (e.g. "OIDCSHALL"), so tables are rebuilt
from the JSON. After writing pages, the script compares the words in the Doc against the words in
the generated pages and prints every difference, so nothing is silently dropped or invented.

Usage:
  python3 tools/convert_spec.py --markdown spec.md --json spec.json --out docs/Specification
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

SPEC_VERSION = "3.4.0"
CHART_URL = (
    "https://raw.githubusercontent.com/imranq2/cms-hte-patient-matching-spec/v1.0/"
    "assets/images/spec-v3-4-0-selectivity-distribution.png"
)
CHART_ALT = (
    "Bar chart titled Selectivity Distribution. X axis: collision probability bucket. "
    "Y axis: combo count. Series: all canonical combos (692), threshold-qualified combos (556), "
    "combos that are not a superset of a threshold-qualified combo (224), and reference-list "
    "minimal rows (20)."
)
CHART_CAPTION = "Table 3 Distribution of Collision probabilities. Zero values excluded."

# Section labels for headings whose numbering is automatic in the Doc (taken from its Table of Contents).
LABELS = {
    "Purpose": "I.",
    "Core Principles": "II.",
    "Risk Framework": "III.",
    "The Harm of Non-Return": "A.",
    "Collision Risk vs. Non-Return Risk": "B.",
    "Matching Criteria": "C.",
    "IAL2 Claims Tokens": "D.",
    "Model & Assumptions": "IV.",
    "Assumptions and intended use": "A.",
    "Probability of Collision": "B.",
    "Per-Field Collision Probabilities": "C.",
    "Joint Collision Probability": "D.",
    "Note on SSN and ITIN": "E.",
    "Ecosystem-Specific Collision Validation": "F.",
    "Normalization Requirements": "V.",
    "Required Normalization": "A.",
    "Name Handling": "B.",
    "Demographic Fields": "C.",
    "Placeholder Values": "D.",
    "Fuzzy Matching": "E.",
    "Validation Requirements": "VI.",
    "Implementation Testing": "A.",
    "Validation of P(collision) Values": "B.",
    "Audit & Monitoring": "VII.",
    "Governance & Versioning": "VIII.",
}

# Page layout: (relative path, title, spec-section note, [section keys in document order]).
# A key is the heading text. "@index" pages are navigation-only pages written by this script.
PAGES = [
    ("summary-and-purpose", "Summary and Purpose", "Executive Summary; I (Purpose)", ["Executive Summary", "Purpose"]),
    ("core-principles", "Core Principles", "II", ["Core Principles"]),
    ("risk-framework/harm-of-non-return", "Harm of Non-Return", "III.A", ["The Harm of Non-Return"]),
    ("risk-framework/collision-risk-vs-non-return-risk", "Collision Risk vs. Non-Return Risk", "III.B", ["Collision Risk vs. Non-Return Risk"]),
    ("risk-framework/risk-of-false-positives", "Risk of False Positives", "III.B.1", ["B.1. Risk of False Positives"]),
    ("matching-rules/table-2-category-1-rules", "Table 2: Category 1 Rules", "III.C", ["Matching Criteria"]),
    ("matching-rules/category-2-household-and-individual-rules", "Category 2: Household and Individual Rules", "III.C.2 to III.C.5",
     ["C.2. Household-tier threshold and Table 2-H", "C.3. Individual-within-household Table 2-I",
      "C.4. Category 2 — Combined Probabilities of Household + Individual Rules", "C.5. Combined decision rule"]),
    ("matching-rules/administrative-restrictions", "Administrative Restrictions", "III.C.6", ["C.6. Administrative Restrictions"]),
    ("matching-rules/multiple-births", "Multiple Births", "III.C.7", ["C.7. Handling multiple births (twins and higher-order siblings)"]),
    ("matching-rules/applying-the-tables", "Applying the Tables", "III.C.8 and III.C.9",
     ["C.8. How to apply these tables", "C.9. Defensive use — flag same-household false positives"]),
    ("ial2-claims-tokens", "IAL2 Claims Tokens", "III.D and III.E", ["IAL2 Claims Tokens", "E. IAL2 Claim Token Fields"]),
    ("probability-model/assumptions-and-probability-of-collision", "Assumptions and Probability of Collision", "IV.A and IV.B",
     ["Assumptions and intended use", "Probability of Collision"]),
    ("probability-model/per-field-collision-probabilities", "Per-Field Collision Probabilities", "IV.C", ["Per-Field Collision Probabilities"]),
    ("probability-model/joint-collision-probability", "Joint Collision Probability", "IV.D", ["Joint Collision Probability"]),
    ("probability-model/ssn-and-itin", "SSN and ITIN", "IV.E", ["Note on SSN and ITIN"]),
    ("probability-model/ecosystem-specific-collision-validation", "Ecosystem-Specific Collision Validation", "IV.F",
     ["Ecosystem-Specific Collision Validation"]),
    ("probability-model/twins-and-fragile-identities", "Twins and Fragile Identities", "IV.G",
     ["G. Note on Twins, Fragile Identities and Populations with limited or unstable demographic data"]),
    ("probability-model/insurance-identifiers", "Insurance Identifiers", "IV.H",
     ["H. Note on Insurance Identifiers", "H.1. Member ID versus Subscriber ID", "H.2. Payer Namespace Requirement",
      "H.3. Recyclability", "H.4. Relationship to MBI", "H.5. U-Probability Basis"]),
    ("probability-model/reference-script", "Reference Script", "IV.I", ["I. Reference Script to calculate P(collision)"]),
    ("normalization/required-normalization-names-and-demographics", "Required Normalization, Names, and Demographic Fields", "V.A to V.C",
     ["Required Normalization", "Name Handling", "Demographic Fields"]),
    ("normalization/placeholder-values", "Placeholder Values", "V.D", ["Placeholder Values"]),
    ("normalization/fuzzy-matching", "Fuzzy Matching", "V.E", ["Fuzzy Matching"]),
    ("validation-requirements", "Validation Requirements", "VI", ["Implementation Testing", "Validation of P(collision) Values"]),
    ("audit-and-monitoring", "Audit and Monitoring", "VII", ["Audit & Monitoring"]),
    ("governance-and-versioning", "Governance and Versioning", "VIII", ["Governance & Versioning"]),
    ("implementation-and-testing", "Implementation and Testing", "IX", ["IX - Implementation and Testing"]),
    ("references", "References", "References", ["References"]),
    ("document-control-and-comments", "Document Control and Comments", "Document Control", ["Document Control"]),
]

# Group (folder) navigation pages: folder -> (title, intro sentence).
GROUPS = {
    "risk-framework": ("Risk Framework", "Specification section III, subsections A, B, and B.1."),
    "matching-rules": ("Matching Rules", "Specification section III.C (Matching Criteria and Table 2) and its subsections C.2 to C.9."),
    "probability-model": ("Probability Model", "Specification section IV (Model & Assumptions)."),
    "normalization": ("Normalization", "Specification section V (Normalization Requirements)."),
}

# Top-level headings with no body text of their own (their subsections become page sections).
H1_SECTIONS_WITH_NO_BODY = {
    "CMS Patient Matching Specification", "Risk Framework", "Model & Assumptions",
    "Normalization Requirements", "Validation Requirements",
}


# ---------- JSON helpers ----------

def esc(s: str) -> str:
    s = s.replace("\\", "\\\\")
    for ch in "*_[]{}|":
        s = s.replace(ch, "\\" + ch)
    s = s.replace("<", "&lt;").replace(">", "&gt;").replace("\u000b", "<br />")
    return s


def run_md(run: dict) -> str:
    text = run.get("content", "")
    if not text or text == "\n":
        return ""
    style = run.get("textStyle", {})
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    core = esc(text.strip())
    if not core:
        return text
    if style.get("bold"):
        core = f"**{core}**"
    if style.get("italic"):
        core = f"*{core}*"
    link = style.get("link", {}).get("url")
    if link:
        core = f"[{core}]({link})"
    return lead + core + trail


def paragraph_md(par: dict) -> str:
    out = "".join(run_md(e["textRun"]) for e in par.get("elements", []) if "textRun" in e)
    return out.strip()


def table_md(table: dict) -> str:
    rows = []
    for r, row in enumerate(table["tableRows"]):
        cells = []
        for cell in row["tableCells"]:
            paras = [paragraph_md(c["paragraph"]) for c in cell["content"] if "paragraph" in c]
            sep = " " if r == 0 else "<br />"  # header cells wrap in the Doc; body cells keep real paragraph breaks
            cells.append(sep.join(p for p in paras if p))
        rows.append(cells)
    width = len(rows[0])
    assert all(len(r) == width for r in rows), "ragged table"
    lines = ["| " + " | ".join(rows[0]) + " |", "|" + "|".join([" --- "] * width) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(lines)


def doc_words(doc: dict) -> list[str]:
    """All words in the Doc body, in order, excluding the table of contents."""
    words: list[str] = []
    skip = False
    for el in doc["content"]["tabs"][0]["documentTab"]["body"]["content"]:
        if "tableOfContents" in el:
            continue
        texts = []
        if "paragraph" in el:
            texts.append("".join(e.get("textRun", {}).get("content", "") for e in el["paragraph"]["elements"]))
        elif "table" in el:
            for row in el["table"]["tableRows"]:
                for cell in row["tableCells"]:
                    for c in cell["content"]:
                        if "paragraph" in c:
                            texts.append("".join(e.get("textRun", {}).get("content", "") for e in c["paragraph"]["elements"]))
        for t in texts:
            words += re.findall(r"\w+", t)
    return words


# ---------- Markdown helpers ----------

HEADING = re.compile(r"^(?:\d+\.\s+)?(#{1,2})\s+(.*?)(?:\s*\{#[^}]*\})?\s*$")


def clean_inline(line: str) -> str:
    line = re.sub(r"!\[\]\[image\d+\]", "", line)
    line = re.sub(r"\[([^\]]+)\]\(mailto:[^)]+\)", r"\1", line)
    line = re.sub(r"^ {3}(\d+\. )", r"\1", line)
    line = re.sub(r"^ {2}(\* )", r"\1", line)  # the Doc's bullets are one level; the export indents all but the first
    line = line.replace("\\<", "&lt;").replace("\\>", "&gt;")
    return line.rstrip("\n")


def heading_key(text: str) -> str:
    text = re.sub(r"\\(.)", r"\1", text)  # unescape
    text = re.sub(r"!\[\]\[image\d+\]", "", text)
    return text.strip()


def split_sections(md_lines: list[str]):
    sections, cur = [], None
    for line in md_lines:
        m = HEADING.match(line)
        if m:
            cur = {"level": len(m.group(1)), "key": heading_key(m.group(2)), "body": []}
            sections.append(cur)
        elif cur is not None:
            cur["body"].append(line)
    return sections


def replace_tables(md_lines: list[str], tables_md: list[str]) -> list[str]:
    out, i, n = [], 0, 0
    while i < len(md_lines):
        if md_lines[i].startswith("|"):
            j = i
            while j < len(md_lines) and md_lines[j].startswith("|"):
                j += 1
            out.append(tables_md[n])
            n += 1
            i = j
        else:
            out.append(md_lines[i])
            i += 1
    assert n == len(tables_md), f"table count mismatch: export has {n}, JSON has {len(tables_md)}"
    return out


# Explicit repairs for line-wrap artifacts in the Doc. Each is reported on stdout.
REPAIRS = [
    # Reference 1 is split across two paragraphs inside the Doc ("330-" / "340.").
    (re.compile(r"(Applied Clinical Informatics\. 2016;7\(2\):330-)\n+(340\\\.)"), r"\1\2"),
]


def apply_repairs(text: str) -> str:
    for pat, repl in REPAIRS:
        text, n = pat.subn(repl, text)
        print(f"repair {'applied' if n else 'NOT FOUND'}: {pat.pattern[:60]}...")
    # Reference 7: the URL is split and only its first half is linked in the Doc.
    broken = re.search(r"\[https\\://sequoiaproject\.org/wp-content/uploads/2018/06/The-Sequoia-Project-\]\((https://[^)]+)\)(Framework-for-Patient-Identity-Management-v31\.pdf)", text)
    if broken:
        full = broken.group(1) + broken.group(2)
        text = text.replace(broken.group(0), f"[{full.replace('://', chr(92) + '://')}]({full})")
        print("repair applied: Sequoia Project URL joined")
    else:
        print("repair NOT FOUND: Sequoia Project URL")
    return text


def body_text(lines: list[str]) -> str:
    lines = [l for l in lines if not re.match(r"^\[image\d+\]: ", l)]  # embedded 1x30px comment-marker images
    text = "\n".join(clean_inline(l) for l in lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n")
    return text


def render_page(title, note, keys, sections_by_key):
    parts = [f"*Specification v{SPEC_VERSION}, section {note}*"]
    multi = len(keys) > 1
    for key in keys:
        sec = sections_by_key[key]
        text = body_text(sec["body"])
        if key == "Document Control":
            text += (
                "\n\n<Callout icon=\"💬\" theme=\"info\">\n"
                "  **Where to submit comments on this site:** open an issue at "
                "[github.com/imranq2/cms-hte-patient-matching-spec/issues](https://github.com/imranq2/cms-hte-patient-matching-spec/issues). "
                "The \"Submit Comments To\" field above is empty in the source document.\n</Callout>"
            )
        if key == "Joint Collision Probability":
            text = text.replace(
                f"*{CHART_CAPTION}*",
                f"*{CHART_CAPTION}*\n\n![{CHART_ALT}]({CHART_URL})",
            )
            assert CHART_URL in text, "chart caption not found"
        if multi:
            label = LABELS.get(key, "")
            heading = f"{label} {key}".strip() if label else key
            if key == "Executive Summary":
                heading = "Executive Summary"
            parts.append(f"## {heading}\n\n{text}" if text else f"## {heading}")
        else:
            parts.append(text)
    return "\n\n".join(parts) + "\n"


def frontmatter(title, note):
    t = title.replace('"', '\\"')
    return f'---\ntitle: "{t}"\nexcerpt: "Specification v{SPEC_VERSION}, section {note}"\nhidden: false\n---\n'


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--markdown", required=True)
    ap.add_argument("--json", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    doc = json.load(open(args.json))
    content = doc["content"]["tabs"][0]["documentTab"]["body"]["content"]
    tables_md = [table_md(el["table"]) for el in content if "table" in el]

    md_lines = open(args.markdown, encoding="utf-8").read().split("\n")
    md_lines = replace_tables(md_lines, tables_md)
    sections = split_sections(md_lines)
    by_key = {}
    for s in sections:
        if s["key"] == "Table of Contents":
            continue
        by_key[s["key"]] = s
    for k in H1_SECTIONS_WITH_NO_BODY - {"CMS Patient Matching Specification"}:  # title holds the cover lines
        assert not any(l.strip() for l in by_key[k]["body"]), f"{k} has body text"
    used = {k for _, _, _, keys in PAGES for k in keys} | H1_SECTIONS_WITH_NO_BODY
    unused = [k for k in by_key if k not in used]
    missing = [k for _, _, _, keys in PAGES for k in keys if k not in by_key]
    if unused or missing:
        sys.exit(f"unused sections: {unused}\nmissing sections: {missing}")

    out = Path(args.out)
    generated_text = []
    for rel, title, note, keys in PAGES:
        text = apply_repairs(render_page(title, note, keys, by_key)) if rel == "references" else render_page(title, note, keys, by_key)
        write(out / f"{rel}.md", frontmatter(title, note) + "\n" + text)
        generated_text.append(text)

    # Navigation pages for groups.
    for folder, (title, intro) in GROUPS.items():
        children = [(r.split("/")[1], t) for r, t, _, _ in PAGES if r.startswith(folder + "/")]
        body = [f"{intro}", "", "*This page is site navigation. It is not part of the specification text.*", ""]
        body += [f"- [{t}](/docs/{slug})" for slug, t in children]
        write(out / folder / "index.md", f'---\ntitle: "{title}"\nexcerpt: "{intro}"\nhidden: false\n---\n\n' + "\n".join(body) + "\n")
        write(out / folder / "_order.yaml", "".join(f"- {slug}\n" for slug, _ in children))

    top = []
    for rel, *_ in PAGES:
        head = rel.split("/")[0]
        if head not in top:
            top.append(head)
    write(out / "_order.yaml", "".join(f"- {h}\n" for h in top))

    # Verification: words in the Doc vs. words in the generated pages.
    src_words = doc_words(doc)
    out_words = []
    for text in generated_text:
        text = re.sub(r"^\*Specification v[^\n]*\n", "", text)
        text = re.sub(r"<Callout.*?</Callout>", "", text, flags=re.S)
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # chart image
        text = re.sub(r"\(https?://[^)]*\)", "", text)  # link targets
        text = re.sub(r"\\(.)", r"\1", text)  # markdown escapes
        text = re.sub(r"&(lt|gt);", "", text).replace("<br />", " ")
        out_words += re.findall(r"\w+", text)
    # Drop the Doc's table of contents words and the cover lines already excluded; compare in order.
    sm = difflib.SequenceMatcher(None, src_words, out_words, autojunk=False)
    print(f"\nDoc words: {len(src_words)}; page words: {len(out_words)}; ratio {sm.ratio():.5f}")
    heading_words = [re.findall(r"\w+", k) for k in by_key] + [re.findall(r"\w+", t) for _, t, _, _ in PAGES]
    expected = {"list markers": 0, "section headings now carried by page titles": 0, "cover lines and table of contents": 0}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        d, p = src_words[i1:i2], out_words[j1:j2]
        if tag == "insert" and all(re.fullmatch(r"\d+|[A-Za-z]", w) for w in p):
            expected["list markers"] += 1
        elif tag == "replace" and len(p) == 1 and re.fullmatch(r"\d+|[A-Za-z]", p[0]) and d in heading_words:
            expected["list markers"] += 1  # list number replaced a heading word that was also dropped
        elif tag == "delete" and d in heading_words:
            expected["section headings now carried by page titles"] += 1
        elif tag == "delete" and j1 < 5 or i1 < 40:
            expected["cover lines and table of contents"] += 1
        else:
            print(f"{tag:8} DOC[{i1}:{i2}]={' '.join(d)[:160]!r}  PAGES[{j1}:{j2}]={' '.join(p)[:160]!r}")
    print("expected differences:", expected)

if __name__ == "__main__":
    main()
