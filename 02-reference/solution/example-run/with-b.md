# Review: Sales.SemanticModel against modeling-guidelines-b.md

- Sales.SemanticModel/definition/tables/Sales.tmdl:17 — M2: measure 'Margin %' has no `formatString`; percentages must use `0.0%`.
- Sales.SemanticModel/definition/tables/Sales.tmdl:22 — M1: measure 'Avg Monthly Sales' divides with `/` (`[Total Sales] / 12`) instead of `DIVIDE()`.
