import io
import math
import pandas as pd

import re
from collections import defaultdict
from jinja2 import Template
from pypdf import PdfReader, PdfWriter
from weasyprint import HTML
from parameters import *
from template import *

# -------------------------
# Normalization
# -------------------------

def normalize_part(s):
    if not isinstance(s, str):
        return ""
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "", s)
    return s


# -------------------------
# Matching rules
# -------------------------

def part_match(a: str, b: str) -> bool:
    if not a or not b:
        return True  # allow missing part

    if a == b:
        return True

    # initial match
    if len(a) == 1 and a == b[0]:
        return True
    if len(b) == 1 and b == a[0]:
        return True

    # containment
    if a in b or b in a:
        return True

    return False


def names_match(f1, l1, f2, l2):
    return part_match(f1, f2) and part_match(l1, l2)


# -------------------------
# Main clustering function
# -------------------------

def cluster_names_df(df, first_col, last_col):
    n = len(df)

    firsts = [normalize_part(x) for x in df[first_col]]
    lasts = [normalize_part(x) for x in df[last_col]]

    # build adjacency
    adj = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            if names_match(firsts[i], lasts[i], firsts[j], lasts[j]):
                adj[i].append(j)
                adj[j].append(i)

    # connected components → cluster labels
    visited = set()
    labels = [None] * n
    cluster_id = 0

    for i in range(n):
        if i in visited:
            continue

        stack = [i]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            labels[node] = cluster_id
            stack.extend(adj[node])

        cluster_id += 1

    return pd.Series(labels, index=df.index, name="cluster")

def format_name(name: str) -> str:
    name = name.title()
    name = re.sub(r"\bMc([a-z])", lambda m: "Mc" + m.group(1).upper(), name)

    return name


# -------------------------
# Preprocessing
# -------------------------

def preprocess_names(df):
    has_first = FIRST_NAME_COL in df.columns
    has_last = LAST_NAME_COL in df.columns
    if not has_first or not has_last:
        split = df[FULL_NAME_COL].str.strip().str.split(r"\s+", n=1, expand=True)
        df = df.copy()
        df[FIRST_NAME_COL] = split[0].fillna("")
        df[LAST_NAME_COL] = split[1].fillna("")
    return df


def classify_snack(value):
    if not isinstance(value, str):
        return None
    v = value.lower()
    if any(w.lower() in v for w in CHOCOLATE_WORDS):
        return "C"
    if any(w.lower() in v for w in STARBURST_WORDS):
        return "S"
    return None


# -------------------------
# Main PDF generation
# -------------------------

def generate_pdf(csv_path, output_pdf, term_name, welsh_phrase):
    df = pd.read_csv(csv_path)

    df = preprocess_names(df)
    df["snack_label"] = df[SNACK_COL].apply(classify_snack)

    # cluster names
    df[LAST_NAME_COL] = df[LAST_NAME_COL].str.strip()
    df = df.sort_values(LAST_NAME_COL)
    df["cluster"] = cluster_names_df(df, FIRST_NAME_COL, LAST_NAME_COL)

    people = []

    for _, group in df.groupby("cluster", sort=False):
        first_name = group[FIRST_NAME_COL].mode()[0]
        last_name = group[LAST_NAME_COL].mode()[0]
        display_name = format_name(f"{first_name} {last_name}".strip())

        notes = group[NOTE_COL].tolist()
        snack_c = int((group["snack_label"] == "C").sum())
        snack_s = int((group["snack_label"] == "S").sum())

        people.append({
            "name": display_name,
            "last_name": last_name,
            "notes": notes,
            "snack_c": snack_c,
            "snack_s": snack_s,
        })

    people.sort(key=lambda p: normalize_part(p["last_name"]))

    template = Template(PAGE_TEMPLATE)
    html_content = template.render(people=people, term_name=term_name, welsh_phrase=welsh_phrase)

    buf = io.BytesIO()
    HTML(string=html_content).write_pdf(buf)

    buf.seek(0)
    reader = PdfReader(buf)
    writer = PdfWriter()

    n = len(reader.pages)
    s = math.ceil(n / 4)  # sheets needed
    order = [pos * s + sheet 
        for sheet in range(s) 
        for pos in range(4) 
        if pos * s + sheet < n]
    
    for i in order:
        writer.add_page(reader.pages[i])

    with open(output_pdf, "wb") as f:
        writer.write(f)

# -------------------------
# Command-line entry
# -------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) not in (3, 5):
        print("Usage: python generate.py input.csv output.pdf [term_name welsh_phrase]")
        sys.exit(1)

    term = sys.argv[3] if len(sys.argv) == 5 else TERM_NAME
    welsh = sys.argv[4] if len(sys.argv) == 5 else WELSH_PHRASE
    generate_pdf(sys.argv[1], sys.argv[2], term, welsh)