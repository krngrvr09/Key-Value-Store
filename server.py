from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from db import DB
import sys
kvstore = None

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        # Check if 'key' parameter is provided in the query string
        
        if "key" in query_params:
            key = query_params["key"][0]
            resp = kvstore.get(key)
            if resp["status"]==200:
                value = resp["data"]
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(value.encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Key not found".encode())
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Missing 'key' parameter in the query string".encode())

def run_server(host, port):
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print(f"Starting server at http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    host = "localhost"
    port = 8000
    if len(sys.argv)<2:
        print('Usage: python3 server.py <filepath>')
        exit(0)
    kvstore_path = sys.argv[1]
    try:
        kvstore = DB(kvstore_path)
    except:
        print("Unable to load KV-Store")
        exit(0)
    run_server(host, port)
