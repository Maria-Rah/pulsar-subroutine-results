# The `pulsar.55` output

The pulsar module (`calc_and_save_pulsar_params`, see [`../code`](../code)) appends one line per neutron star
(NS) and call to `pulsar.55_XXXXXXXX.dat`, where `XXXXXXXX` is the integer part of the physical time in Myr.
In Runs 2–4 the module is called from the output routine of NBODY6++GPU at every global output,
every 0.0352 Myr. Fortran format: `E15.7,1X,I8,1X,I2,1X,14(E15.7,1X),I2,1X,2(F10.4,1X)` (Run 4 source, line 518).

| Col. | Quantity | Unit | Code expression |
|---|---|---|---|
| 1 | time t | Myr | `TIME*TSTAR` |
| 2 | identity | – | `NAME(J)` |
| 3 | stellar type | – | `KSTAR(J)` (13 = NS) |
| 4 | spin period P | s | `PERIOD(J)` |
| 5 | period derivative Ṗ | s s⁻¹ | `PDOT(J)` |
| 6 | surface field B | G | `BMAG(J)` |
| 7–9 | position | pc | `X(k,J)*RBAR` |
| 10–12 | velocity | km s⁻¹ | `XDOT(k,J)*VSTAR` |
| 13–15 | force | code units | `F(k,J)` |
| 16 | E_total | mixed (below) | `0.5*BODY*ZMBAR*v²*VSTAR² + BODY*ZMBAR*PHIDBL(J)` |
| 17 | E_bind | M☉² pc⁻¹ | `-BODY(J)*BODY(I_COMP)*ZMBAR²/(2*R(J)*RBAR)` |
| 18 | scenario label | – | 1 to 7 (see [SCENARIOS.md](SCENARIOS.md)) |
| 19–20 | latitude, longitude of the position | deg | from `X(k,J)` |

Notes on the units and on reading the files:

- **E_total** adds a kinetic energy in M☉ km² s⁻² to a potential energy in which the potential `PHIDBL` is in
  code units, so its value is dominated by the kinetic term. It is positive at every record of Run 4.
- **E_bind** has no gravitational constant and refers to the particle the module takes as companion,
  the particle whose index equals `LIST(1,J)`, the number of neighbours of the NS. It is therefore not the
  binding energy of a bound pair (paper, Sect. 5.2; [MODULE_REVIEW.md](MODULE_REVIEW.md)).
- Every MPI process writes its own copy of each line. Run 2 (two processes) has 277 of its 286 records twice; in
  Run 4, 283 records appear four times and 3 records three times (1141 lines, 286 distinct (t, NAME) records).
  `scripts/pulsar55.py` removes the duplicates.
- In Run 3, 265 of the 568 lines cannot be parsed; the readable lines give 152 distinct records.
- In Runs 2 and 3, P is undefined (NaN) in 77 records. In Run 4 the 13 records labelled S7 in which the
  merger term is undefined are written with Ṗ = 0.
- Files exist for 15–22 and 26–27 Myr. No file exists for 23–25 Myr because no NS is present at any output in that
  interval: NS 521 is removed at 22.712 Myr, NS 522 forms and is removed between two outputs (24.979–24.997 Myr),
  and NS 6 forms at 26.506 Myr.

A minimal reader:

```python
import sys; sys.path.insert(0, "scripts")
from pulsar55 import read_run, per_star, COL
records, n_lines, n_bad = read_run("data/run4")
stars = per_star(records)            # NAME -> records sorted in time
```
