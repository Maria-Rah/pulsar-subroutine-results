"""Figs. 4 and 5 previews, composed from the 20 original appendix PNGs.

The original panels are cropped and placed unchanged (no re-plotting, no
rescaling of one axis against the other). New elements are limited to the
cell headers (group, NS, number of steps, scenario sequence read from
pulsar.55) and, in Fig. 5, one optional summary panel drawn from pulsar.55.
"""
import glob, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seg import load, rowsegs, colsegs

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FIG = os.path.join(ROOT, "figures", "appendix")
RUN4 = os.path.join(ROOT, "data", "run4")
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "."

# --------------------------------------------------------------- pulsar.55
rows = []
for f in sorted(glob.glob(os.path.join(RUN4, "pulsar.55_*.dat"))):
    for line in open(f):
        v = line.split()
        if len(v) == 20:
            rows.append([float(x) for x in v])
rec = {}
for r in rows:
    rec.setdefault((round(r[0], 5), int(r[1])), r)
A = np.array(list(rec.values()))


def ns_info(n):
    s = A[A[:, 1] == n]
    s = s[np.argsort(s[:, 0])]
    seq = [int(s[0, 17])]
    for x in s[1:, 17].astype(int):
        if x != seq[-1]:
            seq.append(x)
    return dict(n=len(s), t0=s[0, 0], t1=s[-1, 0], seq=seq)


# groups re-derived from the scenario column (col 18) of pulsar.55
ORDER = [(1, 517), (2, 4), (3, 516), (3, 5), (4, 523), (5, 518),
         (6, 521), (7, 519), (7, 6), (7, 520)]
INFO = {n: ns_info(n) for _, n in ORDER}

# palette sampled from the original appendix figures
SC = {1: ("#e6a817", "#fff9c4"), 5: ("#222222", "#f1f1f1"),
      7: ("#1a3a6b", "#e5eff9")}
INK, INK2 = "#111111", "#555555"
plt.rcParams.update({"font.family": "DejaVu Sans"})


def header(fig, x, y, w, g, n, extra):
    """Group chip, NS name, extra text, then the scenario-sequence chips.
    x, y, w in figure fractions; sizes are set in inches."""
    Win, Hin = fig.get_size_inches()
    fx, fy = 1 / Win, 1 / Hin
    info = INFO[n]
    h = 0.115 * fy
    def box(x0, wbox, fc, ec, lw=0):
        fig.patches.append(FancyBboxPatch((x0, y), wbox, h, transform=fig.transFigure,
                           boxstyle=f"round,pad=0,rounding_size={0.025 * fx}",
                           fc=fc, ec=ec, lw=lw, mutation_aspect=Win / Hin))
    box(x, 0.22 * fx, INK, "none")
    fig.text(x + 0.11 * fx, y + h / 2, f"G{g}", color="white", fontsize=6.5,
             fontweight="bold", ha="center", va="center")
    fig.text(x + 0.27 * fx, y + h / 2, f"NS {n}", color=INK, fontsize=7,
             fontweight="bold", ha="left", va="center")
    fig.text(x + 0.74 * fx, y + h / 2, extra, color=INK2, fontsize=5.6,
             ha="left", va="center")
    cw, gap = 0.138 * fx, 0.022 * fx
    seq = info["seq"]
    xx = x + w - len(seq) * cw - (len(seq) - 1) * gap
    for s_ in seq:
        fg, bg = SC[s_]
        box(xx, cw, bg, fg, 0.8)
        fig.text(xx + cw / 2, y + h / 2, f"S{s_}", color=fg, fontsize=4.9,
                 fontweight="bold", ha="center", va="center")
        xx += cw + gap


def place(fig, img, x, y, w):
    """Put a PIL image at figure coords (x, y bottom-left), width w, true aspect."""
    W, H = fig.get_size_inches()
    h = w * W * img.size[1] / img.size[0] / H
    ax = fig.add_axes([x, y, w, h])
    ax.imshow(np.asarray(img), interpolation="lanczos")
    ax.set_axis_off()
    return h


# --------------------------------------------------------------- crops
def crop_A_ppdot(n):
    im, g = load(f"{FIG}/FigA_NS{n}_run4.png")
    rs = [r for r in rowsegs(g, 25)]
    big = [r for r in rs if r[1] - r[0] > 300][0]
    top = rs[1][0] - 6                       # first block below the title
    cs = [c for c in colsegs(g, top, big[1], 25) if c[0] < g.shape[1] / 2]
    return im.crop((int(cs[0][0]) - 4, int(top), int(cs[-1][1]) + 6, int(big[1]) + 6))


def crop_A_legend(n):
    im, g = load(f"{FIG}/FigA_NS{n}_run4.png")
    a, b = rowsegs(g, 25)[-1]
    c = colsegs(g, a, b + 1, 40)
    return im.crop((int(c[0][0]) - 6, int(a) - 6, int(c[-1][1]) + 6, int(b) + 6))


def crop_B(n, which):
    im, g = load(f"{FIG}/FigB_NS{n}_run4.png")
    rs = [(int(a), int(b)) for a, b in rowsegs(g, 8)]
    if which == "bar+ebind":
        bar = im.crop((0, rs[1][0] - 4, im.size[0], rs[1][1] + 6))
        eb = im.crop((0, rs[-4][0] - 6, im.size[0], rs[-2][1] + 6))
        out = Image.new("RGB", (im.size[0], bar.size[1] + eb.size[1] + 8), "white")
        out.paste(bar, (0, 0)); out.paste(eb, (0, bar.size[1] + 8))
        return out
    if which == "legend":
        a, b = rs[-1]
        c = colsegs(g, a, b + 1, 40)
        return im.crop((int(c[0][0]) - 6, a - 6, int(c[-1][1]) + 6, b + 6))


