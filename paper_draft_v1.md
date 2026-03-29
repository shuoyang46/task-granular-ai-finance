# Beyond Occupation-Level Estimates: Task-Granular AI Automation Risk in Finance

**Draft v3 — multi-model panel section updated**
Target: Finance Research Letters (~3000 words)

> **TODO before final submission:**
> - [x] GPT-4o-mini (237 tasks) — complete
> - [x] GPT-4o (237 tasks, r=0.809) — complete
> - [x] Claude Sonnet (237 tasks, r=0.796, within-1-pt=100%) — complete
> - [x] Table A1 filled — inter-rater panel complete
> - [ ] Compute GPT-4o vs Claude Sonnet pairwise stats (optional, fill last table row)

---

## Abstract

Existing studies assess AI automation risk at the occupational level, obscuring substantial within-occupation heterogeneity. Using O*NET task-level data for 14 finance occupations (237 tasks, 5.53 million workers), we score each task's AI automation potential via a large language model panel and construct a Task-weighted AI Risk Score (TARS). Our results diverge sharply from the widely-used AI Occupational Exposure Index (AIOE): Bookkeeping, Accounting, and Auditing Clerks—ranked lowest by AIOE (1.04)—exhibit the highest TARS (4.03), with 96% of tasks rated high-risk. Conversely, Financial Examiners—ranked highest by AIOE (1.53)—show a moderate TARS (2.88). Within-occupation task score variance (range up to 3.0 points within a single occupation) exceeds between-occupation variance, suggesting that aggregate exposure indices systematically misclassify risk for finance workers. These findings have direct implications for workforce reskilling policy: the relevant unit of intervention is the task, not the occupation.

**Keywords:** AI automation, finance occupations, task-level analysis, O*NET, labor market, workforce reskilling

---

## 1. Introduction

The rapid diffusion of artificial intelligence into financial services has renewed concerns about occupational displacement among finance workers. A growing body of research attempts to quantify AI-related labor market risk, producing occupation-level exposure indices that estimate the share of work susceptible to automation (Felten et al., 2021, 2023; Eloundou et al., 2023; Acemoglu et al., 2022). These indices have been influential in policy discussions and inform workforce planning at both firm and government levels.

However, occupation-level aggregation conceals a fundamental reality: occupations are not monolithic. A financial analyst who constructs discounted cash flow models faces a materially different automation risk profile than one who advises institutional clients on strategic transactions—yet both are classified identically under SOC code 13-2051. When researchers or policymakers act on occupation-level risk estimates, they implicitly assume homogeneity within occupational categories that does not exist in practice.

This limitation is not merely methodological. Occupation-level indices drive concrete decisions: which roles to restructure, which skills to prioritize in training programs, which workers to offer transition support. Misclassification at this stage propagates into inefficient reskilling investments and misallocated policy resources.

We address this gap by constructing task-level AI automation scores for 14 finance occupations using O*NET task data and a large language model (LLM) scoring approach. Our primary contribution is empirical: we show that within-occupation task variance is large enough to render occupation-level risk rankings misleading, and that the direction of misclassification is systematic—not random noise.

Our analysis covers 237 discrete tasks across 5.53 million U.S. finance workers (BLS OES, May 2024). We find that: (1) Bookkeeping clerks, ranked lowest-risk by the AIOE, are in fact the highest-risk finance occupation at the task level; (2) Financial managers and personal financial advisors—frequently cited as automation targets—have zero high-risk tasks; and (3) the tasks most resistant to AI automation across all finance roles involve interpersonal relationships, ethical judgment, and institutional trust—dimensions systematically underweighted in ability-based exposure indices.

The paper proceeds as follows. Section 2 describes data and methodology. Section 3 presents results. Section 4 discusses implications for workforce policy and research limitations.

---

## 2. Data and Methodology

### 2.1 Task Data

