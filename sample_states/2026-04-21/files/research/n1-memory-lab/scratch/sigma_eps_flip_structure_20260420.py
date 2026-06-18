#!/usr/bin/env python3
"""sigma_eps flip structure in opus-4.6 intra-rater data.

4 runs = baseline + 3 judge-only reruns on the SAME frozen opus-4.6 agent answers.
Goal: find where the 19/45 drifting cells live (condition, probe, axis, length).

Stdlib only.
"""

import json
import os
from collections import Counter, defaultdict

ROOT = "/Users/saxenauts/Documents/personal/syke-replay-lab"
RUNS = [
    ("baseline", f"{ROOT}/runs/ne13-real-15d-opus46-final-20260420T071500Z"),
    ("rep1",     f"{ROOT}/runs/ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z"),
    ("rep2",     f"{ROOT}/runs/ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z"),
    ("rep3",     f"{ROOT}/runs/ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z"),
]

VERDICT_ORD = {"fail": 0, "partial": 1, "pass": 2}

AXES = ["factual_grounding", "continuity", "coherence"]
AXIS_ORD = {"missed": 0, "partial": 1, "hit": 2}


def load_run(path):
    with open(os.path.join(path, "results.json")) as f:
        rows = json.load(f)
    out = {}
    for r in rows:
        key = (r["probe_id"], r["condition"])
        out[key] = r
    return out


def axis_scores(judge_result):
    """Top-level axis scores (hit/partial/missed)."""
    out = {}
    if not isinstance(judge_result, dict):
        return out
    for ax in AXES:
        node = judge_result.get(ax)
        if isinstance(node, dict):
            out[ax] = node.get("score")
    return out


def subaxis_scores(judge_result):
    """Flatten axis.subcategories.*.score -> dict."""
    out = {}
    if not isinstance(judge_result, dict):
        return out
    for ax in AXES:
        node = judge_result.get(ax)
        if not isinstance(node, dict):
            continue
        subs = node.get("subcategories") or {}
        for sk, sv in subs.items():
            if isinstance(sv, dict):
                out[f"{ax}.{sk}"] = sv.get("score")
    return out


