# Reasoning trap

The trap (primary: ionization)
The unknown is a weak base (piperazine, pKa 7.3) and the mobile phase is buffered at pH 7.0, so it is
~2/3 protonated. The charged form is much less retained, so the unknown's observed retention is
depressed relative to its neutral form. The calibration compounds are neutral, so the calibration
line is the neutral relationship. Reading the unknown's depressed log k'_w straight off that line -
the natural LSS procedure - underestimates its log P. The intended route measures the pKa (titration
mode) and rescales k'_obs -> k'_obs / f_neutral, f_neutral = 1/(1+10^(pKa-pH)), before applying the
calibration.

The numbers
Skipping the rescale lands on 4.003 - about 0.6 log P units, ~12x the 0.05 tolerance, below the
correct value, and still inside the "good drug" 1.0-5.0 window, so nothing looks wrong.

The tell
Every fact that forces the rescale is disclosed - basic analyte, buffer pH 7.0, neutral calibrants,
measurable pKa - but the correction is never prescribed and Henderson-Hasselbalch is never named.

Secondary trap
Which archive is candidate_1 must come from the exact-mass match (RDKit + oracle mass reading), not
from which archive's number looks most drug-like.

Why it is fair
Ionization handling is the documented hard part of RP-HPLC log P for basic drugs (OECD 117). Only the
ruling - at pH below pKa the observed retention is not the neutral retention - must be reasoned.
