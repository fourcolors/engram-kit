"""
Schematic Adherence R² from Feuer et al. 2025 (arxiv 2509.20293).
Regress overall verdict on 12 sub-axis scores per judge; report R² and β.
Low R² would indicate schema incoherence (verdict not derivable from sub-axes).

Generated 2026-04-20 during the judge mining pass.
Re-run to refresh numbers after new judge data lands.
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

ROOT = Path(__file__).resolve().parents[3]
CONFIGS = {
    ('gpt-ask', 'gpt-5.4'): ROOT / 'runs/ne13-real-15d-gpt54-final-20260420T071500Z/benchmark_results.json',
    ('opus-ask', 'claude-opus-4-6'): ROOT / 'runs/ne13-real-15d-opus46-final-20260420T071500Z/benchmark_results.json',
    ('gpt-ask', 'claude-opus-4-6'): ROOT / 'runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z/benchmark_results.json',
    ('opus-ask', 'gpt-5.4-mini'): ROOT / 'runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z/benchmark_results.json',
}


def load_cells(path):
    rows = []
    for it in json.load(open(path))['items']:
        jr = it.get('judge_result', {})
        if 'error' in jr: continue
        verdict = it.get('verdict')
        if verdict not in VERDICT_MAP: continue
        feats = []
        ok = True
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
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - p - 1) if (n - p - 1) > 0 else float('nan')
    return r2, r2_adj, coef


def bootstrap_r2(X, y, n_iter=1000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(y)
    r2s = []
    for _ in range(n_iter):
        idx = rng.integers(0, n, n)
        try:
            r2, _, _ = ols_r2(X[idx], y[idx])
            r2s.append(r2)
        except:
            pass
    return np.percentile(r2s, [2.5, 97.5])


if __name__ == '__main__':
    data = {k: load_cells(v) for k, v in CONFIGS.items()}

    # Per (ask × judge) config
    print("Per-config R²:")
    for key, rows in data.items():
        X = np.array([r[0] for r in rows], dtype=float)
        y = np.array([r[1] for r in rows], dtype=float)
        r2, r2_adj, _ = ols_r2(X, y)
        ci = bootstrap_r2(X, y)
        print(f"  ask={key[0]} judge={key[1]} n={len(rows)}  R²={r2:.3f}  adj={r2_adj:.3f}  95%CI [{ci[0]:.3f},{ci[1]:.3f}]")

    # Pooled per judge family. "gpt-family" mixes full gpt-5.4 and gpt-5.4-mini.
    print("\nPooled per judge family:")
    judge_groups = {
        'gpt-family': [('gpt-ask', 'gpt-5.4'), ('opus-ask', 'gpt-5.4-mini')],
        'opus': [('gpt-ask', 'claude-opus-4-6'), ('opus-ask', 'claude-opus-4-6')],
    }
    for judge, members in judge_groups.items():
        pooled = []
        for key in members:
            pooled.extend(data[key])
        X = np.array([r[0] for r in pooled], dtype=float)
        y = np.array([r[1] for r in pooled], dtype=float)
        r2, r2_adj, coef = ols_r2(X, y)
        ci = bootstrap_r2(X, y)
        print(f"\n  {judge}-judge n={len(pooled)}  R²={r2:.3f}  adj={r2_adj:.3f}  95%CI [{ci[0]:.3f},{ci[1]:.3f}]")
        print(f"  unexplained: {1-r2:.1%}")
        # Standardized coefficients
        import statistics
        sds = [statistics.stdev([r[0][i] for r in pooled]) for i in range(12)]
        y_sd = statistics.stdev(y)
        axes = [f"{a}.{s}" for a, s in SUBAXES]
        std_coef = sorted(
            [(axes[i], coef[i+1] * sds[i] / y_sd if y_sd else 0, coef[i+1]) for i in range(12)],
            key=lambda x: abs(x[1]), reverse=True
        )
        print("  β coefficients (std):")
        for name, beta_std, beta_raw in std_coef:
            print(f"    {name:<45} β_std={beta_std:+.3f}  β_raw={beta_raw:+.3f}")

    # Single-axis baseline
    print("\nSingle-axis baseline (best single sub-axis alone):")
    for judge, members in judge_groups.items():
        pooled = []
        for key in members:
            pooled.extend(data[key])
        X = np.array([r[0] for r in pooled], dtype=float)
        y = np.array([r[1] for r in pooled], dtype=float)
        best_r2, best_axis = 0, None
        for i, (a, s) in enumerate(SUBAXES):
            r2, _, _ = ols_r2(X[:, i:i+1], y)
            if r2 > best_r2:
                best_r2, best_axis = r2, f"{a}.{s}"
        print(f"  {judge}-judge best single-axis R² = {best_r2:.3f} ({best_axis})")
