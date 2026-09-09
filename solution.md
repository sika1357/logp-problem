
Goal: Find the unknown compound's log P using RP-HPLC/QSRR.
Candidates: Three benzamide-piperazine compounds, differing only by Cl, Br, or F.
Why HPLC is needed: Computed log P is not reliable for this scaffold - candidate_1's calculated value is ~1.7, while its true value is 4.602.
Step 1: Calculate each candidate's [M+H]+ mass:
Candidate 1: 296.1524 Da
Candidate 2: 340.1019 Da
Candidate 3: 280.1820 Da
Step 2: The unknown is a base. At the buffer pH (7.0), below its pKa (7.3), it is partly ionized, so its retention is depressed to about 1/3 of the neutral value; a correction term must be applied.
Step 3: Query spectroscopy for all three archives and match masses:
archive_C = candidate_1
archive_A = candidate_2
archive_B = candidate_3
Step 4: Use archive_C chromatography and remove invalid rows:
Organic fraction outside 25-65%
Retention time <= void time
Step 5: Calculate void time from the duplicate void-marker injections: t0 = 0.9450 min. Average the duplicate measurements.
Step 6: Calculate k' = tR/t0 - 1, regress log10(k') vs. organic fraction, and take the intercept as log10(k'w).
Calibration:
log10(k'w) = 0.7900 x log P - 0.5501
Unknown (observed, ionization-depressed): log10(k'w) = 2.61.
Correct to the neutral species by dividing k' by f_neutral = 0.334, i.e. add -log10(0.334) = +0.476: neutral log10(k'w) = 3.086.
Final answer:
log P = (3.086 + 0.5501) / 0.7900 = 4.602
(Skipping the correction and using the depressed 2.61 gives (2.61 + 0.5501)/0.7900 = 4.00 - the near-miss.)
Key result
Correct archive: archive_C
Unknown log P: 4.602
Required tolerance: +/-0.05
