"""solution/shortcut.py - deliberately naive solver (skill-local, NOT uploaded to RLS).

Implements the tempting failure mode: skip genuine spectroscopic identification and
instead compute log P for all three archives (using otherwise-correct chromatography),
then pick whichever archive's result looks most like a plausible drug candidate - i.e.
closest to the middle of the stated 1.0-5.0 optimal window - and report that as
`candidate_1`. The chromatography math itself is done correctly, so the wrong answer
is clean and self-consistent, not obviously broken.

Must FAIL against golden/expected.json.
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np

_PRESCRIBED_MIN, _PRESCRIBED_MAX = 25.0, 65.0
_CAL_LOGP = {
    "cal_1": 0.85,
    "cal_2": 1.62,
    "cal_3": 2.40,
    "cal_4": 3.15,
    "cal_5": 4.05,
}


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
            kprime = tR / t0 - 1
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
    # Skip spectroscopic identification entirely; pick the archive whose
    # (correctly-computed) log P sits closest to the middle of the "good drug" window.
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
