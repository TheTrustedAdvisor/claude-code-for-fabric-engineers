# Notes, exercise 2

## Step 2: without the guidelines

- Number of findings: 13
- Messages in /context after the review: 14.3k

## Step 3: your prediction

Which findings will the team's guidelines keep? Write the file:line of each, before step 4.

- Sales.tmdl:17 (Margin % has no formatString, M2)
- Sales.tmdl:22 (divides with /, M1?)

## Step 4: with the guidelines

- Number of findings: 1
- Messages in /context after the review: 8.7k
- Which of your predictions held: Sales.tmdl:17. Sales.tmdl:22 is allowed: M1 says to use / for a constant.

## Step 5: one line changed

- Rule ID you change: M1
- The finding you expect to appear or drop (file:line): Sales.tmdl:22 appears
- What happened: M1 at Sales.tmdl:22 appeared, M2 stayed

## Step 6: one task per session

One sentence: why does the review against the guidelines get its own session?

Three sessions with /clear in between: each review needs only its own model and the guidelines, and the earlier models would only add tokens to every turn.
