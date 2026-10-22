"""Recompute every number quoted from the pulsar.55 output in the paper.

Usage:  python scripts/paper_numbers.py            (from the repository root)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from pulsar55 import COL, per_star, read_run  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
YR = 3.15576e7            # s
MYR = 1e6 * YR            # s
DEATH = 0.17e12           # B/P^2 death line, G s^-2 (Bhattacharya & van den Heuvel 1991)
RT0 = 24.40               # initial tidal radius of the 5000-star model, pc

runs = {r: read_run(os.path.join(ROOT, "data", f"run{r}")) for r in (2, 3, 4)}

print("== Records per run")
for r, (rec, n_lines, n_bad) in runs.items():
    nan_p = np.mean(~np.isfinite(rec[:, COL["P_s"]]))
    print(f"Run {r}: lines {n_lines}, unparsable {n_bad}, distinct records {len(rec)}, "
          f"P undefined in {100 * nan_p:.1f}% ({np.sum(~np.isfinite(rec[:, COL['P_s']]))})")

a4 = runs[4][0]
P, Pd, B = a4[:, COL["P_s"]], a4[:, COL["Pdot"]], a4[:, COL["B_G"]]
pos = a4[:, COL["x_pc"]:COL["z_pc"] + 1]
vel = a4[:, COL["vx_kms"]:COL["vz_kms"] + 1]
scen = a4[:, COL["scenario"]].astype(int)
ebind = a4[:, COL["E_bind"]]

print("\n== Bit identity with Run 4 (same t and NAME)")
key4 = {(round(row[0], 5), int(row[1])): row for row in a4}
groups = {"position": slice(6, 9), "velocity": slice(9, 12), "force": slice(12, 15),
          "E_total": 15, "E_bind": 16, "KSTAR": 2, "scenario": 17,
          "P": 3, "Pdot": 4, "B": 5}
for r in (2, 3):
    rec = runs[r][0]
    out = []
    for name, sl in groups.items():
        same = []
        for row in rec:
            ref = key4[(round(row[0], 5), int(row[1]))]
            x, y = np.atleast_1d(row[sl]), np.atleast_1d(ref[sl])
            same.append(np.all((x == y) | (np.isnan(x) & np.isnan(y))))
        out.append(f"{name} {100 * np.mean(same):.1f}%")
    print(f"Run {r} vs 4 ({len(rec)} records): " + ", ".join(out))

print("\n== Run 3: factor by which Pdot falls between consecutive outputs")
ratios = []
for s in per_star(runs[3][0]).values():
    pdot = s[:, COL["Pdot"]]
    ok = (pdot[:-1] > 0) & (pdot[1:] > 0) & (pdot[1:] < pdot[:-1])
    ratios += list(pdot[:-1][ok] / pdot[1:][ok])
print(f"median factor {np.median(ratios):.3g} (n = {len(ratios)})")

print("\n== Run 4 neutron stars")
stars = per_star(a4)
for name, s in stars.items():
    v = np.linalg.norm(s[:, 9:12], axis=1)
    r = np.linalg.norm(s[:, 6:9], axis=1)
    u = s[:, 9:12] / v[:, None]
    ang = np.degrees(np.arccos(np.clip(u @ u[0], -1, 1))).max()
    dv = np.linalg.norm(s[:, 9:12] - s[:, 9:12].mean(0), axis=1).max()
    print(f"NS {name:3d}: t {s[0, 0]:.3f}-{s[-1, 0]:.3f} Myr ({s[-1, 0] - s[0, 0]:.3f}), "
          f"N {len(s)}, v {v.mean():.1f} km/s (range {100 * (v.max() - v.min()) / v.mean():.2f}%, "
          f"max |dv| {dv:.2f} km/s, direction {ang:.2f} deg), r {r[0]:.2f} -> {r[-1]:.2f} pc")
vall = np.linalg.norm(vel, axis=1)
print(f"speeds {vall.min():.1f}-{vall.max():.1f} km/s = {vall.min() / 2.561:.1f}-{vall.max() / 2.561:.0f} x v_rms(0)")
print(f"E_total > 0 in all records: {np.all(a4[:, COL['E_total']] > 0)}")

print("\n== Run 4 spin states")
g = Pd > 0
print(f"records with Pdot>0: {g.sum()} of {len(a4)}; Pdot = 0: {np.sum(Pd == 0)}, "
      f"labels of those: {sorted(set(scen[Pd == 0]))}")
print(f"P {1e3 * P.min():.2f}-{1e3 * P.max():.2f} ms; Pdot {Pd[g].min():.3g}-{Pd[g].max():.3g}; "
      f"B {B.min():.3g}-{B.max():.3g} G")
print(f"B/sqrt(P Pdot): {np.unique(np.round(B[g] / np.sqrt(P[g] * Pd[g]), -14))}")
tau = P[g] / (2 * Pd[g]) / YR
print(f"tau_c {tau.min():.3g}-{tau.max():.3g} yr, median {np.median(tau):.3g}, "
      f"fraction > 10 Gyr {np.mean(tau > 1e10):.3f}")
below = B / P ** 2 < DEATH
print(f"records below death line: {below.sum()}; NSs ending below: "
      f"{[n for n, s in stars.items() if s[-1, 5] / s[-1, 3] ** 2 < DEATH]}; "
      f"NSs never below: {[n for n, s in stars.items() if not np.any(s[:, 5] / s[:, 3] ** 2 < DEATH)]}")
unchanged, resolvable, factors, changes = 0, 0, [], []
for name, s in stars.items():
    for i in range(1, len(s)):
        if s[i, 3] == s[i - 1, 3] and s[i, 4] == s[i - 1, 4]:
            unchanged += 1
            dt = (s[i, 0] - s[i - 1, 0]) * MYR
            ulp = 10 ** (np.floor(np.log10(s[i, 3])) + 1 - 7)   # E15.7: 7 significant digits
            if s[i - 1, 4] * dt > ulp:
                resolvable += 1
                factors.append(s[i - 1, 4] * dt / ulp)
        else:
            changes.append((round(s[i, 0], 3), name, s[i, 3], s[i, 4]))
n_int = sum(len(s) - 1 for s in stars.values())
print(f"intervals {n_int}: unchanged {unchanged}, of which resolvable {resolvable} "
      f"(median factor {np.median(factors):.2f}); changed {len(changes)}")
for t, name, p, pd in sorted(changes):
    src = [(int(row[1]), round(row[0], 3)) for row in a4
           if row[3] == p and row[4] == pd and int(row[1]) != name and row[0] < t]
    print(f"  {t:.3f} Myr NS {name}: P -> {1e3 * p:.2f} ms, Pdot -> {pd:.3g}"
          + (f"  (state of NS {src[0][0]} at {src[0][1]:.3f} Myr)" if src else ""))
states = sum(len(set(zip(s[s[:, 4] > 0, 3], s[s[:, 4] > 0, 4]))) for s in stars.values())
print(f"distinct per-star states with Pdot>0: {states}")
frac = max(np.max(s[:, 4] * (s[-1, 0] - s[0, 0]) * MYR / s[:, 3]) for s in stars.values())
print(f"largest fractional dipole change of P over a recorded interval: {frac:.2g}")

print("\n== Run 4 scenario labels")
rr = np.linalg.norm(pos, axis=1)
for k in (1, 5, 7):
    m = scen == k
    print(f"S{k}: {m.sum()} steps, E_bind = 0 in {100 * np.mean(ebind[m] == 0):.1f}%, "
          f"median {np.median(ebind[m]):.3f}, min {ebind[m].min():.3f}, beyond {RT0} pc: {np.sum(rr[m] > RT0)}")
for name, s in stars.items():
    lab = s[:, 17].astype(int)
    seq = [lab[0]] + [lab[i] for i in range(1, len(lab)) if lab[i] != lab[i - 1]]
    tr = [f"S{lab[i - 1]}>S{lab[i]} {s[i, 0]:.3f}" for i in range(1, len(lab)) if lab[i] != lab[i - 1]]
    print(f"NS {name:3d}: {'>'.join('S%d' % x for x in seq)}  |  " + "; ".join(tr))
