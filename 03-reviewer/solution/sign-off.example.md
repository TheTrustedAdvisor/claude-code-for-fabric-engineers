# Sign-off: Jonas's review of the Sales measures

## Step 2: mark and spot-check

In "G or U" write `G` (grounded: the statement cites a place in the files) or `U` (ungrounded: no citation).
For the two statements you spot-check, write `yes` or `no` in "Holds?". Leave the others empty.

| # | G or U | Holds? |
|---|---|---|
| 1 | G |   |
| 2 | G | no |
| 3 | G |   |
| 4 | G | yes |
| 5 | U |   |

## Step 3: first judgment

One sentence, before any reviewer, and don't change it later:

Statement 2 is wrong, because M1 says to use / when the denominator is a constant.


## Step 4: delegation message, session A

What did Claude's task prompt for the reviewer contain besides the files and the job?

The hint to apply every rule "including any exceptions written into the rule", and to check 'Date' as marked date table. Claude introduced the result with "The reviewer agrees with your judgment".


## Step 5: delegation message, session B

Same question for the fresh session:

Only files, job and format: no word about exceptions. Statement 2 was still found wrong.


## Step 6: one finding checked at the source

Finding (statement number and what the reviewer said):
Statement 2: wrong, the suggested change to DIVIDE() would break M1.

Quote from the source, copied word for word:

> When the denominator is a constant, such as `/ 12`, use the `/` operator.


## Step 7: final decision

In "Final" write `keep` (passes on as it is), `strike` (doesn't hold) or `not a fact` (can't be checked here).

| # | Final |
|---|---|
| 1 | keep |
| 2 | strike |
| 3 | keep |
| 4 | keep |
| 5 | not a fact |
