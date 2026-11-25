# sm-kurs

Semantic model sm_kurs as a Power BI project (TMDL), Direct Lake on the lakehouse lh_kurs, table orders.

Conventions:
- Measures live in the table orders.
- Currency measures use formatString #,0.00.

Change the model only in the files under sm_kurs.SemanticModel/definition/.
Check your work from the exercise folder: `python3 check.py`.
