"""Fig. 1 preview: comparison of the four NBODY6++GPU runs.

Every number is read from the archived run outputs:
  Runs 2-4: pulsar.55_*.dat files (20 columns), deduplicated by (t, NAME)
  Run 1   : GLOBAL/SEV GUIDE.txt summaries (no pulsar.55 records, no NS)
"""
import glob, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "figures", "main", "Fig1_four_runs.png")

# ---------------------------------------------------------------- data
def read_run(run):
    d = os.path.join(ROOT, "data", run)
    lines, bad, rows = 0, 0, []
    for f in sorted(glob.glob(os.path.join(d, "pulsar.55_*.dat"))):
        for line in open(f):
            lines += 1
            v = line.split()
            try:
                if len(v) != 20:
                    raise ValueError
                rows.append([float(x) for x in v])
            except ValueError:
                bad += 1
    seen, conflict = {}, set()
    for r in rows:
        k = (round(r[0], 5), int(r[1]))
        if k in seen:
            same = all((a == b) or (np.isnan(a) and np.isnan(b))
                       for a, b in zip(seen[k], r))
            if not same:
                conflict.add(k)
            continue
        seen[k] = r
    return dict(lines=lines, unparsable=bad, rec=seen, conflict=len(conflict))

R = {r: read_run(r) for r in ["run2", "run3", "run4"]}
EXPECTED = len(R["run4"]["rec"])          # 286 (t, NAME) pairs
assert set(R["run2"]["rec"]) == set(R["run4"]["rec"])

# Run 1 (top-level version) from its GUIDE summaries
RUN1 = dict(N=50000, t_end=9.14, n_ns=0)
T_END_5K = 28.13                         # Runs 2-4, GLOBAL GUIDE of Run 2

a4 = np.array(list(R["run4"]["rec"].values()))
ns_ids = sorted(set(a4[:, 1].astype(int)))
win = {n: (a4[a4[:, 1] == n, 0].min(), a4[a4[:, 1] == n, 0].max()) for n in ns_ids}

# ---------------------------------------------------------------- style
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
RUNC = {"run1": "#2a78d6", "run2": "#eb6834", "run3": "#1baf7a", "run4": "#eda100"}
RUNLAB = {"run1": "Run 1", "run2": "Run 2", "run3": "Run 3", "run4": "Run 4"}
GOOD, ZERO, BAD, MISS = "#2a78d6", "#c4c3bc", "#d55e00", "#ffffff"   # no red with green (A&A)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5,
    "axes.edgecolor": "#9a9890", "axes.linewidth": 0.6,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.titlesize": 8, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "figure.facecolor": "white", "axes.facecolor": "white",
    "xtick.direction": "in", "ytick.direction": "in",
})

fig = plt.figure(figsize=(6.9, 7.9), dpi=300)
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1.25], hspace=0.55,
                      wspace=0.42, left=0.135, right=0.985, top=0.955,
                      bottom=0.315)
gs_e = fig.add_gridspec(1, 1, left=0.135, right=0.985, top=0.165,
                        bottom=0.065)

# ---------------------------------------------------------------- (a)
ax = fig.add_subplot(gs[0, :])
ax.set_title("(a)  Integrated time and the interval in which neutron stars exist", fontweight="normal")
ys = {"run1": 3, "run2": 2, "run3": 1, "run4": 0}
ax.axvspan(min(w[0] for w in win.values()), max(w[1] for w in win.values()),
           color="#f3efe3", zorder=0)
for run, y in ys.items():
    tend = RUN1["t_end"] if run == "run1" else T_END_5K
    if run == "run3":   # end time not in the archive: solid to last record
        tlast = max(k[0] for k in R["run3"]["rec"])
        ax.barh(y, tlast, height=0.42, color=RUNC[run], zorder=2)
        ax.barh(y, tend - tlast, left=tlast, height=0.42, color="white",
                edgecolor=RUNC[run], hatch="....", linewidth=0.6, zorder=2)
    else:
        ax.barh(y, tend, height=0.42, color=RUNC[run], zorder=2)
