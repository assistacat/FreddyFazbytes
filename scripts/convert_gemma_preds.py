#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys, os

IN = sys.argv[1] if len(sys.argv) > 1 else "data/gemma_preds.csv"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/eval/gemma_preds_norm.csv"

df = pd.read_csv(IN)

# required cols
cols = ["val_pred","ad_pred","irrelevant_pred","rant_pred"]
missing = [c for c in ["review"] + cols if c not in df.columns]
if missing:
    raise SystemExit(f"Missing columns: {missing}")

# build matrix and choose predicted class
mat = df[cols].fillna(0).to_numpy(dtype=float)

# tie-breaking priority (more conservative first): Ad > Rant > Irr > Val
# implement by adding tiny priorities
prio = np.array([0.0, 3e-6, 2e-6, 1e-6])  # aligns with cols order below
# BUT our cols order is [val, ad, irrelevant, rant]
# so reorder priorities to match that order:
prio = np.array([1e-6, 3e-6, 2e-6, 1e-6])

idx = np.argmax(mat + prio, axis=1)

# map index -> label for our column order
idx2label = {0:"Val", 1:"Ad", 2:"Irr", 3:"Rant"}
pred = [idx2label[i] for i in idx]

out = pd.DataFrame({
    "clean_text": df["review"],
    "pred": pred
})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.to_csv(OUT, index=False)
print(f"Wrote {len(out)} rows → {OUT}")
