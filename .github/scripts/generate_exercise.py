import os
import json
import glob
import re
from datetime import date
import anthropic

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATASET_REFERENCE = """
=== sysuse nlsw88 === (NLSW 1988 extract, 2,246 obs, 17 vars)
Variables WITH missing values: grade (2 missing), industry (14), occupation (9), union (368), hours (4), tenure (15)
Variables with NO missing values: idcode, age (34–46), race (1–3, labeled), married (0/1, labeled), never_married (0/1, labeled), collgrad (0/1, labeled), south (0/1, labeled), smsa (0/1, labeled), c_city (0/1, labeled), wage (1.00–40.75, float), ttl_exp (0.12–28.88, float)

=== sysuse auto === (1978 automobile data, 74 obs, 12 vars)
Variables WITH missing values: rep78 (5 missing)
Variables with NO missing values: price (3291–15906), mpg (12–41), headroom (1.5–5), trunk (5–23), weight (1760–4840), length (142–233), turn (31–51), displacement (79–425), gear_ratio (2.19–3.89), foreign (0/1, labeled)
String variable: make

=== sysuse census === (1980 Census by state, 50 obs, 13 vars, NO missing values)
Variables: region (1–4, labeled), pop, poplt5, pop5_17, pop18p, pop65p, popurban, medage (24.2–34.7), death, marriage, divorce
String variables: state, state2

=== sysuse lifeexp === (Life expectancy 1998, 68 obs, 6 vars)
Variables WITH missing values: gnppc (5 missing), safewater (28 missing)
Variables with NO missing values: region (1–3), popgrowth (-0.5–3), lexp (54–79)
String variable: country

=== sysuse bpwide === (Fictional blood-pressure, 120 obs, 5 vars, NO missing values)
Variables: patient (ID), sex (0/1, labeled), agegrp (1–3, labeled), bp_before (138–185), bp_after (125–185)

=== sysuse cancer === (Patient survival in drug trial, 48 obs, 8 vars, NO missing values)
Variables: studytime (1–39), died (0/1, labeled), drug (1–3, labeled), age (47–67)
System variables: _st, _d, _t, _t0

=== webuse grunfeld === (Investment panel, 200 obs, 6 vars, NO missing values)
Variables: company (1–10), year (1935–1954), invest (0.93–1486.7), mvalue (58.12–6241.7), kstock (0.8–2226.3), time (1–20)
Panel structure: company × year

=== webuse laborsup === (Female labor supply, 500 obs, 6 vars, NO missing values)
Variables: fem_educ (8–16), male_educ (8–16), kids (0–4), other_inc (-16.7–109.6), fem_inc (10–84.6), fem_work (0/1)

=== webuse regsmpl === (NLS women panel 1968–1988, 28,534 obs, 13 vars)
Variables WITH missing values: age (24 missing), grade (2), not_smsa (8), south (8), tenure (433), age2 (24), tenure2 (433)
Variables with NO missing values: idcode, year (68–88), ttl_exp (0–28.88), ln_wage (0–5.26), black (0/1)
Panel structure: idcode × year

=== webuse breathe === (NO2 and children's attention, 1,089 obs, 22 vars)
Variables WITH missing values: react (5 missing), correct (5), omissions (5), age0 (7), overweight (26), breastfeed (1), msmoke (2), feducation (3), siblings_old (8), siblings_young (6)
Variables with NO missing values: no2_class (7.8–52.6), no2_home (2.1–118.7), age (7.5–11.6), sex (0/1, labeled), grade (1–3, labeled), lbweight (0/1, labeled), meducation (1–4, labeled), sev_home, green_home, noise_school (28.8–51.1), sev_school, precip

=== webuse mroz87 === (Mroz 1987 PSID, classic female labor supply, 753 obs, 28 vars, NO missing values)
Variables: taxinc (1500–96000), fedtax (0–31386), hsib (0–8), hfedyrs (0–17), hmedyrs (0–17), wsib (0–8), lfp (0/1, labeled, wife's labor force participation), whrs75 (0–4950, wife's hours worked), kl6 (0–3, kids < 6), k618 (0–8, kids 6–18), wifeage (30–60), wedyrs (5–17, wife's education), wwage75 (0–25, wife's hourly wage 1975), wwage76 (0–9.98), hhrs75 (175–5010, husband's hours), husage (30–60), hedyrs (3–17), hwage75 (0.41–40.51), faminc (1500–96000), mtr (0.44–0.94, marginal tax rate), wmedyrs (0–17), wfedyrs (0–17), unemprt (3–14), smsa (0/1, labeled), wexper (0–45), weduc (0/1, labeled), wmeduc (0/1, labeled), nwinc (-0.03–96)

=== webuse nlsy80 === (NLSY 1980 cross-section, 935 obs, 20 vars)
Variables WITH missing values: brthord (83 missing), meduc (78 missing), feduc (194 missing)
Variables with NO missing values: wage (115–3078, monthly earnings), hours (20–80), iq (50–145), kww (12–56, knowledge of world work), educ (9–18), exper (1–23), tenure (0–22), age (28–38), married (0/1), black (0/1), south (0/1), urban (0/1), sibs (0–14), lwage (4.74–8.03), pcollege (0/1), college (0/1), fcollege (0/1)

=== webuse psidextract === (PSID panel, 4,165 obs, 22 vars, NO missing values)
Variables: exp (1–51), wks (5–52), occ (0/1, labeled), ind (0/1, labeled), south (0/1, labeled), smsa (0/1, labeled), ms (0/1, labeled, marital status), fem (0/1, labeled), union (0/1, labeled), ed (4–17), blk (0/1, labeled), lwage (4.61–8.54), id (1–595), t (1–7)
Panel structure: id × t (7 periods)

=== webuse womenwk === (Women and work, 2,000 obs, 6 vars)
Variables WITH missing values: wage (657 missing — women not working have no observed wage)
Variables with NO missing values: county (0–9), age (20–59), education (10–20), married (0/1), children (0–5)
Note: wage is missing by design for non-employed women — ideal for sample selection exercises.

=== webuse 401k === (Firm-level 401k participation, 4,075 obs, 10 vars, NO missing values)
Variables: partic (100–262659), totemp (105–443040), employ (100–286451), mrate (0–2, match rate), prate (0.004–1, participation rate), age (1–71, plan age), sole (0/1, labeled), ltotemp (4.65–13.0), agesq (1–5041), ltotempsq (21.7–169.0)

=== webuse docvisits === (Doctor visits, 4,412 obs, 10 vars, NO missing values)
Variables: docvis (0–134, count outcome), age (2.5–6.4, in decades), income (-50–281, $1000s), female (0/1), black (0/1), hispanic (0/1), married (0/1), physlim (0/1), private (0/1), chronic (0/1)
""".strip()


