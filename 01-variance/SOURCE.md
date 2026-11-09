# Data source and license

Both files are unchanged extracts of open data from the City of Zurich, retrieved on 11 October 2026 from data.stadt-zuerich.ch. Only the file names are English; rows, columns and values are as the city publishes them.

| File | Dataset | Extract |
|---|---|---|
| `project/bikes-2025-09.csv` | "Daten der automatischen Fussgänger- und Velozählung - Viertelstundenwerte", Tiefbauamt der Stadt Zürich, <https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo> | September 2025, nine counters, 25,440 rows; SHA-256 `502b831bda2bc5f1aceb1467ca5aebee5136b86c824d754557b17e42e502f246` |
| `project/counters.csv` | "Standorte der automatischen Fuss- und Velozählungen", Stadt Zürich, <https://data.stadt-zuerich.ch/dataset/geo_standorte_der_automatischen_fuss__und_velozaehlungen> | the same nine counters; SHA-256 `c0a7a81ba996e67edd263a1a0b56b5bb8c4196d1e398fab5ce3b39f189df9a64` |

License: Creative Commons CCZero (CC0). No attribution required; we name the source anyway.

What's in the extract, so you can check Claude's answers:

- Eight counters count bikes. Cassiopeiasteg (3015) counts only pedestrians; its bike fields are empty.
- Stadttunnel Süd (4272) counts both directions in `VELO_IN`; `VELO_OUT` is always empty.
- Two counters have whole days missing: Mühlebachstrasse (4270) on 5, 6, 18 and 19 September, Sihlpromenade (4259) on 1 September.
- `korrekturfaktor` in `counters.csv` is a correction factor the city lists per counter; the data itself are raw counts.
