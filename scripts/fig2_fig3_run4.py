"""Figs. 2 and 3 (final, A&A column width), from Maria's fig1_v4.py / fig2_v2.py.

Kept from her scripts: data selection (P, Pdot, B > 0; dedup by (t, NAME)),
NS fill palette, scenario ring palette, first/last markers, connecting tracks,
inline-labelled reference lines.
Changed (agreed 22 Oct 2026): constant-B coefficient (3.2e19)^2 instead of
9.75e38; death line now Bhattacharya & van den Heuvel (1991),
B/P^2 = 0.17e12 G s^-2; A&A style (no in-figure title, white background, no
grid, lower-case words); scenario names from the reference table; dipole lines
of Fig. 3 in grey shades (A&A: avoid red with green).
"""
import glob, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
RUN4 = os.path.join(ROOT, "data", "run4")

NS_COLORS = {4: '#C0392B', 5: '#7B2D8B', 6: '#1A7A3C', 516: '#E55A1C',
             517: '#E07B00', 518: '#C49A00', 519: '#546E7A',
             520: '#0E7C7B', 521: '#757575', 523: '#1565A0'}
SCEN_RING = {1: '#E6A817', 5: '#222222', 7: '#1A3A6B'}
SCEN_NAME = {1: 'S1: isolated pulsar', 5: 'S5: wide binary', 7: 'S7: NS–BH binary'}
ORDER = [517, 4, 516, 5, 523, 518, 521, 519, 6, 520]
INK, INK2 = '#111111', '#444444'
YR = 3.15576e7
K_DIP = (3.2e19) ** 2                       # B = 3.2e19 (P Pdot)^1/2 G
DL = (0.17e12 / 3.2e19) ** 2                # death line: Pdot = DL * P^3

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 7,
    'axes.linewidth': 0.7, 'axes.edgecolor': '#333333',
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': True, 'ytick.right': True,
    'xtick.major.size': 3.5, 'ytick.major.size': 3.5,
    'xtick.minor.size': 1.8, 'ytick.minor.size': 1.8,
    'xtick.labelsize': 7, 'ytick.labelsize': 7,
    'legend.fontsize': 5.8, 'legend.title_fontsize': 6,
})

# ---------------------------------------------------------------- data
rows = []
for f in sorted(glob.glob(os.path.join(RUN4, 'pulsar.55_*.dat'))):
    for line in open(f):
        v = line.split()
        if len(v) == 20:
            try:
                rows.append([float(x) for x in v])
            except ValueError:
                pass
seen, clean = set(), []
for r in rows:
    k = (round(r[0], 4), int(r[1]))
    if k not in seen:
        seen.add(k); clean.append(r)
data = np.array(clean)
valid = np.isfinite(data[:, 3]) & np.isfinite(data[:, 4]) & \
        (data[:, 3] > 0) & (data[:, 4] > 0) & (data[:, 5] > 0)
dv = data[valid]
print('records', len(data), 'plotted (Pdot>0)', len(dv))


def inline_label(ax, x, y, text, color, xfrac, yoff=1.12, size=5.6, below=False):
    vis = np.isfinite(y)
    xi, yi = x[vis], y[vis]
    lo, hi = ax.get_xlim(); ylo, yhi = ax.get_ylim()
    m = (xi >= lo) & (xi <= hi) & (yi >= ylo) & (yi <= yhi)
    xi, yi = xi[m], yi[m]
    if len(xi) < 5:
        return
    i = int(np.clip(len(xi) * xfrac, 2, len(xi) - 3))
    p0 = ax.transData.transform((xi[i - 2], yi[i - 2]))
    p1 = ax.transData.transform((xi[i + 2], yi[i + 2]))
    ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
    ax.text(xi[i], yi[i] * (1 / yoff if below else yoff), text, fontsize=size,
            color=color, rotation=ang, rotation_mode='anchor', ha='center',
            va='top' if below else 'bottom', zorder=6,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=0.4))


