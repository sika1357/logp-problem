Goal: Find the unknown compound's with log P using RP-HPLC/QSRR.

 Candidates: Three benzamide-piperazine compounds are differentiated by Cl, Br, or F. Why HPLC is needed: Computed log P is not reliable. candidate_1's calculated value is ~1.7, while its true value is 4.602.
 
  Step 1: Calculate candidate [M+H]+ masses: Candidate 1: 296.1524 Da Candidate 2: 340.1019 Da Candidate 3: 280.1820 Da 
  
  Step 2- The unknown is ionized for the difference between pka and buffer and correction term is applied. The retention is depressed to 1/3 of the neutral value. 
  
  Step 3: Query spectroscopy for all three archives and match masses: archive_C = candidate_1 archive_A = candidate_2 archive_B = candidate_3 
  
  Step 4: Use archive_C chromatography and remove invalid rows: Organic fraction outside 25--65% Retention time <= void time 
  
  Step 5: Calculate void time from duplicate void-marker injections: t0 = 0.9450 min. Average duplicate measurements.
  
   Step 6: Calculate k' = tR/t0 - 1, regress log10(k') vs. organic fraction, and use the intercept as log10(k'w). Calibration: log10(k'w) = 0.7900 x log P - 0.5501 Unknown: log10(k'w) = 3.086 Final answer: log P = (3.086 + 0.5501) / 0.7900 = 4.602 Key result Correct archive: archive_C Unknown log P: 4.602 Required tolerance: +/-0.05