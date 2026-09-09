

## Overview of the Task

Domain: computational chemistry, subdomain: HPLC-based structure-property inference (quantitative
structure-retention relationships, QSRR). Real-world application: pharmaceutical lead triage, where octanol/water partition coefficient (log P) governs oral bioavailability, and an experimentally measured log P from reversed-phase HPLC retention (the OECD Test Guideline 117 approach) is used in preference to a fragment-based computational estimate for scaffolds - like this one - where those estimates are known to diverge from measured values.


Goal: Find the unknown compound’s with log P using RP-HPLC/QSRR.
Candidates: Three benzamide-piperazine compounds are differentiated by Cl, Br, or F.
Why HPLC is needed: Computed log P is not reliable for this scaffold - candidate_1’s fragment-based calculated value is ~1.7, while its true value is 4.602.
Step 1: Calculate candidate [M+H]+ masses:
Candidate 1: 296.1524 Da
Candidate 2: 340.1019 Da
Candidate 3: 280.1820 Da
Step 2- The unknown is ionized for the difference between pka and buffer and correction term is applied. The retentio is depressed 1/3 of the neutral value.
Step 3: Query spectroscopy for all three archives and match masses:
archive_C = candidate_1
archive_A = candidate_2
archive_B = candidate_3
Step 4: Use archive_C chromatography and remove invalid rows:
Organic fraction outside 25–65%
Retention time ≤ void time
Step 5: Calculate void time from duplicate void-marker injections: t₀ = 0.9450 min. Average duplicate measurements.
Step 6: Calculate k′ = tR/t₀ − 1, regress log₁₀(k′) vs. organic fraction, and use the intercept as log₁₀(k′w).
Calibration:
log₁₀(k′w) = 0.7900 × log P − 0.5501
Unknown (observed, ionization-depressed): log₁₀(k′w) = 2.61. Only f_neutral = 1/(1+10^(7.3−7.0)) = 0.334 of the analyte is the retained neutral form, so correct back to the neutral species by dividing k′ by f_neutral (equivalently add −log₁₀(0.334) = +0.476): neutral log₁₀(k′w) = 3.086.
Final answer:
log P = (3.086 + 0.5501) / 0.7900 = 4.602
(Skipping the ionization correction and using the depressed 2.61 gives (2.61 + 0.5501)/0.7900 = 4.00 — the near-miss the task is built around.)
Key result
Correct archive: archive_C
Unknown log P: 4.602
Required tolerance: ±0.05

