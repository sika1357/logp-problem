"""solution/main.py - reference solve for the logP-from-HPLC inverse task.

Uses RDKit to identify which archive is `candidate_1` from a high-resolution
mass match, then reconstructs that archive's log P from its HPLC injection log:
filter invalid entries, average replicates, void-time-correct, extrapolate each
calibration compound's retention behavior to the water limit, regress that
extrapolated quantity against known log P, and invert for the unknown.

The unknown is a basic analyte and the mobile phase is buffered below its pKa, so
its charged form is largely unretained and its OBSERVED retention factor is depressed
to the fraction neutral, f_neutral = 1/(1 + 10^(pKa - pH)). The calibration compounds
are neutral, so the calibration line is the neutral relationship; the unknown's k' must
be corrected back to its neutral value (k'_obs / f_neutral) before the calibration is
applied, or its log P comes out too low. The pKa is measured from the oracle's titration
mode; the assay pH is the disclosed buffer pH.
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

_CANDIDATES = {
    "candidate_1": "O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(Cl)cc1",
    "candidate_2": "O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(Br)cc1",
    "candidate_3": "O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(F)cc1",
}
_PROTON_MASS = 1.007276

_CAL_LOGP = {
    "cal_1": 0.85,
    "cal_2": 1.62,
    "cal_3": 2.40,
    "cal_4": 3.15,
    "cal_5": 4.05,
}
_PRESCRIBED_MIN, _PRESCRIBED_MAX = 25.0, 65.0
_ASSAY_PH = 7.0  # disclosed mobile-phase buffer pH


def _fraction_neutral(pka: float, pH: float) -> float:
    return 1.0 / (1.0 + 10.0 ** (pka - pH))


def _candidate_mz(smiles: str) -> float:
    mol = Chem.MolFromSmiles(smiles)
    exact_mass = Descriptors.ExactMolWt(mol)
    return exact_mass + _PROTON_MASS


def _identify_archive(query_oracle) -> str:
    candidate_mz = {name: _candidate_mz(smi) for name, smi in _CANDIDATES.items()}
    best_archive, best_diff = None, None
    for archive in ("archive_A", "archive_B", "archive_C"):
        obs = query_oracle("spectroscopy", {"archive": archive})
        observed_mz = obs["observation"]["mz_M_plus_H"]
        for cand, mz in candidate_mz.items():
            if cand != "candidate_1":
                continue
            diff = abs(observed_mz - mz)
            if best_diff is None or diff < best_diff:
                best_diff, best_archive = diff, archive
    return best_archive


def _process_archive(query_oracle, archive: str, f_neutral_unknown: float):
    injections = query_oracle("chromatography", {"archive": archive})["observation"]["injections"]

    # step 1: drop entries outside the prescribed mobile-phase window (void marker exempt)
    valid = [r for r in injections if r["compound_id"] == "void_marker"
             or (_PRESCRIBED_MIN <= r["mobile_phase_pct_organic"] <= _PRESCRIBED_MAX)]

    # step 2: void-marker replicates -> t0
    t0 = float(np.mean([r["retention_time_min"] for r in valid if r["compound_id"] == "void_marker"]))

    # step 3: drop entries a retained analyte cannot physically produce (failed injections)
    valid = [r for r in valid if r["compound_id"] == "void_marker" or r["retention_time_min"] > t0]

    # step 4: average remaining duplicate injections per (compound, mobile-phase condition)
    def averaged(compound_id, phi_pct):
        vals = [r["retention_time_min"] for r in valid
                if r["compound_id"] == compound_id and r["mobile_phase_pct_organic"] == phi_pct]
        return float(np.mean(vals)) if vals else None

    phi_pcts = sorted({r["mobile_phase_pct_organic"] for r in valid if r["compound_id"] != "void_marker"})

    def extrapolate_to_water(compound_id, f_neutral=1.0):
        phis, log10k = [], []
        for phi_pct in phi_pcts:
            tR = averaged(compound_id, phi_pct)
            if tR is None:
                continue
            # correct the observed retention factor back to the neutral species
            # (f_neutral = 1 for the neutral calibration compounds)
            kprime = (tR / t0 - 1) / f_neutral
            phis.append(phi_pct / 100.0)
            log10k.append(np.log10(kprime))
        slope, intercept = np.polyfit(phis, log10k, 1)
        return intercept  # log10(k'_w) of the neutral species

    cal_logP, cal_log10kw = [], []
    for compound_id, logP in _CAL_LOGP.items():
        cal_logP.append(logP)
        cal_log10kw.append(extrapolate_to_water(compound_id))

    a, b = np.polyfit(cal_logP, cal_log10kw, 1)

    unknown_log10kw = extrapolate_to_water("unknown", f_neutral=f_neutral_unknown)
    return (unknown_log10kw - b) / a


def solve(query_oracle):
    archive = _identify_archive(query_oracle)
    # the unknown is basic and partly ionized at the assay pH: measure its pKa and
    # correct its retention for the fraction neutral before applying the calibration
    pka = query_oracle("titration", {"archive": archive})["observation"]["pKa"]
    f_neutral_unknown = _fraction_neutral(pka, _ASSAY_PH)
    logP = _process_archive(query_oracle, archive, f_neutral_unknown)
    return round(float(logP), 3)


def main():
    sys.path.insert(0, str(Path(__file__).parent.parent / "oracle"))
    import oracle  # type: ignore[import-not-found]  # noqa: E402

    answer = solve(oracle.handle_query)
    print(f"EVERGLADES_SUBMIT_ANSWER: {answer}")
    print(answer)


if __name__ == "__main__":
    main()
