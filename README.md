# pulsar-subroutine-results

Results, data, and scripts of the paper

> **Tracking the spin and magnetic field of millisecond pulsars in globular clusters with NBODY6++GPU-MSP.
> I. Implementation and first four runs**
> M. Rah, R. Spurzem, A. Mickaelian, F. Flammini Dotti (A&A, in preparation)

NBODY6++GPU-MSP is the direct N-body code NBODY6++GPU together with a pulsar module that computes, for every
neutron star (NS) at every output, the spin period P, its derivative Ṗ, and the surface magnetic field B, and
assigns the star to one of seven physical scenarios (S1–S7). This repository holds everything behind the paper
that does not fit in it: the `pulsar.55` records of the runs, the 20 individual tracking diagrams of the NSs of
Run 4 with full captions, the scripts that reproduce every figure and every number of the paper, and detailed
notes on the runs, the module, and the history of the scenario labels through the series.

The module code and its standalone validation are in
[Maria-Rah/pulsar-subroutine-testing](https://github.com/Maria-Rah/pulsar-subroutine-testing).

## Origin of the model and contribution of the series

The physical model of the module was piloted on the NS prescription used by Ye et al. (2019) in Cluster Monte
Carlo (CMC) models: dipole spin-down, exponential field decay, and spin-up by accretion. Song et al. (2025)
independently brought the pulsar model of Chattopadhyay et al. (2020) into NBODY6++GPU. The contribution of this
series is (i) the implementation of the model as a self-contained module of NBODY6++GPU, validated beforehand
outside the host with two independent codes (Rah 2026, RAA), which writes the spin of every NS together with
its dynamical state, and (ii) the classification of every NS at every output into seven physical scenarios.

## What the four runs show

| Run | N | Time covered | Neutron stars | Module output |
|---|---|---|---|---|
| 1 | 50 000 | 0–9.14 Myr | none formed | – |
| 2 | 5000 | 0–28.13 Myr | 10 | P drawn, Ṗ = B = 0, P undefined in 27% of records |
| 3 | 5000 | 0 to ≥ 27.39 Myr | 10 | Ṗ falls by ~4 × 10¹⁶ per output (c mismatch) |
| 4 | 5000 | 0–28.13 Myr | 10 | 286 finite records |

- The module does not feed back on the host: positions, velocities, forces, energies, stellar types, and labels
  are bit-identical in Runs 2–4.
- The ten NSs of Run 4 form between 15.0 and 27.4 Myr with speeds of 19–516 km s⁻¹, far above the rms velocity
  of 2.6 km s⁻¹, and leave the cluster on straight paths within 2.3 Myr. None is retained, none has a bound
  companion.
- Their recorded P (5.6–97.5 ms) and B (1.7–9.9 × 10⁸ G) lie in the ranges from which the module draws its
  initial values; P and Ṗ are unchanged in 258 of 276 intervals, and the remaining changes are transfers between
  stars or new draws, because the spin arrays follow the particle index. Labels S1, S5, and S7 are assigned; S5
  and S7 follow the particle taken from the neighbour list, not a bound companion.
- Every departure of the module from the physical model, and its correction for Paper II, is listed in
  [docs/MODULE_REVIEW.md](docs/MODULE_REVIEW.md).

## Contents

| Path | Content |
|---|---|
| [`docs/RUNS.md`](docs/RUNS.md) | Cluster models, module versions, what each run wrote, bit identity, the ten NSs |
| [`docs/SCENARIOS.md`](docs/SCENARIOS.md) | Reference definitions of S1–S7 and the history of each label through the series |
| [`docs/MODULE_REVIEW.md`](docs/MODULE_REVIEW.md) | Departures of the Run 4 module version from the physical model, with code lines |
| [`docs/NEUTRON_STARS.md`](docs/NEUTRON_STARS.md) | Every NS of Run 4: label intervals, spin states, every change of state |
| [`docs/PULSAR55_FORMAT.md`](docs/PULSAR55_FORMAT.md) | Columns and units of the `pulsar.55` records |
| [`figures/main/`](figures/main) | The five figures of the paper (PNG and PDF) |
| [`figures/appendix/`](figures/appendix) | 20 tracking diagrams (FigA and FigB for each NS) and [their captions](figures/appendix/CAPTIONS.md) |
| [`data/`](data) | `pulsar.55` files of Runs 2–4, Run 4 as CSV, host diagnostics summaries of Runs 1 and 2 |
| [`scripts/`](scripts) | Reader, number reproduction, figure scripts |
| [`code/`](code) | The module source whose logic produced the Run 4 records |

## Reproducing the paper

Python 3 with NumPy, Matplotlib, and Pillow. From the repository root:

```bash
python scripts/paper_numbers.py                 # every number quoted from pulsar.55
python scripts/make_star_docs.py                # docs/NEUTRON_STARS.md and figures/appendix/CAPTIONS.md
python scripts/fig1_four_runs.py out/Fig1.png   # Fig. 1
python scripts/fig2_fig3_run4.py out            # Figs. 2 and 3
python scripts/fig4_fig5_compose.py out         # Figs. 4 and 5 (from figures/appendix)
```

The figure scripts reproduce the files in `figures/main` pixel for pixel. `scripts/edit_appendix_labels.py`
documents the only change made to the 20 original tracking diagrams (S7 legend entry and energy axis labels).

## References

- Chattopadhyay D. et al. 2020, MNRAS 494, 1587
- Rah M. 2026, RAA, doi:10.1088/1674-4527/ae983c
- Rah M., Spurzem R., Mickaelian A., Flammini Dotti F. 2026, ComBAO 73, 68
- Song Y. et al. 2025, arXiv:2511.08850
- Ye C. S. et al. 2019, ApJ 877, 122

Contact: Maria Rah (mariarah.astro@bao.sci.am)
