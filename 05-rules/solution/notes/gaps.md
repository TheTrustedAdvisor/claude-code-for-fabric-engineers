# Gaps

In "Stopped it?" write `yes`, `no` or `partly`. Leave the Fabric row empty if you skip step 9.

| Layer | Stopped it? | What got through, and why |
|---|---|---|
| deny rule | no | `bash deploy.sh prod` and `python3 deploy.py --env=prod` got through: rules match the command text, so every new spelling needs a new rule. |
| hook | partly | It blocked every spelling that says prod, but `python3 deploy.py` with prod set in `.env` got through: the hook reads only the command text. |
| Fabric role |  |  |
