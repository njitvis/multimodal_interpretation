"""
fig   = fig(?:s|ure|ures)?\.?          # Fig / Figs / Figure / Figures, optional dot
sep   = [\s ]*                          # spaces incl. non-breaking space
esc   = re.escape(<number>)             # the literal caption number, dashes normalised
right = (?!\d)(?![.\-]\d)(?![A-Za-z]{2})   # right-boundary guard


Non-box pattern: \b{fig}{sep}{esc}{right}
Box pattern: (?:cross[-\s]chapter\s+)?box{sep}{bnum}\s*,?\s*{fig}{sep}{esc}{right}

The right boundary is the precision-critical part. It prevents false matches by forbidding:
    - a following digit → 5.2 won't match inside 5.21
    - a following separator+digit → 5.2 won't match 5.2.1 or 5.2-1
    - two or more trailing letters → 5 won't match 5th, while a single panel letter (5.2a, 5b) is still allowed.
"""

import os
import re
import ast
import sys
import pandas as pd
import fitz  # PyMuPDF

# Silence non-fatal MuPDF object warnings (e.g. recoverable zlib errors) so the
# progress log stays readable; text extraction still succeeds.
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass


# --------------------------------------------------------------------------- #
# Paths                                                                        #
# --------------------------------------------------------------------------- #
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF_DIR = os.path.join(ROOT, "PDFs")
IN_XLSX = os.path.join(HERE, "chart_caption_context_203.xlsx")
OUT_XLSX = os.path.join(HERE, "chart_caption_context_203_refmatched.xlsx")

# Abbreviations whose trailing period must NOT end a sentence.
ABBR = {
    "fig", "figs", "figure", "no", "nos", "vs", "cf", "al", "eq", "eqs", "ref",
    "refs", "sec", "secs", "ch", "chap", "pp", "p", "dr", "mr", "mrs", "ms",
    "prof", "st", "approx", "ca", "vol", "tab", "tabs", "etc", "col", "min",
    "max", "est", "incl", "co", "inc", "ltd", "dept", "univ", "natl", "intl",
    "ave", "ed", "eds", "pers", "comm", "spp", "var", "temp", "conc",
}

# Any unicode dash -> normalised to ascii '-'.
_DASHES = "‐‑‒–—―−"


# --------------------------------------------------------------------------- #
# Caption -> canonical figure id                                              #
# --------------------------------------------------------------------------- #
def parse_figure_id(caption):
    """Return (number, box) parsed from the start of a caption.

    number : e.g. "9.8", "10-1", "5", "2.25"   (separators preserved)
    box    : box number for "Cross-Chapter Box N, Figure M" captions, else None.
    Returns (None, None) if no figure id can be parsed.
    """
    c = re.sub(r"\s+", " ", str(caption)).strip()

    # Special: "Cross-Chapter Box 12, Figure 1 | ..."
    m = re.match(
        r"^(?:cross[-\s]chapter\s+)?box\s*([0-9]+(?:[.\-][0-9]+)*)\s*,?\s*"
        r"fig(?:ure)?\.?\s*([0-9]+(?:[.\-][0-9]+)*)",
        c, re.IGNORECASE,
    )
    if m:
        return m.group(2), m.group(1)

    # Standard: "Figure 9.8", "Fig. 10-1", "Figure 5", ...
    m = re.match(
        r"^fig(?:ure)?\.?\s*([0-9]+(?:[.\-][0-9]+)*)",
        c, re.IGNORECASE,
    )
    if m:
        return m.group(1), None

    return None, None


