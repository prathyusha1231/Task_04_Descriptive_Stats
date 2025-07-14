import csv
import math
from collections import Counter, defaultdict


FILES = [
    "period_03/2024_fb_posts_president_scored_anon.csv",
    "period_03/2024_fb_ads_president_scored_anon.csv",
    "period_03/2024_tw_posts_president_scored_anon.csv",
]

PAGE_GROUP_LIMIT = 5
PAIR_GROUP_LIMIT = 5

def is_number(s: str):
    try:
        float(s)
        return True
    except:
        return False

def summarize(header, rows, title):
    print(f"\n--- Stats: {title} ---")
    n_cols = len(header)
    
    num_vals = [[] for _ in header]
    nonnum_counters = [Counter() for _ in header]

    for row in rows:
        for i, cell in enumerate(row):
            clean = cell.strip().replace(",", "")
            if clean == "":
                continue
            if is_number(clean):
                num_vals[i].append(float(clean))
            else:
                nonnum_counters[i][cell] += 1

    
    for i, name in enumerate(header):
        vals = num_vals[i]
        if not vals:
            continue
        cnt = len(vals)
        mean = sum(vals) / cnt
        mn = min(vals)
        mx = max(vals)
        
        std = math.sqrt(sum((x - mean) ** 2 for x in vals) / (cnt - 1)) if cnt > 1 else 0.0
        print(f"{name:30s}"
              f"count={cnt:6d}"
              f"  mean={mean:10.2f}"
              f"  min={mn:10.2f}"
              f"  max={mx:10.2f}"
              f"  std={std:10.2f}")

    
    for i, name in enumerate(header):
        ctr = nonnum_counters[i]
        if not ctr:
            continue
        unique = len(ctr)
        top5 = ctr.most_common(5)
        print(f"{name:30s} unique={unique:6d} top5={top5}")

def group_and_summarize(header, rows, group_cols, limit, title):
    
    idxs = [header.index(col) for col in group_cols if col in header]
    if len(idxs) != len(group_cols):
        return  

    
    groups = defaultdict(list)
    for row in rows:
        key = tuple(row[i] for i in idxs)
        groups[key].append(row)

    print(f"\n=== Grouped by {group_cols} (first {limit} groups) ===")
    for i, (key, grp_rows) in enumerate(groups.items()):
        if i >= limit:
            print("... truncated ...")
            break
        print(f"\n-- {dict(zip(group_cols, key))} --")
        summarize(header, grp_rows, title=f"{title} {dict(zip(group_cols, key))}")

if __name__ == "__main__":
    for path in FILES:
        print(f"\n===== PROCESSING FILE: {path} =====")
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)

        # overall
        summarize(header, rows, "Overall Dataset")

        # by page_id
        group_and_summarize(header, rows, ["page_id"], PAGE_GROUP_LIMIT, "Page Group")

        # by (page_id, ad_id)
        group_and_summarize(header, rows, ["page_id", "ad_id"], PAIR_GROUP_LIMIT,
                            "Page & Ad Group")
