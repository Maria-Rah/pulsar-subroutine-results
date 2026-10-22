# Figures of the paper

| File | Figure | Produced by |
|---|---|---|
| `Fig1_four_runs.*` | Fig. 1: the four runs (time covered, record status, recorded Ṗ and B, bit identity with Run 4) | `scripts/fig1_four_runs.py` |
| `Fig2_PPdot_run4.*` | Fig. 2: P–Ṗ diagram of the 273 Run 4 records with Ṗ > 0 | `scripts/fig2_fig3_run4.py` |
| `Fig3_PdotB_run4.*` | Fig. 3: Ṗ–B diagram of the same records | `scripts/fig2_fig3_run4.py` |
| `Fig4_PPdot_atlas_run4.*` | Fig. 4: P–Ṗ panels of the ten NSs, ordered by group | `scripts/fig4_fig5_compose.py` |
| `Fig5_scenario_tracking_run4.*` | Fig. 5: scenario bar and E_bind of the ten NSs, and E_bind of all records by label | `scripts/fig4_fig5_compose.py` |

Running the three scripts from the repository root on the archived data reproduces the PNG files pixel for pixel.

Reading the figures (the paper explains them in Sects. 3.2, 4.2, and 4.3):

- **Fig. 2.** Fill colour: neutron star; ring colour: label at that record (gold S1, black S5, navy S7); circles and
  diamonds: first and last records; thin lines join successive records. Dashed lines: constant surface field
  B = 3.2 × 10¹⁹ (PṖ)^½ G for 10⁸–10¹¹ G; dotted lines: τ_c = P/2Ṗ = 10 Myr and 10 Gyr; solid line: death line
  B/P² = 0.17 × 10¹² G s⁻² (Bhattacharya & van den Heuvel 1991), i.e. Ṗ = 2.8 × 10⁻¹⁷ P³; shaded: P < 30 ms.
  The 13 records with Ṗ = 0 cannot appear on the logarithmic axes.
- **Fig. 3.** Same symbols; dashed lines show the dipole relation for P = 5, 25, 50, and 85 ms. Every point lies on
  the line of its own period by construction, because the module recomputes B from P and Ṗ.
- **Figs. 4 and 5** are assembled from the individual diagrams in [`../appendix`](../appendix) without redrawing them.
