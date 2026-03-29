"""
Score O*NET finance tasks on AI automation potential
Uses a rule-based rubric + prepares for LLM panel scoring
"""
import pandas as pd
import numpy as np
import os
import json
import re

DATA_DIR = "d:/R/research-warn-act"
ONET_DIR = os.path.join(DATA_DIR, "onet_data", "db_30_2_text")

# ============================================================
# Step 1: Load O*NET tasks for finance occupations
# ============================================================
FINANCE_OCCS = {
    "11-3031.00": "Financial Managers",
    "11-3031.01": "Treasurers and Controllers",
    "11-3031.02": "Financial Managers, Branch or Department",
    "13-2011.00": "Accountants and Auditors",
    "13-2051.00": "Financial and Investment Analysts",
    "13-2052.00": "Personal Financial Advisors",
    "13-2061.00": "Financial Examiners",
    "13-2031.00": "Budget Analysts",
    "13-2041.00": "Credit Analysts",
    "13-2082.00": "Tax Preparers",
    "13-2099.00": "Financial Specialists, All Other",
    "13-1111.00": "Management Analysts",
    "13-2054.00": "Financial Risk Specialists",
    "43-3031.00": "Bookkeeping, Accounting, and Auditing Clerks",
}

tasks = pd.read_csv(os.path.join(ONET_DIR, "Task Statements.txt"), sep="\t")
task_ratings = pd.read_csv(os.path.join(ONET_DIR, "Task Ratings.txt"), sep="\t")

finance_tasks = tasks[tasks["O*NET-SOC Code"].isin(FINANCE_OCCS.keys())].copy()
finance_tasks["Occupation"] = finance_tasks["O*NET-SOC Code"].map(FINANCE_OCCS)

print(f"Finance tasks loaded: {len(finance_tasks)}")
print(f"Occupations: {finance_tasks['Occupation'].nunique()}")

# Get task importance ratings
importance = task_ratings[
    (task_ratings["O*NET-SOC Code"].isin(FINANCE_OCCS.keys())) &
    (task_ratings["Scale ID"] == "IM")  # Importance
].copy()
importance = importance[["O*NET-SOC Code", "Task ID", "Data Value"]].rename(
    columns={"Data Value": "importance"}
)

finance_tasks = finance_tasks.merge(importance, on=["O*NET-SOC Code", "Task ID"], how="left")

# ============================================================
# Step 2: Rule-based AI automation scoring rubric
# ============================================================
# Score 1-5: 1=very hard to automate, 5=very easy to automate

# Keyword-based signals for automation potential
HIGH_AUTO_SIGNALS = [
    # Data processing / calculation
    (r'\b(?:calculat|comput|tabulate|tally)\b', 1.0),
    (r'\b(?:record|enter|input|post|log)\b.*\b(?:data|transaction|entry|record)\b', 0.8),
    (r'\b(?:reconcil|verify|match|compare|check)\b.*\b(?:record|account|balance|statement)\b', 0.7),
    (r'\b(?:prepare|generate|produce|create)\b.*\b(?:report|statement|form|return|invoice|bill)\b', 0.6),
    (r'\b(?:compile|aggregate|summarize|consolidate)\b.*\b(?:data|information|record|report)\b', 0.7),
    (r'\b(?:classify|categorize|code|sort)\b', 0.6),
    (r'\b(?:process|handle)\b.*\b(?:payroll|payment|transaction|deposit|disbursement)\b', 0.7),
    (r'\b(?:monitor|track)\b.*\b(?:status|balance|inventory|account)\b', 0.5),
    (r'\b(?:file|submit)\b.*\b(?:tax|return|form|report)\b', 0.6),
    (r'\b(?:transfer|copy|duplicate)\b', 0.5),
]

LOW_AUTO_SIGNALS = [
    # Interpersonal / relationship
    (r'\b(?:establish|maintain|develop|build)\b.*\b(?:relationship|rapport)\b', -0.8),
    (r'\b(?:negotiate|mediat|persuad|convinc)\b', -0.7),
    (r'\b(?:counsel|advise|consult|guid)\b.*\b(?:client|customer|individual|employee)\b', -0.6),
    (r'\b(?:communicat|present|explain)\b.*\b(?:stakeholder|board|director|management|investor)\b', -0.5),
    (r'\b(?:recruit|hire|interview|train|mentor|coach|supervis)\b', -0.7),
    (r'\b(?:network|outreach)\b', -0.6),
    # Strategic judgment
    (r'\b(?:plan|direct|coordinate|oversee|lead|manage)\b.*\b(?:activit|operation|program|staff|team)\b', -0.5),
    (r'\b(?:develop|design|create)\b.*\b(?:strateg|polic|procedure|guideline|framework)\b', -0.6),
    (r'\b(?:evaluat|assess|judg|determin)\b.*\b(?:risk|need|performance|compliance|effectiveness)\b', -0.3),
    (r'\b(?:recommend|propos|suggest)\b.*\b(?:change|improvement|action|solution)\b', -0.4),
    (r'\b(?:resolv|solv)\b.*\b(?:problem|issue|dispute|conflict)\b', -0.5),
]

