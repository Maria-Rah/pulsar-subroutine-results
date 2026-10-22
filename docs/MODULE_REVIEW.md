# Where the module version of Run 4 departs from the physical model

This file expands Sect. 5.2 of the paper with line references to
[`code/calc_and_save_pulsar_params_v5_CORRECTED.f`](../code/calc_and_save_pulsar_params_v5_CORRECTED.f).
That file has the logic that produced the Run 4 records, except two changes made for Run 4: the speed of
light in CGS units in both the dipole term and the field estimator, and Ṗ set to 0 when the merger term is
undefined. For each item: the physical definition, what the code does, the effect in Run 4, and the correction
planned for the next version of the module (used in Paper II).

## 1. Companion identification

- **Physics.** The companion of an NS in a regularised (Kustaanheimo–Stiefel) pair is the other component of the
  pair. For a particle index I ≤ 2 N_pairs it is I + 1 or I − 1; the semi-major axis and the binding energy follow
  from `R(IPAIR)`, `H(IPAIR)`, and the masses, with E_bind = −G m m_c / (2a).
- **Code.** Line 192 `IS_BINARY = (NAME(J) .GT. 0)` is true for every particle. Line 208 `I_COMP = LIST(1,J)`
  takes as companion the particle whose index equals the number of neighbours. Line 217
  `ORBITAL_SEP = R(J) * RBAR` reads the pair array with the particle index. Lines 228–229 compute
  E_bind = −m m_c ZMBAR² / (2a) without G.
- **Run 4.** The S5 and S7 labels and E_bind do not describe bound companions: the ten NSs move on straight lines,
  48 of the 99 S5 steps lie beyond the tidal radius, and S2 (single NS) cannot be assigned.
- **Next version.** Companion from the regularised pair, and from the neighbours only for wider bound systems;
  E_bind with G in physical units.

## 2. Thresholds and units in the criteria

- **S5** (line 365): a > `ATHRESH` = 0.1 pc, about 2 × 10⁴ au, far outside the range of binaries that survive in a
  cluster; the standalone validation used 3 au.
- **S3** (lines 316 and 324): a donor radius fixed at 10¹¹ and a separation limit of 10¹¹ (cm) are compared with a
  separation in pc, so both tests are always true for donors of types 2–9.
- **S6, S7** (lines 242 and 276): the limits 100 and 500 times `YI_CONST` = 10⁶ (the NS radius in cm) are compared
  with a separation in pc, and the capture radius (lines 282–284) uses a mass in M☉ with G in CGS units and c in
  code units.
- **Next version.** Separations compared with the SSE stellar radii and with the Roche-lobe radius of Eggleton
  (1983) in the same unit; the wide-binary threshold set relative to the hard–soft boundary of the cluster.

## 3. Time step of the spin update

- **Physics.** P(t + Δt) = P(t) + Ṗ Δt and B(t + Δt) = B(t) exp(−Δt/τ_B), with Δt the time elapsed since the
  previous call, in the units of Ṗ and τ_B.
- **Code.** Line 458 `PERIOD(J) = PERIOD(J) + PDOT(J) * STEP(J) * TSTAR` and line 464
  `BMAG(J) = BMAG(J) * EXP(-STEP(J) * TSTAR / XKTAU)` use the current individual time step in Myr; `XKTAU` = 10⁸
  is intended in years.
- **Run 4.** P and Ṗ are exactly unchanged in 258 of 276 intervals. In 161 of them the intended increment
  Ṗ Δt_out exceeds the last printed digit of P (median factor 2). The effective decay time is 10⁸ Myr.
- **Next version.** Store the time of the previous call for each NS; elapsed time in seconds; τ_B in the same
  unit, with one documented value for the standalone and the coupled module.

## 4. Storage by particle index

- **Physics.** The spin state belongs to the star.
- **Code.** All arrays of `/PULSAR/` are indexed by the particle index J, which the host changes when pairs form or
  dissolve; at an index used for the first time, `FIRST_CALL` triggers a new draw (lines 168–173).
