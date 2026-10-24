"""Reader for the pulsar.55 output of the NBODY6++GPU pulsar module.

Each line of pulsar.55_XXXXXXXX.dat holds 20 columns (see docs/PULSAR55_FORMAT.md).
Lines that cannot be parsed are counted and skipped. A record is identified by
(time, NAME); every MPI process of the host writes its own copy of each line
(twice in Run 2, up to four times in Run 4), so duplicates are removed.
"""
import glob
import os

import numpy as np

COLUMNS = ["t_Myr", "NAME", "KSTAR", "P_s", "Pdot", "B_G",
           "x_pc", "y_pc", "z_pc", "vx_kms", "vy_kms", "vz_kms",
           "Fx", "Fy", "Fz", "E_total", "E_bind", "scenario", "lat_deg", "lon_deg"]
COL = {name: i for i, name in enumerate(COLUMNS)}


def read_run(directory):
    """Return (records, n_lines, n_unparsable) for one run directory.

    records: float array (n, 20), one row per distinct (t, NAME), sorted by time
    and NAME. NaN values are kept as NaN.
    """
    rows, n_lines, n_bad = [], 0, 0
    for path in sorted(glob.glob(os.path.join(directory, "pulsar.55_*.dat"))):
        with open(path) as handle:
            for line in handle:
                if not line.strip():
                    continue
                n_lines += 1
                fields = line.split()
                try:
                    if len(fields) != 20:
                        raise ValueError
                    rows.append([float(x) for x in fields])
                except ValueError:
                    n_bad += 1
    seen, unique = set(), []
    for row in rows:
        key = (round(row[0], 5), int(row[1]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    records = np.array(unique)
    order = np.lexsort((records[:, 1], records[:, 0]))
    return records[order], n_lines, n_bad


def per_star(records):
    """Dictionary NAME -> records of that star sorted in time."""
    out = {}
    for name in np.unique(records[:, 1]).astype(int):
        sel = records[records[:, 1] == name]
        out[name] = sel[np.argsort(sel[:, 0])]
    return out
