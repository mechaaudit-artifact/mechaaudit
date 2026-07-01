#!/usr/bin/env python3
"""
Compute contract-level detection metrics from MechaAudit results.

Usage:
    python scripts/eval_metrics.py \
        --results results/main/mechaaudit_metrics.json \
        --benchmark benchmark/manifest.jsonl

Or for a custom results JSONL:
    python scripts/eval_metrics.py \
        --predictions my_results.jsonl \
        --benchmark benchmark/manifest.jsonl \
        --output my_metrics.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_benchmark_labels(manifest_path: Path) -> Dict[str, str]:
    """Load ground-truth labels from benchmark manifest."""
    labels = {}
    with open(manifest_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            case_id = entry.get("case_id", "")
            label = entry.get("label", "")
            if case_id and label:
                labels[case_id] = label
    return labels


def compute_contract_metrics(
    predictions: Dict[str, str],
    labels: Dict[str, str],
) -> Dict:
    """Compute TP/FP/FN/TN and derived metrics.

    Args:
        predictions: {case_id: "VULN" or "SAFE"}
        labels:      {case_id: "VULN" or "SAFE"}

    Returns:
        Metrics dict with tp, fp, fn, tn, precision, recall, fpr, f1.
    """
    tp = fp = fn = tn = 0
    for case_id, gt in labels.items():
        pred = predictions.get(case_id, "SAFE")
        if gt == "VULN" and pred == "VULN":
            tp += 1
        elif gt == "SAFE" and pred == "VULN":
            fp += 1
        elif gt == "VULN" and pred == "SAFE":
            fn += 1
        elif gt == "SAFE" and pred == "SAFE":
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "fpr": round(fpr, 4),
        "f1": round(f1, 4),
    }


def load_predictions_from_jsonl(predictions_path: Path) -> Dict[str, str]:
    """Load predictions from a JSONL file.

    Each line must have: {"case_id": "...", "verdict": "VULN" or "SAFE"}
    """
    predictions = {}
    with open(predictions_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            case_id = row.get("case_id", "")
            verdict = row.get("verdict", "SAFE")
            if case_id:
                if verdict == "VULN":
                    predictions[case_id] = "VULN"
                else:
                    predictions.setdefault(case_id, "SAFE")
    return predictions


def print_metrics_table(metrics: Dict, title: str = "Results"):
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")
    print(f"  TP={metrics['tp']:3d}  FP={metrics['fp']:3d}  FN={metrics['fn']:3d}  TN={metrics['tn']:3d}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  FPR:       {metrics['fpr']:.4f}")
    print(f"  F1:        {metrics['f1']:.4f}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Compute MechaAudit evaluation metrics.")
    parser.add_argument("--results", type=Path,
                        help="Pre-computed metrics JSON (e.g. results/main/mechaaudit_metrics.json).")
    parser.add_argument("--predictions", type=Path,
                        help="Custom predictions JSONL ({case_id, verdict} per line).")
    parser.add_argument("--benchmark", type=Path, default=Path("benchmark/manifest.jsonl"),
                        help="Benchmark manifest JSONL (default: benchmark/manifest.jsonl).")
    parser.add_argument("--output", type=Path, help="Write computed metrics to this JSON file.")
    args = parser.parse_args()

    if args.results:
        data = json.loads(args.results.read_text())
        overall = data.get("overall", {})
        print_metrics_table(overall, title=f"MechaAudit (from {args.results.name})")
        by_bm = data.get("by_benchmark", {})
        for bm, m in by_bm.items():
            print_metrics_table(m, title=f"  {bm}")
        return

    if not args.predictions:
        parser.error("Provide --results or --predictions.")

    labels = load_benchmark_labels(args.benchmark)
    predictions = load_predictions_from_jsonl(args.predictions)

    bm_lookup: Dict[str, str] = {}
    with open(args.benchmark) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            bm_lookup[entry.get("case_id", "")] = entry.get("benchmark", "")

    by_benchmark: Dict[str, Dict] = {}
    for bm in ["sherlock", "web3bugs", "defihacklabs"]:
        bm_labels = {cid: lbl for cid, lbl in labels.items() if bm_lookup.get(cid) == bm}
        if bm_labels:
            by_benchmark[bm] = compute_contract_metrics(predictions, bm_labels)

    overall = compute_contract_metrics(predictions, labels)

    output = {"overall": overall, "by_benchmark": by_benchmark}
    print_metrics_table(overall, "Overall")
    for bm, m in by_benchmark.items():
        print_metrics_table(m, bm)

    if args.output:
        args.output.write_text(json.dumps(output, indent=2))
        print(f"Metrics written to {args.output}")


def _get_benchmark(case_id: str, manifest_path: Path) -> str:
    """Look up benchmark for a case_id from the manifest."""
    with open(manifest_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("case_id") == case_id:
                return entry.get("benchmark", "")
    return ""


if __name__ == "__main__":
    main()