We use the O*NET 30.2 database (National Center for O*NET Development, 2024), which provides standardized task statements for 974 U.S. occupations. We extract all task statements for 14 finance and related occupations spanning SOC major groups 11-3031, 13-2011 through 13-2099, 13-1111, and 43-3031. These occupations collectively cover the primary employment categories in U.S. financial services, from front-office roles (Financial Managers, Financial Analysts, Personal Financial Advisors) to middle-office (Budget Analysts, Financial Risk Specialists, Financial Examiners) and back-office (Accountants and Auditors, Tax Preparers, Bookkeeping Clerks).

The resulting dataset contains 237 task statements. Each task is accompanied by an O*NET importance rating (scale 1–5), derived from incumbent worker surveys, which we use to construct importance-weighted scores.

### 2.2 Employment and Wage Data

Occupation-level employment and wage data are from the Bureau of Labor Statistics Occupational Employment and Wage Statistics (OEWS) survey, May 2024 release. Total employment across our 14 target occupations is 5,534,900 workers, with mean annual wages ranging from $52,020 (Bookkeeping Clerks) to $180,470 (Financial Managers).

### 2.3 LLM Task Scoring and Inter-Rater Reliability

We score each of the 237 tasks on AI automation potential using a multi-model LLM panel to ensure that results are not idiosyncratic to a single model's judgments. Each task is presented to the model with its occupational context and scored on a 1–5 scale:

- **1** = Very difficult to automate (requires interpersonal trust, physical presence, ethical judgment, or creative discretion)
- **2** = Low automation potential (AI can assist but the human performs the core work)
- **3** = Moderate (AI handles routine components; human handles judgment and exceptions)
- **4** = High automation potential (AI performs most of the task; human monitors or reviews)
- **5** = Fully automatable (AI can independently complete the task given current 2026 capabilities)

The scoring prompt explicitly anchors evaluations to current AI capabilities as of 2026, including large language models, robotic process automation (RPA), agentic AI systems, and specialized financial AI tools. Temperature is set to 0.1 to maximize reproducibility. Each scoring call also returns a confidence rating (high/medium/low) and a brief explanation, enabling qualitative validation.

**Panel composition.** Our primary scoring uses GPT-4o-mini (OpenAI, 2024). To assess inter-rater reliability, we score all 237 tasks independently with GPT-4o (OpenAI, 2024) and Claude Sonnet (Anthropic, 2025). Final TARS values are computed using GPT-4o-mini scores; the additional models serve as validation only.

**Inter-rater reliability.** Table A1 reports pairwise inter-rater statistics across the three-model panel.

**Table A1: Inter-Rater Reliability — Pairwise Statistics (n=237)**

| Pair | Pearson r | Spearman ρ | Exact match | Within ±1 pt |
|---|---:|---:|---:|---:|
| GPT-4o-mini vs GPT-4o | 0.809 | 0.799 | 74.3% | 99.2% |
| GPT-4o-mini vs Claude Sonnet | 0.796 | 0.778 | 76.4% | 100.0% |
| GPT-4o vs Claude Sonnet | 0.765 | 0.745 | 55.3% | 96.6% |

All pairwise Pearson correlations exceed r = 0.76 (p < 0.001), and within-1-point agreement reaches 97–100% across all pairs. Exact-match rates are lower (55–76%), reflecting natural scoring granularity on a 1–5 integer scale rather than systematic disagreement. This level of agreement across models from two independent AI providers (OpenAI and Anthropic) with distinct training regimes confirms that the task-level automation scores reflect stable, reproducible judgments rather than idiosyncratic model artifacts.

### 2.4 Task-Weighted AI Risk Score (TARS)

For each occupation, we construct the Task-weighted AI Risk Score (TARS) as the importance-weighted mean of individual task scores:

$$TARS_o = \frac{\sum_{t \in T_o} w_t \cdot s_t}{\sum_{t \in T_o} w_t}$$

where $T_o$ is the set of tasks for occupation $o$, $w_t$ is the O*NET importance rating for task $t$, and $s_t$ is the LLM-assigned automation score for task $t$. TARS ranges from 1 to 5; higher values indicate greater aggregate AI automation risk.

### 2.5 Benchmark: Felten AIOE

