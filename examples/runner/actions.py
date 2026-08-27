import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from forester_client_http import RemoteActionRequest, TickResult

hostName = "127.0.0.1"
serverPort = 10001


class MyServer(BaseHTTPRequestHandler):
    def read_request(self) -> RemoteActionRequest:
        content_length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(content_length))
        return RemoteActionRequest.from_dict(body)

    def send_tick_result(self, result: TickResult):
        self.send_response(200)
        self.send_header("Content-Type", "application/json;charset=UTF-8")
        self.end_headers()
        self.wfile.write(json.dumps(result.to_dict()).encode("utf-8"))

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
        if self.path == "/check":
            request = self.read_request()

            if request.tick < 20:
                print(f"tick {request.tick} - no obstacle")
                self.send_tick_result(TickResult.success())
            else:
                print(f"tick {request.tick} - here is an obstacle")
                self.send_tick_result(TickResult.failure("obstacle detected"))

        elif self.path == "/forward":
            self.read_request()
            print("forward ...")
            self.send_tick_result(TickResult.success())

        elif self.path == "/stop":
            self.read_request()
            print("stop ...")
            self.send_tick_result(TickResult.success())

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
