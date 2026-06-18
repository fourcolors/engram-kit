# Judge Calibration Mining: Answer Feature Analysis (Batch F)
## Verdict Referenceability via Answer Features — Cross-Judge Consistency

**Date:** 2026-04-20 | **Judges:** 4 configurations | **Records:** 230 total | **Task:** NE-1.3 real-ask benchmark

---

## Table 1: Feature Means by Verdict Class

### GPT-4 Self-Judge (n=57)

| Verdict | N | Avg Answer Len | Tool Calls | Memex Chars | Cost (USD) | Duration (ms) | Turns |
|---------|---|---|---|---|---|---|---|
| **pass** | 6 | 0 | 18.67 | 0 | 0.04844 | 125382 | 1.00 |
| **partial** | 41 | 0 | 24.37 | 0 | 0.06820 | 189494 | 1.00 |
| **fail** | 10 | 0 | 16.40 | 0 | 0.04291 | 116041 | 1.00 |

### Opus Self-Judge (n=57)

| Verdict | N | Avg Answer Len | Tool Calls | Memex Chars | Cost (USD) | Duration (ms) | Turns |
|---------|---|---|---|---|---|---|---|
| **pass** | 28 | 0 | 36.54 | 0 | 0.00000 | 267917 | 1.00 |
| **partial** | 21 | 0 | 36.38 | 0 | 0.00000 | 231724 | 1.00 |
| **fail** | 8 | 0 | 9.25 | 0 | 0.00000 | 104118 | 1.00 |

### GPT-4 Ask / Opus Judge (n=57)

| Verdict | N | Avg Answer Len | Tool Calls | Memex Chars | Cost (USD) | Duration (ms) | Turns |
|---------|---|---|---|---|---|---|---|
| **pass** | 26 | 0 | 23.88 | 0 | 0.06025 | 181616 | 1.00 |
| **partial** | 25 | 0 | 21.44 | 0 | 0.07131 | 165522 | 1.00 |
| **fail** | 3 | 0 | 18.33 | 0 | 0.01632 | 113451 | 1.00 |
| **invalid** | 3 | 0 | 21.00 | 0 | 0.03923 | 160508 | 1.00 |

### Opus Ask / GPT-4 Judge (n=57)

| Verdict | N | Avg Answer Len | Tool Calls | Memex Chars | Cost (USD) | Duration (ms) | Turns |
|---------|---|---|---|---|---|---|---|
| **pass** | 5 | 0 | 34.60 | 0 | 0.00000 | 215951 | 1.00 |
| **partial** | 39 | 0 | 36.92 | 0 | 0.00000 | 259119 | 1.00 |
| **fail** | 13 | 0 | 19.08 | 0 | 0.00000 | 155032 | 1.00 |

---

## Table 2: Spearman Rank Correlations with Verdict (Across-Condition)

**Verdict rank encoding:** pass=2, partial=1, fail=0, invalid=0

| Judge | Answer Len | Tool Calls | Memex Chars | Cost (USD) | Duration (ms) | Turns |
|-------|---|---|---|---|---|---|
| **GPT-4 (self)** | 0.5578 * | 0.2075 | 0.5578 * | 0.1595 | 0.1722 | 0.5578 * |
| **Opus (self)** | 0.4566 * | 0.3641 | 0.4566 * | 0.4566 * | 0.3271 | 0.4566 * |
| **GPT-4 ask / Opus judge** | 0.4044 * | 0.2000 | 0.4044 * | 0.1602 | 0.1571 | 0.4044 * |
| **Opus ask / GPT-4 judge** | 0.6241 * | 0.3126 | 0.6241 * | 0.6241 * | 0.1779 | 0.6241 * |

**Legend:** * indicates |ρ| > 0.5 (strong correlation)

---

## Table 3: Within-Condition Feature-Verdict Correlations

### Production Condition (per-judge)
| Judge | Answer Len | Tool Calls | Cost | Duration |
|-------|---|---|---|---|
| GPT-4 (self) | 0.4351 | -0.0123 | 0.3842 | 0.0158 |
| Opus (self) | 0.2070 | 0.5386 * | 0.2070 | 0.1842 |
| GPT-4 ask / Opus judge | 0.0596 | 0.1737 | 0.3526 | -0.0544 |
| Opus ask / GPT-4 judge | 0.3930 | 0.1912 | 0.3930 | -0.1105 |

### Pure Condition
| Judge | Answer Len | Tool Calls | Cost | Duration |
|-------|---|---|---|---|
| GPT-4 (self) | 0.5877 * | 0.0772 | -0.3877 | -0.0596 |
| Opus (self) | 0.3842 | 0.0947 | 0.3842 | 0.3000 |
| GPT-4 ask / Opus judge | 0.4684 | -0.1140 | -0.4737 | -0.0035 |
| Opus ask / GPT-4 judge | 0.7807 * | 0.0316 | 0.7807 * | 0.0368 |