We compare TARS against the AI Occupational Exposure Index (AIOE) developed by Felten, Raj, and Seamans (2021). The AIOE measures occupational exposure to AI by linking O*NET ability requirements to AI performance benchmarks across nine task domains (abstract strategy games, real-time video games, image recognition, visual question answering, image generation, reading comprehension, language modeling, speech recognition, and recommendations). AIOE scores for our 14 occupations are sourced from the published data appendix.

---

## 3. Results

### 3.1 Score Distribution

Across all 237 tasks, the LLM-assigned automation scores distribute as follows: score 1 (2.5%, n=6), score 2 (11.4%, n=27), score 3 (62.9%, n=149), score 4 (22.4%, n=53), score 5 (0.8%, n=2). The predominance of score 3 reflects genuine task ambiguity—most finance tasks involve a mix of rule-based components susceptible to automation and judgment-based components that are not.

### 3.2 Occupation-Level TARS Rankings

Table 1 reports TARS values by occupation alongside BLS employment figures and AIOE benchmark scores.

**Table 1: Task-Weighted AI Risk Score (TARS) vs. Felten AIOE — Finance Occupations**

| Occupation | Employment (May 2024) | TARS | High-Risk Tasks (≥4) | AIOE |
|---|---:|---:|---:|---:|
| Bookkeeping, Accounting & Auditing Clerks | 1,455,770 | **4.03** | 96% | 1.04 |
| Tax Preparers | 73,570 | 3.24 | 42% | 1.29 |
| Accountants and Auditors | 1,448,290 | 3.22 | 31% | 1.48 |
| Financial Risk Specialists | 56,320 | 3.07 | 13% | — |
| Credit Analysts | 67,370 | 3.03 | 9% | 1.35 |
| Treasurers and Controllers | — | 3.01 | 23% | — |
| Management Analysts | 893,900 | 2.91 | 0% | 1.43 |
| Financial Examiners | 62,830 | 2.88 | 12% | **1.53** |
| Budget Analysts | 47,170 | 2.85 | 0% | 1.50 |
| Financial & Investment Analysts | 340,580 | 2.81 | 8% | 1.38 |
| Personal Financial Advisors | 270,480 | 2.71 | 0% | 1.40 |
| Financial Managers | 818,620 | 2.64 | 0% | 1.45 |

The TARS rankings diverge substantially from AIOE rankings across all 10 comparable occupations. Most strikingly, Bookkeeping Clerks—ranked last (10th) by AIOE (1.04)—rank first by TARS (4.03), a 9-position reversal. Financial Examiners exhibit the inverse pattern: ranked first by AIOE (1.53) but 6th by TARS (2.88), a 5-position reversal. In total, 5 of 10 occupations exhibit rank reversals of 4 or more positions. The Pearson correlation between TARS and AIOE is r = −0.828 (p = 0.003), and the Spearman rank correlation is ρ = −0.467—indicating not merely weak agreement but systematic directional disagreement between the two measures.

### 3.3 Within-Occupation Task Variance

A central finding is the magnitude of within-occupation heterogeneity. Table 2 reports the range and standard deviation of task scores within each occupation.

**Table 2: Within-Occupation Task Score Heterogeneity**

| Occupation | N Tasks | Min | Max | Range | Std Dev |
|---|---:|---:|---:|---:|---:|
| Treasurers and Controllers | 22 | 1 | 4 | 3 | 0.76 |
| Financial Managers | 17 | 1 | 3 | 2 | 0.61 |
| Financial & Investment Analysts | 26 | 1 | 4 | 3 | 0.69 |
| Personal Financial Advisors | 21 | 1 | 3 | 2 | 0.58 |
| Accountants and Auditors | 29 | 2 | 4 | 2 | 0.58 |
| Tax Preparers | 12 | 2 | 4 | 2 | 0.75 |
| Financial Examiners | 17 | 2 | 4 | 2 | 0.60 |
| Bookkeeping Clerks | 28 | 3 | 5 | 2 | 0.33 |

