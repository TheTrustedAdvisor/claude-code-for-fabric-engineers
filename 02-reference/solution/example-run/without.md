# Review: Sales.SemanticModel

- Sales.SemanticModel/definition/tables/Sales.tmdl:17 — `Margin %` has no `formatString`, so it shows as a raw decimal (0.2345) instead of a percentage; add `formatString: 0.0%`.
- Sales.SemanticModel/definition/tables/Sales.tmdl:22 — `Avg Monthly Sales` divides by a hardcoded 12, so it is wrong for partial years, a single month, multi-year selections, or any filter other than one full year; use `AVERAGEX ( VALUES ( 'Date'[Month] ), [Total Sales] )` or divide by the count of months in context.
- Sales.SemanticModel/definition/tables/Sales.tmdl:22 — the `/` operator is used instead of `DIVIDE`. Harmless with a constant 12, but it will become a divide-by-zero risk once the denominator is made dynamic.
- Sales.SemanticModel/definition/tables/Date.tmdl:13 — the Date table only has `Date` and `Year`. There is no Month/Quarter column, so `Avg Monthly Sales` can't be computed per month and users can't slice by month.
- Sales.SemanticModel/definition/tables/Sales.tmdl:52 — `Amount` is visible with `summarizeBy: sum` even though `Total Sales` wraps it. This creates a competing implicit measure; hide it and set `summarizeBy: none`.
- Sales.SemanticModel/definition/tables/Sales.tmdl:58 — `Cost` is visible with `summarizeBy: sum` even though `Total Cost` wraps it. Same issue: hide it and set `summarizeBy: none`.
- Sales.SemanticModel/definition/tables/Sales.tmdl:45 — `OrderDate` is the fact-side relationship key but isn't hidden, so users can slice by it instead of `'Date'[Date]`, which breaks time intelligence such as `Sales LY`.
- Sales.SemanticModel/definition/tables/Sales.tmdl:39 — `OrderID` is a technical key that is not hidden; it should be hidden, since `Order Count` already exposes it.
- Sales.SemanticModel/definition/relationships.tmdl:2 — the relationship joins on `dateTime` columns. If `order_date` carries a time component, rows won't match `Date[Date]` (blank member, missing sales); make sure the source column is date-only, or cast it.
- Sales.SemanticModel/definition/tables/Sales.tmdl:18 — `Margin %` is the only measure in a `Margin` display folder while every other base measure is in `Sales`/`Time`. The folder scheme is inconsistent.
- Sales.SemanticModel/definition/tables/Sales.tmdl:6 — currency measures (`Total Sales`, `Total Cost`, `Avg Monthly Sales`, `Sales LY` at lines 6/12/23/29) use `#,0` with no currency symbol or decimals, so amounts are rounded and have no currency.
- Sales.SemanticModel/definition/expressions.tmdl:3 — the server and database are hardcoded in the expression, with no parameters. You can't repoint the model between dev/test/prod without editing the source.
- Sales.SemanticModel/.platform:9 — `logicalId` is the all-zero placeholder GUID. Fabric Git integration needs a unique ID, and this one will collide with other items.
