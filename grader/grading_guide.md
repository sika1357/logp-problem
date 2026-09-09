# Grading Guidance

## Correct answer

4.602

## Grader directive

```
[grader: tolerance=[0.05], type=[abs]]
[grader: require_oracle_calls=[{"mode": "spectroscopy"}, {"mode": "titration"}, {"mode": "chromatography"}]]
```

## Acceptance criteria

A single decimal number, log P (dimensionless). Accept within 0.05 absolute of 4.602 (i.e. 4.552 to
4.652). No units or explanatory text required alongside the number; if present, the numeric value
alone is graded.

## Common near-misses

| Submitted | Why it loses |
|---|---|
| `~4.00` | PRIMARY trap. Correct archive, correct chromatography, but the unknown's retention is read straight off the neutral calibration line without correcting for ionization. The basic unknown is ~2/3 protonated at the assay pH 7.0 (pKa 7.3), so its charged form is under-retained; skipping the k'_obs / f_neutral rescale underestimates log P by ~0.6 units. A clean, plausible-looking underestimate still inside the "good drug" window. |
| `2.283` (or any plausibility pick) | Skipped the mass-match archive identification entirely and picked whichever archive's computed log P looked most drug-like (secondary/weaker trap). |
| `1.706` | RDKit's own Crippen/Wildman-Crippen computed log P for candidate_1's structure, submitted directly with no chromatography at all - a fragment-based estimate that diverges substantially from the experimentally-inferred value for this basic, hydrogen-bonding-rich scaffold. |
| `~8` (or any value well outside 1-10) | Raw retention time (or an uncorrected retention factor) fit directly against log P, skipping the void-marker correction and the log-transform entirely. |
| single-condition read | Correct void-time correction and log-transform, but using a single mobile-phase condition instead of extrapolating the full multi-condition series to the water limit. |

## Edge cases the judge should know

If the model submits the answer wrapped in units or prose ("log P = 4.602" or "The computed log P
is approximately 4.60"), extract and grade the numeric value. Reject a response that submits more
than one distinct numeric candidate without committing to one.
