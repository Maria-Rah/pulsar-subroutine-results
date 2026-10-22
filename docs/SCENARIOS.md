# The seven scenarios: reference definitions and their history

From the A&A paper of this repository on, the scenario labels S1–S7 have the meaning given in the first
table below. The second table follows each label through the papers of the series and the code, and the
notes explain every change. Where earlier papers differ from the reference definitions, the reference
definitions supersede them.

## Reference definitions

| ID | Name | Physical configuration | Expected region of the P–Ṗ diagram | Dominant spin terms | Criterion in the code (Run 4 version) |
|---|---|---|---|---|---|
| S1 | Isolated pulsar | Single NS without accretion history; spins down by dipole braking while its field decays | Normal pulsars, moving towards the death line | dipole, field decay | Default when no other test applies |
| S2 | Isolated recycled MSP | Single NS that was recycled in a binary and lost its companion | MSPs with τ_c of order Gyr | weak dipole, field decay | Single now; in a binary before; accretion flag set by S3; mass gain > 0.01 M☉ |
| S3 | Accretion-recycled MSP (LMXB, RLOF) | Evolving donor fills its Roche lobe; NS spun up while the field is buried | From normal pulsars to MSPs; Ṗ < 0 while accreting | accretion, dipole | Mass gain rate > 10⁻¹⁰; donor type 2–9; a < 10¹¹; donor radius above the Roche-lobe radius (Eggleton 1983) |
| S4 | Exchange MSP | NS acquires a new companion in an encounter in the core | Unchanged at the exchange; prepares later recycling | dynamical, environmental, dipole | Single before or new companion; large change of E_bind or of companion type; `STEP` < 10⁻⁶; inside the core radius |
| S5 | Wide binary | Detached binary without mass transfer | As S1 or S2 | dipole, environmental | a > `ATHRESH` = 0.1 pc; no mass gain; companion MS, WD, NS, or BH |
| S6 | NS–NS binary | Double NS; orbital decay by GW emission (deferred) | As S1 or S2 | dipole, merger | NS companion; imminent merger or mass change > 0.3 M₀ |
| S7 | NS–BH binary | NS with a BH companion; faster GW decay than S6 (deferred) | As S1 or S2 | dipole, merger | BH companion; capture, mass change > 0.5 M₀, or speed > 500 km s⁻¹ |

Thresholds without units are in the mixed units of the code. The code tests the scenarios in the order
S6, S7, S3, S4, S5, S2; S1 is the default. How the code identifies the companion, and why the S5 and S7
labels of Run 4 do not mark bound companions, is described in [MODULE_REVIEW.md](MODULE_REVIEW.md).

## The labels through the series

| ID | ComBAO II (Rah et al. 2025a) | ComBAO III (Rah et al. 2025b) | Code, versions 4–5 (2026) | RAA (Rah 2026) | Springer paper (submitted) | ComBAO IV (Rah et al. 2026) | Reference (A&A paper) |
|---|---|---|---|---|---|---|---|
| S1 | Isolated pulsar formation and evolution | Isolated pulsars with dipole spin-down | 1, isolated pulsar (default) | Young pulsar | Young pulsar spin-down with field decay | Young isolated pulsar; in Run 4 “isolated spin-down” | Isolated pulsar |
| S2 | Isolated MSP after companion disruption | Isolated MSPs recycled through past accretion | 2, isolated MSP | Isolated MSP | Isolated MSP, weak-torque regime | Isolated MSP | Isolated recycled MSP |
| S3 | MSP formation via accretion in a binary system | Accreting systems with ongoing mass transfer | 3, MSP via accretion (RLOF) | Accreting MSP (LMXB) | Accretion-driven recycling in an LMXB | Accreting LMXB | Accretion-recycled MSP (LMXB, RLOF) |
| S4 | MSP formation via dynamical interactions in GCs | Exchange MSPs with dynamically acquired companions | 4, MSP via dynamics (exchange) | Dynamic MSP (environmental torque in a dense core) | Dynamical exchange, tested through its environmental torque | MSP in a dense core | Exchange MSP |
| S5 | Pulsar in a wide binary without RLOF (10–100 au) | Wide binaries | 5, wide binary (a > 0.1 pc) | Wide-binary MSP (WD at 3 au) | Wide binary, negligible tides | MSP with a wide companion; in Run 4 “wide-binary evolution” | Wide binary |
| S6 | NS–NS merger leading to an MSP or a BH | Double NS binaries approaching merger | 6, NS–NS merger | NS–NS binary (GW deferred) | NS–NS compact binary, dipole only | NS–NS compact binary | NS–NS binary |
| S7 | NS–BH merger and removal | NS–BH binaries with tidal effects | 7, NS–BH merger (also speed > 500 km s⁻¹) | NS–BH binary (GW deferred) | NS–BH compact binary, dipole only | NS–BH compact binary; in Run 4 “merger-or-kick events” | NS–BH binary |

## Why each label changed

- **S1** keeps its meaning throughout. In Run 4 it is assigned mostly to NSs without neighbours, which is the
  right configuration for an escaping NS.
- **S2** moved from the outcome of a disruption (ComBAO II) to the accretion history that defines it (ComBAO III,
  code). The reference name, isolated recycled MSP, keeps both: a single NS that was recycled in a binary. The
  code version of Run 4 cannot assign it, because every particle counts as a binary member (`NAME > 0`).
- **S3** described common-envelope evolution followed by RLOF in ComBAO II; the code and the later papers
  treat the RLOF phase of an LMXB. The reference definition is that phase.
- **S4** is the label whose meaning changed most. ComBAO II and III defined it as a discrete exchange (or capture)
  that gives the NS a new companion. A single NS outside a cluster cannot undergo a discrete exchange, so the
  standalone validation (RAA) tested only the environmental torque of a dense core, and the RAA and ComBAO IV
  tables name it accordingly. The reference definition returns to the exchange itself. An exchange changes the
  companion, not the spin, so in the next version S4 marks the configuration (a change of the companion's
  identity in a regularised pair) and any spin-up comes from the S3 physics that may follow.
- **S5** used separations of 10–100 au (ComBAO II) and 3 au (RAA), whereas the code requires more than 0.1 pc
  (about 2 × 10⁴ au), far beyond the hard–soft boundary of a cluster. The next version sets the threshold
  relative to that boundary.
- **S6, S7** were framed as mergers (ComBAO II, code) and then as compact binaries in which only dipole braking is
  followed and GW-driven orbital decay is deferred (RAA, Springer). The reference names describe the binaries.
  The code version of Run 4 also assigns S7 for speeds above 500 km s⁻¹, a criterion unrelated to a BH
  companion, which matches the description “merger-or-kick events” of ComBAO IV; the next version removes it.
- ComBAO IV also mentions “tidally synchronised” and “magnetar-like” channels. They have no counterpart in the
  code or in the reference definitions.

## References

- Rah M. et al. 2025a, ComBAO 72, 55, doi:10.52526/25792776-25.72.1-55
- Rah M. et al. 2025b, ComBAO 72, 279, doi:10.52526/25792776-25.72.2-279
- Rah M. 2026, RAA, doi:10.1088/1674-4527/ae983c
- Rah M., Spurzem R., Mickaelian A., Flammini Dotti F. 2026, ComBAO 73, 68, doi:10.52526/25792776-26.73.1-68
- Rah M., Spurzem R., Mickaelian A., Flammini Dotti F., submitted, “Integrating a Normal Pulsar and Millisecond
  Pulsar Evolution Subroutine into NBODY6++GPU”
- Eggleton P. P. 1983, ApJ 268, 368
