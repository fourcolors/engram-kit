"""
Retroactive s_state tip-currency gate on the 114 cross-judge pair-cells.

For each (probe_id, condition) cell of the 2x2 cross, pair gpt-judge and
opus-judge verdicts on the SAME agent's answer. Derive per-judge tip/landscape
from judge_result sub-axis scores (no new LLM calls), apply the iteration-2
tip-currency gate, and report the rejudged verdicts.

Rule (iteration-2 structural-bias anatomy):
  - tip_hit from continuity.active_thread_selection.score:
        strong=1.0, partial=0.5, missed=0.0
  - landscape_hit from continuity.salience_relevance.score same mapping.
  - verdict mapping:
        tip=1.0 AND landscape>=0.5 -> pass
        tip=1.0 AND landscape<0.5  -> partial
        tip=0.5                    -> partial  (ambiguous boundary)
        tip=0.0                    -> partial  (at most partial; demoted to
                                                fail iff also artifact/contra
                                                mismatch flagged)
"""
import json
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path('/Users/saxenauts/Documents/personal/syke-replay-lab')

# gpt-judge runs over both agents
GPT_J_GPT_A = REPO / 'runs/ne13-real-15d-gpt54-final-20260420T071500Z/benchmark_results.json'
GPT_J_OPUS_A = REPO / 'runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z/benchmark_results.json'
# opus-judge runs over both agents
OPUS_J_OPUS_A = REPO / 'runs/ne13-real-15d-opus46-final-20260420T071500Z/benchmark_results.json'
OPUS_J_GPT_A = REPO / 'runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z/benchmark_results.json'

VERDICT_MAP = {'pass': 2, 'partial': 1, 'fail': 0}
SCORE_MAP = {'strong': 1.0, 'partial': 0.5, 'missed': 0.0}


def load_items(path):
    out = {}
    data = json.load(open(path))
    for it in data['items']:
        out[(it['probe_id'], it['condition'])] = it
    return out


def tip_landscape(it):
    """Extract tip_hit, landscape_hit, and a 'major_mismatch' flag from judge_result."""
    jr = it.get('judge_result', {})
    if not jr or 'error' in jr or it.get('verdict') == 'invalid':
        return None
    cont = jr.get('continuity', {}).get('subcategories', {})
    a = cont.get('active_thread_selection', {}).get('score')
    s = cont.get('salience_relevance', {}).get('score')
    if a not in SCORE_MAP or s not in SCORE_MAP:
        return None
    tip = SCORE_MAP[a]
    land = SCORE_MAP[s]

    # A secondary contradiction / artifact mismatch flag from coherence.
    coh = jr.get('coherence', {}).get('subcategories', {})
    cont_h = coh.get('contradiction_handling', {}).get('score')
    art = coh.get('artifact_routing_consistency', {}).get('score')
    major_mismatch = (cont_h == 'missed') or (art == 'missed')

    return {
        'tip': tip, 'land': land, 'major_mismatch': major_mismatch,
        'orig_verdict': it.get('verdict'),
    }


def rule_verdict(tip, land, major_mismatch):
    """
    Apply iteration-2 tip-currency gate.
    Verdicts: 'pass', 'partial', 'fail'.
    """
    if tip >= 1.0:  # full tip hit
        if land >= 0.5:  # >= partial on landscape -> pass
            return 'pass'
        return 'partial'
    elif tip >= 0.5:  # partial tip
        # capped at partial; fail iff also major mismatch
        return 'fail' if major_mismatch and land < 0.5 else 'partial'
    else:  # tip missed
        # at most partial; demote to fail if major mismatch
        return 'fail' if major_mismatch else 'partial'


def cohens_kappa(pairs, levels):
    """Cohen's kappa on an iterable of (a, b) with discrete levels."""
    if not pairs:
        return float('nan')
    n = len(pairs)
    counts_a = Counter(a for a, _ in pairs)
    counts_b = Counter(b for _, b in pairs)
    pa = sum(1 for a, b in pairs if a == b) / n
    pe = sum((counts_a[l] / n) * (counts_b[l] / n) for l in levels)
    if pe == 1.0:
        return float('nan')
    return (pa - pe) / (1.0 - pe)


