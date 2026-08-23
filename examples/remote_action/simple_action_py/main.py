import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from forester_client_http import ForesterClient

hostName = "localhost"
serverPort = 10001


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Respond to a GET request."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/action":
            content_length = int(self.headers["Content-Length"])
            # The body is a RemoteActionRequest:
            # {"tick": .., "args": [{"name": .., "value": ..}], "serv_url": ..}
            body = json.loads(self.rfile.read(content_length))

            tick = body["tick"]
            serv_url = body["serv_url"]

            # The client talks back to the Forester HTTP server at `serv_url`.
            client = ForesterClient(serv_url)

            # Write to the blackboard.
            client.put("test", {"f1": 1, "f2": 2, "f3": 3})

            # Read it back.
            print("blackboard['test'] =", client.get("test"))

            # Record an event in the tracer.
            client.trace("simple action executed", tick)

            self.send_response(200)
            self.send_header("Content-Type", "application/json;charset=UTF-8")
            self.end_headers()

            # Respond with a TickResult ("Success", "Running", or {"Failure": ..}).
            self.wfile.write(json.dumps("Success").encode("utf-8"))
        else:
            self.send_error(404)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
