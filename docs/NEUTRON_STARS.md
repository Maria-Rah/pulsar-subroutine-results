# The neutron stars of Run 4

The host forms eleven neutron stars (NSs) in Run 4; the module records ten of them. Formation and removal are taken from [`data/run4/host_neutron_stars.csv`](../data/run4/host_neutron_stars.csv) (kick lines of the host log and the escaper list `esc.11`):

| NAME | Supernova (Myr) | M₀ (M☉) | M_NS (M☉) | Kick (km/s) | Speed after kick (km/s) | First record (Myr) | Removed (Myr) | at r (pc) | Records |
|---|---|---|---|---|---|---|---|---|---|
| 516 | 15.045 | 15.29 | 2.461 | 24.3 | 24.2 | 15.048 | 16.946 | 46.5 | 54 |
| 517 | 16.598 | 14.21 | 1.999 | 18.3 | 19.5 | 16.630 | 18.985 | 46.1 | 67 |
| 4 | 16.697 | 14.15 | 1.974 | 33.5 | 33.4 | 16.700 | 18.071 | 46.7 | 39 |
| 518 | 16.936 | 14.01 | 1.916 | 21.6 | 22.9 | 16.946 | 18.915 | 46.6 | 56 |
| 519 | 19.392 | 12.72 | 1.567 | 71.8 | 71.0 | 19.407 | 20.040 | 46.5 | 18 |
| 5 | 20.831 | 12.11 | 1.489 | 33.8 | 33.1 | 20.849 | 22.185 | 45.9 | 38 |
| 520 | 21.675 | 11.79 | 1.448 | 439.0 | 439.9 | 21.692 | 21.798 | 58.9 | 3 |
| 521 | 22.476 | 11.51 | 1.412 | 211.1 | 212.2 | 22.501 | 22.712 | 51.3 | 6 |
| 522 | 24.979 | 10.74 | 1.314 | 361.5 | 362.6 | – | 24.997 | 46.4 | 0 |
| 6 | 26.506 | 10.34 | 1.278 | 413.7 | 414.4 | 26.509 | 26.615 | 46.1 | 3 |
| 523 | 27.322 | 10.14 | 1.278 | 516.5 | 515.8 | 27.353 | 27.423 | 54.2 | 2 |

NS 522 forms at least 39 pc from the centre, beyond the tidal radius, and is removed as an escaper at the next output, 0.019 Myr later, before the module is called. No other NS is present between 22.71 and 26.51 Myr, which is why no `pulsar.55` file exists for 23–25 Myr. The sections below describe the ten recorded NSs.

All values below are read from `data/run4/pulsar.55_*.dat` by `scripts/make_star_docs.py`.
Times are physical times in Myr; P in ms, Ṗ in s s⁻¹, B in G, distances in pc, speeds in km s⁻¹.
E_bind is in M☉² pc⁻¹ and E_total in the mixed units described in [PULSAR55_FORMAT.md](PULSAR55_FORMAT.md). The meaning of the labels and of the changes of spin
is discussed in Sects. 4 and 5 of the paper and in [MODULE_REVIEW.md](MODULE_REVIEW.md).

## Group 1: NS 517

- Label sequence: **S1 → S5 → S7 → S5 → S1 → S5**
- Records: 67, from 16.630 to 18.950 Myr (2.320 Myr)
- Mean speed 19.3 km/s (range 19.22–19.48); distance from the centre 0.40 → 44.99 pc; E_total 369.3641 to 380.3031 (always > 0)
- E_bind from -4.887 to -0.114 M☉² pc⁻¹
- Host: supernova at 16.598 Myr (progenitor 14.21 M☉, NS 1.999 M☉), speed after the kick 19.5 km/s; removed as an escaper at 18.985 Myr, 46.1 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 16.630 | 16.630 | 1 |
| S5 (wide binary) | 16.665 | 16.911 | 8 |
| S7 (NS–BH binary) | 16.946 | 17.333 | 12 |
| S5 (wide binary) | 17.368 | 18.036 | 20 |
| S1 (isolated pulsar) | 18.071 | 18.071 | 1 |
| S5 (wide binary) | 18.106 | 18.950 | 25 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 51.35 | 1.84 × 10⁻²⁰ | 9.92 × 10⁸ | 4.42 × 10¹⁰ | no | 16.630 | 17.122 | 15 |
| 53.06 | 0 | 3.00 × 10⁸ | – | yes | 17.157 | 17.333 | 6 |
| 53.06 | 1.62 × 10⁻²¹ | 3.00 × 10⁸ | 5.18 × 10¹¹ | yes | 17.368 | 18.036 | 20 |
| 33.81 | 1.87 × 10⁻²⁰ | 8.11 × 10⁸ | 2.87 × 10¹⁰ | no | 18.071 | 18.950 | 26 |

