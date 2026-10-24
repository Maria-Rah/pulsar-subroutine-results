# The four runs

All four runs were made with NBODY6++GPU and the pulsar module on the Chewbacca GPU server of the
National Astronomical Observatories of China (NAOC). The set-up below is read from the input files
([`data/inputs`](../data/inputs)) and the host logs ([`data/logs`](../data/logs)); the cluster quantities from the
host diagnostics archived in `data/run1/*GUIDE.txt` and `data/run2/*GUIDE.txt`; the pulsar quantities are computed
from `data/run*/pulsar.55_*.dat` by `scripts/paper_numbers.py`.

## Set-up

| | Run 1 | Runs 2–4 |
|---|---|---|
| Input file (MD5) | `run1_N50k.inp` (993fb2ef…) | `runs2-4_N50k.inp` (7b7c31d1…, the same for Runs 2, 3, and 4) |
| N, primordial binaries | 50 000, 2500 | 5000, 500 |
| Metallicity Z | 0.001 | 0.0002 |
| Stellar-evolution level (Kamlah et al. 2022) | B | C |
| Initial model | Plummer, Q = 0.5, length scale 1.223 pc | same |
| Mass function | Kroupa (2001), 0.08–150 M☉ | same |
| Tidal field | point-mass galaxy of 1.78 × 10¹¹ M☉ at 13.3 kpc | same |
| Time unit T* | 0.11429 Myr | 0.35158 Myr |
| End time, output interval (TCRIT = 80, DELTAT = 0.1 in N-body units) | 9.14 Myr, 0.0114 Myr | 28.13 Myr, 0.0352 Myr |
| Escaper removal | at about twice the tidal radius (KZ(23) = 2) | same |
| Processes | 2 MPI × 16 OpenMP threads, one GPU each | same for Runs 2 and 3; not recorded for Run 4 |
| CPU time of the host | 48.3 min | 3.0 min |

All four runs end normally at TCRIT. The "80 Myr" in the folder names is 80 N-body time units.

## Cluster models

| | Run 1 | Runs 2–4 |
|---|---|---|
| Global outputs | 801 (every 0.0114 Myr) | 801 (every 0.0352 Myr) |
| Core radius, initial → final | 0.473 → 0.549 pc | 0.549 → 0.746 pc |
| Tidal radius, initial → final | 51.61 → 50.35 pc | 24.40 → 22.22 pc |
| Core density, initial → final | 3.73 × 10⁴ → 5.28 × 10³ M☉ pc⁻³ | 3.65 × 10³ → 1.52 × 10² M☉ pc⁻³ |
| rms velocity, initial → final | 7.938 → 5.288 km s⁻¹ | 2.561 → 1.156 km s⁻¹ |
| Relative energy error, first adjustment interval | 0.12 | 0.15 |
| Relative energy error, all later intervals together | −1.9 × 10⁻³ | 1.4 × 10⁻⁴ |
| Neutron stars formed by the host / recorded | 0 / 0 | 11 / 10 |

Energy errors are ΔE/max(T, |E|) as defined in `adjust.F` (T kinetic, E total energy).

## What the host did

- **Input.** Every log prints `inbse: invalid Namelist format`. The `&INBSE` line of the input contains `NSFLAG`,
  `BHFLAG`, and `PSFLAG`, which belong to `&INSSE`, so the whole block was rejected and the defaults of each level
  were used. Level C: NS flag 4, PS 1, MD 4, BH 2, KMECH 4, λ = 0, α = 1, BHSPINFL 0, KICKTYPE −2, σ = 265 km s⁻¹.
- **Primordial binaries.** At set-up the host prints negative orbital periods for them (P_min = −1.07 × 10¹¹ d,
  P_max = 0). In Runs 2–4 no regularised pair is left at the first output (0.035 Myr) or at any later output:
  `bdat.9` holds the 500 pairs at t = 0 and only its header afterwards. Run 1 loses its pairs within 0.05 Myr. The
  runs therefore evolve as clusters of single stars.
- **Natal kicks.** Maxwellian with σ = 265 km s⁻¹ (Hobbs et al. 2005), multiplied by (1 − f_fb), by 1.4 M☉/M_NS,
  and by 0.1 when the carbon–oxygen core exceeds 3 M☉ (`kick.F` sets `KMECH = 3` at every call, overriding the
  level value 4). The 5000-star model forms 18 BHs (4.0–40.5 M☉; kicks of 0.6–11.8 km s⁻¹ or zero) and 11 NSs
  (1.28–2.46 M☉; kicks of 18–517 km s⁻¹). The 50 000-star model forms 82 BHs and no NS by 9.14 Myr. The kick events
  are listed in [`data/logs/run3_kicks.csv`](../data/logs/run3_kicks.csv) and
  [`data/logs/run1_kicks.csv`](../data/logs/run1_kicks.csv).
- **Escapers.** By 28.13 Myr, 500 single stars have left the 5000-star model (N = 4500), among them all 11 NSs
  ([`data/logs/run4_esc11_neutron_stars.txt`](../data/logs/run4_esc11_neutron_stars.txt)).

## Versions of the module and what each run wrote

| | Run 1 | Run 2 | Run 3 | Run 4 |
|---|---|---|---|---|
| Lines / distinct records in `pulsar.55` | – | 563 / 286 | 568 / 152 (265 lines unparsable) | 1141 / 286 |
| P | – | drawn; NaN in 77 records (26.9%) | drawn; NaN in 77 records (50.7%) | drawn; all finite |
| Ṗ | – | 0 wherever defined | falls by a factor of about 3.96 × 10¹⁶ per output until redrawn | > 0, except 13 S7 records set to 0 |
| B | – | 0 in all records | falls by about 2 × 10⁸ per output | B = 3.22873 × 10¹⁹ (PṖ)^½ G exactly when Ṗ > 0 |