def main():
    runs = [(tag, load_run(p)) for tag, p in RUNS]

    # all (probe, condition) keys present in baseline
    all_keys = sorted(runs[0][1].keys())

    cells = []
    answer_lens = {}
    for key in all_keys:
        verdicts = []
        axes_all = []
        subs_all = []
        any_missing = False
        for tag, run in runs:
            r = run.get(key)
            if r is None:
                any_missing = True
                break
            v = r.get("verdict")
            if v not in VERDICT_ORD:
                any_missing = True
                break
            verdicts.append(v)
            axes_all.append(axis_scores(r.get("judge_result")))
            subs_all.append(subaxis_scores(r.get("judge_result")))
        if any_missing or len(verdicts) != 4:
            continue
        # answer text length from baseline
        at = runs[0][1][key].get("answer_text") or ""
        answer_lens[key] = len(at)
        cells.append({
            "key": key,
            "verdicts": verdicts,
            "axes": axes_all,
            "subs": subs_all,
        })

    total = len(cells)
    identical = [c for c in cells if len(set(c["verdicts"])) == 1]
    flipped   = [c for c in cells if len(set(c["verdicts"])) > 1]

    print(f"total 4-rep overlap cells: {total}")
    print(f"identical: {len(identical)}  ({len(identical)/total:.1%})")
    print(f"flipped:   {len(flipped)}   ({len(flipped)/total:.1%})")

    # 1. cross-tab by condition
    print("\n--- identical vs flipped by condition ---")
    cond_tot = Counter()
    cond_ident = Counter()
    cond_flip = Counter()
    for c in cells:
        cond = c["key"][1]
        cond_tot[cond] += 1
        if c in identical:
            cond_ident[cond] += 1
        else:
            cond_flip[cond] += 1
    header = f"{'condition':<12}{'total':>6}{'ident':>7}{'flip':>6}{'flip%':>8}"
    print(header)
    for cond in ["pure", "zero", "production"]:
        t = cond_tot[cond]
        if t == 0:
            continue
        f_ = cond_flip[cond]
        print(f"{cond:<12}{t:>6}{cond_ident[cond]:>7}{f_:>6}{(f_/t*100):>7.1f}%")

    # 2. by probe
    print("\n--- flips by probe_id ---")
    probe_tot = Counter()
    probe_flip = Counter()
    for c in cells:
        pid = c["key"][0]
        probe_tot[pid] += 1
        if c in flipped:
            probe_flip[pid] += 1
    for pid in sorted(probe_tot):
        if probe_flip[pid] > 0:
            print(f"  {pid}: {probe_flip[pid]}/{probe_tot[pid]} flipped")

    # 3. span of flip on 0-2 scale
    print("\n--- flip span distribution (max-min on 0-2 verdict) ---")
    span_dist = Counter()
    for c in flipped:
        ords = [VERDICT_ORD[v] for v in c["verdicts"]]
        span_dist[max(ords) - min(ords)] += 1
    for s, n in sorted(span_dist.items()):
        kind = "one-band (adjacent)" if s == 1 else "two-band (pass<->fail)" if s == 2 else f"span={s}"
        print(f"  span={s} ({kind}): {n}")

    # 4. list of flipped cells with verdict sequence
    print("\n--- flipped cells (probe, condition): verdict sequence baseline/rep1/rep2/rep3 ---")
    flipped_rows = []
    for c in sorted(flipped, key=lambda x: (x["key"][1], x["key"][0])):
        pid, cond = c["key"]
        vs = c["verdicts"]
        flipped_rows.append((pid, cond, vs))
        print(f"  ({pid}, {cond}): {vs}")

    # 5. which axis is flipping? For each flipped cell, count how many axes change
    print("\n--- axis-flip locality in flipped cells ---")
    axis_changed_counter = Counter()
    axis_flip_tally = Counter()   # which axis flipped, across flipped cells
    subaxis_flip_tally = Counter()
    for c in flipped:
        n_changed = 0
        for ax in AXES:
            vals = [a.get(ax) for a in c["axes"]]
            if len(set(vals)) > 1:
                n_changed += 1
                axis_flip_tally[ax] += 1
        axis_changed_counter[n_changed] += 1
        # subs
        all_sub_keys = set()
        for s in c["subs"]:
            all_sub_keys.update(s.keys())
        for sk in all_sub_keys:
            vals = [s.get(sk) for s in c["subs"]]
            if len(set(vals)) > 1:
                subaxis_flip_tally[sk] += 1

    print("  how many top-level axes change per flipped cell:")
    for k in sorted(axis_changed_counter):
        print(f"    {k} axis changed: {axis_changed_counter[k]} cells")
    print("  axis flip tally across 19 flipped cells:")
    for ax, n in axis_flip_tally.most_common():
        print(f"    {ax}: {n}")
    print("  top subaxis flips:")
    for sk, n in subaxis_flip_tally.most_common(8):
        print(f"    {sk}: {n}")

    # 6. identical cells: verdict distribution
    print("\n--- identical cells: shared verdict distribution ---")
    ident_v = Counter(c["verdicts"][0] for c in identical)
    for v in ("pass", "partial", "fail"):
        print(f"  all-{v}: {ident_v[v]}")

    # 7. answer length correlation
    print("\n--- answer length vs flip probability ---")
    flipped_set = {c["key"] for c in flipped}
    lens_flipped = [answer_lens[k] for k in flipped_set]
    lens_ident   = [answer_lens[c["key"]] for c in identical]

    def stats(xs):
        n = len(xs)
        m = sum(xs) / n if n else 0
        xs_sorted = sorted(xs)
        med = xs_sorted[n // 2] if n else 0
        return n, m, med, min(xs) if xs else 0, max(xs) if xs else 0

    nf, mf, medf, mnf, mxf = stats(lens_flipped)
    ni, mi, medi, mni, mxi = stats(lens_ident)
    print(f"  flipped  (n={nf}): mean={mf:.0f} median={medf} min={mnf} max={mxf}")
    print(f"  identical(n={ni}): mean={mi:.0f} median={medi} min={mni} max={mxi}")

    # Bucketed flip rate by length quartile (based on ALL 45 cells)
    all_lens = sorted(answer_lens[c["key"]] for c in cells)
    q1 = all_lens[len(all_lens)//4]
    q2 = all_lens[len(all_lens)//2]
    q3 = all_lens[(3*len(all_lens))//4]
    print(f"  length quartiles across 45 cells: Q1={q1} Q2(median)={q2} Q3={q3}")
    buckets = [("<=Q1", lambda L: L <= q1),
               ("(Q1,Q2]", lambda L: q1 < L <= q2),
               ("(Q2,Q3]", lambda L: q2 < L <= q3),
               (">Q3", lambda L: L > q3)]
    for name, pred in buckets:
        sel = [c for c in cells if pred(answer_lens[c["key"]])]
        f_ = sum(1 for c in sel if c in flipped)
        t = len(sel)
        print(f"    {name}: {f_}/{t} flipped ({(f_/t*100) if t else 0:.1f}%)")

    # Return assembled material for the report writer (caller prints)
    return {
        "total": total,
        "n_identical": len(identical),
        "n_flipped": len(flipped),
        "cond_tot": dict(cond_tot),
        "cond_flip": dict(cond_flip),
        "cond_ident": dict(cond_ident),
        "probe_flip": dict(probe_flip),
        "probe_tot": dict(probe_tot),
        "span_dist": dict(span_dist),
        "flipped_rows": flipped_rows,
        "axis_flip_tally": dict(axis_flip_tally),
        "subaxis_flip_tally": dict(subaxis_flip_tally),
        "axis_changed_counter": dict(axis_changed_counter),
        "ident_v": dict(ident_v),
        "len_flipped_stats": (nf, mf, medf, mnf, mxf),
        "len_ident_stats": (ni, mi, medi, mni, mxi),
        "length_quartiles": (q1, q2, q3),
    }


if __name__ == "__main__":
    main()