def draw_tracks(ax, xcol, ycol):
    for name in ORDER:
        d = dv[dv[:, 1] == name]
        if not len(d):
            continue
        d = d[np.argsort(d[:, 0])]
        x, y, s = d[:, xcol], d[:, ycol], d[:, 17].astype(int)
        c = NS_COLORS[name]
        if len(x) > 1:
            ax.plot(x, y, '-', color=c, lw=0.8, alpha=0.45, zorder=5)
        for i in range(len(x)):
            ax.scatter(x[i], y[i], s=13, c=c, edgecolors=SCEN_RING.get(s[i], '#444'),
                       linewidths=0.9, zorder=8)
        ax.scatter(x[0], y[0], s=34, c=c, edgecolors=INK, linewidths=1.0,
                   marker='o', zorder=10)
        ax.scatter(x[-1], y[-1], s=30, c=c, edgecolors=INK, linewidths=1.0,
                   marker='D', zorder=10)


def legends(ax, ns_loc, ns_anchor, sc_loc, sc_anchor, extra=None, ex_loc=None, ex_anchor=None):
    kw = dict(framealpha=0.92, facecolor='white', edgecolor='#999999',
              borderpad=0.45, labelspacing=0.25, handletextpad=0.4,
              borderaxespad=0.3, fancybox=False)
    ns = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=NS_COLORS[n],
                        markeredgecolor='#555', markeredgewidth=0.6, markersize=4.5,
                        label=f'NS {n}') for n in ORDER]
    l1 = ax.legend(handles=ns, ncol=2, loc=ns_loc, bbox_to_anchor=ns_anchor,
                   title='neutron star (fill)', columnspacing=0.8, **kw)
    ax.add_artist(l1)
    sc = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor='#dddddd',
                        markeredgecolor=SCEN_RING[s], markeredgewidth=1.3, markersize=4.5,
                        label=SCEN_NAME[s]) for s in (1, 5, 7)]
    sc += [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor='#999',
                         markeredgecolor=INK, markeredgewidth=0.9, markersize=5,
                         label='first recorded step'),
           mlines.Line2D([0], [0], marker='D', color='w', markerfacecolor='#999',
                         markeredgecolor=INK, markeredgewidth=0.9, markersize=4.5,
                         label='last recorded step')]
    l2 = ax.legend(handles=sc, loc=sc_loc, bbox_to_anchor=sc_anchor,
                   title='scenario (ring)', **kw)
    if extra:
        ax.add_artist(l2)
        ax.legend(handles=extra, loc=ex_loc, bbox_to_anchor=ex_anchor, **kw)


def finish(fig, ax, name):
    for s in ax.spines.values():
        s.set_color('#333333')
    fig.savefig(os.path.join(OUT, name + '.pdf'), bbox_inches='tight', pad_inches=0.02)
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=400, bbox_inches='tight',
                pad_inches=0.02, facecolor='white')
    plt.close(fig)


# ================================================================ Fig. 2  P-Pdot
Plo, Phi, Ylo, Yhi = 1e-3, 1e0, 1e-23, 1e-15
fig = plt.figure(figsize=(3.46, 4.22))
ax = fig.add_axes([0.155, 0.300, 0.80, 0.685])
lax = fig.add_axes([0.0, 0.0, 1.0, 0.205]); lax.set_axis_off()
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(Plo, Phi); ax.set_ylim(Ylo, Yhi)
ax.axvspan(Plo, 0.03, color='#eaf2fb', zorder=0, lw=0)
ax.text(1.3e-3, 7e-16, 'millisecond pulsars', fontsize=6, color='#1565A0', va='top')
ax.text(0.037, 7e-16, 'normal pulsars', fontsize=6, color='#7a5a10', va='top')
fig.canvas.draw()
P = np.logspace(-3.2, 0.2, 800)
for lgB, xf in [(8, 0.86), (9, 0.86), (10, 0.70), (11, 0.80)]:
    y = (10.0 ** lgB) ** 2 / (K_DIP * P)
    ax.plot(P, y, '--', color='#C8641E', lw=0.7, alpha=0.85, zorder=1)
    inline_label(ax, P, y, rf'$10^{{{lgB}}}$ G', '#B0520F', xf)