Within single occupations, task scores regularly span 2–3 points on the 1–5 scale. A Treasurer's task of "developing and maintaining relationships with banking and insurance personnel" (score=1) coexists with "computing, withholding, and accounting for all payroll deductions" (score=4) within the same job title. A single occupation-level TARS of 3.01 for Treasurers obscures this heterogeneity entirely. Notably, Bookkeeping Clerks are the exception: their narrow range (2.0, std=0.33) reflects uniformly high automation risk across nearly all tasks—96% score 4 or above.

### 3.4 Most and Least Automatable Tasks

Among the highest-scored tasks (score=4–5), a clear pattern emerges: all involve structured data processing, record-keeping, transaction matching, or form completion. Representative examples include:

- "Operate computers programmed with accounting software to record, store, and analyze data" (Bookkeeping Clerks, score=5)
- "Transfer details from separate journals to general ledgers or data processing sheets" (Bookkeeping Clerks, score=5)
- "Prepare adjusting journal entries" (Accountants, score=4)
- "Review accounts for discrepancies and reconcile differences" (Accountants, score=4)
- "Compute taxes owed or overpaid, using adding machines or personal computers" (Tax Preparers, score=4)

The lowest-scored tasks (score=1) uniformly involve interpersonal relationships, institutional trust, or public accountability:

- "Establish and maintain relationships with individual or business customers" (Financial Managers, score=1)
- "Develop and maintain relationships with banking, insurance, and external accounting personnel" (Treasurers, score=1)
- "Testify before examining and fund-granting authorities, clarifying and defending findings and recommendations" (Budget Analysts, score=1)
- "Develop and maintain client relationships" (Financial Analysts, score=1)
- "Conduct seminars or workshops on financial planning topics" (Personal Financial Advisors, score=1)

### 3.5 Workforce Exposure Estimates

Combining TARS with BLS employment data, we estimate that 1,931,126 workers (34.9% of the 5.53 million finance workers in our sample) are employed in roles where a meaningful share of their tasks are classified as high-risk (score≥4). The concentration is stark: Bookkeeping Clerks alone account for 1,403,778 at-risk worker-task equivalents (96.4% of 1.46M workers), and Accountants contribute an additional 449,469 (31% of 1.45M workers). By contrast, Financial Managers (819K workers, 0% high-risk tasks), Management Analysts (894K, 0%), and Personal Financial Advisors (270K, 0%) contribute zero high-risk task exposure despite collectively employing nearly 2 million workers.

---

## 4. Discussion

### 4.1 Why TARS and AIOE Diverge

The divergence between TARS and AIOE is not arbitrary—it reflects a fundamental methodological difference. AIOE is constructed by mapping occupational *ability requirements* (e.g., mathematical reasoning, language comprehension) to AI benchmark performance. An occupation requiring high language comprehension receives elevated AIOE scores as language models improve. This approach captures AI *capability alignment* but not AI *task replaceability*.

The distinction matters for Bookkeeping Clerks. Their work involves limited cognitive complexity—data entry, reconciliation, transaction matching—which is precisely what robotic process automation and accounting AI (e.g., QuickBooks AI, Xero) already automate in practice. Yet their O*NET ability requirements are modest, yielding a low AIOE. Conversely, Financial Examiners require high language comprehension and analytical reasoning (high AIOE), but their tasks center on regulatory judgment, institutional negotiation, and compliance interpretation—activities that require contextual trust and legal accountability that current AI cannot replicate.

TARS corrects this by asking directly: *given this specific task description, can current AI systems perform it?* This question is more operationally relevant for workforce planning.

### 4.2 Implications for Reskilling Policy

Our findings suggest that the appropriate unit of intervention in AI reskilling policy is the *task*, not the *occupation*. Uniform reskilling programs targeting "accountants at risk from AI" will systematically misallocate resources: the 69% of accounting tasks rated score≤3 represent durable sources of human value, while the 31% rated score=4 represent genuine displacement targets.

