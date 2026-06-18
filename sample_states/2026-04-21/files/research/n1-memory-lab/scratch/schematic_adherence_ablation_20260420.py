"""
Reduced-schema R² ablation (12 → 5 → 3 → 1 axes) per judge.

Reuses the axis list, SCORE_MAP, VERDICT_MAP, and pooling convention from
`schematic_adherence_20260420.py`. For each judge we:
  1. Fit OLS on the full 12-axis predictor set (baseline).
  2. Rank axes by |standardized β| from that fit.
  3. Re-fit on the a-priori TOP-5 set (per task prompt).
  4. Re-fit on the empirical TOP-3 (largest |β_std| in the full fit).
  5. Re-fit on TOP-1 = state_transition_tracking.

Reports R², adj-R², ΔR² vs full, and a near-zero-β flag (|β_std| < 0.05).

Caveat: TOP-k subsets (3, 5 empirical) are chosen on the same data used
to compute their R². Reported R² for reduced models is optimistic.
"""
import json
import numpy as np
from pathlib import Path

SCORE_MAP = {'strong': 2, 'partial': 1, 'missed': 0}
VERDICT_MAP = {'pass': 2, 'partial': 1, 'fail': 0}
SUBAXES = [
    ('factual_grounding', 'support'),
    ('factual_grounding', 'boundedness'),
    ('factual_grounding', 'uncertainty_calibration'),
    ('continuity', 'active_thread_selection'),
    ('continuity', 'salience_relevance'),
    ('continuity', 'state_transition_tracking'),
    ('continuity', 'forgetting_residue_control'),
    ('continuity', 'continuation_value'),
    ('coherence', 'cross_harness_braid'),
    ('coherence', 'cross_session_consistency'),
    ('coherence', 'artifact_routing_consistency'),
    ('coherence', 'contradiction_handling'),
]
AXIS_NAMES = [f"{a}.{s}" for a, s in SUBAXES]

REPO = Path('/Users/saxenauts/Documents/personal/syke-replay-lab')
CONFIGS = {
    ('gpt', 'gpt'):   REPO / 'runs/ne13-real-15d-gpt54-final-20260420T071500Z/benchmark_results.json',
    ('opus', 'opus'): REPO / 'runs/ne13-real-15d-opus46-final-20260420T071500Z/benchmark_results.json',
    ('gpt', 'opus'):  REPO / 'runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z/benchmark_results.json',
    ('opus', 'gpt'):  REPO / 'runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z/benchmark_results.json',
}

A_PRIORI_TOP5 = {
    'opus': [
        'continuity.state_transition_tracking',
        'factual_grounding.support',
        'continuity.active_thread_selection',
        'continuity.continuation_value',
        'continuity.salience_relevance',
    ],
    'gpt': [
        'continuity.state_transition_tracking',
        'coherence.cross_session_consistency',
        'factual_grounding.boundedness',
        'coherence.contradiction_handling',
        'continuity.forgetting_residue_control',
    ],
}

TOP1 = 'continuity.state_transition_tracking'


def load_cells(path):
    rows = []
    for it in json.load(open(path))['items']:
        jr = it.get('judge_result', {})
        if 'error' in jr: continue
        verdict = it.get('verdict')
        if verdict not in VERDICT_MAP: continue
        feats, ok = [], True
        for axis, sub in SUBAXES:
            s = jr.get(axis, {}).get('subcategories', {}).get(sub, {}).get('score')
            if s not in SCORE_MAP: ok = False; break
            feats.append(SCORE_MAP[s])
        if ok:
            rows.append((feats, VERDICT_MAP[verdict]))
    return rows


def ols_r2(X, y):
    n, p = X.shape
    X_aug = np.hstack([np.ones((n, 1)), X])
    coef, _, _, _ = np.linalg.lstsq(X_aug, y, rcond=None)
    y_pred = X_aug @ coef
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - p - 1) if (n - p - 1) > 0 else float('nan')
    return r2, r2_adj, coef


