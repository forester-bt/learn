# Runner

The Runner executes a behavior tree from the file system without writing the application boilerplate. It is a wrapper above the `Forester` engine that is configured with an optional YAML run profile instead of code.

Unlike [Simulation](./sim.md), which replaces the actions with stubs, the Runner performs a real execution: all actions must be implemented, either as [remote actions](./rem_action.md) registered in the profile or as built-in actions.

*Available since `forester-rs 0.7.0` and `f-tree 0.4.0`.*

## Run Profile

The run profile is a YAML file where every section is optional and falls back to its default value when absent. An empty file (or no profile at all) gives the default profile: run until the root finishes, no tracing, no blackboard load/dump, no server, no remote actions.

**Note: The relative paths in the profile are resolved against the folder that contains the main tree file.**

Example profile:

```yaml
run_until:
  limit: 10          # or `run_until: no_limit` (the default)

bb:
  load: "bb_init.json"
  dump: "bb_final.json"

tracer:
  indent: 2
  time_format: "%H:%M:%S"
  to_file: "trace.log"

api:
  type: http
  host: "localhost"
  port: 8080

actions:
  - type: http
    name: fetch_data
    url: "http://localhost:10000/action"
```

### `run_until` Section

Defines when the run stops.

| Setting | Description | Default |
| :--- | :--- | :--- |
| `no_limit` | Runs until the root tree returns `Success` or `Failure`. | ✔ |
| `limit` | Runs at most the given number of ticks. | — |

### `bb` Section

The blackboard configuration.

| Setting | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `load` | A JSON file with a blackboard snapshot to load the initial data from before the run. | None (disabled) | `bb_init.json` |
| `dump` | A file to dump the final blackboard state to as JSON after the run. | None (disabled) | `bb_final.json` |

### `tracer` Section

Maps to the engine [tracer](./trace.md).

| Setting | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `indent` | The indent for the nested trace lines. | `2` | `4` |
| `time_format` | The time format for the trace timestamps (`chrono` format string). | None | `"%H:%M:%S"` |
| `to_file` | A file to write the trace to. When absent the trace stays in memory. | None | `trace.log` |

### `api` Section

The [HTTP server](./http_api.md) the engine exposes during the execution. The remote actions send their requests to it to reach the blackboard and the tracer.

| Setting | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `type` | The server type. Only `http` for now. | **Required** | `http` |
| `host` | The host the server binds to. | `127.0.0.1` | `localhost` |
| `port` | The port the server binds to. | `0` (a random available port) | `8080` |

### `actions` Section

The [remote actions](./rem_action.md) to register in the engine. The `name` should match the action name in the tree.

| Setting | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `type` | The action type. Only `http` for now. | **Required** | `http` |
| `name` | The name of the action in the tree. | **Required** | `fetch_data` |
| `url` | The url of the remote server executing the action. | **Required** | `http://localhost:10000/action` |

## Process

You can run a tree via the CLI or directly in Rust code.

### In the Console

Use the `f-tree` CLI:

```shell
f-tree run --root tree/tests/runner/smoke/ --profile profile.yaml
```

**CLI Defaults:**
- `--root`: If omitted, defaults to the current working directory (`<pwd>`).
- `--main`: If omitted, defaults to `main.tree`.
- `--tree`: If omitted, defaults to `main`.
- `--profile`: If omitted, the default profile is used. The path is resolved against the root folder.

### In the Code

Use `Runner` from the `runner` module:

```rust
use std::path::PathBuf;
use forester_rs::runner::Runner;
use forester_rs::runner::config::RunProfile;

fn smoke() {
    let profile = RunProfile::from_file("runner/smoke/profile.yaml").unwrap();

    let mut runner = Runner::build(
        PathBuf::from("runner/smoke/main.tree"),
        "main".to_string(),
        profile,
    )
    .unwrap();

    let result = runner.run().unwrap();
    println!("Result: {:?}", result);
}
```

`Runner::build` accepts the path to the main tree file, the name of the root tree in that file, and the profile (`RunProfile::default()` for the default one). `Runner::run` executes the tree until the root finishes or the `run_until` tick limit is reached, and afterwards dumps the blackboard if `bb.dump` is set.