def get_dataset_ref_for(exercise_text):
    """Extract the dataset name from an exercise and return its reference block."""
    m = re.search(r'(?:sysuse|webuse)\s+(\w+)', exercise_text)
    if not m:
        return DATASET_REFERENCE  # fallback: give all
    name = m.group(1)
    # Find the matching block
    for block in DATASET_REFERENCE.split("\n\n"):
        if name in block:
            return block
    return DATASET_REFERENCE  # fallback: give all

def count_exercises():
    files = glob.glob(os.path.join(REPO_ROOT, "exercises", "day_*.md"))
    return len(files)

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def get_topic(day):
    if day <= 5:   return "Absolute basics (load data, describe, summarize, tabulate)"
    if day <= 10:  return "Data quality (missingness, impossible values, data types)"
    if day <= 15:  return "Visualization (histogram, scatter, bar, twoway)"
    if day <= 20:  return "Variable creation (generate, replace, recode, label)"
    if day <= 25:  return "Conditional logic and groups (if/in, bysort)"
    if day <= 30:  return "Merging and reshaping (merge, append, reshape)"
    if day <= 35:  return "Loops and macros (forvalues, foreach, local, global)"
    if day <= 40:  return "Inference and regression (ttest, regress, margins)"
    if day <= 45:  return "Regression output (estout, outreg2, coefplot)"
    if day <= 50:  return "Panel data (xtset, xtreg, areg)"
    return "Advanced topics (IV, DiD, LASSO, egen, frames — rotate each day)"

def get_difficulty(day):
    if day <= 5:  return "⬛⬜⬜⬜⬜"
    if day <= 15: return "⬛⬛⬜⬜⬜"
    if day <= 30: return "⬛⬛⬛⬜⬜"
    if day <= 45: return "⬛⬛⬛⬛⬜"
    return "⬛⬛⬛⬛⬛"