def score_task_rule_based(task_text):
    """Score a task 1-5 on AI automation potential using keyword signals"""
    high_score = 0.0
    low_score = 0.0
    task_lower = task_text.lower()

    for pattern, weight in HIGH_AUTO_SIGNALS:
        if re.search(pattern, task_lower):
            high_score += weight

    for pattern, weight in LOW_AUTO_SIGNALS:
        if re.search(pattern, task_lower):
            low_score += abs(weight)

    # Net score: high automation signals push up, low push down
    if high_score > 0 and low_score == 0:
        score = 3.5 + min(high_score, 1.5)  # 3.5 - 5.0
    elif low_score > 0 and high_score == 0:
        score = 2.5 - min(low_score, 1.5)  # 1.0 - 2.5
    elif high_score > 0 and low_score > 0:
        # Mixed signals - lean toward middle but favor stronger signal
        net = high_score - low_score
        score = 3.0 + net * 0.5
    else:
        # No signals matched - use secondary heuristics
        if re.search(r'\b(?:data|number|figure|amount|rate|balance|total)\b', task_lower):
            score = 3.5  # data-heavy = somewhat automatable
        elif re.search(r'\b(?:people|client|customer|staff|team|employee)\b', task_lower):
            score = 2.5  # people-heavy = less automatable
        else:
            score = 3.0

    return round(max(1.0, min(5.0, score)), 1)

# ============================================================
# Step 3: Score all tasks
# ============================================================
print("\nScoring tasks...")

finance_tasks["ai_auto_score"] = finance_tasks["Task"].apply(score_task_rule_based)

# Categorize tasks
def categorize_task(task_text):
    task_lower = task_text.lower()
    if re.search(r'(?:calculat|comput|reconcil|record|enter|classify|process|prepare.*report|file.*tax|prepare.*bill|prepare.*invoice)', task_lower):
        return "Routine/Computational"
    elif re.search(r'(?:analyz|evaluat|assess|examin|investigat|review|inspect|audit)', task_lower):
        return "Analytical/Judgment"
    elif re.search(r'(?:communicat|present|advise|counsel|negotiate|establish.*relation|network|recruit|train|supervis|mentor)', task_lower):
        return "Interpersonal/Communication"
    elif re.search(r'(?:plan|direct|coordinate|oversee|manage|lead|develop.*strateg|develop.*polic)', task_lower):
        return "Strategic/Managerial"
    else:
        return "Mixed/Other"

finance_tasks["task_category"] = finance_tasks["Task"].apply(categorize_task)

# ============================================================
# Step 4: Analysis
# ============================================================
print("\n" + "=" * 70)
print("TASK-LEVEL AI AUTOMATION RISK IN FINANCE OCCUPATIONS")
print("=" * 70)

# Summary by occupation
print("\n--- Average AI Automation Score by Occupation ---")
occ_summary = finance_tasks.groupby(["O*NET-SOC Code", "Occupation"]).agg(
    n_tasks=("Task", "size"),
    avg_score=("ai_auto_score", "mean"),
    median_score=("ai_auto_score", "median"),
    high_risk=("ai_auto_score", lambda x: (x >= 4.0).sum()),
    low_risk=("ai_auto_score", lambda x: (x <= 2.0).sum()),
    avg_importance=("importance", "mean"),
).reset_index()
occ_summary["pct_high_risk"] = occ_summary["high_risk"] / occ_summary["n_tasks"] * 100
occ_summary = occ_summary.sort_values("avg_score", ascending=False)

print(f"\n{'Occupation':<45} {'Tasks':>5} {'Avg':>5} {'High%':>6} {'Low#':>5}")
print("-" * 70)
for _, row in occ_summary.iterrows():
    print(f"{row['Occupation']:<45} {row['n_tasks']:>5} {row['avg_score']:>5.2f} "
          f"{row['pct_high_risk']:>5.1f}% {row['low_risk']:>5.0f}")

# Summary by task category
print("\n--- AI Automation Score by Task Category ---")
cat_summary = finance_tasks.groupby("task_category").agg(
    n_tasks=("Task", "size"),
    avg_score=("ai_auto_score", "mean"),
    std_score=("ai_auto_score", "std"),
).reset_index()
cat_summary = cat_summary.sort_values("avg_score", ascending=False)

print(f"\n{'Category':<30} {'Tasks':>5} {'Avg Score':>10} {'Std':>6}")
print("-" * 55)
for _, row in cat_summary.iterrows():
    print(f"{row['task_category']:<30} {row['n_tasks']:>5} {row['avg_score']:>10.2f} {row['std_score']:>6.2f}")