# --------------------------------------------------------------- Fig. 4
def grid_layout(imgs, ncol, width_in, mx_in, gx_in, head_in, gy_in, tail_in):
    """Return figure height (in) and, per image, (x, y_top) in inches from top."""
    w_in = (width_in - 2 * mx_in - (ncol - 1) * gx_in) / ncol
    pos, y, rowmax = [], mx_in, 0.0
    for i, im in enumerate(imgs):
        r, c = divmod(i, ncol)
        if c == 0 and i > 0:
            y += rowmax + gy_in
            rowmax = 0.0
        h = w_in * im.size[1] / im.size[0]
        rowmax = max(rowmax, head_in + h)
        pos.append((mx_in + c * (w_in + gx_in), y, w_in, h))
    return y + rowmax + tail_in, pos, w_in


def put(fig, Hin, Win, img, x, ytop, w, h):
    ax = fig.add_axes([x / Win, 1 - (ytop + h) / Hin, w / Win, h / Hin])
    ax.imshow(np.asarray(img), interpolation="lanczos")
    ax.set_axis_off()


def fig4():
    Win, head = 6.69, 0.17
    imgs = [crop_A_ppdot(n) for _, n in ORDER]
    Hin, pos, w = grid_layout(imgs, 3, Win, 0.05, 0.09, head, 0.10, 0.05)
    fig = plt.figure(figsize=(Win, Hin), dpi=500)
    for (g, n), img, (x, y, w_, h) in zip(ORDER, imgs, pos):
        header(fig, x / Win, 1 - (y + 0.13) / Hin, w_ / Win, g, n,
               f"{INFO[n]['n']} steps")
        put(fig, Hin, Win, img, x, y + head, w_, h)
    # legend and note in the two free slots of the last row
    leg = crop_A_legend(517)
    x0 = pos[-1][0] + w + 0.09
    lw = 2 * w + 0.09
    lh = lw * leg.size[1] / leg.size[0]
    y0 = pos[-1][1] + head + (pos[-1][3] - lh) / 2
    put(fig, Hin, Win, leg, x0, y0, lw, lh)
    fig.savefig(f"{OUTDIR}/fig4_preview.png", dpi=500, facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------- Fig. 5
def fig5(summary=True):
    Win, head = 6.69, 0.17
    imgs = [crop_B(n, "bar+ebind") for _, n in ORDER]
    tail = 2.05 if summary else 0.35
    Hin, pos, w = grid_layout(imgs, 2, Win, 0.05, 0.10, head, 0.09, tail)
    fig = plt.figure(figsize=(Win, Hin), dpi=500)
    for (g, n), img, (x, y, w_, h) in zip(ORDER, imgs, pos):
        info = INFO[n]
        header(fig, x / Win, 1 - (y + 0.13) / Hin, w_ / Win, g, n,
               f"t = {info['t0']:.2f}\u2013{info['t1']:.2f} Myr")
        put(fig, Hin, Win, img, x, y + head, w_, h)
    ybot = max(p[1] + head + p[3] for p in pos)
    leg = crop_B(517, "legend")
    lw = 4.2
    lh = lw * leg.size[1] / leg.size[0]
    put(fig, Hin, Win, leg, (Win - lw) / 2, ybot + 0.08, lw, lh)
    if summary:
        top = ybot + 0.08 + lh + 0.38
        ax = fig.add_axes([0.13, 1 - (Hin - 0.40) / Hin, 0.82,
                           (Hin - 0.40 - top) / Hin])
        rng = np.random.default_rng(1)
        for j, s in enumerate([1, 5, 7]):
            e = A[A[:, 17] == s, 16]
            yy = j + rng.uniform(-0.25, 0.25, len(e))
            fg, bg = SC[s]
            ax.scatter(e, yy, s=9, color=fg, edgecolor="white", lw=0.3, zorder=3)
            ax.text(0.5, j, f"{len(e)} steps, median {np.median(e):.2f}".replace("-", "\u2212"),
                    va="center", ha="left", fontsize=6, color=INK2)
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["S1", "S5", "S7"], fontsize=7, fontweight="bold")
        for t, s in zip(ax.get_yticklabels(), [1, 5, 7]):
            t.set_color(SC[s][0])
        ax.set_xlim(-11, 4.2); ax.set_ylim(-0.6, 2.6)
        ax.axvline(0, color="#999999", lw=0.6, zorder=1)
        ax.set_xlabel(r"$E_\mathrm{bind}$ recorded at the same step (code units)",
                      fontsize=6.5)
        ax.tick_params(labelsize=6)
        ax.set_ylabel("scenario assigned", fontsize=6.5)
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        ax.tick_params(direction="in", top=False, right=False)
    fig.savefig(f"{OUTDIR}/fig5_preview.png", dpi=500, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    for _, n in ORDER:
        i = INFO[n]
        print(n, i["n"], f"{i['t0']:.3f}-{i['t1']:.3f}", "->".join(f"S{s}" for s in i["seq"]))
    fig4()
    fig5()
    print("done")
