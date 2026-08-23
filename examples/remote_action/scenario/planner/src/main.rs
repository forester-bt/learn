use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::routing::{get, post};
use axum::{Json, Router};
use forester_client_http::{ForesterClient, RemoteActionRequest, TickResult};
use serde_json::json;
use std::net::SocketAddr;
use std::time::Duration;

#[tokio::main]
async fn main() {
    let routing = Router::new()
        .route("/", get(|| async { "OK" }))
        .route("/calculate", post(handler))
        .into_make_service();
    println!("The server is starting on .10000");
    axum::Server::bind(&SocketAddr::from(([127, 0, 0, 1], 10000)))
        .serve(routing)
        .await
        .unwrap();
}

async fn handler(Json(req): Json<RemoteActionRequest>) -> impl IntoResponse {
    // The client talks back to the Forester HTTP server exposed at `serv_url`.
    let client = ForesterClient::new(&req.serv_url).unwrap();
    println!("serv_url:{}", req.serv_url);
    client.put("calculated", json!(true)).await.unwrap();

    client.lock("calculated").await.unwrap();
    tokio::time::sleep(Duration::from_millis(500)).await;
    client.unlock("calculated").await.unwrap();

    client.trace("Calculated", req.tick).await.unwrap();
    println!("the end");
    (StatusCode::OK, Json(TickResult::Success))
}
