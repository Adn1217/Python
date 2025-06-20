"""This module provides a mock API server for testing purposes."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv


class MockAPIHandler(BaseHTTPRequestHandler):
    """Handler for the mock API server."""

    def do_get(self):
        """Handle GET requests to the mock API server."""
        parsedUrl = urlparse(self.path)
        path = parsedUrl.path
        queryParams = parse_qs(parsedUrl.query)
        load_dotenv()
        actionsEndpoint = "/" + str(os.getenv("ACTIONS_ENDPOINT"))
        authEndpoint = "/" + str(os.getenv("AUTH_ENDPOINT"))
        scriptDir = os.path.dirname(__file__)

        if path == actionsEndpoint:
            sampleDataFileName = "sampleData.json"
            sampleDataFilePath = os.path.join(scriptDir, sampleDataFileName)
            # with open(rkGUI\PyBot\sampleData.jsonk, 'r') as f:
            with open(sampleDataFilePath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode("utf-8"))
            # if 'id' in query_params:
            #     user_id = int(query_params['id'][0])
            #     user = next((user for user in data['users'] if user['id'] == user_id), None)
            #     if user:
            #         self.send_response(200)
            #         self.send_header('Content-type', 'application/json')
            #         self.end_headers()
            #         self.wfile.write(json.dumps(user).encode('utf-8'))
            #     else:
            #             self.send_response(404)
            #             self.end_headers()
            #             self.wfile.write(b'{"message": "User not found"}')
            # else:
            #     self.send_response(200)
            #     self.send_header('Content-type', 'application/json')
            #     self.end_headers()
            #     self.wfile.write(json.dumps(data['users']).encode('utf-8'))
        elif path == authEndpoint:
            sampleTokenFileName = "sampleToken.json"
            sampleTokenFilePath = os.path.join(scriptDir, sampleTokenFileName)
            # with open(r'GUI\PyBot\sampleData.json', 'r') as f:
            with open(sampleTokenFilePath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path.startswith("/posts"):
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            if "userId" in queryParams:
                userId = int(queryParams["userId"][0])
                posts = [post for post in data["posts"] if post["userId"] == userId]
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(posts).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(
                    b'{"message": "Posts not found for the specified user"}'
                )
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"message": "Not found"}')


def run(port=8000, serverClass=HTTPServer, handlerClass=MockAPIHandler):
    """Run the mock API server."""
    serverAddress = ("", port)
    httpd = serverClass(serverAddress, handlerClass)
    print(f"Starting mock API server on port {port}...")
    httpd.serve_forever()


def main():
    """Main function to run the mock API server."""
    print("Enter localhost port (Default = 8000): ")
    port = input()

    if port == "":
        run()
    else:
        port = int(port)
        run(port)


if __name__ == "__main__":
    main()
