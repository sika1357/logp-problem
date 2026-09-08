# Determining an unknown drug candidate's octanol/water partition coefficient from HPLC retention data

A pharmaceutical discovery team is triaging three synthesized candidates from the same benzamide-piperazine series. For a compound to be worth advancing as an orally active drug candidate, its octanol/water partition coefficient (log P) should fall between 1.0 and 5.0 - too low and it will not cross lipid membranes efficiently, too high and it will have poor aqueous solubility and high plasma protein binding.

The team has decided against relying on a purely computational estimate of log P for the true candidate - fragment-based/atomic-contribution log P calculators are known to drift substantially from measured values for polyfunctional, basic, or hydrogen-bonding-rich scaffolds such as this one, and this series is exactly that case. Instead, the standard experimental route is used: log P is determined from reversed-phase HPLC retention behavior, calibrated against compounds of known log P, run on the same column under the same conditions as the unknown.

## The three candidates

Three structures were synthesized in this series. Molecular structure, molecular formula, and stereochemistry are given for each.

| Candidate | SMILES | Molecular formula | Stereochemistry |
|---|---|---|---|
| `candidate_1` | `O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(Cl)cc1` | C15H22ClN3O | (S) at the benzylic-adjacent carbon |
| `candidate_2` | `O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(Br)cc1` | C15H22BrN3O | (S) at the benzylic-adjacent carbon |
| `candidate_3` | `O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(F)cc1` | C15H22FN3O | (S) at the benzylic-adjacent carbon |

The three differ only in the para-halogen on the benzamide ring (Cl / Br / F) - everything else about the scaffold, including the stereocenter, is identical.

## The chromatography archives

Three HPLC columns, matched in stationary phase, dimensions, and thermostatted to the same temperature, were each used to run a full characterization set: the same panel of calibration compounds (of independently established, literature log P), a void-marker compound that is not retained by the stationary phase at all, and an unknown sample. Every compound - calibration or unknown - was injected in duplicate at each of several mobile-phase organic-solvent fractions, and the void-marker was likewise injected in duplicate at each condition. The three resulting datasets are archived as `archive_A`, `archive_B`, and `archive_C`.

Exactly one of the three archives is `candidate_1`; the other two archives are the other two candidates, run through the same characterization protocol as controls/matched references. Which archive is which is not stated.

"Matched" here means matched in stationary-phase chemistry, column dimensions, and temperature - it does not mean interchangeable. Even columns packed with nominally the same stationary phase show real, measurable, column-to-column differences in retention selectivity (a well-documented phenomenon in reversed-phase HPLC, independent of any operator error). Each archive's calibration relationship is a property of that specific column's run and should be treated as such.

The protocol prescribes mobile-phase organic fractions between 25% and 65% for calibration-valid runs; anything recorded outside that window reflects a condition the method was never validated for, not a legitimate data point. Each archive's raw injection log also contains a small, archive-specific number of unusable entries: an incomplete chromatogram, a failed injection, or a run recorded outside that window. These are mixed in with the valid entries and are not flagged for you - identify and exclude them yourself before using an archive's data for anything. The three archives do not contain the same number of unusable entries.

## What the data can tell you

An analyte's retention time on this column carries two things at once: the genuine time it spends interacting with the stationary phase, and a mechanical baseline - the time any species, retained or not, needs simply to traverse the column and its connecting tubing - set by geometry and flow rather than by chemistry. The void-marker compound has no affinity whatsoever for the stationary phase, so its own measured transit time is exactly that baseline, observed directly and free of any chemistry.

Under fixed column and temperature, a compound's retention weakens smoothly as the mobile phase carries more organic modifier - one characteristic trend per compound, never a jump or a change of behavior partway through. Every compound here was measured at several different mobile-phase compositions rather than just one, because a single reading at one working composition mixes a compound's own affinity for the stationary phase with the arbitrary choice of how much organic modifier happened to be used that day. Two compounds sharing the same underlying preference for octanol over water need not retain identically at any particular working composition - but their trends, followed far enough, agree on something that no longer depends on the mobile phase's composition at all, and it is that composition-independent quantity, not a reading from any one working condition, that lines up linearly with log P across the calibration panel. (As a sanity check on your own numbers: for a well-behaved compound in an assay like this, how fast that trend moves with organic fraction typically falls between about 2 and 6, not a percentage-scale correction.) Two compounds that behave identically at every matching mobile-phase composition, under otherwise identical conditions, are indistinguishable by this assay and should be treated accordingly.

Do not relate a raw retention time directly to log P, and do not fit any single mobile-phase condition's reading directly against log P either. Duplicate injections are technical replicates of the same measurement, not independent data points - average them before doing anything else with them, and do the same for the void-marker's duplicate injections. Use every valid calibration compound the archive provides; do not discard a calibration point because its behavior seems, at a glance, out of line with the others.

## Available data

A high-resolution spectroscopic observation is available for each archive's unknown sample, reachable through `query_oracle`, alongside each archive's full chromatography injection log.

## Your task

Write a Python script (using RDKit and `query_oracle` as needed) that determines `candidate_1`'s computationally inferred log P from the data above. Call `submit_answer` with the result as a single decimal number. Your answer is graded as correct if it is within 0.05 (absolute) of the reference value.
