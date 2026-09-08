<!-- DRAFT - skill-local, never published. Real numbers, terse by design (lint aims ~200 words). -->

What this is
HPLC-derived log P (OECD TG 117 / Snyder-Soczewinski LSS model) for candidate_1, a
benzamide-piperazine compound, identified by mass match among three archived columns.

Why this is the only answer
Mass spec pins archive identity factually (candidate masses 16-60 Da apart, oracle noise ~2 ppm) -
plausibility cannot substitute. Only the phi-extrapolated log10(k'_w) is linear in log P; a single
condition or raw retention time is not.

Interaction with the oracle
`spectroscopy(archive)`: [M+H]+ mass reading, mandatory - the only route to archive identity.
`chromatography(archive)`: full injection log (retention time, phi, replicate, compound).

Route
1. RDKit exact mass + proton mass on each candidate SMILES -> [M+H]+ 296.1524 / 340.1019 / 280.1820 Da.
2. Query spectroscopy per archive, match masses -> archive_C = candidate_1.
3. Query chromatography(archive_C), drop out-of-window (25-65%) and sub-void-time rows -> filtered log.
4. Average void-marker duplicates -> t0 = 0.9450 min; average remaining duplicates per (compound, phi).
5. k' = tR/t0 - 1 per point; regress log10(k') vs phi per compound, take intercept -> log10(k'_w) per compound.
6. Regress calibration intercepts vs known log P -> a=0.7900, b=-0.5501. Invert unknown's log10(k'_w)=3.0964 -> log P = 4.617.

Near-miss
Picking archive_A (candidate_2) by plausibility instead of the mass match, with otherwise-correct
math, gives 2.761 - ~37x the 0.05 tolerance off.
