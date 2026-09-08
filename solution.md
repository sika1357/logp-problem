

## Overview of the Task

Domain: computational chemistry, subdomain: HPLC-based structure-property inference (quantitative
structure-retention relationships, QSRR). Real-world application: pharmaceutical lead triage, where octanol/water partition coefficient (log P) governs oral bioavailability, and an experimentally measured log P from reversed-phase HPLC retention (the OECD Test Guideline 117 approach) is used in preference to a fragment-based computational estimate for scaffolds - like this one - where those estimates are known to diverge from measured values.

Goal: Find the unknown compound’s with log P using RP-HPLC/QSRR.
Candidates: Three benzamide-piperazine compounds are differentiated by Cl, Br, or F.
Why HPLC is needed: Computed log P is somehow reliable. candidate_1’s calculated value is ~1.7, while its true value is 4.617.
Step 1: Calculate candidate [M+H]+ masses:
Candidate 1: 296.1524 Da
Candidate 2: 340.1019 Da
Candidate 3: 280.1820 Da
Step 2: Query spectroscopy for all three archives and match masses:
archive_C = candidate_1
archive_A = candidate_2
archive_B = candidate_3
Step 3: Use archive_C chromatography and remove invalid rows:
Organic fraction outside 25–65%
Retention time ≤ void time
Step 4: Calculate void time from duplicate void-marker injections: t₀ = 0.9450 min. Average duplicate measurements.
Step 5: Calculate k′ = tR/t₀ − 1, regress log₁₀(k′) vs. organic fraction, and use the intercept as log₁₀(k′w).
Calibration:
log₁₀(k′w) = 0.7900 × log P − 0.5501
Unknown: log₁₀(k′w) = 3.0964
Final answer:
log P = (3.0964 + 0.5501) / 0.7900 = 4.617
Key result
Correct archive: archive_C
Unknown log P: 4.617
Required tolerance: ±0.05