def main():
    client = anthropic.Anthropic()

    os.makedirs(os.path.join(REPO_ROOT, "exercises"), exist_ok=True)
    os.makedirs(os.path.join(REPO_ROOT, "feedback"), exist_ok=True)
    os.makedirs(os.path.join(REPO_ROOT, "progress"), exist_ok=True)
    os.makedirs(os.path.join(REPO_ROOT, "solutions"), exist_ok=True)

    N = count_exercises()
    today = N + 1
    today_str = f"{today:03d}"
    yesterday_str = f"{N:03d}" if N >= 1 else None
    five_days_str = f"{N-4:03d}" if N >= 5 else None

    files_changed = []
    retries_yesterday = []
    retries_5day = []

    # --- Step 1: Review ALL unreviewed solutions ---
    solution_files = sorted(glob.glob(os.path.join(REPO_ROOT, "solutions", "day_*.do")))
    for sol_path in solution_files:
        sol_name = os.path.basename(sol_path)                   # day_006.do
        day_label = sol_name.replace("day_", "").replace(".do", "")  # "006"
        day_num = int(day_label)

        feedback_path = os.path.join(REPO_ROOT, "feedback", f"day_{day_label}.md")
        exercise_path = os.path.join(REPO_ROOT, "exercises", f"day_{day_label}.md")
        progress_path = os.path.join(REPO_ROOT, "progress", f"day_{day_label}_status.json")

        # Skip if feedback already exists
        if read_file(feedback_path):
            continue

        solution = read_file(sol_path)
        exercise = read_file(exercise_path)

        if not solution or not exercise:
            continue

        print(f"Generating feedback for Day {day_num}...")

        dataset_ref = get_dataset_ref_for(exercise)

        prompt = f"""You are reviewing a Stata solution written by Francesco, a beginner learning Stata.

EXERCISE (day_{day_label}.md):
{exercise}

SOLUTION (day_{day_label}.do):
{solution}

DATASET REFERENCE (ground truth — use this to verify claims about variables, missingness, and ranges):
{dataset_ref}

Review each numbered task. You cannot run the code, so judge based on whether the Stata commands are syntactically and logically correct for the task. Use the dataset reference above to verify whether the student's comments about variable properties (e.g., missing values, ranges) are correct.

For each task assign: PASS, PARTIAL (attempted but has errors or gaps), or FAIL (not addressed).

Respond with two sections:

1. A markdown feedback file with this exact structure:
# Feedback: Day {day_num}

**Overall**: [one-line summary]

## Task-by-task

| Task | Status | Comment |
|------|--------|---------|
| 1. [name] | PASS/PARTIAL/FAIL | [brief honest comment] |
| 2. [name] | ... | ... |
| 3. [name] | ... | ... |
| 4. [name] | ... | ... |
| Bonus | PASS/SKIP | ... |

## What to work on
[2-3 sentences of direct, actionable advice for failed/partial tasks. Be honest, not encouraging about wrong code.]

2. Then on a new line write exactly: ---JSON---
Then a JSON object like:
{{"day": {day_num}, "tasks": [{{"number": 1, "name": "...", "status": "pass"}}, ...]}}

Only include numbered tasks (1-4), not the bonus."""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text

        if "---JSON---" in raw:
            parts = raw.split("---JSON---")
            feedback_text = parts[0].strip()
            try:
                status_data = json.loads(parts[1].strip())
                write_file(progress_path, json.dumps(status_data, indent=2))
                files_changed.append(f"progress/day_{day_label}_status.json")
            except Exception:
                pass
        else:
            feedback_text = raw.strip()

        write_file(feedback_path, feedback_text)
        files_changed.append(f"feedback/day_{day_label}.md")

    # --- Step 2: Collect retries (from most recent and 5-days-ago progress) ---
    if yesterday_str:
        progress = read_file(os.path.join(REPO_ROOT, "progress", f"day_{yesterday_str}_status.json"))
        if progress:
            data = json.loads(progress)
            retries_yesterday = [t for t in data.get("tasks", []) if t["status"] in ("fail", "partial")]

    if five_days_str:
        progress = read_file(os.path.join(REPO_ROOT, "progress", f"day_{five_days_str}_status.json"))
        if progress:
            data = json.loads(progress)
            retries_5day = [t for t in data.get("tasks", []) if t["status"] in ("fail", "partial")]

    # --- Step 3: Generate today's exercise ---
    topic = get_topic(today)
    difficulty = get_difficulty(today)

    retry_context = ""
    if retries_yesterday:
        names = ", ".join(f"Task {t['number']} ({t['name']})" for t in retries_yesterday)
        retry_context += f"\nFailed tasks from yesterday (Day {N}) to include as retries: {names}"
    if retries_5day:
        names = ", ".join(f"Task {t['number']} ({t['name']})" for t in retries_5day)
        retry_context += f"\nFailed tasks from 5 days ago (Day {N-4}) to include as retries: {names}"

    if retries_yesterday and yesterday_str:
        ex_yesterday = read_file(os.path.join(REPO_ROOT, "exercises", f"day_{yesterday_str}.md")) or ""
    else:
        ex_yesterday = ""

    if retries_5day and five_days_str:
        ex_5day = read_file(os.path.join(REPO_ROOT, "exercises", f"day_{five_days_str}.md")) or ""
    else:
        ex_5day = ""

    retry_exercises_context = ""
    if ex_yesterday:
        retry_exercises_context += f"\nOriginal exercise Day {N}:\n{ex_yesterday}\n"
    if ex_5day:
        retry_exercises_context += f"\nOriginal exercise Day {N-4}:\n{ex_5day}\n"

    # Build list of datasets recently used (last 3 exercises) to enforce rotation
    recent_datasets = []
    for i in range(max(1, today - 3), today):
        ex = read_file(os.path.join(REPO_ROOT, "exercises", f"day_{i:03d}.md"))
        if ex:
            for line in ex.split("\n"):
                if line.startswith("**Dataset**"):
                    recent_datasets.append(line)
                    break

    rotation_note = ""
    if recent_datasets:
        rotation_note = "\n\nRecent exercises used these datasets (do NOT reuse unless no alternative fits):\n"
        rotation_note += "\n".join(f"  - {d}" for d in recent_datasets)

    prompt = f"""You are creating a daily Stata coding exercise for Francesco, a beginner learning Stata for labor economics research at Bocconi University.

Today is Day {today}. Topic area: {topic}

CRITICAL RULE — NEVER INVENT DATASET PROPERTIES:
Every claim you make about a variable (missing values, range, type, labels) MUST match
the reference tables below. If you say a variable has missing values, it must actually
have missing values according to the reference. If a variable has zero missing values,
do NOT write tasks that assume it has missing values.

AVAILABLE DATASETS (use ONLY these):

{DATASET_REFERENCE}
{rotation_note}

Write a markdown exercise file with this EXACT structure (no deviations):

# Day {today}: [specific topic name]

**Dataset**: `sysuse/webuse dataset_name`
**Estimated time**: ~25 minutes
**Difficulty**: {difficulty}

## Background
[2 sentences: what the dataset contains and why this topic is useful for quantitative research]

## Your tasks

1. **[Task name]** — [clear, specific instruction]
2. **[Task name]** — [slightly more involved]
3. **[Task name]** — [builds on task 2]
4. **[Task name]** — [requires combining two concepts]
5. *(Bonus)* **[Task name]** — [optional harder challenge]

## Hints
<details>
<summary>Click to reveal hints (try first!)</summary>

- **Hint 1**: [guide toward the right command — do NOT give the answer]
- **Hint 2**: [second targeted hint for a different task]

</details>

## Solution check
Save your solution as `solutions/day_{today_str}.do` and push to the repo.

---
*Exercise {today} in Francesco's Stata learning series.*{retry_context}

{retry_exercises_context}

If there are retry tasks listed above, append this section AFTER the main exercise (after the closing line):

---

## Retries

[Include only applicable sub-sections]

### From yesterday (Day {N})
[For each failed task: restate it clearly as a standalone mini-exercise with a fresh hint. Label: "Retry: Day {N}, Task X — original task name"]

### From 5 days ago (Day {N-4})
[Same format. Label: "Retry: Day {N-4}, Task X — original task name"]

Rules:
- Every variable property you mention MUST match the reference above — do not invent missing values, ranges, or types
- Do NOT give away solutions in hints
- Write entirely in English
- Tasks must build progressively"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    exercise_content = response.content[0].text.strip()

    exercise_path = os.path.join(REPO_ROOT, "exercises", f"day_{today_str}.md")
    write_file(exercise_path, exercise_content)
    files_changed.append(f"exercises/day_{today_str}.md")

    # Write commit message
    first_line = exercise_content.split("\n")[0].replace("# ", "")
    commit_msg = f"Day {today}: {first_line}"
    if retries_yesterday or retries_5day:
        commit_msg += " (+ retries)"
    feedback_days = [f for f in files_changed if f.startswith("feedback/")]
    if feedback_days:
        day_nums = [f.replace("feedback/day_", "").replace(".md", "").lstrip("0") or "0" for f in feedback_days]
        commit_msg += f" (+ feedback Day {', '.join(day_nums)})"

    with open("/tmp/commit_message.txt", "w") as f:
        f.write(commit_msg)

    print(f"Done. Files written: {', '.join(files_changed)}")
    print(f"Commit message: {commit_msg}")

if __name__ == "__main__":
    main()
