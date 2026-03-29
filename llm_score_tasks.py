"""
LLM Panel Scoring of 237 Finance Tasks
Uses GPT-4o-mini API to score each task on AI automation potential (1-5)
"""
import pandas as pd
import numpy as np
import json, time, os, urllib.request

DATA_DIR = "d:/R/research-warn-act"
ONET_DIR = os.path.join(DATA_DIR, "onet_data", "db_30_2_text")
API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")

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

PROMPT = """You are an expert in AI capabilities and labor economics (2026).

Score the following occupational task on AI automation potential:
1 = Very hard to automate (requires interpersonal trust, physical presence, creativity, ethical judgment)
2 = Low potential (AI assists but human does the core work)
3 = Moderate (AI handles routine parts, human handles judgment/exceptions)
4 = High potential (AI does most of it, human reviews/monitors)
5 = Fully automatable (AI can independently complete this task today in 2026)

Consider: LLMs, RPA, agentic AI, specialized financial AI tools available in 2026.

Occupation: {occupation}
Task: {task}

Respond ONLY with valid JSON:
{{"score": <1-5>, "confidence": "<high|medium|low>", "reasoning": "<one sentence>", "key_factor": "<main barrier or enabler>"}}"""

def call_gpt(occupation, task, retries=3):
    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": PROMPT.format(occupation=occupation, task=task)}],
        "max_tokens": 150,
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=payload,
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())
            result = json.loads(resp["choices"][0]["message"]["content"])
            return {"score": int(result.get("score", 3)), "confidence": result.get("confidence", "medium"),
                    "reasoning": result.get("reasoning", ""), "key_factor": result.get("key_factor", "")}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  FAILED: {e}")
                return {"score": 3, "confidence": "low", "reasoning": "API error", "key_factor": ""}

# Load tasks
tasks = pd.read_csv(os.path.join(ONET_DIR, "Task Statements.txt"), sep="\t")
ratings = pd.read_csv(os.path.join(ONET_DIR, "Task Ratings.txt"), sep="\t")
finance_tasks = tasks[tasks["O*NET-SOC Code"].isin(FINANCE_OCCS.keys())].copy()
finance_tasks["Occupation"] = finance_tasks["O*NET-SOC Code"].map(FINANCE_OCCS)
importance = ratings[(ratings["O*NET-SOC Code"].isin(FINANCE_OCCS.keys())) & (ratings["Scale ID"] == "IM")][
    ["O*NET-SOC Code", "Task ID", "Data Value"]].rename(columns={"Data Value": "importance"})
finance_tasks = finance_tasks.merge(importance, on=["O*NET-SOC Code", "Task ID"], how="left").reset_index(drop=True)

output_path = os.path.join(DATA_DIR, "task_llm_scores.csv")
existing = pd.read_csv(output_path) if os.path.exists(output_path) else pd.DataFrame()
done_ids = set(existing["Task ID"].astype(str)) if not existing.empty else set()

print(f"Tasks: {len(finance_tasks)} | Already done: {len(done_ids)} | Remaining: {len(finance_tasks)-len(done_ids)}")

results = []
for i, row in finance_tasks.iterrows():
    if str(row["Task ID"]) in done_ids:
        continue
    print(f"[{i+1}/{len(finance_tasks)}] {row['Occupation'][:28]:<28} | {row['Task'][:55]}")
    s = call_gpt(row["Occupation"], row["Task"])
    results.append({"O*NET-SOC Code": row["O*NET-SOC Code"], "Occupation": row["Occupation"],
                    "Task ID": str(row["Task ID"]), "Task": row["Task"],
                    "importance": row.get("importance", np.nan),
                    "gpt_score": s["score"], "gpt_confidence": s["confidence"],
                    "gpt_reasoning": s["reasoning"], "gpt_key_factor": s["key_factor"]})
    if len(results) % 25 == 0:
        out = pd.concat([existing, pd.DataFrame(results)], ignore_index=True) if not existing.empty else pd.DataFrame(results)
        out.to_csv(output_path, index=False)
        print(f"  >> Checkpoint saved ({len(out)} total)")
    time.sleep(0.3)

if results:
    full = pd.concat([existing, pd.DataFrame(results)], ignore_index=True) if not existing.empty else pd.DataFrame(results)
    full.to_csv(output_path, index=False)
else:
    full = existing

print(f"\nTotal scored: {len(full)}")
print("\n=== Score Distribution ===")
for s in range(1, 6):
    n = (full["gpt_score"] == s).sum()
    print(f"  {s}: {n:3d} ({n/len(full)*100:.1f}%) {'#'*int(n/len(full)*50)}")

print("\n=== Avg Score by Occupation (sorted) ===")
occ = full.groupby("Occupation").agg(n=("gpt_score","size"), mean=("gpt_score","mean"),
    pct_high=("gpt_score", lambda x: (x>=4).sum()/len(x)*100)).sort_values("mean", ascending=False)
for name, r in occ.iterrows():
    print(f"  {name:<45} avg={r['mean']:.2f}  high%={r['pct_high']:.0f}%")

print("\n=== Top 10 Most Automatable ===")
for _, r in full.nlargest(10, "gpt_score").iterrows():
    print(f"  [{r['gpt_score']}] {r['Occupation'][:25]:<25} | {r['Task'][:65]}")

print("\n=== Top 10 Most AI-Resistant ===")
for _, r in full.nsmallest(10, "gpt_score").iterrows():
    print(f"  [{r['gpt_score']}] {r['Occupation'][:25]:<25} | {r['Task'][:65]}")

full["importance_w"] = pd.to_numeric(full["importance"], errors="coerce").fillna(3.0)
full["weighted"] = full["gpt_score"] * full["importance_w"]
tars = full.groupby("Occupation").apply(lambda x: x["weighted"].sum()/x["importance_w"].sum()).reset_index(name="TARS")
print("\n=== TARS (Importance-Weighted Score) ===")
for _, r in tars.sort_values("TARS", ascending=False).iterrows():
    print(f"  {r['Occupation']:<45} {r['TARS']:.3f}  {'#'*int(r['TARS']*8)}")

print(f"\nDone. Saved: {output_path}")
