import os
import json
import glob
from datetime import date
import anthropic

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    # --- Step 1: Review yesterday's solution ---
    if yesterday_str:
        solution_path = os.path.join(REPO_ROOT, "solutions", f"day_{yesterday_str}.do")
        feedback_path = os.path.join(REPO_ROOT, "feedback", f"day_{yesterday_str}.md")
        exercise_path = os.path.join(REPO_ROOT, "exercises", f"day_{yesterday_str}.md")
        progress_path = os.path.join(REPO_ROOT, "progress", f"day_{yesterday_str}_status.json")

        solution = read_file(solution_path)
        exercise = read_file(exercise_path)

        if solution and exercise and not read_file(feedback_path):
            prompt = f"""You are reviewing a Stata solution written by Francesco, a beginner learning Stata.

EXERCISE (day_{yesterday_str}.md):
{exercise}

SOLUTION (day_{yesterday_str}.do):
{solution}

Review each numbered task. You cannot run the code, so judge based on whether the Stata commands are syntactically and logically correct for the task.

For each task assign: PASS, PARTIAL (attempted but has errors or gaps), or FAIL (not addressed).

Respond with two sections:

1. A markdown feedback file with this exact structure:
# Feedback: Day {N}

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
{{"day": {N}, "tasks": [{{"number": 1, "name": "...", "status": "pass"}}, ...]}}

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
                    files_changed.append(f"progress/day_{yesterday_str}_status.json")
                except Exception:
                    pass
            else:
                feedback_text = raw.strip()

            write_file(feedback_path, feedback_text)
            files_changed.append(f"feedback/day_{yesterday_str}.md")

    # --- Step 2: Collect retries ---
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

    prompt = f"""You are creating a daily Stata coding exercise for Francesco, a beginner learning Stata for labor economics research at Bocconi University.

Today is Day {today}. Topic area: {topic}

Use ONLY Stata built-in datasets: sysuse auto, sysuse nlsw88, sysuse lifeexp, sysuse bpwide, sysuse cancer, sysuse census, webuse grunfeld, webuse laborsup, webuse regsmpl, webuse breathe.

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
- Only built-in Stata datasets
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
    if yesterday_str and read_file(os.path.join(REPO_ROOT, "feedback", f"day_{yesterday_str}.md")):
        commit_msg += f" (+ feedback Day {N})"

    with open("/tmp/commit_message.txt", "w") as f:
        f.write(commit_msg)

    print(f"Done. Files written: {', '.join(files_changed)}")
    print(f"Commit message: {commit_msg}")

if __name__ == "__main__":
    main()
