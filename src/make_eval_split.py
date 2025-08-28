#!/usr/bin/env python3
import argparse, json, os
import pandas as pd
import numpy as np

def parse_rating(s):
    try:
        d = json.loads(s)
        return int(d.get("rating")) if "rating" in d else None
    except Exception:
        return None

def length_bucket(n):
    # tweak thresholds if you want
    if n < 50:
        return "short"
    if n <= 200:
        return "medium"
    return "long"

def main():
    ap = argparse.ArgumentParser()
    # UK spelling by default
    ap.add_argument("--gold", default="data/labelled_subset.csv")
    ap.add_argument("--out", default="data/eval/balanced_eval.csv")
    ap.add_argument("--n", type=int, default=120, help="target eval size")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    # robust CSV read (handles commas inside quotes; skips malformed lines)
    df = pd.read_csv(args.gold, quotechar='"', escapechar='\\', on_bad_lines='skip')
    assert "clean_text" in df.columns, "missing clean_text"
    assert ("category" in df.columns) or ("true_label" in df.columns), "need category or true_label"

    df["gold"] = df["category"] if "category" in df.columns else df["true_label"]

    # derive features for balancing
    df["rating_num"] = df["metadata"].apply(parse_rating)
    df["length"] = df["clean_text"].astype(str).str.split().apply(len)
    df["len_bucket"] = df["length"].apply(length_bucket)

    def star_bucket(r):
        if r in [1, 2]:
            return "low"
        if r == 3:
            return "mid"
        if r in [4, 5]:
            return "high"
        return "unk"

    df["star_bucket"] = df["rating_num"].apply(star_bucket)

    # round-robin sample across star_bucket × len_bucket
    grid = df.groupby(["star_bucket", "len_bucket"])
    buckets = list(grid.groups.keys())

    np.random.seed(args.seed)
    take_per_round = 1
    picked_idx = []

    while len(picked_idx) < args.n:
        any_added = False
        for key in buckets:
            sub = df.loc[grid.groups[key]]
            remaining = sub.index.difference(picked_idx)
            if len(remaining) == 0:
                continue
            choice = np.random.choice(remaining, size=min(take_per_round, len(remaining)), replace=False)
            picked_idx.extend(choice.tolist())
            any_added = True
            if len(picked_idx) >= args.n:
                break
        if not any_added:
            break

    eval_df = df.loc[picked_idx].copy().reset_index(drop=True)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    eval_df[["clean_text", "metadata", "gold", "rating_num", "length", "len_bucket", "star_bucket"]].to_csv(
        args.out, index=False
    )
    print(f"Wrote {len(eval_df)} rows to {args.out}")
    print(eval_df[["star_bucket", "len_bucket"]].value_counts().sort_index())
    print("Tip: share this CSV with P3 to standardize which rows get scored.")

if __name__ == "__main__":
    main()
