""" import csv
import json
import http.server

filename = 'LE2.txt'

with open(filename, 'r', newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    data = list(reader)  # read once

class handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received request from {self.client_address}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        print("Data sent")

http.server.HTTPServer(('localhost', 8000), handler).serve_forever()
# Run this server and access http://localhost:8000 to see the JSON data """

print("This is a placeholder for Exercise 202.py")