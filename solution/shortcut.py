"""solution/shortcut.py - deliberately naive solver (skill-local, NOT uploaded to RLS).

PRIMARY naive path (`naive_solve`): the ionization-skip failure. It identifies the
archive correctly by the mass match and does the void-time correction, replicate
averaging, and water-limit extrapolation correctly - but treats the basic unknown's
OBSERVED retention as if it were the neutral-species retention, skipping the
correction for the fraction ionized at the assay pH. Because the charged unknown is
under-retained, its log P comes out too low (a clean, self-consistent, plausible-looking
underestimate around 3.8, well inside the "good drug 1.0-5.0" window).

REGRESSION LOCK (`naive_solve_plausibility`): the earlier, weaker near-miss - skip the
mass-match identification entirely and pick the archive whose computed log P looks most
drug-like. Kept so the door closed in the previous version stays regression-tested.

Both must FAIL against golden/expected.json.
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

_PRESCRIBED_MIN, _PRESCRIBED_MAX = 25.0, 65.0
_PROTON_MASS = 1.007276
_CANDIDATES = {
    "candidate_1": "O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(Cl)cc1",
    "candidate_2": "O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(Br)cc1",
    "candidate_3": "O=C(N[C@@H](C)CN1CCN(CC1)C)c1ccc(F)cc1",
}
_CAL_LOGP = {
    "cal_1": 0.85, "cal_2": 1.62, "cal_3": 2.40, "cal_4": 3.15, "cal_5": 4.05,
}


def _identify_archive(query_oracle) -> str:
    target = Descriptors.ExactMolWt(Chem.MolFromSmiles(_CANDIDATES["candidate_1"])) + _PROTON_MASS
    best_archive, best_diff = None, None
    for archive in ("archive_A", "archive_B", "archive_C"):
        mz = query_oracle("spectroscopy", {"archive": archive})["observation"]["mz_M_plus_H"]
        diff = abs(mz - target)
        if best_diff is None or diff < best_diff:
            best_diff, best_archive = diff, archive
    return best_archive


def _process_archive(query_oracle, archive: str) -> float:
    injections = query_oracle("chromatography", {"archive": archive})["observation"]["injections"]
    valid = [r for r in injections if r["compound_id"] == "void_marker"
             or (_PRESCRIBED_MIN <= r["mobile_phase_pct_organic"] <= _PRESCRIBED_MAX)]
    t0 = float(np.mean([r["retention_time_min"] for r in valid if r["compound_id"] == "void_marker"]))
    valid = [r for r in valid if r["compound_id"] == "void_marker" or r["retention_time_min"] > t0]

    def averaged(compound_id, phi_pct):
        vals = [r["retention_time_min"] for r in valid
                if r["compound_id"] == compound_id and r["mobile_phase_pct_organic"] == phi_pct]
        return float(np.mean(vals)) if vals else None

    phi_pcts = sorted({r["mobile_phase_pct_organic"] for r in valid if r["compound_id"] != "void_marker"})

    def extrapolate_to_water(compound_id):
        phis, log10k = [], []
        for phi_pct in phi_pcts:
            tR = averaged(compound_id, phi_pct)
            if tR is None:
                continue
            kprime = tR / t0 - 1  # NAIVE: no ionization correction on the unknown
            phis.append(phi_pct / 100.0)
            log10k.append(np.log10(kprime))
        slope, intercept = np.polyfit(phis, log10k, 1)
        return intercept

    cal_logP, cal_log10kw = [], []
    for compound_id, logP in _CAL_LOGP.items():
        cal_logP.append(logP)
        cal_log10kw.append(extrapolate_to_water(compound_id))
    a, b = np.polyfit(cal_logP, cal_log10kw, 1)

    unknown_log10kw = extrapolate_to_water("unknown")
    return (unknown_log10kw - b) / a


def naive_solve(query_oracle):
    # Correct archive ID + correct chromatography, but SKIP the ionization correction.
    archive = _identify_archive(query_oracle)
    return round(float(_process_archive(query_oracle, archive)), 3)


def naive_solve_plausibility(query_oracle):
    # Regression lock: skip the mass-match ID; pick the archive whose (uncorrected)
    # log P sits closest to the middle of the "good drug" window.
    results = {arch: _process_archive(query_oracle, arch) for arch in ("archive_A", "archive_B", "archive_C")}
    best_archive = min(results, key=lambda a: abs(results[a] - 3.0))
    return round(float(results[best_archive]), 3)


def main():
    sys.path.insert(0, str(Path(__file__).parent.parent / "oracle"))
    import oracle  # type: ignore[import-not-found]  # noqa: E402

    answer = naive_solve(oracle.handle_query)
    print(f"EVERGLADES_SUBMIT_ANSWER: {answer}")
    print(answer)


if __name__ == "__main__":
    main()
