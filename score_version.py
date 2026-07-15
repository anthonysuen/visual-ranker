#!/usr/bin/env python3
"""Deterministic, reproducible product scorecard. No model judge - every
point is a checkable fact about the HTML, so the score cannot drift with
opinion. Run after each iteration: python3 score_version.py [git_ref]"""
import subprocess, sys, re

# (weight, label, regex that must appear in the HTML to earn it)
RUBRIC = [
    (10, "Core: weighted-rubric scoring", r"function fit\("),
    (8,  "Four views (list/tournament/quadrant/tiers)", r'data-mode="tiers"'),
    (6,  "Wikipedia photo fetch", r"fetchWikiImage"),
    (6,  "Photo fetch on item add (not just page load)", r"fetchWikiImage\(nc\)"),
    (8,  "No board blank-out on non-Latin names", r"encodeURIComponent\(svg\)"),
    (5,  "Surrogate-safe initials", r"\[\.\.\.w\]\[0\]"),
    (7,  "Destructive-action confirms (import/delete)", r"Import replaces ALL"),
    (4,  "Debounced save on slider drag", r"scheduleSave"),
    (12, "AGGREGATION engine (multi-board)", r"function aggregateData|function groupIndex"),
    (10, "Disagreement/variance surfaced", r"spread"),
    (10, "Group lens across all four views", r"let groupMode"),
    (8,  "Board portability: file save + import", r"function downloadBoard"),
    (6,  "Shareable link (no backend)", r"#board="),
    (7,  "Starter sample packs (multi-domain)", r"SAMPLE_PACKS"),
    (5,  "Studio data-loss fix (tier/wikiTried)", r"preserve fields index"),
]
TOTAL = sum(w for w, _, _ in RUBRIC)

def score(ref):
    try:
        html = subprocess.run(["git", "show", f"{ref}:index.html"],
                              capture_output=True, text=True).stdout
    except Exception:
        html = ""
    if not html:
        return None
    got, rows = 0, []
    for w, label, rx in RUBRIC:
        hit = bool(re.search(rx, html))
        got += w if hit else 0
        rows.append((w if hit else 0, w, label, hit))
    return got, rows, len(html)

refs = sys.argv[1:] or ["HEAD"]
results = {r: score(r) for r in refs}
print(f"{'capability':44s} " + "".join(f"{r[:12]:>14s}" for r in refs))
print("-" * (44 + 14 * len(refs)))
base = results[refs[0]]
for i, (_, _, label, _) in enumerate(base[1]):
    line = f"{label:44s} "
    for r in refs:
        got, rows, _ = results[r]
        g, w, _, hit = rows[i]
        line += f"{('+' if hit else '·')+str(g)+'/'+str(w):>14s}"
    print(line)
print("-" * (44 + 14 * len(refs)))
line = f"{'SCORE / ' + str(TOTAL):44s} "
for r in refs:
    got, _, size = results[r]
    line += f"{str(got)+'/'+str(TOTAL):>14s}"
print(line)
line = f"{'  as %':44s} "
for r in refs:
    got, _, size = results[r]
    line += f"{str(round(100*got/TOTAL))+'%':>14s}"
print(line)
line = f"{'  size (KB)':44s} "
for r in refs:
    _, _, size = results[r]
    line += f"{round(size/1024):>14d}"
print(line)
