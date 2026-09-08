# Grading Guidance

## Correct answer

4.617

## Grader directive

```
[grader: tolerance=[0.05], type=[abs]]
[grader: require_oracle_calls=[{"mode": "spectroscopy"}, {"mode": "chromatography"}]]
```

## Acceptance criteria

A single decimal number, log P (dimensionless). Accept within 0.05 absolute of 4.617 (i.e. 4.567 to
4.667). No units or explanatory text required alongside the number; if present, the numeric value
alone is graded.

## Common near-misses

| Submitted | Why it loses |
|---|---|
| `2.761` | Correct chromatography procedure applied to `archive_A` (candidate_2) instead of the spectroscopically-confirmed `archive_C` - picked because it looks like a plausible mid-range "good drug" value rather than by the mass-spectrometry identification. |
| `~5.2-5.3` | Correct chromatography procedure applied to `archive_B` (candidate_3) - the third, out-of-window decoy archive. |
| `1.706` | RDKit's own Crippen/Wildman-Crippen computed log P for candidate_1's structure, submitted directly with no chromatography at all - a fragment-based estimate that diverges substantially from the experimentally-inferred value for this basic, hydrogen-bonding-rich scaffold. |
| `~8.4` (or any value well outside 1-10) | Raw retention time (or an uncorrected retention factor) fit directly against log P, skipping the void-marker correction and the log-transform entirely. |
| `~5.2` | Correct void-time correction and log-transform, but using a single mobile-phase condition instead of extrapolating the full multi-condition series to the water limit. |

## Edge cases the judge should know

If the model submits the answer wrapped in units or prose ("log P = 4.617" or "The computed log P
is approximately 4.62"), extract and grade the numeric value. Reject a response that submits more
than one distinct numeric candidate without committing to one.
