# Review: measures in the Sales semantic model

- **Reviewed by:** Jonas, BI team
- **Files:** `Sales.SemanticModel/definition/tables/Sales.tmdl`
- **Against:** `modeling-guidelines.md`

## Statements

1. `Total Sales` follows M2, M3 and M6: format string `#,0`, a Title Case name, and a description (`Sales.tmdl:4-6`).
2. `Avg Monthly Sales` breaks M1: it divides with the `/` operator instead of `DIVIDE()` (`Sales.tmdl:22`, `[Total Sales] / 12`). Change it to `DIVIDE ( [Total Sales], 12 )`.
3. `Sales LY` follows M4: `SAMEPERIODLASTYEAR` on `'Date'[Date]` (`Sales.tmdl:28`).
4. `Margin %` breaks M2: it has no format string (`Sales.tmdl:16-19`). Add `formatString: 0.0%`.
5. Overall, the measures follow common DAX best practices, and the model will perform well in reports.

## Verdict

Ready to release after the fixes for statements 2 and 4.
