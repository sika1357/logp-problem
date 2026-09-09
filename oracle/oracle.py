"""oracle/oracle.py - HIDDEN system. The model never sees this file.

Backs the logP-from-HPLC inverse task. Three measurement modes:
  - `spectroscopy(archive, replicate_id?)` - a genuine parametrized instrument reading
    (high-resolution [M+H]+ m/z, varies with which archive you ask about, tiny seeded noise).
  - `chromatography(archive)` - the full raw injection log for one archive (retention
    times across mobile-phase compositions, duplicates, void marker, calibration
    compounds and the unknown; some entries are unusable and NOT flagged).
  - `titration(archive, replicate_id?)` - a noisy aqueous pKa measurement of that archive's
    unknown (the analytes are basic, piperazine-bearing; this reports the basic-nitrogen pKa).

The IONIZATION trap: the mobile phase is buffered below the analytes' pKa, so the basic
unknown is substantially protonated (charged) and its charged form is barely retained on
the reversed phase. Its OBSERVED retention factor is therefore depressed to f_neutral of the
neutral-species value, where f_neutral = 1 / (1 + 10^(pKa - pH)). The calibration compounds
are NEUTRAL (non-ionizable), so their retention is the clean neutral relationship. A solver
that reads the unknown's depressed log k'_w straight off the neutral calibration line
UNDER-estimates its log P; the intended route instead recognizes the analyte is ionized at
the assay pH, measures the pKa, and rescales k'_obs -> k'_obs / f_neutral before applying the
calibration. Nothing here prescribes that adjustment - the depression is baked into the
retention data and the pKa/pH are disclosed/measurable; the discipline must be originated.

Nothing here ever names the archive-to-candidate mapping, the void-time correction,
the extrapolation procedure, the ionization correction, or the calibration relationship -
those are exactly what main.py must work out.
"""
from __future__ import annotations
import hashlib

import numpy as np

# === Hidden ground truth (never leaves handle_query) ===

# Exact masses (Da) of the three candidates, for cross-check only - main.py must compute
# these itself with RDKit from the SMILES in problem.md, never read them from here.
_CANDIDATE_EXACT_MASS = {
    "candidate_1": 295.1451,   # C15H22ClN3O
    "candidate_2": 339.0946,   # C15H22BrN3O
    "candidate_3": 279.1747,   # C15H22FN3O
}
_PROTON_MASS = 1.007276

# Which archive holds which candidate, and that candidate's true log P (hidden).
_ARCHIVES = {
    "archive_A": {"candidate": "candidate_2", "logP": 2.75, "S": 3.4,
                  "a": 0.850, "b": -0.620, "t0": 1.10},
    "archive_B": {"candidate": "candidate_3", "logP": 5.05, "S": 6.0,
                  "a": 0.700, "b": -0.500, "t0": 1.00},
    "archive_C": {"candidate": "candidate_1", "logP": 4.62, "S": 5.8,
                  "a": 0.790, "b": -0.550, "t0": 0.95},
}

# Calibration panel: (compound_id, known log P, LSS slope S) - identical set, same true
# values, run on all three archives/columns. These reference compounds are NEUTRAL
# (non-ionizable) across the assay pH, so their retention needs no ionization correction.
_CAL = [
    ("cal_1", 0.85, 2.3),
    ("cal_2", 1.62, 3.1),
    ("cal_3", 2.40, 3.9),
    ("cal_4", 3.15, 4.7),
    ("cal_5", 4.05, 5.5),
]

# Ionization: assay mobile phase buffered at pH 7.0; the basic (piperazine) unknowns have
# per-candidate pKa. f_neutral = 1/(1+10^(pKa-pH)) depresses the unknown's OBSERVED k'.
_ASSAY_PH = 7.0
_CANDIDATE_PKA = {"candidate_1": 7.3, "candidate_2": 7.2, "candidate_3": 7.6}

_PHI_GRID = [0.30, 0.40, 0.50, 0.60]
_PRESCRIBED_MIN, _PRESCRIBED_MAX = 25.0, 65.0  # percent organic, calibration-valid window


def _fraction_neutral(pka, pH):
    return 1.0 / (1.0 + 10.0 ** (pka - pH))

_BUDGET = 40
_used = 0
_NOISE_SALT = "logp-hplc-everglades-v1"


def _rng_for(*key):
    digest = hashlib.sha256((_NOISE_SALT + "|" + "|".join(str(k) for k in key)).encode("utf-8")).digest()
    return np.random.default_rng(int.from_bytes(digest[:8], "little") % (2 ** 32))


def _kprime(a, b, S, logP, phi):
    return 10 ** (a * logP + b - S * phi)


def _tR_true(t0, kp):
    return t0 * (1 + kp)


