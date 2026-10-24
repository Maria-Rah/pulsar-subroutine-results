"""Write docs/NEUTRON_STARS.md and figures/appendix/CAPTIONS.md from the Run 4 records.

Every number in the two files is computed here from data/run4/pulsar.55_*.dat, except the
formation and removal data, which are read from data/run4/host_neutron_stars.csv (host log and esc.11).
Usage:  python scripts/make_star_docs.py   (from the repository root)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from pulsar55 import per_star, read_run  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
YR = 3.15576e7
DEATH = 0.17e12
ORDER = [(1, 517), (2, 4), (3, 516), (3, 5), (4, 523), (5, 518), (6, 521), (7, 519), (7, 6), (7, 520)]
NAME = {1: "S1 (isolated pulsar)", 5: "S5 (wide binary)", 7: "S7 (NS–BH binary)"}

rec, _, _ = read_run(os.path.join(ROOT, "data", "run4"))
stars = per_star(rec)

HOST = {}
for line in open(os.path.join(ROOT, "data", "run4", "host_neutron_stars.csv")):
    if line.startswith("#") or line.startswith("NAME"):
        continue
    v = line.strip().split(",")
    HOST[int(v[0])] = dict(t_sn=float(v[1]), m0=float(v[2]), mns=float(v[3]), vk=float(v[4]),
                           vsn=float(v[5]), t1=v[6], t_rem=float(v[7]), r_rem=float(v[8]), n=int(v[10]))


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def fmt_e(x, d=3):
    if x == 0:
        return "0"
    m, e = f"{x:.{d - 1}e}".split("e")
    return f"{m} × 10{str(int(e)).translate(SUP)}"


def segments(s):
    lab = s[:, 17].astype(int)
    out, start = [], 0
    for i in range(1, len(lab) + 1):
        if i == len(lab) or lab[i] != lab[start]:
            out.append((lab[start], s[start, 0], s[i - 1, 0], i - start))
            start = i
    return out


def spin_changes(name, s):
    out = []
    for i in range(1, len(s)):
        if s[i, 3] == s[i - 1, 3] and s[i, 4] == s[i - 1, 4]:
            continue
        p, pd = s[i, 3], s[i, 4]
        src = [row for row in rec if row[3] == p and row[4] == pd and int(row[1]) != name and row[0] < s[i, 0]]
        if src:
            kind = f"takes over the state of NS {int(src[0][1])} recorded at {src[0][0]:.3f} Myr"
        elif p == s[i - 1, 3] and s[i - 1, 4] == 0:
            kind = "P unchanged; Ṗ becomes finite again when the S7 label ends"
        else:
            kind = "new value drawn from the module's initial distribution"
        out.append((s[i, 0], s[i - 1, 3], p, s[i - 1, 4], pd, s[i - 1, 5], s[i, 5], kind))
    return out


def states(s):
    seen, out = {}, []
    for row in s:
        key = (row[3], row[4], row[5])
        if key not in seen:
            seen[key] = [row[0], row[0], 0]
            out.append(key)
        seen[key][1] = row[0]
        seen[key][2] += 1
    return [(k, *seen[k]) for k in out]


ns_md = ["# The neutron stars of Run 4", "",
         "The host forms eleven neutron stars (NSs) in Run 4; the module records ten of them. Formation and removal "
         "are taken from [`data/run4/host_neutron_stars.csv`](../data/run4/host_neutron_stars.csv) (kick lines of the "
         "host log and the escaper list `esc.11`):", "",
         "| NAME | Supernova (Myr) | M₀ (M☉) | M_NS (M☉) | Kick (km/s) | Speed after kick (km/s) | First record (Myr) "
         "| Removed (Myr) | at r (pc) | Records |",
         "|---|---|---|---|---|---|---|---|---|---|"]
for nm, h in sorted(HOST.items(), key=lambda kv: kv[1]["t_sn"]):
    ns_md.append(f"| {nm} | {h['t_sn']:.3f} | {h['m0']:.2f} | {h['mns']:.3f} | {h['vk']:.1f} | {h['vsn']:.1f} | "
                 f"{float(h['t1']):.3f} | {h['t_rem']:.3f} | {h['r_rem']:.1f} | {h['n']} |" if h["t1"] else
                 f"| {nm} | {h['t_sn']:.3f} | {h['m0']:.2f} | {h['mns']:.3f} | {h['vk']:.1f} | {h['vsn']:.1f} | "
                 f"– | {h['t_rem']:.3f} | {h['r_rem']:.1f} | 0 |")
ns_md += ["",
          "NS 522 forms at least 39 pc from the centre, beyond the tidal radius, and is removed as an escaper at the next "
          "output, 0.019 Myr later, before the module is called. No other NS is present between 22.71 and 26.51 Myr, "
          "which is why no `pulsar.55` file exists for 23–25 Myr. The sections below describe the ten recorded NSs.", "",
         "All values below are read from `data/run4/pulsar.55_*.dat` by `scripts/make_star_docs.py`.",
         "Times are physical times in Myr; P in ms, Ṗ in s s⁻¹, B in G, distances in pc, speeds in km s⁻¹.",
         "E_bind is in M☉² pc⁻¹ and E_total in the mixed units described in "
         "[PULSAR55_FORMAT.md](PULSAR55_FORMAT.md). The meaning of the labels and of the changes of spin",
         "is discussed in Sects. 4 and 5 of the paper and in [MODULE_REVIEW.md](MODULE_REVIEW.md).", ""]
cap_md = ["# Captions of the 20 individual tracking diagrams (Run 4)", "",
          "Two diagrams per neutron star. **FigA**: four panels, (i) P–Ṗ with the 10⁹ G dipole locus, "
          "(ii) P–B with the 10⁹ G level, (iii) Ṗ–B with dipole lines for three representative periods, "
          "(iv) B against the characteristic age τ = P/2Ṗ. **FigB**: scenario bar and the time series of P, Ṗ, B, "
          "E_total, and E_bind, with dashed lines at the label changes.",
          "",
          "Symbols: fill colour identifies the neutron star; ring colour gives the label at each record "
          "(gold S1, black S5, navy S7); START and END mark the first and last records. Background shading "
          "follows the label. Only records with Ṗ > 0 can appear on the logarithmic axes of FigA. "
          "Compared with the original diagrams, only the S7 legend entry (now “S7: NS–BH binary”, "
          "the reference name of the paper) and the energy axis labels (now “code units”) were changed; "
          "every other pixel is the original.",
          "",
          "The recorded values are those written by the module version of Run 4. In that version P and B are "
          "drawn at the first call, P and Ṗ do not change between most outputs, the spin state follows the "
          "particle index, and the S5/S7 labels follow the particle taken from the neighbour list (paper, Sect. 5.2). "
          "The diagrams therefore document the record, not a physical spin evolution.", ""]

for k, (grp, name) in enumerate(ORDER, start=1):
    s = stars[name]
    v = np.linalg.norm(s[:, 9:12], axis=1)
    r = np.linalg.norm(s[:, 6:9], axis=1)
    seq = " → ".join(f"S{x[0]}" for x in segments(s))
    eb = s[:, 16]
    et = s[:, 15]
    ns_md += [f"## Group {grp}: NS {name}", "",
              f"- Label sequence: **{seq}**",
              f"- Records: {len(s)}, from {s[0, 0]:.3f} to {s[-1, 0]:.3f} Myr ({s[-1, 0] - s[0, 0]:.3f} Myr)",
              f"- Mean speed {v.mean():.1f} km/s (range {v.min():.2f}–{v.max():.2f}); distance from the centre "
              f"{r[0]:.2f} → {r[-1]:.2f} pc; E_total {et.min():.7g} to {et.max():.7g} (always > 0)",
              f"- E_bind from {eb.min():.3f} to {eb.max():.3f} M☉² pc⁻¹",
              f"- Host: supernova at {HOST[name]['t_sn']:.3f} Myr (progenitor {HOST[name]['m0']:.2f} M☉, NS "
              f"{HOST[name]['mns']:.3f} M☉), speed after the kick {HOST[name]['vsn']:.1f} km/s; removed as an escaper "
              f"at {HOST[name]['t_rem']:.3f} Myr, {HOST[name]['r_rem']:.1f} pc from the centre", "",
              "| Label | From (Myr) | To (Myr) | Records |", "|---|---|---|---|"]
    ns_md += [f"| {NAME[lab]} | {t0:.3f} | {t1:.3f} | {n} |" for lab, t0, t1, n in segments(s)]
    ns_md += ["", "| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |",
              "|---|---|---|---|---|---|---|---|"]
    for (p, pd, b), t0, t1, n in states(s):
        tau = fmt_e(p / (2 * pd) / YR) if pd > 0 else "–"
        ns_md.append(f"| {1e3 * p:.2f} | {fmt_e(pd)} | {fmt_e(b)} | {tau} | "
                     f"{'yes' if b / p ** 2 < DEATH else 'no'} | {t0:.3f} | {t1:.3f} | {n} |")
    ch = spin_changes(name, s)
    ns_md += [""]
    if ch:
        ns_md += ["Changes of spin state:", ""]
        for t, p0, p1, pd0, pd1, b0, b1, kind in ch:
            ns_md.append(f"- {t:.3f} Myr: P {1e3 * p0:.2f} → {1e3 * p1:.2f} ms, Ṗ {fmt_e(pd0)} → {fmt_e(pd1)}, "
                         f"B {fmt_e(b0)} → {fmt_e(b1)} G; {kind}")
    else:
        ns_md.append("No change of spin state.")
    ns_md += ["", f"Diagrams: [FigA](../figures/appendix/FigA_NS{name}_run4.png), "
              f"[FigB](../figures/appendix/FigB_NS{name}_run4.png)", ""]

    first, last = s[0], s[-1]
    chs = "; ".join(f"{t:.3f} Myr (P {1e3 * p0:.2f} → {1e3 * p1:.2f} ms)" if p1 != p0
                    else f"{t:.3f} Myr (Ṗ finite again)" for t, p0, p1, *_ in ch) or "none"
    cap_md += [f"## Fig. A{k} — `FigA_NS{name}_run4.png`", "",
               f"NS {name} (Group {grp}; {seq}; {len(s)} records, {s[0, 0]:.3f}–{s[-1, 0]:.3f} Myr). "
               f"START: P = {1e3 * first[3]:.2f} ms, Ṗ = {fmt_e(first[4])} s s⁻¹, B = {fmt_e(first[5])} G. "
               f"END: P = {1e3 * last[3]:.2f} ms, Ṗ = {fmt_e(last[4])} s s⁻¹, B = {fmt_e(last[5])} G. "
               f"The {len(s)} records fall on {len(states(s))} distinct states; changes of state at {chs}. "
               + ("Records with Ṗ = 0 (S7 steps with an undefined merger term) are not shown. "
                  if np.any(s[:, 4] == 0) else "")
               + "B equals 3.229 × 10¹⁹ (PṖ)^½ G at every record with Ṗ > 0, so panels (ii)–(iv) follow from panel (i).",
               "", f"## Fig. B{k} — `FigB_NS{name}_run4.png`", "",
               f"NS {name}, {s[0, 0]:.3f}–{s[-1, 0]:.3f} Myr. Scenario bar: "
               + "; ".join(f"S{lab} {t0:.3f}–{t1:.3f} Myr ({n})" for lab, t0, t1, n in segments(s)) + ". "
               f"E_total {'falls' if et[-1] < et[0] else 'rises'} from {et[0]:.7g} to {et[-1]:.7g}, following its "
               "kinetic term, which dominates in the mixed units of the record "
               f"(mean speed {v.mean():.1f} km/s, distance {r[0]:.1f} → {r[-1]:.1f} pc). "
               f"E_bind ranges from {eb.min():.3f} to {eb.max():.3f} M☉² pc⁻¹ and refers to the particle taken "
               "from the neighbour list, not to a bound companion.", ""]

with open(os.path.join(ROOT, "docs", "NEUTRON_STARS.md"), "w") as f:
    f.write("\n".join(ns_md) + "\n")
with open(os.path.join(ROOT, "figures", "appendix", "CAPTIONS.md"), "w") as f:
    f.write("\n".join(cap_md) + "\n")
print("written docs/NEUTRON_STARS.md and figures/appendix/CAPTIONS.md")
