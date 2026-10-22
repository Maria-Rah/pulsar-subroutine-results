# Module source

`calc_and_save_pulsar_params_v5_CORRECTED.f` is the pulsar routine whose logic produced the records of Run 4
(its header still reads "VERSION 4.0", January 2026). Run 4 used two further changes that are not in this
file and that are visible in its output:

1. the speed of light in CGS units (c = 3 × 10¹⁰ cm s⁻¹) in both the dipole term and the field estimator, which
   gives B/√(PṖ) = 3.22873 × 10¹⁹ in every record with Ṗ > 0;
2. Ṗ set to 0 when the merger term is undefined (13 records, all labelled S7).

The routine needs the `/PULSAR/` common block in `common6.h` and the initialisation in `file_init.F` described in
the coupling instructions of the code repository,
[Maria-Rah/pulsar-subroutine-testing](https://github.com/Maria-Rah/pulsar-subroutine-testing).
[`../docs/MODULE_REVIEW.md`](../docs/MODULE_REVIEW.md) lists, with line numbers, where this version departs from
the physical model and how the next version corrects it.
