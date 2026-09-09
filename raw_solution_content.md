<!-- DRAFT - skill-local, never published. Real numbers, terse by design (lint aims ~200 words). -->

What this is
HPLC-derived log P (OECD TG 117 / Snyder-Soczewinski LSS) for candidate_1, a basic benzamide-
piperazine, identified by mass match among three archived columns. PRIMARY difficulty: the unknown
is a base, ionized at the assay pH, so its observed retention must be corrected to the neutral
species before the neutral calibration line applies.

Why this is the only answer
Mass spec pins archive identity (candidate masses 16-60 Da apart). Only the phi-extrapolated
log10(k'_w) is linear in log P - and only for the NEUTRAL species; the basic unknown's observed value
is depressed and must be rescaled by 1/f_neutral or log P comes out too low.

Interaction with the oracle
`spectroscopy(archive)`: [M+H]+ -> archive identity. `titration(archive)`: pKa -> fraction ionized.
`chromatography(archive)`: full injection log. Assay pH 7.0 disclosed.

Route
1. RDKit exact mass + proton -> [M+H]+ 296.1524 / 340.1019 / 280.1820; match -> archive_C = candidate_1.
2. Titration -> pKa 7.3; pH 7.0 -> f_neutral = 1/(1+10^(7.3-7.0)) = 0.334 (~2/3 ionized).
3. chromatography(archive_C); drop out-of-window (25-65%) and sub-void-time rows; t0 = 0.9450 min; average duplicates.
4. k' = tR/t0-1; regress log10(k') vs phi per NEUTRAL calibrant -> intercepts; regress vs known log P -> a=0.790, b=-0.550.
5. Unknown: rescale k'_obs / f_neutral to the neutral species, extrapolate, invert -> log P = 4.602.

Near-miss
Skip the ionization rescale (read the depressed value straight off the line): 4.003, ~0.6 units /
12x tol too low - clean, plausible, still in the "good drug" 1-5 window. Weaker near-miss: pick the
archive by plausibility instead of the mass match.
