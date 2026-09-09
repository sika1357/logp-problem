# MANIFEST - file → RLS form field

Open https://studio.mercor.com/, create a task in your domain, paste per the table, then click magic-star → STEM Software Runner for the Taiga eval.

> **After Taiga runs the task, run `submission-check` on the runs before trusting the result** - don't skip it.

## Grading directive (paste into the Grading Guidance field)

The platform reads per-field tolerances and abs/rel types from this line. Put it in the Grading Guidance field together with the golden answer:

```
[grader: tolerance=[0.05], type=[abs]]
```
rel = fraction (0.02 = 2%); abs = the field's own units. Types are explicit on purpose - the platform defaults to ABSOLUTE when `type` is omitted. Leave the legacy numeric **Tolerance** field blank.

> **Re-run `export.py` and re-paste this line after ANY edit to `golden/expected.json`** (tolerances, types, or the answer). Nothing binds the pasted text to the file, so a stale paste grades against the old tolerances while the local gate passes.

_Direction: **inverse**._

| File | RLS field | Type |
|---|---|---|
| `problem.md` | **User Prompt** | text - paste contents |
| `oracle/oracle.py` | **Oracle File** | file upload (inverse only) |
| `solution/main.py` | **Verification Code** | file upload |
| `golden/expected.json → answer` | **Golden Response** | text (bare value the model submits) |
| `golden/expected.json → [grader:] directive` | **Grading Guidance** | text - paste the [grader: tolerance=[...], type=[...]] line (below) together with the golden answer and grading_guide.md into the ONE Grading Guidance field |
| `grader/grading_guide.md` | **Grading Guidance** | text - near-miss table + acceptance prose (same field as above) |
| `(legacy numeric Tolerance field)` | **Tolerance** | numeric - LEAVE BLANK when using the [grader:] directive; single-value tasks only |
| `reasoning_trap.md` | **Reasoning Trap** | text |
| `requirements.txt` | **Required Packages** | text |
| `config.yaml → domain` | **Domain** | dropdown |
| `config.yaml → sub_domain` | **Subdomain** | text |
| `config.yaml → direction` | **Directionality** | Forward / Inverse |
| `config.yaml → simulator` | **Required Tool** | text |
| `solution_steps.md` | **Explanation/Context** | text - paste contents: the explanation AND the step-by-step derivation (one file, one field) |

**Not uploaded (skill-local):** `solution/shortcut.py`, `BRIEF.md`, `STATE.md`, `MANIFEST.md`, `runs/*`