Changes of spin state:

- 17.157 Myr: P 51.35 → 53.06 ms, Ṗ 1.84 × 10⁻²⁰ → 0, B 9.92 × 10⁸ → 3.00 × 10⁸ G; new value drawn from the module's initial distribution
- 17.368 Myr: P 53.06 → 53.06 ms, Ṗ 0 → 1.62 × 10⁻²¹, B 3.00 × 10⁸ → 3.00 × 10⁸ G; P unchanged; Ṗ becomes finite again when the S7 label ends
- 18.071 Myr: P 53.06 → 33.81 ms, Ṗ 1.62 × 10⁻²¹ → 1.87 × 10⁻²⁰, B 3.00 × 10⁸ → 8.11 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS517_run4.png), [FigB](../figures/appendix/FigB_NS517_run4.png)

## Group 2: NS 4

- Label sequence: **S1 → S5 → S7 → S5 → S7 → S5**
- Records: 39, from 16.700 to 18.036 Myr (1.336 Myr)
- Mean speed 33.3 km/s (range 33.29–33.39); distance from the centre 2.13 → 44.67 pc; E_total 1093.654 to 1100.841 (always > 0)
- E_bind from -10.375 to -0.191 M☉² pc⁻¹
- Host: supernova at 16.697 Myr (progenitor 14.15 M☉, NS 1.974 M☉), speed after the kick 33.4 km/s; removed as an escaper at 18.071 Myr, 46.7 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 16.700 | 16.700 | 1 |
| S5 (wide binary) | 16.735 | 16.911 | 6 |
| S7 (NS–BH binary) | 16.946 | 16.946 | 1 |
| S5 (wide binary) | 16.981 | 16.981 | 1 |
| S7 (NS–BH binary) | 17.016 | 17.333 | 10 |
| S5 (wide binary) | 17.368 | 18.036 | 20 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 5.56 | 1.24 × 10⁻²⁰ | 2.69 × 10⁸ | 7.07 × 10⁹ | no | 16.700 | 17.122 | 13 |
| 47.73 | 0 | 4.44 × 10⁸ | – | no | 17.157 | 17.333 | 6 |
| 47.73 | 3.95 × 10⁻²¹ | 4.44 × 10⁸ | 1.91 × 10¹¹ | no | 17.368 | 18.036 | 20 |

Changes of spin state:

- 17.157 Myr: P 5.56 → 47.73 ms, Ṗ 1.24 × 10⁻²⁰ → 0, B 2.69 × 10⁸ → 4.44 × 10⁸ G; new value drawn from the module's initial distribution
- 17.368 Myr: P 47.73 → 47.73 ms, Ṗ 0 → 3.95 × 10⁻²¹, B 4.44 × 10⁸ → 4.44 × 10⁸ G; P unchanged; Ṗ becomes finite again when the S7 label ends

Diagrams: [FigA](../figures/appendix/FigA_NS4_run4.png), [FigB](../figures/appendix/FigB_NS4_run4.png)

## Group 3: NS 516

- Label sequence: **S1 → S5 → S7 → S1**
- Records: 54, from 15.048 to 16.911 Myr (1.863 Myr)
- Mean speed 24.1 km/s (range 24.06–24.19); distance from the centre 2.46 → 45.17 pc; E_total 712.6297 to 720.729 (always > 0)
- E_bind from -2.864 to 0.000 M☉² pc⁻¹
- Host: supernova at 15.045 Myr (progenitor 15.29 M☉, NS 2.461 M☉), speed after the kick 24.2 km/s; removed as an escaper at 16.946 Myr, 46.5 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 15.048 | 15.048 | 1 |
| S5 (wide binary) | 15.083 | 15.399 | 10 |
| S7 (NS–BH binary) | 15.434 | 15.434 | 1 |
| S1 (isolated pulsar) | 15.470 | 16.911 | 42 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 39.47 | 9.85 × 10⁻²¹ | 6.37 × 10⁸ | 6.35 × 10¹⁰ | no | 15.048 | 16.278 | 36 |
| 48.73 | 1.68 × 10⁻²⁰ | 9.25 × 10⁸ | 4.59 × 10¹⁰ | no | 16.313 | 16.384 | 3 |
| 49.22 | 5.56 × 10⁻²² | 1.69 × 10⁸ | 1.40 × 10¹² | yes | 16.419 | 16.735 | 10 |
| 28.48 | 9.93 × 10⁻²² | 1.72 × 10⁸ | 4.55 × 10¹¹ | no | 16.770 | 16.911 | 5 |

