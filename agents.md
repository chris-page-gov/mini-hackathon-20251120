# agents.md – Suggested agent roles and instructions

This file defines a light‑weight agent pattern you can use with ChatGPT (Deep Research and regular chat), Codex‑style tools, or GitHub Copilot Chat.

You do not need a fully automated agent framework to benefit from this – you can simply copy and paste the relevant prompts into each tool and act as the human orchestrator.

---

## 1. Orchestrator (you + a general LLM)

**Role**

- Decide which dataset and SME question to tackle.
- Select one of the nine strategies (see `plans/`).
- Coordinate Deep Research, Code, and Storytelling agents.
- Keep the work focused on a single clear narrative for the final presentation.

**Checklist**

1. Pick dataset + SME question.
2. Pick strategy plan file and skim it.
3. Run Deep Research prompt (optional but useful).
4. Run Code agent prompt to build the pipeline.
5. Run Insight and Slide prompts.
6. Iterate until:
   - the story is clear,
   - the visuals are readable,
   - the “so what?” is obvious for a non‑technical audience.

---

## 2. Deep Research Agent

**Intended tool**: ChatGPT Deep Research (or similar multi‑step research mode).

**Goal**

- Quickly gather context on:
  - the chosen dataset,
  - key indicators and their definitions,
  - how others have analysed similar questions,
  - potential pitfalls (e.g. comparability over time, data gaps).

**Usage**

- Copy `prompts/deep_research_prompt.md`.
- Fill in:
  - `{{DATASET_NAME}}`,
  - `{{SME_QUESTION}}`,
  - `{{PLAN_FILE}}` (optional, if you want it to read the plan).
- Paste into the Deep Research tool.

---

## 3. Code & Data Agent

**Intended tool**: ChatGPT with Code Interpreter, GitHub Copilot Chat, or another code‑capable LLM (Codex‑style).

**Goal**

- Implement the plan from `plans/<strategy>.md` as working code.
- Produce:
  - a clean, documented Python notebook or script,
  - one or more CSVs with summarised data,
  - clear chart specifications for your visualisation tool of choice.

**Key behaviours to request**

- Ask it to:
  - explain every major transformation step in comments,
  - log assumptions (for example: mapping of region codes),
  - keep everything in a single notebook or script unless you have time to modularise.

**Usage**

- Copy `prompts/code_agent_prompt.md`.
- Fill in:
  - `{{DATASET_NAME}}`,
  - `{{STRATEGY_NAME}}`,
  - `{{PLAN_FILE}}`,
  - details of your local file paths.
- Paste into your code‑capable LLM.

---

## 4. Insight / Narrative Agent

**Intended tool**: standard ChatGPT‑style chat.

**Goal**

- Turn your tables and charts into:
  - a short narrative,
  - a set of key messages for decision‑makers,
  - a small set of “calls to action” or policy questions.

**Usage**

- Copy `prompts/insight_prompt.md`.
- Paste in:
  - 3–5 key charts (described in words if needed),
  - any headline numbers,
  - who the audience is.
- Use the output as the basis for your presentation script.

---

## 5. Slide Assembly Agent

**Intended tool**: standard ChatGPT‑style chat.

**Goal**

- Generate slide outlines and speaker notes that you can paste into the `Presentation Submission.potx` template.

**Usage**

- Copy `prompts/slide_prompt.md`.
- Provide:
  - the chosen dataset and strategy,
  - the one‑sentence “so what?” for your work,
  - your key visual elements (e.g. one main chart plus a supporting view).
- Ask for:
  - slide titles,
  - bullet points,
  - speaker notes.

---

## 6. Common constraints for all agents

When you use or adapt these prompts, it helps to include some shared constraints:

- **Audience**: non‑technical decision‑makers who understand policy questions but not statistical details.
- **Tone**: clear, direct, and honest about limitations. Avoid hype.
- **Reproducibility**: code and steps should be written so another team can pick them up later.
- **Time‑boxing**: keep scope realistic for a mini hackathon – prioritise one strong story over many half‑finished views.

You can refine this file after the hackathon to match how your organisation usually runs these exercises.
