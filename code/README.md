# Module source and host changes of Runs 2–4

| File | Content |
|---|---|
| `calc_and_save_pulsar_params_v4_CORRECTED.f` | The pulsar routine compiled for Run 4 (MD5 `8a29777d2cad768ad26d03c240f2b4bc`). Last edited on 25 May 2026 at 05:47:11, compiled at 05:48:15, linked into `nbody6++.avx.gpu.mpi` at 05:49:04; Run 4 started at 05:50:02 (China Standard Time). Its header still reads "VERSION 4.0", January 2026. |
| `common6_pulsar_block.h` | The `/PULSAR/` common block added to `include/common6.h`. |
| `host_changes.diff` | Changes to the host files (`output.F`, `mdot.F`, `file_init.F`, `irr.avx.cpp`, `irr.sse.cpp`) relative to the stable NBODY6++GPU tree. |

What the Run 4 version does differently from the earlier copy published here (`v5`):

1. a new draw of P and B whenever both are zero at a particle index (line 168), instead of a test of `FIRST_CALL`;
2. `XKFIELD` set to 2.59 × 10⁻⁴⁴ g⁻¹ cm⁻² when it is not positive (lines 399–401), and τ_B = 10⁸ when `XKTAU` is not
   positive (lines 473–477);
3. c = 3 × 10¹⁰ cm s⁻¹ in the dipole term (line 409) and in the field estimator (line 482), which gives
   B/√(PṖ) = 3.22873 × 10¹⁹ in every record with Ṗ > 0;
4. an undefined Ṗ replaced by 0 (line 458; 13 records of Run 4, all labelled S7), and an undefined or non-positive P
   reset to 1 ms (lines 403–405 and 468; never triggered in Run 4);
5. 14 instead of 15 floating-point fields in the output format (line 518), which matches the 20 written columns.

Host changes (`host_changes.diff`):

- `output.F`: after each global output, a loop over `I = 1, N` calls the routine for every particle with
  `KSTAR(I) = 13`. The loop includes the components of regularised pairs. There is no MPI rank test, so every
  process appends its own copy of each line.
- `mdot.F`: at a type change to 13 the routine is also called, after setting `XMNS0(I)`. This call wrote no record in
  Runs 2–4: every record falls on an output time.
- `file_init.F`: unit 55 is renamed `pulsar.55`, and a block that zeroes the module arrays and assigns the coefficients
  (`XKACC` = 2 × 10⁻¹⁶, `XKENV` = 5 × 10⁻²⁹, `XKDYN` = 10⁻²², `XKASYM` = 10⁻²⁷, `XKGW` = 10⁻¹⁵,
  `XKMERGE` = 10⁻¹⁰, `XKTAU` = 10⁸, `ATHRESH` = 0.1) is added **after the `RETURN` statement** of the subroutine, so it
  is never executed. In Runs 2–4 all these quantities are therefore zero, except `XKFIELD` and `XKTAU`, which the
  routine replaces by the values of item 2. Ṗ is the dipole term alone, and the S5 test reduces to a positive
  separation.
- `irr.avx.cpp`, `irr.sse.cpp`: `NNBMAX` changed from 800 to 600 (19 May 2026).

`kick.F`, `input.F`, `hrdiag.f`, and `adjust.F` are unchanged. [`../docs/MODULE_REVIEW.md`](../docs/MODULE_REVIEW.md)
lists, with the line numbers of the Run 4 file, where this version departs from the physical model and how the next
version corrects it. The standalone validation of the module is in
[Maria-Rah/pulsar-subroutine-testing](https://github.com/Maria-Rah/pulsar-subroutine-testing).