- **Run 4.** NS 518 takes over the state of NS 517 at 17.157 and at 18.071 Myr; fourteen other changes are new draws;
  most changes happen at the same output in several distant NSs (17.157, 17.368, 18.071, 21.763 Myr).
- **Next version.** State keyed to `NAME`, so that it follows the star through regularisation, exchanges, and
  mergers.

## 5. Reference mass

- **Code.** `XMNS0` enters the S6 and S7 mass tests (lines 245 and 279) and the merger term (line 423,
  `DM / XMNS0(J)`). Where it was never set at the current index, the S7 mass test is met for any BH taken as
  companion, and the merger term is undefined.
- **Run 2 and Run 4.** Undefined periods in Run 2, starting at S7 steps; the 13 records with Ṗ = 0 in Run 4, all S7.
- **Next version.** M₀ and the formation time set when the star becomes an NS, under its identity.

## 6. The field as an independent variable

- **Physics.** B decays and is buried by accretion; Ṗ follows from B through the dipole formula. The relation
  B = 3.2 × 10¹⁹ (PṖ)^½ G is an observational estimate.
- **Code.** Lines 469–470 replace B, after every step with Ṗ > 0, by the estimate from P and Ṗ, with the module's
  constants (B/√(PṖ) = 3.22873 × 10¹⁹ in all 273 such records of Run 4).
- **Next version.** B evolved as a state variable, with decay and with burial proportional to the accreted mass;
  the estimate written only as a diagnostic.

## 7. Initial spin

- **Code.** Lines 169–170 draw P uniformly in 1–100 ms and B uniformly in 10⁸–10⁹ G at the first call. This sets
  every recorded value, the characteristic ages above 10 Gyr (91% of the records with Ṗ > 0), and the 83 records
  below the death line.
- **Next version.** Birth values at NS formation as in the pilot model of Ye et al. (2019), B in 10^11.5–10^13.8 G
  and P in 30–1000 ms, which bracket the young pulsar population (Faucher-Giguère & Kaspi 2006); MSPs then arise
  only through S3.

## 8. Energies

- **Code.** Lines 476–477: E_total adds ½ m v² in M☉ km² s⁻² to m Φ with Φ in code units; E_bind has no G.
- **Next version.** Both in physical units, E_bind for the companion of item 1.

## 9. Calls, output, and random numbers

- In Runs 2–4 the routine is called from the output routine every 0.0352 Myr; exchanges and the onset of mass
  transfer happen inside the regularisation and binary-evolution routines on much shorter time-scales.
- Each Run 4 record is written up to four times.
- The initial draws use the host generator `RAN2(IDUM1)`.
- **Next version.** Calls also when a pair forms or dissolves and when BSE changes the mass of an NS; stellar type 13
  checked for components of regularised pairs as well as single stars; each record written once; a separate
  random-number generator.

## 10. Cluster model

- With N = 5000 and an rms velocity of 2.6 km s⁻¹, every NS escapes within 2.3 Myr of its formation, and 28 Myr
  cover only the first NSs. Paper II uses N = 250 000 over 100 Myr; the kick distribution (Hobbs et al. 2005
  Maxwellian, or the log-normal of Disberg & Mandel 2025) decides the retained fraction.

## Other details of the code worth recording

- Line 460 sets a floor P ≥ 10⁻⁴ s; it is never reached in Run 4.
- Line 289: S7 is also assigned for speeds above 500 km s⁻¹, unrelated to a BH companion.
- Line 349: S4 uses `STEP(J) < 10⁻⁶` (code units) as a sign of a recent encounter.
- The integration report of May 2026 lists `XKFIELD = 0` in `file_init.F`; the Run 4 records imply
  K_field = 2.59 × 10⁻⁴⁴ g⁻¹ cm⁻² with c = 3 × 10¹⁰ cm s⁻¹, since (c³/K_field R⁶)^½ = 3.22873 × 10¹⁹ for
  R = 10⁶ cm.
