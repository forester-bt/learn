# Runner example

A minimal [Runner](../../src/runner.md) scenario: the tree drives a robot forward until an obstacle appears (at tick 20), then falls back to `stop()`. All three actions are remote HTTP actions served by a small Python server and registered in `profile.yaml`.

## Files

- `main.tree` — the behavior tree.
- `profile.yaml` — the run profile registering the remote actions and capping the run at 25 ticks (the root re-ticks forever otherwise).
- `actions.py` — the Python server implementing `/check`, `/forward` and `/stop` with `forester_client_http`.

## Run

Start the action server with Python:

```shell
pip install forester_client_http
python actions.py
```

Then run the tree with `f-tree` from this folder:

```shell
f-tree run --profile profile.yaml
```

Ticks 1–19 succeed (`check_obstacle` → `go_forward`); from tick 20 `check_obstacle` returns `{"Failure": "obstacle detected"}` and the fallback executes `stop()`.
