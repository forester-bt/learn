import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from forester_client_http import ForesterClient

hostName = "localhost"
serverPort = 10001


class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):

        if self.path == "/move_to":
            content_length = int(self.headers["Content-Length"])
            # The body is a RemoteActionRequest:
            # {"tick": .., "args": [{"name": .., "value": ..}], "serv_url": ..}
            body = json.loads(self.rfile.read(content_length))

            print(f"receive = {body}")
            tick = body["tick"]
            serv_url = body["serv_url"]

            self.send_response(200)
            self.send_header("Content-Type", "application/json;charset=UTF-8")
            self.end_headers()

            if tick == 5:
                client = ForesterClient(serv_url)
                client.put("calculated", False)
                client.trace("Bump!. Recalculate", tick)

            if tick > 10:
                self.wfile.write(json.dumps("Success").encode("utf-8"))
            else:
                self.wfile.write(json.dumps("Running").encode("utf-8"))
        else:
            print("error 404")
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