Changes of spin state:

- 16.313 Myr: P 39.47 → 48.73 ms, Ṗ 9.85 × 10⁻²¹ → 1.68 × 10⁻²⁰, B 6.37 × 10⁸ → 9.25 × 10⁸ G; new value drawn from the module's initial distribution
- 16.419 Myr: P 48.73 → 49.22 ms, Ṗ 1.68 × 10⁻²⁰ → 5.56 × 10⁻²², B 9.25 × 10⁸ → 1.69 × 10⁸ G; new value drawn from the module's initial distribution
- 16.770 Myr: P 49.22 → 28.48 ms, Ṗ 5.56 × 10⁻²² → 9.93 × 10⁻²², B 1.69 × 10⁸ → 1.72 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS516_run4.png), [FigB](../figures/appendix/FigB_NS516_run4.png)

## Group 3: NS 5

- Label sequence: **S1 → S5 → S7 → S1**
- Records: 38, from 20.849 to 22.150 Myr (1.301 Myr)
- Mean speed 33.0 km/s (range 32.83–33.09); distance from the centre 1.09 → 44.81 pc; E_total 802.842 to 815.6475 (always > 0)
- E_bind from -7.022 to 0.000 M☉² pc⁻¹
- Host: supernova at 20.831 Myr (progenitor 12.11 M☉, NS 1.489 M☉), speed after the kick 33.1 km/s; removed as an escaper at 22.185 Myr, 45.9 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 20.849 | 20.849 | 1 |
| S5 (wide binary) | 20.884 | 20.919 | 2 |
| S7 (NS–BH binary) | 20.954 | 20.954 | 1 |
| S1 (isolated pulsar) | 20.989 | 22.150 | 34 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 6.81 | 6.26 × 10⁻²⁰ | 6.67 × 10⁸ | 1.72 × 10⁹ | no | 20.849 | 21.200 | 11 |
| 24.94 | 3.41 × 10⁻²⁰ | 9.41 × 10⁸ | 1.16 × 10¹⁰ | no | 21.235 | 21.728 | 15 |
| 90.55 | 9.45 × 10⁻²¹ | 9.45 × 10⁸ | 1.52 × 10¹¹ | yes | 21.763 | 21.833 | 3 |
| 83.20 | 6.56 × 10⁻²¹ | 7.55 × 10⁸ | 2.01 × 10¹¹ | yes | 21.868 | 22.150 | 9 |

Changes of spin state:

- 21.235 Myr: P 6.81 → 24.94 ms, Ṗ 6.26 × 10⁻²⁰ → 3.41 × 10⁻²⁰, B 6.67 × 10⁸ → 9.41 × 10⁸ G; new value drawn from the module's initial distribution
- 21.763 Myr: P 24.94 → 90.55 ms, Ṗ 3.41 × 10⁻²⁰ → 9.45 × 10⁻²¹, B 9.41 × 10⁸ → 9.45 × 10⁸ G; new value drawn from the module's initial distribution
- 21.868 Myr: P 90.55 → 83.20 ms, Ṗ 9.45 × 10⁻²¹ → 6.56 × 10⁻²¹, B 9.45 × 10⁸ → 7.55 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS5_run4.png), [FigB](../figures/appendix/FigB_NS5_run4.png)

## Group 4: NS 523

- Label sequence: **S1 → S5**
- Records: 2, from 27.353 to 27.388 Myr (0.035 Myr)
- Mean speed 515.5 km/s (range 515.54–515.54); distance from the centre 17.18 → 35.44 pc; E_total 169778.4 to 169778.8 (always > 0)
- E_bind from -1.162 to -1.153 M☉² pc⁻¹
- Host: supernova at 27.322 Myr (progenitor 10.14 M☉, NS 1.278 M☉), speed after the kick 515.8 km/s; removed as an escaper at 27.423 Myr, 54.2 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 27.353 | 27.353 | 1 |
| S5 (wide binary) | 27.388 | 27.388 | 1 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 85.29 | 1.15 × 10⁻²¹ | 3.20 × 10⁸ | 1.17 × 10¹² | yes | 27.353 | 27.388 | 2 |