ax.set_yticks([3, 2, 1, 0])
ax.set_yticklabels(["Run 1\nN = 50 000", "Run 2\nN = 5 000",
                    "Run 3\nN = 5 000", "Run 4\nN = 5 000"], color=INK)
ax.tick_params(axis="y", length=0)
ax.text(RUN1["t_end"] + 0.35, 3, "stops at 9.14 Myr, before any neutron star forms",
        va="center", color=INK2, fontsize=7)
for run, y in [("run2", 2), ("run3", 1), ("run4", 0)]:
    ax.text(T_END_5K + 0.35, y, f"{len(R[run]['rec'])} records",
            va="center", color=INK2, fontsize=7)
# per-NS tracked windows: one lane per NS, ordered by first record
for i, n in enumerate(sorted(ns_ids, key=lambda k: win[k][0])):
    t0, t1 = win[n]
    yk = 3.55 + 0.2 * i
    ax.plot([t0, max(t1, t0 + 0.06)], [yk, yk], color=INK, lw=1.6,
            solid_capstyle="butt", zorder=3)
    ax.text(max(t1, t0 + 0.06) + 0.25, yk, f"NS {n}", ha="left",
            va="center", fontsize=5.8, color=INK2)
ax.text(14.6, 4.45, "interval in which each\nneutron star is recorded", ha="right",
        va="center", fontsize=6.5, color=INK2)
ax.set_xlim(0, 33.5); ax.set_ylim(-0.5, 5.55)
ax.set_xlabel("Physical time $t$ (Myr)")
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)

# ---------------------------------------------------------------- (b)
ax = fig.add_subplot(gs[1, 0])
ax.set_title("(b)  Status of the 286 records", pad=4, fontweight="normal")
qty = [(3, "$P$"), (4, r"$\dot P$"), (5, "$B$")]
ypos, ylab = [], []
y = 0
for run in ["run4", "run3", "run2"]:
    rec = R[run]["rec"]
    arr = np.array(list(rec.values()))
    for c, lab in qty[::-1]:
        x = arr[:, c]
        good = np.sum(np.isfinite(x) & (x > 0))
        zero = np.sum(x == 0)
        nan = np.sum(~np.isfinite(x))
        miss = EXPECTED - len(arr)
        left = 0
        for val, col, hatch in [(good, GOOD, None), (zero, ZERO, None),
                                (nan, BAD, None), (miss, MISS, "//////")]:
            if val:
                ax.barh(y, val / EXPECTED * 100, left=left, height=0.72,
                        color=col, edgecolor="#6b6a64" if hatch else "white",
                        hatch=hatch, linewidth=0.5 if hatch else 0.8)
                left += val / EXPECTED * 100
        ypos.append(y); ylab.append(lab)
        y += 1
    ax.text(0.5, y - 0.35, f"{RUNLAB[run]}", va="bottom", ha="left",
            fontsize=7, color=INK, fontweight="bold")
    y += 1.0
ax.set_yticks(ypos); ax.set_yticklabels(ylab)
ax.set_xlim(0, 100); ax.set_xlabel("Share of records (%)")
ax.set_ylim(-0.7, y - 0.5)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.legend(handles=[Patch(color=GOOD, label="finite, > 0"),
                   Patch(color=ZERO, label="exactly 0"),
                   Patch(color=BAD, label="NaN"),
                   Patch(facecolor=MISS, edgecolor="#6b6a64", hatch="//////",
                         label="line not readable")],
          loc="upper center", bbox_to_anchor=(0.55, -0.2), ncol=2,
          frameon=False, fontsize=6.5, handlelength=1.4, columnspacing=0.8)

