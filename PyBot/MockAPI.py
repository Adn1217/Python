import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv;

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        load_dotenv();
        actionsEndpoint = '/'+os.getenv("ACTIONS_ENDPOINT");
        authEndpoint = '/'+os.getenv("AUTH_ENDPOINT");
        scriptDir = os.path.dirname(__file__);

        if path == actionsEndpoint:
            sampleDataFileName = 'sampleData.json';
            sampleDataFilePath = os.path.join(scriptDir,sampleDataFileName);
            # with open(r'GUI\PyBot\sampleData.json', 'r') as f:
            with open(sampleDataFilePath, 'r') as f:
                data = json.load(f)
                if(data):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode('utf-8'))
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
            sampleTokenFileName = 'sampleToken.json';
            sampleTokenFilePath = os.path.join(scriptDir,sampleTokenFileName);
            # with open(r'GUI\PyBot\sampleData.json', 'r') as f:
            with open(sampleTokenFilePath, 'r') as f:
                data = json.load(f)
                if(data):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode('utf-8'))

        elif path.startswith('/posts'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            if 'userId' in query_params:
                    user_id = int(query_params['userId'][0])
                    posts = [post for post in data['posts'] if post['userId'] == user_id]
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(posts).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"message": "Posts not found for the specified user"}')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"message": "Not found"}')

def run( port=8000, server_class=HTTPServer, handler_class=MockAPIHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting mock API server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    print("Enter localhost port (Default = 8000): ");
    port=input();
    
    if(port==""):
       run();
    else:
       port = int(port);
       run(port);
         
    
         