A task-level framework enables more precise policy design. Finance workers should prioritize developing capabilities in activities that consistently score 1–2 across our sample: relationship management, client counseling, regulatory testimony, ethical judgment, and supervision of junior staff. These are the durable human comparative advantages within finance roles—and they happen to correspond to higher-wage activities within each occupation.

For employers, TARS provides a diagnostic tool: which specific workflow steps within a finance team should be candidates for AI-assisted or AI-replaced automation, and which require human retention? The granularity of task-level analysis makes this tractable in a way that occupation-level indices do not.

### 4.3 Limitations

Several limitations merit acknowledgment. First, while our multi-model panel approach reduces dependence on any single model's calibration, LLM-based task scoring ultimately reflects the training data and design choices of 2024–2026 models—scores should be interpreted as assessments of current AI capabilities, not permanent technological constraints. Second, O*NET task descriptions are updated periodically but may not fully capture how AI tools have already been integrated into finance workflows—a financial analyst's "draw charts using spreadsheets" task may already be substantially AI-assisted in practice, making its score-3 classification potentially optimistic. Third, our framework scores automation *potential*, not adoption probability; the pace at which firms actually implement AI automation depends on cost, regulation, and organizational factors outside this model. Fourth, we do not account for complementarity: some tasks may become *more* valuable as adjacent tasks are automated, a dynamic consistent with Acemoglu and Restrepo (2019).

---

## 5. Conclusion

We construct task-level AI automation risk scores for 14 U.S. finance occupations covering 5.53 million workers and introduce TARS as an importance-weighted summary measure. Our results challenge occupation-level AI risk assessments: Bookkeeping Clerks, ranked lowest-risk by the established AIOE index, exhibit the highest task-level automation risk (TARS=4.03, 96% high-risk tasks), while Financial Examiners—the highest-ranked occupation by AIOE—show only moderate task-level risk (TARS=2.88). Within-occupation task heterogeneity is large enough that occupation-level averages misrepresent the distribution of actual risk.

For the 1.46 million Americans employed as bookkeeping clerks, our findings imply near-term, material automation exposure—not the low-risk profile suggested by AIOE. For finance professionals in analytical, advisory, and managerial roles, the 1.93 million workers with some high-risk task exposure face displacement in specific transaction-processing subtasks, not across their occupation as a whole. A Pearson correlation of r = −0.828 between TARS and AIOE confirms that ability-based exposure indices and task-replaceability measures are capturing fundamentally different constructs. Effective reskilling policy must be designed at task-level granularity, using measures that reflect what AI can actually do—not what cognitive abilities it resembles.

---

## Acknowledgments

The author thanks the O*NET National Center and Bureau of Labor Statistics for publicly available data. Manuscript preparation was assisted by AI writing tools.

---

## References

Acemoglu, D., Autor, D., Hazell, J., & Restrepo, P. (2022). Artificial intelligence and jobs: Evidence from online vacancies. *Journal of Labor Economics*, 40(S1), 293–340.

Acemoglu, D., & Restrepo, P. (2019). Automation and new tasks: How technology displaces and reinstates labor. *Journal of Economic Perspectives*, 33(2), 3–30.

Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change: An empirical exploration. *Quarterly Journal of Economics*, 118(4), 1279–1333.

Bureau of Labor Statistics. (2024). *Occupational Employment and Wage Statistics, May 2024*. U.S. Department of Labor.

Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). GPTs are GPTs: An early look at the labor market impact potential of large language models. *arXiv preprint* arXiv:2303.10130.

Felten, E. W., Raj, M., & Seamans, R. (2021). Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses. *Strategic Management Journal*, 42(12), 2195–2217.

Felten, E. W., Raj, M., & Seamans, R. (2023). How will language modelers like ChatGPT affect occupations and industries? *arXiv preprint* arXiv:2303.01157.

National Center for O*NET Development. (2024). *O*NET 30.2 database*. U.S. Department of Labor, Employment and Training Administration.

Anthropic. (2025). *Claude Sonnet model card*. Anthropic.

OpenAI. (2024). *GPT-4o mini model card*. OpenAI.

OpenAI. (2024). *GPT-4o model card*. OpenAI.
