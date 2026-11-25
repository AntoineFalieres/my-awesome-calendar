# Calendar Backlog Runner Reports

The Calendar backlog runner archives one Markdown report here for every run,
including runs that stop before making product changes.

Use the run date and the automation run ID in each filename:

```text
YYYY-MM-DD-<run-id>.md
```

If the run ID is not available in the automation context, use the current
session ID instead. Keep prior reports unchanged. Reports are ordinary
worktree changes for review; the runner does not commit or push them.
