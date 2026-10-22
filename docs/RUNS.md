# The four runs

All four runs were made with NBODY6++GPU and the pulsar module on the Chewbacca GPU server of the
National Astronomical Observatories of China (NAOC). The cluster quantities below are taken from the
host diagnostics archived in `data/run1/*GUIDE.txt` and `data/run2/*GUIDE.txt`; the pulsar quantities are
computed from `data/run*/pulsar.55_*.dat` by `scripts/paper_numbers.py`.

## Cluster models

Both models use a Kroupa (2001) initial mass function. Runs 2–4 start from the same initial realisation
and differ only in the version of the module (their dynamics are bit-identical, see below).

| | Run 1 | Runs 2–4 |
|---|---|---|
| N | 50 000 | 5000 |
| Primordial binaries | 2500 | 500 |
| Physical time covered | 0–9.14 Myr | 0–28.13 Myr (Run 3: records up to 27.39 Myr; end time not archived) |
| Global outputs | 801 (every 0.0114 Myr) | 801 (every 0.0352 Myr) |
| Core radius, initial → final | 0.473 → 0.549 pc | 0.549 → 0.746 pc |
| Tidal radius, initial → final | 51.61 → 50.35 pc | 24.40 → 22.22 pc |
| Core density, initial → final | 3.73 × 10⁴ → 5.28 × 10³ M☉ pc⁻³ | 3.65 × 10³ → 1.52 × 10² M☉ pc⁻³ |
| rms velocity, initial → final | 7.938 → 5.288 km s⁻¹ | 2.561 → 1.156 km s⁻¹ |
| Relative energy error | 3.7 × 10⁻⁶ | 9.9 × 10⁻⁹ |
| Neutron stars recorded | 0 | 10 |

The archive of Run 1 also contains a second realisation of the same model with 500 primordial binaries
(`data/run1/realisation_v2`), which reaches 9.36 Myr and likewise forms no NS.

## Versions of the module and what each run wrote

| | Run 1 | Run 2 | Run 3 | Run 4 |
|---|---|---|---|---|
| Lines / distinct records in `pulsar.55` | – | 563 / 286 | 568 / 152 (265 lines unparsable) | 1141 / 286 |
| P | – | drawn at first call; NaN in 77 records (26.9%) | drawn; NaN in 77 records (50.7%) | drawn; all finite |
| Ṗ | – | 0 wherever defined | falls by a factor of about 3.96 × 10¹⁶ per output until redrawn | > 0, except 13 S7 records set to 0 |
| B | – | 0 in all records | falls by about 2 × 10⁸ per output | B = 3.22873 × 10¹⁹ (PṖ)^½ G exactly when Ṗ > 0 |

- **Run 1** stopped at 9.14 Myr, before the first NS formed. The module had no NS to process. While preparing
  Run 2, the block of `file_init.F` that initialises the module arrays and coefficients was found after a
  `RETURN` statement (never executed) and moved before it.
- **Run 2**: the undefined periods first appear at steps labelled S7 (NS 4, 517, and 521) and are then carried
  along, also to NS 518 when it takes over the state of NS 517. In S6 and S7 the merger term divides the mass
  change by the reference mass `XMNS0`, which is zero at indices where it was never set.
- **Run 3**: the dipole term and the field estimator used different values of the speed of light, one in
  CGS units and one in code units. Each recomputation of B from Ṗ, followed by Ṗ from B, multiplies Ṗ by the
  cube of the ratio of the two values, which gives the discrete bands at Ṗ ≈ 10⁻²⁰, 10⁻³⁷, 10⁻⁵⁴, 10⁻⁷¹,
  and 10⁻⁸⁸ s s⁻¹ in Fig. 1c of the paper.
- **Run 4**: c in CGS units in both places, and Ṗ set to 0 when the merger term is undefined. These two changes
  are not in the file `code/calc_and_save_pulsar_params_v5_CORRECTED.f`, whose logic is otherwise the one
  that produced the Run 4 records (see [MODULE_REVIEW.md](MODULE_REVIEW.md)).

## The module does not feed back on the host

Comparing each record of Runs 2 and 3 with the record of the same NS at the same time in Run 4:

| Quantity | Run 2 vs Run 4 (286 records) | Run 3 vs Run 4 (152 records) |
|---|---|---|
| position, velocity, force | 100% | 100% |
| E_total, E_bind | 100% | 100% |
| stellar type, scenario label | 100% | 100% |
| P | 73.1% | 49.3% |
| Ṗ | 0% | 13.8% |
| B | 0% | 50.7% |

The spin computations therefore do not change the N-body integration, and the scenario label depends only on
the dynamical state. The identical values of P come from identical initial draws: the module uses the
random-number generator of the host (`RAN2` with seed `IDUM1`). For the same reason it may shift later random
draws of the host, for example natal kicks, relative to a run without the module; all three runs contain the
module, so this comparison cannot test it.

## The ten neutron stars of Run 4

| NS | Group | Label sequence | First record (Myr) | Records | Mean speed (km s⁻¹) | r first → last (pc) |
|---|---|---|---|---|---|---|
| 517 | 1 | S1→S5→S7→S5→S1→S5 | 16.630 | 67 | 19.3 | 0.40 → 44.99 |
| 4 | 2 | S1→S5→S7→S5→S7→S5 | 16.700 | 39 | 33.3 | 2.13 → 44.67 |
| 516 | 3 | S1→S5→S7→S1 | 15.048 | 54 | 24.1 | 2.46 → 45.17 |
| 5 | 3 | S1→S5→S7→S1 | 20.849 | 38 | 33.0 | 1.09 → 44.81 |
| 523 | 4 | S1→S5 | 27.353 | 2 | 515.5 | 17.18 → 35.44 |
| 518 | 5 | S1→S7→S5→S7→S1 | 16.946 | 56 | 22.8 | 1.31 → 45.85 |
| 521 | 6 | S7→S1 | 22.501 | 6 | 212.1 | 6.12 → 43.92 |
| 519 | 7 | S1 | 19.407 | 18 | 70.9 | 0.72 → 43.53 |
| 6 | 7 | S1 | 26.509 | 3 | 414.2 | 1.42 → 30.92 |
| 520 | 7 | S1 | 21.692 | 3 | 439.6 | 9.27 → 42.65 |

All ten move on almost straight lines (speed constant to 1.4%, direction to 4°, velocity vector to better
than 1 km s⁻¹) and leave the cluster within 0.035–2.32 Myr; none is retained and none has a bound companion.
Full per-star details, including every change of spin state, are in [NEUTRON_STARS.md](NEUTRON_STARS.md).
