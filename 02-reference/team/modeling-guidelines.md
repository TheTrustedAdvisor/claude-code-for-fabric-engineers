# Modeling guidelines: Sales semantic model

Team rules for measures. Every rule has an ID; reviews cite it.

## Measures

- **M1 Division.** Divide with `DIVIDE()`, so a zero or blank denominator returns blank instead of an error. When the denominator is a constant, such as `/ 12`, use the `/` operator.
- **M2 Format.** Every measure sets a `formatString`. Percentages use `0.0%`.
- **M3 Names.** Measure names are in Title Case and readable in a report, with no prefixes such as `m_` or `Measure`.
- **M4 Time intelligence.** Time intelligence uses `'Date'[Date]` of the marked date table. `SAMEPERIODLASTYEAR` and `DATEADD` are both fine.
- **M5 Reuse.** A measure that builds on another measure references it by name, such as `[Total Sales]`, instead of repeating its expression.
- **M6 Description.** Every measure has a description: a `///` line directly above it in TMDL.
