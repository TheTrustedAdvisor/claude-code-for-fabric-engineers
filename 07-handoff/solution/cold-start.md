# Cold-start tests

1. The note doesn't say how many copies may run in parallel; it lists that as the open question. First file: config/source.yaml.
2. Same answer after Claude had found the number in the session: "The note doesn't say." The finding was only in the chat.
3. After I added the finding: at most 16, from config/source.yaml. First file now pipeline-content.json.
4. Before I end a session, I test the note with a fresh claude -p session, because a new session only knows what is in files.
