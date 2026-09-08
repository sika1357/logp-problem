<!-- DRAFT ONLY - this is the skill's raw material, not solution.md. Per publish.py's own policy,
     solution.md must be rewritten in your own words, with your own framing and judgment, before
     it ships. Every number below is real (computed in this task's own pipeline / gate records),
     not invented - reuse the numbers freely, rewrite the prose. -->

## Overview of the Task

Domain: computational chemistry, subdomain: HPLC-based structure-property inference (quantitative
structure-retention relationships, QSRR). Real-world application: pharmaceutical lead triage, where
octanol/water partition coefficient (log P) governs oral bioavailability, and an experimentally
measured log P from reversed-phase HPLC retention (the OECD Test Guideline 117 approach) is used in
preference to a fragment-based computational estimate for scaffolds - like this one - where those
estimates are known to diverge from measured values.

System and setup: three candidate structures from one benzamide-piperazine series (differing only in
a para-halogen: Cl / Br / F), each characterized on its own RP-HPLC column (archive_A, archive_B,
archive_C) against a shared five-compound calibration panel of known log P, with duplicate
injections, a duplicated void-marker injection, and one unknown-sample injection per archive, each
measured at four mobile-phase organic fractions (30/40/50/60%).

Governing model: the linear-solvent-strength (LSS) relationship log10(k'(phi)) = log10(k'_w) - S*phi,
and the QSRR calibration line log10(k'_w) = a*logP + b (Snyder/Soczewinski).

Hidden parameters the solver must recover: (1) which archive is spectroscopically confirmed as
`candidate_1` (a categorical identification, not disclosed); (2) that archive's unknown compound's
true log P (the graded scalar, golden = 4.617, tolerance 0.05 absolute); (3) which specific
injections in the identified archive are invalid (undisclosed counts and identities per archive).

## Why this is the only possible answer

The governing principle is that mass spectrometry gives an unambiguous, physically grounded identity
match - each candidate's exact mass, computed to four decimal places with RDKit, is 16-60 Da apart
from the other two (candidate_1 296.1524, candidate_2 340.1019, candidate_3 280.1820 Da as [M+H]+),
far outside the oracle's ~2 ppm reading noise. A solver cannot substitute chemical plausibility
(which archive's resulting number "looks like a good drug") for this match: none of the three
candidates' true log P values are derivable from their structures alone - candidate_1's own
RDKit-Crippen computed log P is ~1.7, nowhere near its true HPLC-inferred value of 4.617, so a purely
computational shortcut is closed by design, not by omission.

The naive route also fails on the chromatography side even when the correct archive is used: only
the phi-extrapolated log10(k'_w) is actually linear in log P. Fitting raw retention time, or a single
mobile-phase condition's retention factor, directly against log P uses a quantity that is not linear
in log P at all - it is a mathematically wrong model, not merely an imprecise one. Computed in this
task's own pipeline: picking the archive by plausibility (archive_A) and doing the chromatography
correctly still lands on 2.761, 1.856 away from the 4.617 golden value (roughly 37x the 0.05
tolerance); doing the correct archive but skipping the phi-extrapolation (a single condition only)
lands on approximately 5.185, about 0.565 away (roughly 11x tolerance).

## Interaction with the Oracle

The oracle exposes two modes. `spectroscopy(archive, replicate_id?)` is a genuine parametrized
high-resolution mass-spec reading ([M+H]+ in Da) that varies by which archive is queried, with small
(~2 ppm) seeded noise on a requested replicate and a fixed central value with none. `chromatography
(archive)` returns that archive's complete raw injection log - retention time in minutes, mobile-phase
organic percent, replicate index, and compound ID - for every calibration compound, the void marker,
and the unknown, with no valid/invalid flag attached.

The mandatory, non-optional probe is `spectroscopy`, queried for all three archives and compared
against each candidate's RDKit-computed exact mass. Without it there is no legitimate route to
knowing which archive is `candidate_1`, and a submission that skips this comparison - however
correctly it processes some archive's chromatography data - scores zero, because grading is against
the archive_C answer specifically, not against any internally-consistent number a solver happens to
produce.

## Route

**Step 1:** Compute each candidate's exact monoisotopic mass from its disclosed SMILES with RDKit
(`Chem.MolFromSmiles` + `Descriptors.ExactMolWt`), then add the proton mass (1.007276 Da) -> each
candidate's [M+H]+: candidate_1 = 296.1524 Da, candidate_2 = 340.1019 Da, candidate_3 = 280.1820 Da.

**Step 2:** Query `spectroscopy` for each of the three archives and match the returned [M+H]+ reading
against the three computed values -> archive_C identified as `candidate_1` (the graded archive);
archive_A is candidate_2, archive_B is candidate_3.

**Step 3:** Query `chromatography` for archive_C and discard the entries a retained analyte cannot
legitimately produce: rows outside the disclosed 25-65% prescribed mobile-phase window, and rows
whose retention time falls at or below the void time -> a filtered injection log.

**Step 4:** Average the void-marker's two replicate injections to obtain the column's void time
(t0 = 0.9450 min), then average the remaining duplicate injections for each (compound, mobile-phase)
pair -> one retention time per compound per condition.

**Step 5:** For each of the five calibration compounds and for the unknown, convert each averaged
retention time to a retention factor, k' = t_R/t0 - 1, then regress log10(k') against mobile-phase
organic fraction phi across the four valid conditions and take the intercept -> each compound's
water-extrapolated log10(k'_w). Regressing the five calibration compounds' intercepts against their
known log P values gives the column's calibration line: a = 0.7900, b = -0.5501.

**Step 6:** Invert the calibration line using the unknown's own extrapolated log10(k'_w) = 3.0964 ->
log P = (3.0964 - (-0.5501)) / 0.7900 = 4.617, the submitted answer.
