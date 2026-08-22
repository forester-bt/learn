# Forester HTTP API

Forester embeds a small HTTP server that exposes the **blackboard** and the **tracer** to remote actions. The server starts automatically when a Forester instance is configured with an HTTP server address and stops when the tree finishes.

The API is documented as an OpenAPI 3.1 specification using [`utoipa`](https://crates.io/crates/utoipa). The specification is generated at compile time from the `#[utoipa::path]` annotations on the route handlers and is available in two ways:

* Programmatically via `forester_rs::runtime::forester::serv::ApiDoc::openapi()`.
* At runtime via the `GET /openapi.json` endpoint of the running server.

The full specification lives in the Forester repository: [HTTP API OpenAPI specification](https://github.com/forester-bt/forester/blob/main/docs/http-api.md).

## Endpoints

| Method | Path                 | Description                                          |
| ------ | -------------------- | ---------------------------------------------------- |
| GET    | `/`                  | Health check, always returns `OK`.                   |
| GET    | `/openapi.json`      | The OpenAPI specification of this server.            |
| GET    | `/bb/{key}`          | Read the value stored under `key` (`null` if absent).|
| POST   | `/bb/{key}`          | Store a value under `key`.                           |
| GET    | `/bb/{key}/take`     | Read and remove the value stored under `key`.        |
| GET    | `/bb/{key}/lock`     | Lock `key` so it cannot be taken.                    |
| GET    | `/bb/{key}/unlock`   | Unlock `key`.                                        |
| GET    | `/bb/{key}/locked`   | Return whether `key` is locked.                      |
| GET    | `/bb/{key}/contains` | Return whether `key` exists.                         |
| POST   | `/tracer/custom`     | Record a custom event in the tracer.                 |
| GET    | `/tracer/print`      | Return the tracer content as a string.               |

All endpoints return `200` on success and `500` with the error message in the body on failure.

## Blackboard values (`RtValue`)

The blackboard endpoints exchange a free-form JSON value (`RtValue`). A value is one of:

| Type    | JSON representation         |
| ------- | --------------------------- |
| String  | JSON string                 |
| Bool    | JSON boolean                |
| Number  | JSON number (int or float)  |
| Array   | JSON array of values        |
| Object  | JSON object of values       |
| Pointer | not serializable            |
| Call    | not serializable            |

Examples:

* `POST /bb/greeting` with body `"hello"`
* `POST /bb/count` with body `42`
* `POST /bb/config` with body `{"timeout": 5, "tags": ["a", "b"]}`

## Tracer events

`POST /tracer/custom` accepts a `CustomEvent`:

```json
{
  "text": "some event",
  "tick": 3
}
```

## Remote actions

A remote action (`RemoteHttpAction`) delegates its execution to an external HTTP endpoint. When ticked, Forester `POST`s a `RemoteActionRequest` to the action's URL:

```json
{
  "tick": 3,
  "args": [
    { "name": "arg", "value": 42 }
  ],
  "serv_url": "http://127.0.0.1:46123"
}
```

* `tick` — the current tick of the tree.
* `args` — the arguments passed to the action.
* `serv_url` — the URL of the **Forester HTTP server**. The remote action uses this URL to read/write the blackboard and record tracer events while it is being executed.

The remote endpoint is expected to answer with a JSON `TickResult`, one of `"Success"`, `"Running"` or `{"Failure": "reason"}`.

## Server configuration

The server address is configured with `ForesterBuilder::http_serv`:

```rust
fb.http_serv("127.0.0.1".to_string(), 0);
```

* `host` is the address the server binds to. Any valid IP address is allowed (for example `0.0.0.0` to bind on all interfaces).
* `port` is the port to bind to. A port of `0` selects a random available port; the resulting URL is available from the `ServInfo` returned by `serv::start`.

The simulator reads the same configuration from the profile file:

```yaml
config:
  http:
    host: 127.0.0.1
    port: 8080
```