def build_ref_regex(number, box=None):
    """Strict regex matching references to exactly this figure in prose.

    Right boundary forbids:
      - a following digit          (5.2  vs  5.21)
      - a following sep+digit      (5.2  vs  5.2.1 / 5.2-1)
      - two+ trailing letters      (5    vs  "5th"); a single panel letter
                                    (5.2a, 5b) is allowed.
    """
    num = number
    for d in _DASHES:
        num = num.replace(d, "-")
    # match either '.' or '-' separators interchangeably is NOT desired; keep
    # the caption's separators literal so dot/dash styles never conflate.
    esc = re.escape(num)
    fig = r"fig(?:s|ure|ures)?\.?"
    sep = r"[\s ]*"
    right = r"(?!\d)(?![.\-]\d)(?![A-Za-z]{2})"
    if box:
        bnum = box
        for d in _DASHES:
            bnum = bnum.replace(d, "-")
        pat = (
            rf"(?:cross[-\s]chapter\s+)?box{sep}{re.escape(bnum)}\s*,?\s*"
            rf"{fig}{sep}{esc}{right}"
        )
    else:
        pat = rf"\b{fig}{sep}{esc}{right}"
    return re.compile(pat, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# PDF text -> sentences                                                        #
# --------------------------------------------------------------------------- #
def clean_text(text):
    """De-hyphenate line breaks, normalise dashes/spaces, flatten newlines."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # join split words
    for d in _DASHES:
        text = text.replace(d, "-")
    text = text.replace(" ", " ")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


_PH = "\x00"  # placeholder for protected (non-terminal) periods


def split_sentences(text):
    """Sentence splitter tuned for scientific prose (decimals, abbreviations)."""
    t = text
    # protect decimals: 5.2, 0.05
    t = re.sub(r"(\d)\.(\d)", r"\1" + _PH + r"\2", t)
    # protect single capital initials: "B. Netz"
    t = re.sub(r"\b([A-Z])\.", r"\1" + _PH, t)
    # protect known abbreviations
    def _prot(m):
        w = m.group(0)
        return (w[:-1] + _PH) if w[:-1].lower() in ABBR else w
    t = re.sub(r"\b[A-Za-z]{1,6}\.", _prot, t)
    # multi-dot abbreviations e.g. / i.e.
    t = t.replace("e.g" + _PH, "e" + _PH + "g" + _PH)
    t = t.replace("i.e" + _PH, "i" + _PH + "e" + _PH)
    # split on sentence terminator + space + capital/number/opener (incl. { [ )
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\[{\"'])", t)
    return [p.replace(_PH, ".").strip() for p in parts if p.strip()]


# run of >=4 bare numbers/ranges separated only by whitespace == axis-tick dump
# (a token may be a plain number or a hyphenated range like "1980-90")
_NUMTOK = r"-?\d[\d.,]*(?:-\d[\d.,]*)?"
_NUM_RUN = re.compile(rf"(?<![\w.]){_NUMTOK}(?:\s+{_NUMTOK}){{3,}}")


def strip_number_runs(text):
    """Remove embedded axis-tick number runs from an otherwise-prose sentence."""
    text = _NUM_RUN.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------------- #
# Sentence quality filters                                                     #
# --------------------------------------------------------------------------- #
def _norm(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())


def is_chart_noise(sentence):
    """True for figure-region text dominated by axis tick numbers.

    Distinguishes axis dumps ("-600 -400 -200 0 200 400 ...") from genuinely
    data-rich prose ("increased over 1984-2011 in 7 of 10 regions") by looking
    for a RUN of >=4 bare numbers separated only by whitespace, rather than the
    raw number count (which wrongly flags quantitative sentences).
    """
    if _NUM_RUN.search(sentence):
        return True
    # backstop: extreme numeric density with almost no prose
    nums = re.findall(r"(?<![A-Za-z])-?\d+(?:\.\d+)?(?![A-Za-z])", sentence)
    words = re.findall(r"[A-Za-z]{2,}", sentence)
    return len(nums) >= 12 and len(nums) > len(words)


def is_prose(sentence):
    """Require a few real word tokens so fragments/labels are dropped."""
    words = re.findall(r"[A-Za-z]{2,}", sentence)
    return len(words) >= 4


# Attribution / licensing / reprint credit lines that ride along with figure
# regions but are not descriptive prose (e.g. "Reprinted with permission from
# Elsevier Ltd.", "Data Source: IEA data", "© 2014 IPCC").
_ATTRIB_RX = re.compile(
    r"""(?:
          \breprinted\b
        | \breproduced\b
        | \bredrawn\b
        | \b(?:adapted|modified|derived)\s+from\b
        | \bwith\s+permission\b
        | \bby\s+permission\b
        | \bpermission\s+(?:of|from|to)\b
        | \ball\s+rights\s+reserved\b
        | \bcopyright\b
        | ©                         # © sign
        | \(c\)\s*\d{4}
        | \bcc[\s-]by\b                  # Creative Commons
        | \bcourtesy\s+of\b
        | \b(?:photo|image|figure|map|data)\s+credits?\b
        | \bcredits?\s*:
        | \b(?:data\s+)?sources?\s*:     # "Source:" / "Data Source:"
        | \bdoi:\s*\S+
        | cambridge\s+university\s+press
    )""",
    re.IGNORECASE | re.VERBOSE,
)


def is_attribution(sentence):
    """True for source/credit/licensing/reprint lines that should be excluded."""
    return bool(_ATTRIB_RX.search(sentence))


def is_own_caption(sentence, caption):
    """Drop only the figure's own caption LINE (i.e. a 'sentence' that begins
    with the caption text). Body sentences that merely got merged with caption
    text on their tail are kept, so real references are not lost."""
    cap_key = _norm(caption)[:30]
    return bool(cap_key) and _norm(sentence).startswith(cap_key)


# --------------------------------------------------------------------------- #
# Table exclusion                                                              #
# --------------------------------------------------------------------------- #
# Fraction of a text block that must fall inside a detected table region for
# the block to be treated as table content and dropped.
_TABLE_OVERLAP = 0.5


def _rect_overlap_ratio(inner, outer):
    """Fraction of `inner`'s area that lies within `outer` (0..1)."""
    area = inner.get_area()
    if area <= 0:
        return 0.0
    inter = fitz.Rect(inner)
    inter.intersect(outer)
    ia = inter.get_area()
    return (ia / area) if ia > 0 else 0.0


