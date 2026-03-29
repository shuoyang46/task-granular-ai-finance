# Beyond Occupation-Level Estimates: Task-Granular AI Automation Risk in Finance

**Shuo Yang, MBA** | Independent Researcher | sy590@georgetown.edu

> Replication code and data for the paper submitted to *Finance Research Letters*.

---

## Abstract

Existing AI automation risk indices assess exposure at the occupational level, masking substantial within-occupation task heterogeneity. Using O\*NET 30.2 task data for 14 U.S. finance occupations (237 tasks, 5.53 million workers), this paper constructs a Task-weighted AI Risk Score (TARS) via LLM-based scoring with a three-model inter-rater panel. TARS and the Felten et al. (2021) AI Occupational Exposure Index (AIOE) are negatively correlated (*r* = −0.828, *p* = 0.003), indicating systematic directional disagreement. Bookkeeping clerks — ranked last by AIOE — rank first by TARS, a 9-position reversal. The findings suggest that reskilling policy should target tasks, not occupations.

---

## Repository Structure

```
├── paper_draft_v1.md          # Paper manuscript (markdown)
├── task_llm_scores.csv        # GPT-4o-mini scores (primary, n=237)
├── task_scores_gpt_4o.csv     # GPT-4o scores (validation, n=237)
├── task_scores_claude.csv     # Claude Sonnet scores (validation, n=237)
├── finance_occ_config.py      # Finance occupation definitions
├── llm_score_tasks.py         # LLM scoring script (GPT-4o-mini)
├── score_tasks_ai.py          # TARS construction and analysis
└── occupation_ai_summary.csv  # Occupation-level TARS summary
```

---

## Data Sources

| Dataset | Source | Access |
|---------|--------|--------|
| Task statements | O\*NET 30.2 | Free at [onetcenter.org](https://www.onetcenter.org/database.html) |
| Employment & wages | BLS OES May 2024 | Free at [bls.gov](https://www.bls.gov/oes/tables.htm) |
| AIOE benchmark | Felten et al. (2021) | Free at [SSRN](https://ssrn.com/abstract=3815668) |
| LLM scores | Generated (included) | See `task_llm_scores.csv` |

O\*NET and BLS files are not included in this repo due to size. Download links above.

---

## Replication

### Requirements
```
pip install openai pandas scipy openpyxl
```

### Steps
1. Download O\*NET 30.2 database into `onet_data/`
2. Download BLS OES May 2024 into root directory as `national_M2024_dl.xlsx`
3. Run LLM scoring (requires OpenAI API key):
   ```bash
   python llm_score_tasks.py
   ```
4. Run analysis:
   ```bash
   python score_tasks_ai.py
   ```

LLM scores are pre-computed and included in CSV files — steps 1–3 are only needed to reproduce scoring from scratch.

---

## Inter-Rater Reliability

| Model Pair | Pearson *r* | Spearman *ρ* | Exact Match | Within ±1 pt |
|---|---|---|---|---|
| GPT-4o-mini vs GPT-4o | 0.809 | 0.799 | 74.3% | 99.2% |
| GPT-4o-mini vs Claude Sonnet | 0.796 | 0.778 | 76.4% | 100.0% |
| GPT-4o vs Claude Sonnet | 0.765 | 0.745 | 55.3% | 96.6% |

---

## Citation

```
Yang, S. (2025). Beyond Occupation-Level Estimates: Task-Granular AI Automation
Risk in Finance. Working paper.
```

---

## License

Code: MIT License. Data (LLM scores): CC BY 4.0.