No change of spin state.

Diagrams: [FigA](../figures/appendix/FigA_NS523_run4.png), [FigB](../figures/appendix/FigB_NS523_run4.png)

## Group 5: NS 518

- Label sequence: **S1 → S7 → S5 → S7 → S1**
- Records: 56, from 16.946 to 18.880 Myr (1.934 Myr)
- Mean speed 22.8 km/s (range 22.77–22.91); distance from the centre 1.31 → 45.85 pc; E_total 496.5479 to 503.376 (always > 0)
- E_bind from -2.896 to 0.000 M☉² pc⁻¹
- Host: supernova at 16.936 Myr (progenitor 14.01 M☉, NS 1.916 M☉), speed after the kick 22.9 km/s; removed as an escaper at 18.915 Myr, 46.6 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 16.946 | 16.946 | 1 |
| S7 (NS–BH binary) | 16.981 | 16.981 | 1 |
| S5 (wide binary) | 17.016 | 17.192 | 6 |
| S7 (NS–BH binary) | 17.227 | 17.227 | 1 |
| S1 (isolated pulsar) | 17.263 | 18.880 | 47 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 55.67 | 1.22 × 10⁻²⁰ | 8.41 × 10⁸ | 7.24 × 10¹⁰ | no | 16.946 | 17.122 | 6 |
| 51.35 | 1.84 × 10⁻²⁰ | 9.92 × 10⁸ | 4.42 × 10¹⁰ | no | 17.157 | 18.036 | 26 |
| 53.06 | 1.62 × 10⁻²¹ | 3.00 × 10⁸ | 5.18 × 10¹¹ | yes | 18.071 | 18.880 | 24 |

Changes of spin state:

- 17.157 Myr: P 55.67 → 51.35 ms, Ṗ 1.22 × 10⁻²⁰ → 1.84 × 10⁻²⁰, B 8.41 × 10⁸ → 9.92 × 10⁸ G; takes over the state of NS 517 recorded at 16.630 Myr
- 18.071 Myr: P 51.35 → 53.06 ms, Ṗ 1.84 × 10⁻²⁰ → 1.62 × 10⁻²¹, B 9.92 × 10⁸ → 3.00 × 10⁸ G; takes over the state of NS 517 recorded at 17.368 Myr

Diagrams: [FigA](../figures/appendix/FigA_NS518_run4.png), [FigB](../figures/appendix/FigB_NS518_run4.png)

## Group 6: NS 521

- Label sequence: **S7 → S1**
- Records: 6, from 22.501 to 22.677 Myr (0.176 Myr)
- Mean speed 212.1 km/s (range 212.07–212.08); distance from the centre 6.12 → 43.92 pc; E_total 31760.47 to 31762.59 (always > 0)
- E_bind from 0.000 to 0.000 M☉² pc⁻¹
- Host: supernova at 22.476 Myr (progenitor 11.51 M☉, NS 1.412 M☉), speed after the kick 212.2 km/s; removed as an escaper at 22.712 Myr, 51.3 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S7 (NS–BH binary) | 22.501 | 22.501 | 1 |
| S1 (isolated pulsar) | 22.536 | 22.677 | 5 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 22.50 | 0 | 4.14 × 10⁸ | – | no | 22.501 | 22.501 | 1 |
| 69.62 | 3.44 × 10⁻²¹ | 5.00 × 10⁸ | 3.20 × 10¹¹ | yes | 22.536 | 22.642 | 4 |
| 12.75 | 5.85 × 10⁻²¹ | 2.79 × 10⁸ | 3.45 × 10¹⁰ | no | 22.677 | 22.677 | 1 |

Changes of spin state:

- 22.536 Myr: P 22.50 → 69.62 ms, Ṗ 0 → 3.44 × 10⁻²¹, B 4.14 × 10⁸ → 5.00 × 10⁸ G; new value drawn from the module's initial distribution
- 22.677 Myr: P 69.62 → 12.75 ms, Ṗ 3.44 × 10⁻²¹ → 5.85 × 10⁻²¹, B 5.00 × 10⁸ → 2.79 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS521_run4.png), [FigB](../figures/appendix/FigB_NS521_run4.png)