- **In every run** the block of `file_init.F` that initialises the module arrays and coefficients stands after the
  `RETURN` statement and is never executed. This was noticed while preparing Run 2, but the block was not moved.
  The routine instead draws new values wherever P and B are both zero and replaces a zero `XKFIELD` and `XKTAU` by
  built-in values. All other coefficients and `ATHRESH` are zero, so in Runs 2–4 Ṗ is the dipole term alone and the
  S5 test needs only a positive separation ([MODULE_REVIEW.md](MODULE_REVIEW.md), item 0).
- **Run 1** stopped at 9.14 Myr, before the first NS formed. The module had no NS to process.
- **Run 2**: the undefined periods first appear at steps labelled S7 (NS 4, 517, and 521) and are then carried
  along, also to NS 518 when it takes over the state of NS 517. In S6 and S7 the merger term divides the mass
  change by the reference mass `XMNS0`, which is zero at indices where it was never set.
- **Run 3**: the dipole term and the field estimator used different values of the speed of light, one in
  CGS units and one in code units. Each recomputation of B from Ṗ, followed by Ṗ from B, multiplies Ṗ by the
  cube of the ratio of the two values, which gives the discrete bands at Ṗ ≈ 10⁻²⁰, 10⁻³⁷, 10⁻⁵⁴, 10⁻⁷¹,
  and 10⁻⁸⁸ s s⁻¹ in Fig. 1c of the paper.
- **Run 4**: c = 3 × 10¹⁰ cm s⁻¹ in both places, an undefined Ṗ replaced by 0, and an undefined or non-positive P
  reset to 1 ms (never triggered). The source compiled for Run 4 is
  [`code/calc_and_save_pulsar_params_v4_CORRECTED.f`](../code/calc_and_save_pulsar_params_v4_CORRECTED.f).
- Every MPI process writes its own copy of each line: Run 2, with two processes, has 277 of its 286 records twice;
  Run 4 has 283 records four times and 3 records three times.

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

For the whole cluster, the escaper lists (`esc.11`) and the Lagrangian radii (`lagr.7`) of Runs 3 and 4 are
identical byte for byte. The spin computations therefore do not change the N-body integration, and the scenario
label depends only on the dynamical state. The identical values of P come from identical initial draws: the module
uses the random-number generator of the host (`RAN2` with seed `IDUM1`). For the same reason it may shift later
random draws of the host, for example natal kicks, relative to a run without the module; all three runs contain the
module, so this comparison cannot test it.

## The neutron stars of Run 4

| NS | Group | Label sequence | Supernova (Myr) | First record (Myr) | Records | Mean speed (km s⁻¹) | r first → last (pc) | Removed (Myr) |
|---|---|---|---|---|---|---|---|---|
| 517 | 1 | S1→S5→S7→S5→S1→S5 | 16.598 | 16.630 | 67 | 19.3 | 0.40 → 44.99 | 18.985 |
| 4 | 2 | S1→S5→S7→S5→S7→S5 | 16.697 | 16.700 | 39 | 33.3 | 2.13 → 44.67 | 18.071 |
| 516 | 3 | S1→S5→S7→S1 | 15.045 | 15.048 | 54 | 24.1 | 2.46 → 45.17 | 16.946 |
| 5 | 3 | S1→S5→S7→S1 | 20.831 | 20.849 | 38 | 33.0 | 1.09 → 44.81 | 22.185 |
| 523 | 4 | S1→S5 | 27.322 | 27.353 | 2 | 515.5 | 17.18 → 35.44 | 27.423 |
| 518 | 5 | S1→S7→S5→S7→S1 | 16.936 | 16.946 | 56 | 22.8 | 1.31 → 45.85 | 18.915 |
| 521 | 6 | S7→S1 | 22.476 | 22.501 | 6 | 212.1 | 6.12 → 43.92 | 22.712 |
| 519 | 7 | S1 | 19.392 | 19.407 | 18 | 70.9 | 0.72 → 43.53 | 20.040 |
| 6 | 7 | S1 | 26.506 | 26.509 | 3 | 414.2 | 1.42 → 30.92 | 26.615 |
| 520 | 7 | S1 | 21.675 | 21.692 | 3 | 439.6 | 9.27 → 42.65 | 21.798 |
| 522 | – | not recorded | 24.979 | – | 0 | (362.6 after the kick) | – | 24.997 |

All recorded NSs move on almost straight lines (speed constant to 1.4%, direction to 4°, velocity vector to better
than 1 km s⁻¹) and are removed 0.10–2.39 Myr after their supernova; none is retained and none has a bound companion.
NS 522 forms at least 39 pc from the centre and is removed at the next output, before the module is called. Full
per-star details, including every change of spin state, are in [NEUTRON_STARS.md](NEUTRON_STARS.md).

## Notes on the archive

- The log of Run 4 was not preserved (`output_run4.log` contains one line of a shell error); its host evolution is
  that of Run 3 ([`data/logs/run3_output_run3_extract.txt`](../data/logs/run3_output_run3_extract.txt)).
- The folder `run1_results` in the home directory on Chewbacca holds copies of Run 2 files, not of Run 1; the
  original Run 1 folder is complete. The Run 1 numbers of this repository come from the original folder.