for tau, lab, xf in [(1e7, '10 Myr', 0.10), (1e10, '10 Gyr', 0.10)]:
    y = P / (2 * tau * YR)
    ax.plot(P, y, ':', color='#2E7D32', lw=0.9, zorder=1)
    inline_label(ax, P, y, lab, '#2E7D32', xf)
ydl = DL * P ** 3
ax.plot(P, ydl, '-', color=INK, lw=1.3, zorder=4)
inline_label(ax, P, ydl, 'death line', INK, 0.80, yoff=1.6, size=6)
draw_tracks(ax, 3, 4)
ax.set_xlabel(r'$P$ (s)', fontsize=8)
ax.set_ylabel(r'$\dot P$ (s s$^{-1}$)', fontsize=8)
kw = dict(framealpha=1.0, facecolor='white', edgecolor='#aaaaaa', borderpad=0.45,
          labelspacing=0.25, handletextpad=0.4, fancybox=False)
ns = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=NS_COLORS[n],
                    markeredgecolor='#555', markeredgewidth=0.6, markersize=4.5,
                    label=f'NS {n}') for n in ORDER]
l1 = lax.legend(handles=ns, ncol=2, loc='upper left', bbox_to_anchor=(0.01, 1.0),
                title='neutron star (fill)', columnspacing=0.7, **kw)
lax.add_artist(l1)
sc = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor='#dddddd',
                    markeredgecolor=SCEN_RING[k], markeredgewidth=1.3, markersize=4.5,
                    label=SCEN_NAME[k]) for k in (1, 5, 7)]
sc += [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor='#999',
                     markeredgecolor=INK, markeredgewidth=0.9, markersize=5,
                     label='first recorded step'),
       mlines.Line2D([0], [0], marker='D', color='w', markerfacecolor='#999',
                     markeredgecolor=INK, markeredgewidth=0.9, markersize=4.5,
                     label='last recorded step')]
l2 = lax.legend(handles=sc, loc='upper left', bbox_to_anchor=(0.395, 1.0),
                title='scenario (ring)', **kw)
lax.add_artist(l2)
ref = [mlines.Line2D([0], [0], color='#C8641E', lw=0.8, ls='--', label=r'constant $B$'),
       mlines.Line2D([0], [0], color='#2E7D32', lw=0.9, ls=':', label=r'constant $\tau_{\rm c}$'),
       mlines.Line2D([0], [0], color=INK, lw=1.3, label='death line')]
l3 = lax.legend(handles=ref, loc='upper left', bbox_to_anchor=(0.745, 1.0),
                title='reference lines', **kw)
for L in (l1, l2, l3):
    L.get_frame().set_linewidth(0.5)
for sp in ax.spines.values():
    sp.set_color('#333333')
fig.savefig(os.path.join(OUT, 'Fig2_PPdot_run4_final.pdf'), pad_inches=0.02)
fig.savefig(os.path.join(OUT, 'Fig2_PPdot_run4_final.png'), dpi=400, facecolor='white')
plt.close(fig)

# ================================================================ Fig. 3  Pdot-B
Blo, Bhi, Ylo, Yhi = 1e8, 1e10, 1e-22, 1e-18
fig, ax = plt.subplots(figsize=(3.46, 3.2))
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(Blo, Bhi); ax.set_ylim(Ylo, Yhi)
fig.canvas.draw()
B = np.logspace(7.8, 10.2, 800)
greys = ['#BBBBBB', '#949494', '#6B6B6B', '#3F3F3F']
for (Ps, lab, xf), col in zip([(0.005, '5 ms', 0.80), (0.025, '25 ms', 0.80),
                               (0.050, '50 ms', 0.80), (0.085, '85 ms', 0.80)], greys):
    y = B ** 2 / K_DIP / Ps
    ax.plot(B, y, '--', color=col, lw=0.9, zorder=1)
    inline_label(ax, B, y, rf'$P$ = {lab}', col if col != '#BBBBBB' else '#8a8a8a', xf,
                 below=(lab == '85 ms'))
draw_tracks(ax, 5, 4)
ax.set_xlabel(r'$B$ (G)', fontsize=8)
ax.set_ylabel(r'$\dot P$ (s s$^{-1}$)', fontsize=8)
finish(fig, ax, 'Fig3_PdotB_run4_final')
print('done')
