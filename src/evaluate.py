#!/usr/bin/env python3
import argparse, os, sys, json
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import matplotlib.pyplot as plt

# canonical label sets
FOUR_CLASSES = ["Ad", "Irr", "Rant", "Val"]
BINARY_CLASSES = ["Ad", "Non-Ad"]

def norm_4(label):
    if not isinstance(label, str): return None
    t = label.strip().lower()
    if t in {"ad","ads","advert","advertisement"}: return "Ad"
    if t in {"irr","irrelevant","not relevant","offtopic"}: return "Irr"
    if t in {"rant","angry","complaint-no-visit"}: return "Rant"
    if t in {"val","valid","relevant","clean"}: return "Val"
    return None

def norm_bin(label):
    if not isinstance(label, str): return None
    t = label.strip().lower().replace(" ", "")
    if t in {"ad","ads"}: return "Ad"
    if t in {"non-ad","nonad","notad","other"}: return "Non-Ad"
    # collapse 4-class to binary
    four = norm_4(label)
    if four is None: return None
    return "Ad" if four == "Ad" else "Non-Ad"

def collapse_gold_to_bin(y):
    return ["Ad" if norm_4(v) == "Ad" else "Non-Ad" for v in y]

def plot_cm(cm, labels, title, outpath):
    fig = plt.figure(figsize=(5,4))
    plt.imshow(cm, interpolation='nearest', cmap="Blues")
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45, ha="right")
    plt.yticks(tick_marks, labels)
    thresh = cm.max() / 2.0 if cm.size else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i,j] > thresh else "black")
    plt.ylabel("True")
    plt.xlabel("Predicted")
    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)

def load_gold(path):
    df = pd.read_csv(path)
    if "category" in df.columns:
        y = df["category"].tolist()
    elif "true_label" in df.columns:
        y = df["true_label"].tolist()
    else:
        raise ValueError("Gold file needs a 'category' or 'true_label' column.")
    y_norm = [norm_4(v) for v in y]
    return df, y_norm

def evaluate_run(gold_df, gold_4, pred_path, run_name, results_dir="results", mode=None):
    pred_df = pd.read_csv(pred_path)
    if "clean_text" not in pred_df.columns or "pred" not in pred_df.columns:
        raise ValueError(f"{pred_path} must have columns: clean_text, pred")

    merged = pd.merge(
        gold_df[["clean_text"]].assign(_row=np.arange(len(gold_df))),
        pred_df[["clean_text","pred"]],
        on="clean_text",
        how="left"
    ).sort_values("_row")
    y_pred_raw = merged["pred"].tolist()

    # --- choose mode ---
    if mode in {"binary", "multiclass"}:
        chosen_mode = mode
    else:
        sample = [p for p in y_pred_raw if isinstance(p, str)][:20]
        bin_like  = sum(1 for s in sample if norm_bin(s) in BINARY_CLASSES)
        four_like = sum(1 for s in sample if norm_4(s)  in FOUR_CLASSES)
        chosen_mode = "binary" if bin_like >= four_like else "multiclass"

    if chosen_mode == "multiclass":
        y_true = gold_4
        y_pred = [norm_4(v) for v in y_pred_raw]
        labels = FOUR_CLASSES
    else:
        y_true = collapse_gold_to_bin(gold_4)
        y_pred = [norm_bin(v) for v in y_pred_raw]
        labels = BINARY_CLASSES

    mask = [(yt is not None) and (yp is not None) for yt, yp in zip(y_true, y_pred)]
    y_true_f = [yt for yt, m in zip(y_true, mask) if m]
    y_pred_f = [yp for yp, m in zip(y_pred, mask) if m]

    p,r,f1,_ = precision_recall_fscore_support(
        y_true_f, y_pred_f, labels=labels, average="macro", zero_division=0
    )
    report = classification_report(y_true_f, y_pred_f, labels=labels, digits=3, zero_division=0)

    cm = confusion_matrix(y_true_f, y_pred_f, labels=labels)
    # include mode in filename so we don’t overwrite
    cm_path = os.path.join(results_dir, f"confusion_{run_name}_{chosen_mode}.png")
    plot_cm(cm, labels, f"{run_name} ({chosen_mode})", cm_path)

    summary = []
    summary.append(f"=== {run_name} ===")
    summary.append(f"Mode: {chosen_mode}")
    summary.append(f"Macro Precision: {p:.3f} Recall: {r:.3f} F1: {f1:.3f}")
    summary.append("\nPer-class report:\n" + report)
    summary.append(f"Confusion matrix image: {cm_path}")
    return "\n".join(summary)

def main():
    ap = argparse.ArgumentParser(description="Evaluate predictions against labelled_subset.csv")
    ap.add_argument("--gold", default="data/labelled_subset.csv", help="Path to gold CSV.")
    ap.add_argument("--pred", nargs="+", required=True, help="Prediction CSV(s).")
    ap.add_argument("--names", nargs="+", help="Optional run names.")
    ap.add_argument("--out", default="results/metrics.txt", help="Summary output file.")
    ap.add_argument("--mode", choices=["binary","multiclass"], help="Force evaluation mode.")
    args = ap.parse_args()

    gold_df, gold_4 = load_gold(args.gold)

    if args.names and len(args.names)!=len(args.pred):
        print("If provided, --names must match number of --pred files", file=sys.stderr)
        sys.exit(2)

    summaries = []
    for i,pth in enumerate(args.pred):
        run_name = args.names[i] if args.names else os.path.splitext(os.path.basename(pth))[0]
        print(f"Evaluating {run_name} ...")
        summaries.append(evaluate_run(gold_df, gold_4, pth, run_name, results_dir="results", mode=args.mode))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out,"w",encoding="utf-8") as f:
        f.write("\n\n".join(summaries))
    print(f"Wrote metrics to {args.out}")
    
if __name__ == "__main__":
    main()   
