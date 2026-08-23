use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::routing::{get, post};
use axum::{Json, Router};
use forester_client_http::{ForesterClient, RemoteActionRequest, TickResult};
use serde_json::json;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    let routing = Router::new()
        .route("/", get(|| async { "OK" }))
        .route("/action", post(handler))
        .into_make_service_with_connect_info::<SocketAddr>();

    axum::Server::bind(&SocketAddr::from(([127, 0, 0, 1], 10000)))
        .serve(routing)
        .await
        .unwrap();
}

async fn handler(Json(req): Json<RemoteActionRequest>) -> impl IntoResponse {
    // The client talks back to the Forester HTTP server exposed at `serv_url`.
    let client = ForesterClient::new(&req.serv_url).unwrap();

    // Write to the blackboard.
    client
        .put("test", json!({"f1": 1, "f2": 2, "f3": 3}))
        .await
        .unwrap();

    // Read it back.
    let value = client.get("test").await.unwrap();
    println!("blackboard['test'] = {value:?}");

    // Record an event in the tracer.
    client.trace("simple action executed", req.tick).await.unwrap();

    (StatusCode::OK, Json(TickResult::Success))
}