def main():
    gpt_j_gpt_a = load_items(GPT_J_GPT_A)
    gpt_j_opus_a = load_items(GPT_J_OPUS_A)
    opus_j_opus_a = load_items(OPUS_J_OPUS_A)
    opus_j_gpt_a = load_items(OPUS_J_GPT_A)

    # For each agent, iterate over its 57 cells and pair the two judges.
    # agent label -> (gpt_j map, opus_j map)
    agents = {
        'gpt-agent': (gpt_j_gpt_a, opus_j_gpt_a),
        'opus-agent': (opus_j_opus_a, opus_j_opus_a),
    }
    # Fix: opus-judge on opus-agent is opus_j_opus_a; gpt-judge on opus-agent is gpt_j_opus_a
    agents = {
        'gpt-agent':  (gpt_j_gpt_a,   opus_j_gpt_a),    # gpt-judge, opus-judge on gpt-agent
        'opus-agent': (gpt_j_opus_a,  opus_j_opus_a),   # gpt-judge, opus-judge on opus-agent
    }

    all_pairs = []  # list of dicts per cell

    for agent, (gpt_j, opus_j) in agents.items():
        keys = sorted(set(gpt_j.keys()) & set(opus_j.keys()))
        for k in keys:
            g_it = gpt_j[k]
            o_it = opus_j[k]
            g = tip_landscape(g_it)
            o = tip_landscape(o_it)
            if g is None or o is None:
                # one judge returned invalid; skip from pair-cell pool
                continue
            g_rej = rule_verdict(g['tip'], g['land'], g['major_mismatch'])
            o_rej = rule_verdict(o['tip'], o['land'], o['major_mismatch'])
            all_pairs.append({
                'agent': agent, 'probe': k[0], 'cond': k[1],
                'gpt_orig':  g['orig_verdict'], 'opus_orig': o['orig_verdict'],
                'gpt_rej':   g_rej,             'opus_rej':  o_rej,
                'gpt_tip':   g['tip'],          'opus_tip':  o['tip'],
                'gpt_land':  g['land'],         'opus_land': o['land'],
                'gpt_mm':    g['major_mismatch'], 'opus_mm': o['major_mismatch'],
            })

    print(f"Total usable pair-cells: {len(all_pairs)}")
    print(f"  gpt-agent: {sum(1 for p in all_pairs if p['agent']=='gpt-agent')}")
    print(f"  opus-agent: {sum(1 for p in all_pairs if p['agent']=='opus-agent')}")

    # Originally-mismatched (any 3-level disagreement) baseline set
    mismatched = [p for p in all_pairs if p['gpt_orig'] != p['opus_orig']]
    print(f"\nOriginally-mismatched pair-cells: {len(mismatched)}")

    # How many originally-mismatched are now agreed under the rule?
    now_agreed = [p for p in mismatched if p['gpt_rej'] == p['opus_rej']]
    print(f"  of which now agreed under rule: {len(now_agreed)} "
          f"({100.0*len(now_agreed)/len(mismatched):.1f}%)")

    # Directional shift on originally-mismatched:
    # "toward gpt's" = both judges' rejudged verdict == gpt's original verdict
    # "toward opus's" = both judges' rejudged verdict == opus's original verdict
    # "split/neither" = rejudged verdicts agree but match neither original, or still disagree
    toward_gpt  = 0
    toward_opus = 0
    other_agreed = 0
    still_split = 0
    for p in mismatched:
        if p['gpt_rej'] == p['opus_rej']:
            v = p['gpt_rej']
            if v == p['gpt_orig'] and v != p['opus_orig']:
                toward_gpt += 1
            elif v == p['opus_orig'] and v != p['gpt_orig']:
                toward_opus += 1
            else:
                other_agreed += 1
        else:
            still_split += 1
    print(f"\nDirectional shift on originally-mismatched (n={len(mismatched)}):")
    print(f"  rejudged agrees with gpt-original: {toward_gpt} "
          f"({100.0*toward_gpt/len(mismatched):.1f}%)")
    print(f"  rejudged agrees with opus-original: {toward_opus} "
          f"({100.0*toward_opus/len(mismatched):.1f}%)")
    print(f"  rejudged agrees with neither original: {other_agreed} "
          f"({100.0*other_agreed/len(mismatched):.1f}%)")
    print(f"  rejudged still disagrees: {still_split} "
          f"({100.0*still_split/len(mismatched):.1f}%)")

    # Rejudge verdict distribution across all rejudged pair-cells (2 verdicts each)
    dist_gpt  = Counter(p['gpt_rej']  for p in all_pairs)
    dist_opus = Counter(p['opus_rej'] for p in all_pairs)
    pooled = Counter()
    for p in all_pairs:
        pooled[p['gpt_rej']]  += 1
        pooled[p['opus_rej']] += 1
    print(f"\nRejudged verdict distribution (pooled, 2 per cell, n={2*len(all_pairs)}):")
    for v in ('pass', 'partial', 'fail'):
        print(f"  {v:<8}: {pooled[v]:3d}  ({100.0*pooled[v]/(2*len(all_pairs)):.1f}%)")
    print(f"\n  gpt-judge rejudged : pass={dist_gpt['pass']}, "
          f"partial={dist_gpt['partial']}, fail={dist_gpt['fail']}")
    print(f"  opus-judge rejudged: pass={dist_opus['pass']}, "
          f"partial={dist_opus['partial']}, fail={dist_opus['fail']}")

    # Cross-pair kappa, 3-level, original vs rejudged
    levels3 = ['pass', 'partial', 'fail']
    levels2 = ['useful', 'not_useful']

    def binary(v):
        return 'useful' if v in ('pass', 'partial') else 'not_useful'

    orig_pairs = [(p['gpt_orig'], p['opus_orig']) for p in all_pairs]
    rej_pairs  = [(p['gpt_rej'],  p['opus_rej'])  for p in all_pairs]
    orig_bin   = [(binary(a), binary(b)) for a, b in orig_pairs]
    rej_bin    = [(binary(a), binary(b)) for a, b in rej_pairs]

    k3_orig = cohens_kappa(orig_pairs, levels3)
    k3_rej  = cohens_kappa(rej_pairs, levels3)
    k2_orig = cohens_kappa(orig_bin, levels2)
    k2_rej  = cohens_kappa(rej_bin, levels2)

    pa3_orig = sum(1 for a, b in orig_pairs if a == b) / len(orig_pairs)
    pa3_rej  = sum(1 for a, b in rej_pairs  if a == b) / len(rej_pairs)
    pa2_orig = sum(1 for a, b in orig_bin   if a == b) / len(orig_bin)
    pa2_rej  = sum(1 for a, b in rej_bin    if a == b) / len(rej_bin)

    print(f"\nCross-pair kappa on pair-cells (n={len(all_pairs)}):")
    print(f"  3-level orig : kappa={k3_orig:+.3f}  exact-match={100*pa3_orig:.1f}%")
    print(f"  3-level rej  : kappa={k3_rej:+.3f}  exact-match={100*pa3_rej:.1f}%  "
          f"Δ={k3_rej-k3_orig:+.3f}")
    print(f"  binary  orig : kappa={k2_orig:+.3f}  exact-match={100*pa2_orig:.1f}%")
    print(f"  binary  rej  : kappa={k2_rej:+.3f}  exact-match={100*pa2_rej:.1f}%  "
          f"Δ={k2_rej-k2_orig:+.3f}")

    # Rule-ambiguous cells: both judges saw tip as partial (0.5)
    ambiguous = [p for p in all_pairs
                 if p['gpt_tip'] == 0.5 and p['opus_tip'] == 0.5]
    print(f"\nRule-ambiguous cells (both judges tip=partial): {len(ambiguous)}")
    for p in ambiguous[:15]:
        print(f"    {p['agent']:<10} {p['probe']}/{p['cond']:<10} "
              f"gpt_rej={p['gpt_rej']:<7} opus_rej={p['opus_rej']:<7} "
              f"gpt_orig={p['gpt_orig']}/opus_orig={p['opus_orig']}")

    # Agreed-pass anchor: the cells that were agreed pass originally
    anchor_all = [p for p in all_pairs
                  if p['gpt_orig'] == 'pass' and p['opus_orig'] == 'pass']
    print(f"\nAgreed-pass anchor (pre-R13): {len(anchor_all)} cells")
    hold_both_pass = sum(1 for p in anchor_all
                        if p['gpt_rej'] == 'pass' and p['opus_rej'] == 'pass')
    hold_any_pass = sum(1 for p in anchor_all
                       if p['gpt_rej'] == 'pass' or p['opus_rej'] == 'pass')
    print(f"  both rejudged verdicts still pass: {hold_both_pass}/{len(anchor_all)}")
    print(f"  at least one rejudged verdict still pass: {hold_any_pass}/{len(anchor_all)}")
    for p in anchor_all:
        print(f"    {p['agent']:<10} {p['probe']}/{p['cond']:<10} "
              f"gpt_rej={p['gpt_rej']:<7} opus_rej={p['opus_rej']:<7} "
              f"gpt_tip={p['gpt_tip']} opus_tip={p['opus_tip']} "
              f"gpt_land={p['gpt_land']} opus_land={p['opus_land']}")

    # Post-R13 anchor: drop the 3 R13 cells
    r13_drop = {('R13','pure'), ('R13','production')}
    anchor_post_r13 = [p for p in anchor_all
                       if (p['probe'], p['cond']) not in r13_drop]
    hold_post = sum(1 for p in anchor_post_r13
                   if p['gpt_rej'] == 'pass' and p['opus_rej'] == 'pass')
    print(f"\nAgreed-pass anchor (post-R13): {len(anchor_post_r13)} cells; "
          f"both still pass: {hold_post}/{len(anchor_post_r13)}")

    # Per-agent direction sanity check
    print("\nPer-agent directional shift:")
    for agent in ('gpt-agent', 'opus-agent'):
        sub = [p for p in mismatched if p['agent'] == agent]
        tg = sum(1 for p in sub if p['gpt_rej']==p['opus_rej']==p['gpt_orig'] and p['gpt_orig']!=p['opus_orig'])
        to = sum(1 for p in sub if p['gpt_rej']==p['opus_rej']==p['opus_orig'] and p['gpt_orig']!=p['opus_orig'])
        print(f"  {agent}: n_mismatched={len(sub)}, toward-gpt={tg}, toward-opus={to}")


if __name__ == '__main__':
    main()
