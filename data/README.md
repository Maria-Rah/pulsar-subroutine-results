# Data

| Folder | Content |
|---|---|
| `inputs/` | The input files: `run1_N50k.inp` (Run 1, MD5 993fb2efa6e265af4875b4ca9caad3dc) and `runs2-4_N50k.inp` (identical in Runs 2, 3, and 4, MD5 7b7c31d19e0662f063515294b501281c). Both are named `N50k.inp` in the run folders. |
| `logs/` | Extracts of the host logs of Run 1 and Run 3 (input echo, stellar-evolution parameters, scaling, largest energy error, end of the run), the kick events parsed from them (`run1_kicks.csv`, `run3_kicks.csv`), and the lines of `esc.11` for the eleven NSs of Run 4. The log of Run 4 was not preserved; its host evolution is identical to that of Run 3. |
| `run1/` | Host diagnostics summaries (`GLOBAL`, `SEV`, `BEV` guides) of Run 1 (N = 50 000, 0–9.14 Myr). No NS forms, so there are no `pulsar.55` records. |
| `run2/` | `pulsar.55_*.dat` of Run 2 and the host diagnostics summaries of the 5000-star model shared by Runs 2–4. |
| `run3/` | `pulsar.55_*.dat` of Run 3. |
| `run4/` | `pulsar.55_*.dat` of Run 4, the basis of Sect. 4 of the paper; `run4_records.csv`, the 286 distinct records with a header line; and `host_neutron_stars.csv`, formation and removal of the eleven NSs (Table 5 of the paper). |

The files cover 15–22 and 26–27 Myr; no file exists for 23–25 Myr because no NS is present at any output in that
interval. The column format is described
in [`../docs/PULSAR55_FORMAT.md`](../docs/PULSAR55_FORMAT.md).
