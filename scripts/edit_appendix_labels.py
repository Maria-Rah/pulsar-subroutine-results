"""Target-element edits on the 20 original appendix PNGs (Run 4).

Only two kinds of text are changed; every other pixel is kept:
  1. legend entry  'S7: Merger/kick'  ->  'S7: NS–BH binary'  (FigA and FigB)
  2. FigB y-axis labels  '(N-body)'   ->  '(code units)'      (E_total, E_bind)
New text is rendered with the same font (DejaVu Sans, matplotlib) at a size
calibrated on the original text it replaces.
"""
import glob, io, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seg import load, rowsegs, runs

SRC = sys.argv[1]   # folder with the original diagrams
DST = sys.argv[2]   # output folder
os.makedirs(DST, exist_ok=True)
INK = "#111111"


def render(text, size_pt, color=INK, rotate=False, dpi=100):
    """Render text tightly with matplotlib; returns an RGB PIL image on white."""
    fig = plt.figure(figsize=(0.01, 0.01), dpi=dpi)
    t = fig.text(0, 0, text, fontsize=size_pt, color=color,
                 family="DejaVu Sans", rotation=90 if rotate else 0)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight",
                pad_inches=0.02, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    im = Image.open(buf).convert("RGB")
    g = np.asarray(im.convert("L"))
    ys, xs = np.where(g < 200)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def ink_box(g, x0, x1, y0, y1, thr=150):
    sub = g[y0:y1, x0:x1] < thr
    ys, xs = np.where(sub)
    return x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1


def calibrate(text, target, axis, rotate=False):
    """Font size (pt at dpi=100) whose rendered ink extent matches target px."""
    lo, hi = 4.0, 60.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        im = render(text, mid, rotate=rotate)
        ext = im.size[0] if axis == "x" else im.size[1]
        if ext < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


log = []
for f in sorted(glob.glob(os.path.join(SRC, "Fig*_run4.png"))):
    name = os.path.basename(f)
    im, g = load(f)
    out = im.copy()
    W, H = im.size
    # ---------------- 1. legend entry S7 ----------------
    rs = [(int(a), int(b)) for a, b in rowsegs(g, 8 if name.startswith("FigB") else 25)]
    a, b = rs[-1]
    y0, y1 = a + 7, b - 6
    arr = np.asarray(im)[y0:y1]
    navy = np.where((np.abs(arr[..., 0].astype(int) - 26) < 25) &
                    (np.abs(arr[..., 1].astype(int) - 58) < 25) &
                    (np.abs(arr[..., 2].astype(int) - 107) < 25))
    if len(navy[1]):
        nx1 = int(navy[1].max())
        segs = [(int(p), int(q)) for p, q in runs((g[y0:y1] < 150).any(0), 18)]
        txt = [s for s in segs if s[0] > nx1][0]
        nxt = [s for s in segs if s[0] > txt[1]][0]
        bx0, by0, bx1, by1 = ink_box(g, txt[0], txt[1] + 1, y0, y1)
        size = calibrate("S7: Merger/kick", bx1 - bx0, "x")
        new = render("S7: NS–BH binary", size)
        room = nxt[0] - 14 - bx0
        if new.size[0] > room:
            new = render("S7: NS–BH", size)
        # blank old text (legend face is white) and paste new, same baseline box
        out.paste((255, 255, 255), (bx0 - 2, by0 - 3, txt[1] + 3, by1 + 3))
        ytop = by1 - new.size[1] + (0 if "g" not in "S7: NS–BH binary" else 0)
        # align by vertical centre of the original ink box
        yc = (by0 + by1) // 2 - new.size[1] // 2
        out.paste(new, (bx0, yc))
        log.append(f"{name}: legend S7 text {bx1-bx0}px -> {new.size[0]}px (room {room})")
    # ---------------- 2. FigB energy axis labels ----------------
    if name.startswith("FigB"):
        rsb = [(int(p), int(q)) for p, q in rowsegs(g, 8)]
        # last two big panels before the tick labels are E_total and E_bind
        big = [s for s in rsb if s[1] - s[0] > 300]
        # E_total is the panel above E_bind; panels may be merged in the
        # segmentation, so locate labels by column scanning in two row bands
        eb = big[-1]
        et = (eb[0] - 394, eb[0] - 15)
        for (r0, r1), old, newtxt in [
                (et, r"$E_{\rm total}$ (N-body)", r"$E_{\rm total}$ (code units)"),
                (eb, r"$E_{\rm bind}$ (N-body)", r"$E_{\rm bind}$ (code units)")]:
            cols = [(int(p), int(q)) for p, q in runs((g[r0:r1, :260] < 150).any(0), 6)]
            lab = cols[0]
            bx0, by0, bx1, by1 = ink_box(g, lab[0], lab[1] + 1, r0, r1)
            size = calibrate(old, by1 - by0, "y", rotate=True)
            new = render(newtxt, size, rotate=True)
            xc = (bx0 + bx1) // 2 - new.size[0] // 2
            yc = (by0 + by1) // 2 - new.size[1] // 2
            if yc < r0 or yc + new.size[1] > r1:
                log.append(f"{name}: WARNING label does not fit in panel {old}")
            out.paste((255, 255, 255), (bx0 - 2, by0 - 2, bx1 + 2, by1 + 2))
            out.paste(new, (xc, max(yc, r0)))
            log.append(f"{name}: {old} {by1-by0}px -> {new.size[1]}px")
    out.save(os.path.join(DST, name))
print("\n".join(log))