def fit_subset(pooled, idxs):
    X = np.array([[r[0][i] for i in idxs] for r in pooled], dtype=float)
    y = np.array([r[1] for r in pooled], dtype=float)
    return ols_r2(X, y)


def std_betas(pooled, coef):
    X_cols = list(zip(*[r[0] for r in pooled]))
    y = [r[1] for r in pooled]
    sds = [float(np.std(c, ddof=1)) for c in X_cols]
    y_sd = float(np.std(y, ddof=1))
    out = []
    for i in range(len(SUBAXES)):
        b_raw = float(coef[i + 1])
        b_std = b_raw * sds[i] / y_sd if y_sd else 0.0
        out.append((AXIS_NAMES[i], b_std, b_raw))
    return out


def main():
    data = {k: load_cells(v) for k, v in CONFIGS.items()}

    print("=" * 80)
    print("Reduced-schema R² ablation (pooled per-judge)")
    print("=" * 80)

    results = {}
    for judge in ('gpt', 'opus'):
        pooled = data[('gpt', judge)] + data[('opus', judge)]
        n = len(pooled)
        print(f"\n## {judge}-judge  (n={n})")

        # Full fit
        all_idx = list(range(12))
        r2_full, adj_full, coef_full = fit_subset(pooled, all_idx)
        sb = std_betas(pooled, coef_full)
        sb_ranked = sorted(sb, key=lambda x: abs(x[1]), reverse=True)

        # Top-5 a priori
        top5_names = A_PRIORI_TOP5[judge]
        top5_idx = [AXIS_NAMES.index(n_) for n_ in top5_names]
        r2_5, adj_5, _ = fit_subset(pooled, top5_idx)

        # Top-3 empirical (largest |β_std| from the 12-fit)
        top3_names = [sb_ranked[i][0] for i in range(3)]
        top3_idx = [AXIS_NAMES.index(n_) for n_ in top3_names]
        r2_3, adj_3, _ = fit_subset(pooled, top3_idx)

        # Top-1 = state_transition_tracking
        top1_idx = [AXIS_NAMES.index(TOP1)]
        r2_1, adj_1, _ = fit_subset(pooled, top1_idx)

        print(f"  ALL-12  R²={r2_full:.3f}  adj={adj_full:.3f}  ΔR²=0.000")
        print(f"  TOP-5   R²={r2_5:.3f}  adj={adj_5:.3f}  ΔR²={r2_5-r2_full:+.3f}  "
              f"axes={top5_names}")
        print(f"  TOP-3   R²={r2_3:.3f}  adj={adj_3:.3f}  ΔR²={r2_3-r2_full:+.3f}  "
              f"axes={top3_names}")
        print(f"  TOP-1   R²={r2_1:.3f}  adj={adj_1:.3f}  ΔR²={r2_1-r2_full:+.3f}  "
              f"axis={TOP1}")

        print("\n  Ranked β (standardized) in the ALL-12 fit:")
        for name, b_std, b_raw in sb_ranked:
            flag = "  <-- near-zero" if abs(b_std) < 0.05 else ""
            print(f"    {name:<45} β_std={b_std:+.3f}  β_raw={b_raw:+.3f}{flag}")

        vacuous = [n_ for n_, b_std, _ in sb_ranked if abs(b_std) < 0.05]
        print(f"\n  Near-zero axes (|β_std| < 0.05, candidates for pruning): {vacuous or '(none)'}")

        results[judge] = {
            'n': n,
            'full':  (r2_full, adj_full),
            'top5':  (r2_5, adj_5, top5_names),
            'top3':  (r2_3, adj_3, top3_names),
            'top1':  (r2_1, adj_1),
            'ranked': sb_ranked,
            'vacuous': vacuous,
        }

    return results


if __name__ == '__main__':
    main()
