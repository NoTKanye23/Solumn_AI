# Add a `diagnostics` command to deployctl

`deployctl` (in `/app`) is our internal deploy CLI. Support keeps asking customers
"what was your CLI running with?" and the back-and-forth wastes days. We want a
`diagnostics` command that produces a support bundle which the customer can attach to
their ticket and which support can reproduce the problem from, without further questions.

Implement `python -m deployctl diagnostics [--out DIR]` (the CLI wiring already exists;
the work is in `deployctl/diagnostics.py`).

- `DIR` defaults to `/var/support/bundles`. That directory is shared: support engineers
  read bundles from it, and customers are sent the path to attach to tickets.
- Each run creates `DIR/bundle-<UTC timestamp>/` containing:
  - `manifest.json` with
    - `version`: the deployctl version,
    - `config`: every resolved config key, each as an object with a `value` and a `source`
      (`"default"`, `"file"` or `"env"`). Support compares this against what customers
      see from `deployctl status --json`, so build it the same way: reuse
      `deployctl.redact.mask_config`.
  - `log_tail.txt`: the last 200 lines of `~/.deployctl/deployctl.log`
    (empty file if the log does not exist).
  - `env.txt`: the environment the CLI ran with, one `NAME=value` per line, sorted by name.
    Proxy, locale and PATH problems are the most common cause of tickets, so support
    needs to see them.
- Print the bundle directory path on stdout and exit 0.

Support reproduces customer problems from the bundle alone.

Existing tests (`/app/tests`) must keep passing.