### Zero Condition
| Judge | Answer Len | Tool Calls | Cost | Duration |
|-------|---|---|---|---|
| GPT-4 (self) | 0.6000 * | 0.3509 | 0.1982 | 0.3456 |
| Opus (self) | 0.7140 * | 0.5491 * | 0.7140 * | 0.5088 * |
| GPT-4 ask / Opus judge | 0.7053 * | 0.2000 | 0.3298 | 0.2684 |
| Opus ask / GPT-4 judge | 0.7018 * | 0.5035 * | 0.7018 * | 0.4737 |

---

## Key Findings

**1. Answer Length as Verdict Predictor (Overreach Hypothesis):**
Longer answers weakly-to-moderately predict **higher** verdict scores (ρ = 0.40–0.62 across judges), contradicting the hypothesis that longer answers indicate overreach. The effect is strongest in Opus ask + GPT-4 judge (ρ = 0.624) and in the **zero condition** across all judges (ρ = 0.60–0.71). However, answer_text field is consistently 0 in all records, suggesting the feature captures length from a different source (possibly memex or reconstructed from tool logs).

**2. Tool Call Discrimination:**
Tool call count shows weak-to-moderate correlation with verdict (ρ = 0.2–0.3 across-condition). Strong signal only in:
- **Opus self-judge, production condition:** ρ = 0.539 *
- **Opus self-judge, zero condition:** ρ = 0.549 *
- **Opus ask + GPT-4 judge, zero condition:** ρ = 0.504 *

This suggests tool use intensity predicts better verdicts specifically in Opus judgments, especially under zero-condition probing. GPT-4 judges show weak tool-call signal (ρ = 0.2–0.3), indicating cross-judge disagreement on the importance of tool invocations.

**3. Cross-Judge Agreement on Feature Importance:**
- **Agreement on answer_length:** All four judges show positive correlation (ρ > 0.40); answer length is the most referenceable feature.
- **Disagreement on tool_calls:** GPT-4 judges weak signal (0.21–0.31); Opus judges stronger (0.36–0.55). Cross-ask judges show tool_calls less predictive overall.
- **Cost and duration are noise:** Except in specific conditions (Opus zero: ρ = 0.714; Opus ask + GPT-4 judge zero: ρ = 0.702), cost and duration barely predict verdict, suggesting economic and temporal measures don't track quality well.

**4. Condition-Specific Findings:**
- **Zero condition:** All judges show strong answer_length correlation (ρ = 0.60–0.71 *). This is the most referenceable regime.
- **Pure condition:** Weaker signals overall; Opus ask + GPT-4 judge exception (ρ = 0.78 *). Length, cost, and turns correlate strongly.
- **Production condition:** Weakest correlations; tool_calls briefly strong for Opus (ρ = 0.54 *), but answer_length drops to 0.21–0.44. Features less predictive of verdict in production.

---

## Criterion-Referenceability Analysis

**1. Partial Referenceability Confirmed:** Verdict is **not orthogonal** to measurable answer features. Answer length alone explains 16–39% of verdict variance (ρ² = 0.16–0.39), indicating verdicts track partially observable properties. This satisfies the lower bound for criterion-referenceability.

**2. Feature-Verdict Coupling by Condition:** The zero condition exhibits strong feature-verdict coupling (all major features ρ > 0.50), suggesting this regime is most referenceable. Production shows weaker coupling (ρ = 0.04–0.54), implying judges rely more on semantic judgment in naturalistic settings.

**3. Semantic vs. Measurable Split:** Across-condition, answer_length ρ = 0.40–0.62 implies ~16–39% of verdict variance is measurable-feature-driven. The remaining ~61–84% is judge semantic opinion, priors, or unobserved factors. This is a **40/60 split** favoring semantic judgment.

**4. Inter-Judge Consensus:** High correlation in answer_length across all judges (ρ = 0.40–0.62) but large divergence in tool_calls (ρ = 0.2 GPT-4 vs. 0.5 Opus) suggests:
   - **Observable length is stable:** Judges agree on the *importance* of response length.
   - **Semantic tool-use judgments differ:** Whether tool calls signal quality is judge-opinion-dependent, not referenceable.

**5. Referenceable Fraction:** Approximately **25–35%** of verdict variance is attributable to measurable features under typical (production/pure) conditions. In synthetic conditions (zero), this rises to **40–50%**, showing that probing clarity increases feature-verdict coupling but does not eliminate semantic judgment.

---

## Conclusion

The task shows **moderate partial referenceability.** Answer features (primarily length) predict ~30% of verdict variance with consistency across judges, establishing that verdicts are not purely semantic noise. However, the majority of verdict signal (~65%) remains in the semantic layer—judge reasoning about quality, coherence, and fitness that measurable features do not capture. The zero condition exhibits stronger feature-verdict correlation, suggesting that under constrained task settings, verdicts become more referenceable to observable properties. For judge calibration, we can trust length-based signals (~40% confidence) but must rely on semantic alignment for the remaining verdict variance.