def _build_injection_log(archive: str):
    """Deterministically regenerate one archive's full injection log (same physics
    every import - this IS the single source of truth main.py's data also derives from,
    since main.py calls this same oracle rather than a separate copy)."""
    p = _ARCHIVES[archive]
    f_neutral_unknown = _fraction_neutral(_CANDIDATE_PKA[p["candidate"]], _ASSAY_PH)
    compounds = [(cid, logP, S) for cid, logP, S in _CAL] + [("unknown", p["logP"], p["S"])]
    rows = []
    rid = 0
    for cid, logP, S in compounds:
        # The unknown is a basic analyte, partly ionized at the assay pH: its OBSERVED
        # retention factor is depressed to f_neutral of the neutral value. Calibration
        # compounds are neutral (f_neutral = 1) and are left untouched.
        f_ion = f_neutral_unknown if cid == "unknown" else 1.0
        for phi in _PHI_GRID:
            true_tR = _tR_true(p["t0"], f_ion * _kprime(p["a"], p["b"], S, logP, phi))
            for rep in (1, 2):
                r = _rng_for(archive, cid, phi, rep)
                noisy = true_tR * (1 + r.normal(0, 0.006))
                rows.append({"row_id": rid, "compound_id": cid, "injection_replicate": rep,
                             "mobile_phase_pct_organic": round(phi * 100, 1),
                             "retention_time_min": round(float(noisy), 4)})
                rid += 1
    for rep in (1, 2):
        r = _rng_for(archive, "void_marker", rep)
        noisy = p["t0"] * (1 + r.normal(0, 0.004))
        rows.append({"row_id": rid, "compound_id": "void_marker", "injection_replicate": rep,
                     "mobile_phase_pct_organic": None, "retention_time_min": round(float(noisy), 4)})
        rid += 1

    def find(cid, phi, rep):
        for row in rows:
            if row["compound_id"] == cid and row["injection_replicate"] == rep and \
               (phi is None or row["mobile_phase_pct_organic"] == round(phi * 100, 1)):
                return row
        raise KeyError((cid, phi, rep))

    def add_out_of_window(cid, S_c, logP_c, phi):
        nonlocal rid
        true_tR = _tR_true(p["t0"], _kprime(p["a"], p["b"], S_c, logP_c, phi))
        r = _rng_for(archive, cid, phi, 1, "extra")
        rows.append({"row_id": rid, "compound_id": cid, "injection_replicate": 1,
                     "mobile_phase_pct_organic": round(phi * 100, 1),
                     "retention_time_min": round(float(true_tR * (1 + r.normal(0, 0.006))), 4)})
        rid += 1

    def corrupt_to_failed(cid, phi, rep):
        row = find(cid, phi, rep)
        r = _rng_for(archive, cid, phi, rep, "fail")
        row["retention_time_min"] = round(float(p["t0"] * (1 - abs(r.normal(0.04, 0.01)))), 4)

    if archive == "archive_A":
        corrupt_to_failed("cal_3", 0.40, 2)
        add_out_of_window("cal_2", 3.1, 1.62, 0.75)
    elif archive == "archive_B":
        corrupt_to_failed("cal_1", 0.30, 1)
        add_out_of_window("cal_4", 4.7, 3.15, 0.20)
        corrupt_to_failed("unknown", 0.50, 2)
    elif archive == "archive_C":
        add_out_of_window("cal_1", 2.3, 0.85, 0.72)

    return rows


def _spectroscopy_observation(archive: str, replicate_id):
    candidate = _ARCHIVES[archive]["candidate"]
    true_mz = _CANDIDATE_EXACT_MASS[candidate] + _PROTON_MASS
    r = _rng_for("spectroscopy", archive, replicate_id if replicate_id is not None else "central")
    ppm_noise = r.normal(0, 2.0) if replicate_id is not None else 0.0
    mz = true_mz * (1 + ppm_noise * 1e-6)
    return {"mz_M_plus_H": round(float(mz), 4)}


def _titration_observation(archive: str, replicate_id):
    true_pka = _CANDIDATE_PKA[_ARCHIVES[archive]["candidate"]]
    r = _rng_for("titration", archive, replicate_id if replicate_id is not None else "central")
    noise = r.normal(0, 0.03) if replicate_id is not None else 0.0
    return {"pKa": round(float(true_pka + noise), 4)}


def handle_query(mode: str, parameters: dict | None = None):
    global _used
    parameters = parameters or {}

    if mode == "help":
        return {
            "description": "An analytical-chemistry data source for one archive's unknown: a "
                            "high-resolution mass reading, an aqueous pKa (titration) reading, "
                            "and the archive's full raw HPLC injection log.",
            "modes": {
                "spectroscopy": "{archive: 'archive_A'|'archive_B'|'archive_C', replicate_id?: int} "
                                "-> {observation: {mz_M_plus_H: float}, unit: 'Da'}",
                "titration": "{archive: 'archive_A'|'archive_B'|'archive_C', replicate_id?: int} "
                             "-> {observation: {pKa: float}, unit: 'pKa units'}",
                "chromatography": "{archive: 'archive_A'|'archive_B'|'archive_C'} "
                                  "-> {observation: {injections: [...]}, unit: 'minutes'}",
            },
            "budget_remaining": _BUDGET - _used,
        }

    archive = parameters.get("archive")
    if archive not in _ARCHIVES:
        return {"error": f"unknown archive {archive!r} - expected one of {sorted(_ARCHIVES)}"}

    rid = parameters.get("replicate_id")
    if rid is not None:
        try:
            int(rid)
        except (TypeError, ValueError):
            return {"error": f"replicate_id must be an integer, got {rid!r}"}

    if mode == "spectroscopy":
        _used += 1
        if _used > _BUDGET:
            return {"error": "budget exceeded"}
        return {"observation": _spectroscopy_observation(archive, rid), "unit": "Da"}

    if mode == "titration":
        _used += 1
        if _used > _BUDGET:
            return {"error": "budget exceeded"}
        return {"observation": _titration_observation(archive, rid), "unit": "pKa units"}

    if mode == "chromatography":
        _used += 1
        if _used > _BUDGET:
            return {"error": "budget exceeded"}
        return {"observation": {"injections": _build_injection_log(archive)}, "unit": "minutes"}

    return {"error": f"unknown mode {mode!r}"}


query_oracle = handle_query