# ---------------------------------------------------------------- (c), (d)
rng = np.random.default_rng(3)
def sci(v):
    m, e = f"{v:.1e}".split("e")
    return rf"${m}\times10^{{{int(e)}}}$"
for k, (c, lab, unit, xl) in enumerate([
        (4, r"$\dot P$", r"$\dot P$ (s s$^{-1}$)", (1e-92, 1e-17)),
        (5, "$B$", r"$B$ (G)", (1e-36, 1e11))]):
    ax = fig.add_subplot(gs[1, 1 + k])
    ax.set_title(f"({'cd'[k]})  Recorded {lab}", fontweight="normal")
    for j, run in enumerate(["run4", "run3", "run2"]):
        arr = np.array(list(R[run]["rec"].values()))
        x = arr[:, c]
        pos = x[np.isfinite(x) & (x > 0)]
        if len(pos):
            yy = j + rng.uniform(-0.22, 0.22, len(pos))
            ax.scatter(pos, yy, s=7, color=RUNC[run], edgecolor="white",
                       linewidth=0.3, zorder=3)
            lo, hi = pos.min(), pos.max()
            ax.text(xl[1] * 0.6, j + 0.36, f"{sci(lo)} to {sci(hi)}",
                    ha="right", va="bottom", fontsize=6, color=INK2)
        else:
            ax.text(np.sqrt(xl[0] * xl[1]), j, "no value > 0", ha="center",
                    va="center", fontsize=6.5, color=INK2, style="italic")
    ax.set_xscale("log"); ax.set_xlim(*xl)
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["Run 4", "Run 3", "Run 2"])
    ax.set_ylim(-0.6, 2.75); ax.set_xlabel(unit)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_major_locator(matplotlib.ticker.LogLocator(numticks=6))
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())

# ---------------------------------------------------------------- (e)
ax = fig.add_subplot(gs_e[0, 0])
ax.set_title("(e)  Fraction of records bit-identical to Run 4", pad=16, fontweight="normal")
cols = [(slice(6, 9), "position"), (slice(9, 12), "velocity"),
        (slice(12, 15), "force"), (15, r"$E_\mathrm{total}$"),
        (16, r"$E_\mathrm{bind}$"), (2, "KSTAR"), (17, "scenario"),
        (3, "$P$"), (4, r"$\dot P$"), (5, "$B$")]
M, rowlab = [], []
for run in ["run2", "run3"]:
    common = sorted(set(R[run]["rec"]) & set(R["run4"]["rec"]))
    row = []
    for c, _ in cols:
        A = np.array([np.atleast_1d(R[run]["rec"][q][c]) for q in common])
        B = np.array([np.atleast_1d(R["run4"]["rec"][q][c]) for q in common])
        row.append(np.all((A == B) | (np.isnan(A) & np.isnan(B)), axis=1).mean())
    M.append(row); rowlab.append(f"{RUNLAB[run]} vs Run 4\n{len(common)} records")
M = np.array(M)
cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    "blue", ["#f4f8fd", "#9ec5f4", "#3987e5", "#184f95"])
ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, f"{M[i, j]:.3f}", ha="center", va="center", fontsize=7,
                color="white" if M[i, j] > 0.6 else INK)
ax.set_xticks(range(len(cols))); ax.set_xticklabels([c[1] for c in cols])
ax.set_yticks([0, 1]); ax.set_yticklabels(rowlab)
ax.axvline(6.5, color=INK, lw=1.2)
ax.text(3.0, -0.62, "from the N-body state (incl. scenario label)", ha="center", va="bottom", fontsize=7, color=INK2)
ax.text(8.0, -0.62, "spin parameters", ha="center", va="bottom", fontsize=7, color=INK2)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)

fig.savefig(OUT, dpi=400)
fig.savefig(OUT.replace(".png", ".pdf"))
print("saved", OUT)
print("conflicting duplicate keys:", {r: R[r]["conflict"] for r in R})
print("matrix:\n", np.round(M, 3))
