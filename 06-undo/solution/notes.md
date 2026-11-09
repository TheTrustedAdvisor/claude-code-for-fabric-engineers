# Notes

## Prediction (write it before you open /rewind)

After "Restore code", which files are back as in the baseline, and does your own line stay?

All three files go back to the baseline, and my own line stays, because I typed it myself.

## What happened

- The notebook: the checkpoint brought it back. "Restore code" on the prompt from step 2 restored `notebook-content.py` whole, so my own line ("Reviewed by Ana, Nov 5.") was gone with Claude's heading.
- `clean_counts.py`: the checkpoint didn't cover it, because Claude changed it with `sed` in the shell. `git restore clean_counts.py` brought it back.
- The backup copy `clean_counts.bak.py`: made with `cp`, so neither the checkpoint nor `git restore` knew it. `git clean -n` listed it, `git clean -f clean_counts.bak.py` deleted only that file.

## My rule for undoing Claude's changes

I undo Claude's file edits with /rewind and shell changes with Git, and run git status afterward, because a checkpoint covers only the files Claude edited with its file tools. I don't add my own lines to a file Claude just changed until I've committed or rewound its change, and once it's committed, I undo with Git. I commit before a bigger change.
