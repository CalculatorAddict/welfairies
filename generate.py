import pandas as pd

import re
from collections import defaultdict
from jinja2 import Template
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
# Main PDF generation
# -------------------------

def generate_pdf(csv_path, output_pdf):
    df = pd.read_csv(csv_path)

    # cluster names
    df[last_name_col] = df[last_name_col].str.strip()
    df = df.sort_values(last_name_col)
    df["cluster"] = cluster_names_df(df, first_name_col, last_name_col)

    people = []

    for _, group in df.groupby("cluster"):
        first_name = group[first_name_col].mode()[0]
        last_name = group[last_name_col].mode()[0]
        display_name = format_name(f"{first_name} {last_name}".strip())

        notes = group[note_col].tolist()
        candy_counts = group[snack_col].value_counts().to_dict()

        people.append({
            "name": display_name,
            "notes": notes,
            "candy_counts": candy_counts
        })
    
    template = Template(PAGE_TEMPLATE)
    html_content = template.render(people=people)

    HTML(string=html_content).write_pdf(output_pdf)

# -------------------------
# Command-line entry
# -------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python generate_pdf.py input.csv output.pdf")
        sys.exit(1)

    generate_pdf(sys.argv[1], sys.argv[2])