def _page_text_excluding_tables(page):
    """Page text with detected data-table regions removed.

    Tables (rows of numbers, header cells, units) reference the figure region
    but are not descriptive prose, so they pollute the caption context. We use
    PyMuPDF's table finder to locate table bounding boxes and drop any text
    block that lies mostly inside one; everything else is returned verbatim.
    """
    try:
        table_rects = [fitz.Rect(t.bbox) for t in page.find_tables().tables]
    except Exception:
        table_rects = []          # old PyMuPDF or detection failure -> keep all
    if not table_rects:
        return page.get_text()

    kept = []
    for block in page.get_text("blocks"):
        brect = fitz.Rect(block[:4])
        if any(_rect_overlap_ratio(brect, tr) >= _TABLE_OVERLAP
               for tr in table_rects):
            continue              # block sits inside a table -> exclude it
        kept.append(block[4])
    return "\n".join(kept)


# --------------------------------------------------------------------------- #
# Per-source text cache                                                        #
# --------------------------------------------------------------------------- #
_sentence_cache = {}


def get_sentences(source):
    if source in _sentence_cache:
        return _sentence_cache[source]
    path = os.path.join(PDF_DIR, source)
    if not os.path.exists(path):
        _sentence_cache[source] = None
        return None
    doc = fitz.open(path)
    raw = "\n".join(_page_text_excluding_tables(page) for page in doc)
    doc.close()
    sents = split_sentences(clean_text(raw))
    _sentence_cache[source] = sents
    return sents


def extract_context(source, caption):
    number, box = parse_figure_id(caption)
    if number is None:
        return None, []  # could not parse a figure id

    sents = get_sentences(source)
    if sents is None:
        return number if box is None else f"Box {box}, Fig {number}", None  # missing PDF

    rx = build_ref_regex(number, box)
    seen, hits = set(), []
    for s in sents:
        if not rx.search(s):
            continue
        if is_own_caption(s, caption):
            continue                      # the figure's own caption line
        if is_attribution(s):
            continue                      # source/credit/reprint/licensing line
        # strip any axis-tick run that merged onto this sentence, then re-check
        # that a genuine reference + prose survives (so the instance is kept).
        cleaned = strip_number_runs(s)
        if not rx.search(cleaned) or not is_prose(cleaned) or is_chart_noise(cleaned):
            continue
        key = _norm(cleaned)
        if key in seen:
            continue
        seen.add(key)
        hits.append(cleaned)

    fig_id = number if box is None else f"Box {box}, Figure {number}"
    return fig_id, hits


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #
def main():
    df = pd.read_excel(IN_XLSX)
    if "context" in df.columns:
        df = df.rename(columns={"context": "context_old"})

    figure_ids, contexts, counts = [], [], []
    missing_pdfs, no_id, zero_hits = [], [], []

    for idx, row in df.iterrows():
        source = str(row["PDF link (source)"]).strip()
        caption = row["caption"]
        fig_id, hits = extract_context(source, caption)

        figure_ids.append(fig_id if fig_id is not None else "")
        if fig_id is None:
            no_id.append((idx, str(caption)[:60]))
            contexts.append("[]")
            counts.append(0)
        elif hits is None:
            missing_pdfs.append((idx, source))
            contexts.append("")
            counts.append(-1)  # PDF not found
        else:
            contexts.append(repr(hits))  # stringified python list (round-trips)
            counts.append(len(hits))
            if not hits:
                zero_hits.append((idx, fig_id, source))
        print(f"[{idx+1:3}/{len(df)}] {source[:32]:32} fig={str(fig_id)[:10]:10} "
              f"-> {counts[-1]} sentence(s)")

    df["figure_id"] = figure_ids
    df["context"] = contexts
    df["n_context"] = counts

    # tidy column order: keep originals, place new context near the old one
    df.to_excel(OUT_XLSX, index=False)

    print("\n" + "=" * 60)
    print(f"Wrote {OUT_XLSX}")
    print(f"Rows: {len(df)}")
    print(f"  with >=1 context sentence : {sum(1 for c in counts if c > 0)}")
    print(f"  zero context (parsed, none found) : {len(zero_hits)}")
    print(f"  caption id unparsed       : {len(no_id)}")
    print(f"  missing PDF               : {len(missing_pdfs)}")
    if no_id:
        print("  -- unparsed captions --")
        for i, c in no_id:
            print(f"     row {i}: {c}")
    if missing_pdfs:
        print("  -- missing PDFs --")
        for i, s in missing_pdfs:
            print(f"     row {i}: {s}")


if __name__ == "__main__":
    main()