# Top most automatable tasks
print("\n--- Top 15 Most Automatable Tasks (Score >= 4.0) ---")
high_auto = finance_tasks.nlargest(15, "ai_auto_score")
for _, row in high_auto.iterrows():
    print(f"  [{row['ai_auto_score']:.1f}] {row['Occupation'][:25]:<25} | {row['Task'][:80]}")

# Top most AI-resistant tasks
print("\n--- Top 15 Most AI-Resistant Tasks (Score <= 2.0) ---")
low_auto = finance_tasks.nsmallest(15, "ai_auto_score")
for _, row in low_auto.iterrows():
    print(f"  [{row['ai_auto_score']:.1f}] {row['Occupation'][:25]:<25} | {row['Task'][:80]}")

# The key finding: within-occupation variance
print("\n--- Within-Occupation Task Variance (The Key Finding) ---")
occ_var = finance_tasks.groupby("Occupation").agg(
    score_range=("ai_auto_score", lambda x: x.max() - x.min()),
    score_std=("ai_auto_score", "std"),
    min_score=("ai_auto_score", "min"),
    max_score=("ai_auto_score", "max"),
    n_tasks=("Task", "size"),
).reset_index()
occ_var = occ_var.sort_values("score_range", ascending=False)

print(f"\n{'Occupation':<40} {'Range':>6} {'Min':>5} {'Max':>5} {'Std':>5} {'N':>3}")
print("-" * 70)
for _, row in occ_var.iterrows():
    print(f"{row['Occupation']:<40} {row['score_range']:>6.2f} {row['min_score']:>5.2f} "
          f"{row['max_score']:>5.2f} {row['score_std']:>5.2f} {row['n_tasks']:>3.0f}")

# Importance-weighted score (tasks that matter more, weighted higher)
print("\n--- Importance-Weighted AI Risk Score (TARS) ---")
finance_tasks["weighted_score"] = finance_tasks["ai_auto_score"] * finance_tasks["importance"].fillna(3.0)
tars = finance_tasks.groupby("Occupation").agg(
    tars=("weighted_score", "sum"),
    total_importance=("importance", "sum"),
).reset_index()
tars["tars_normalized"] = tars.apply(
    lambda r: r["tars"] / r["total_importance"] if r["total_importance"] > 0 else np.nan, axis=1
)
tars = tars.sort_values("tars_normalized", ascending=False)

print(f"\n{'Occupation':<45} {'TARS (1-5)':>10}")
print("-" * 60)
for _, row in tars.iterrows():
    if pd.isna(row["tars_normalized"]):
        continue
    bar = "#" * int(row["tars_normalized"] * 5)
    print(f"{row['Occupation']:<45} {row['tars_normalized']:>6.2f}  {bar}")

# ============================================================
# Step 5: BLS Employment data (manual for now)
# ============================================================
# Source: BLS OES May 2024
BLS_EMPLOYMENT = {
    "Financial Managers": 781_200,
    "Treasurers and Controllers": 0,  # subset of Financial Managers
    "Financial Managers, Branch or Department": 0,  # subset
    "Accountants and Auditors": 1_538_400,
    "Financial and Investment Analysts": 328_600,
    "Personal Financial Advisors": 263_200,
    "Financial Examiners": 68_400,
    "Budget Analysts": 55_100,
    "Credit Analysts": 69_600,
    "Tax Preparers": 57_300,
    "Financial Specialists, All Other": 126_900,
    "Management Analysts": 979_400,
    "Financial Risk Specialists": 101_200,
    "Bookkeeping, Accounting, and Auditing Clerks": 1_533_000,
}

print("\n--- Workforce Impact Estimate ---")
total_workers = 0
high_risk_workers = 0
for _, row in occ_summary.iterrows():
    occ = row["Occupation"]
    emp = BLS_EMPLOYMENT.get(occ, 0)
    if emp > 0:
        pct_risk = row["pct_high_risk"] / 100
        at_risk = int(emp * pct_risk)
        total_workers += emp
        high_risk_workers += at_risk
        print(f"  {occ:<40} {emp:>10,} workers | {pct_risk*100:>5.1f}% high-risk tasks | "
              f"~{at_risk:>10,} worker-task-equivalents at risk")

print(f"\n  TOTAL: {total_workers:,} finance workers")
print(f"  HIGH-RISK TASK EXPOSURE: ~{high_risk_workers:,} worker-task-equivalents")
print(f"  That's {high_risk_workers/total_workers*100:.1f}% of finance workforce has significant AI-automatable tasks")

# Save
output = finance_tasks[["O*NET-SOC Code", "Occupation", "Task ID", "Task",
                         "importance", "ai_auto_score", "task_category"]].copy()
output.to_csv(f"{DATA_DIR}/task_ai_scores.csv", index=False)
occ_summary.to_csv(f"{DATA_DIR}/occupation_ai_summary.csv", index=False)

print(f"\nSaved to task_ai_scores.csv and occupation_ai_summary.csv")
print("Done.")