## Group 7: NS 519

- Label sequence: **S1**
- Records: 18, from 19.407 to 20.005 Myr (0.598 Myr)
- Mean speed 70.9 km/s (range 70.88–70.92); distance from the centre 0.72 → 43.53 pc; E_total 3935.109 to 3940.606 (always > 0)
- E_bind from -1.448 to 0.000 M☉² pc⁻¹
- Host: supernova at 19.392 Myr (progenitor 12.72 M☉, NS 1.567 M☉), speed after the kick 71.0 km/s; removed as an escaper at 20.040 Myr, 46.5 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 19.407 | 20.005 | 18 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 54.46 | 5.60 × 10⁻²¹ | 5.64 × 10⁸ | 1.54 × 10¹¹ | no | 19.407 | 19.407 | 1 |
| 42.36 | 2.07 × 10⁻²⁰ | 9.55 × 10⁸ | 3.25 × 10¹⁰ | no | 19.442 | 20.005 | 17 |

Changes of spin state:

- 19.442 Myr: P 54.46 → 42.36 ms, Ṗ 5.60 × 10⁻²¹ → 2.07 × 10⁻²⁰, B 5.64 × 10⁸ → 9.55 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS519_run4.png), [FigB](../figures/appendix/FigB_NS519_run4.png)

## Group 7: NS 6

- Label sequence: **S1**
- Records: 3, from 26.509 to 26.579 Myr (0.070 Myr)
- Mean speed 414.2 km/s (range 414.18–414.19); distance from the centre 1.42 → 30.92 pc; E_total 109583.4 to 109586 (always > 0)
- E_bind from -0.150 to 0.000 M☉² pc⁻¹
- Host: supernova at 26.506 Myr (progenitor 10.34 M☉, NS 1.278 M☉), speed after the kick 414.4 km/s; removed as an escaper at 26.615 Myr, 46.1 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 26.509 | 26.579 | 3 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 15.99 | 4.07 × 10⁻²⁰ | 8.24 × 10⁸ | 6.23 × 10⁹ | no | 26.509 | 26.509 | 1 |
| 97.53 | 9.56 × 10⁻²¹ | 9.86 × 10⁸ | 1.62 × 10¹¹ | yes | 26.544 | 26.579 | 2 |

Changes of spin state:

- 26.544 Myr: P 15.99 → 97.53 ms, Ṗ 4.07 × 10⁻²⁰ → 9.56 × 10⁻²¹, B 8.24 × 10⁸ → 9.86 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS6_run4.png), [FigB](../figures/appendix/FigB_NS6_run4.png)

## Group 7: NS 520

- Label sequence: **S1**
- Records: 3, from 21.692 to 21.763 Myr (0.070 Myr)
- Mean speed 439.6 km/s (range 439.64–439.65); distance from the centre 9.27 → 42.65 pc; E_total 139966.9 to 139972.5 (always > 0)
- E_bind from 0.000 to 0.000 M☉² pc⁻¹
- Host: supernova at 21.675 Myr (progenitor 11.79 M☉, NS 1.448 M☉), speed after the kick 439.9 km/s; removed as an escaper at 21.798 Myr, 58.9 pc from the centre

| Label | From (Myr) | To (Myr) | Records |
|---|---|---|---|
| S1 (isolated pulsar) | 21.692 | 21.763 | 3 |

| P (ms) | Ṗ (s s⁻¹) | B (G) | τ_c (yr) | Below death line | From (Myr) | To (Myr) | Records |
|---|---|---|---|---|---|---|---|
| 64.89 | 7.44 × 10⁻²² | 2.24 × 10⁸ | 1.38 × 10¹² | yes | 21.692 | 21.728 | 2 |
| 78.59 | 5.78 × 10⁻²¹ | 6.88 × 10⁸ | 2.15 × 10¹¹ | yes | 21.763 | 21.763 | 1 |

Changes of spin state:

- 21.763 Myr: P 64.89 → 78.59 ms, Ṗ 7.44 × 10⁻²² → 5.78 × 10⁻²¹, B 2.24 × 10⁸ → 6.88 × 10⁸ G; new value drawn from the module's initial distribution

Diagrams: [FigA](../figures/appendix/FigA_NS520_run4.png), [FigB](../figures/appendix/FigB_NS520_run4.png)

