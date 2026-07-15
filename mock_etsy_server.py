import http.server
import socketserver
import json
import urllib.parse
from uuid import uuid4

PORT = 8082

# In-memory store for Etsy listings
listings = []

class DummyEtsyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # We only support searching listings by SKU: /v3/application/shops/1/listings?sku=...
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.endswith("/listings"):
            query = urllib.parse.parse_qs(parsed.query)
            sku_search = query.get("sku", [None])[0]
            
            results = []
            for l in listings:
                if sku_search:
                    if l.get("sku") == sku_search:
                        results.append(l)
                else:
                    results.append(l)
            
            # Note: This is a dumb mock. It literally just checks the sku field if provided.
            response_data = {
                "count": len(results),
                "results": results
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            return
            
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path.endswith("/listings"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                body = json.loads(post_data.decode('utf-8'))
            except Exception:
                body = {}
                
            new_listing = {
                "id": str(uuid4()),
                "title": body.get("title", "Untitled"),
                "sku": body.get("sku", ""),
                "description": body.get("description", "")
            }
            
            listings.append(new_listing)
            
            response_data = {
                "id": new_listing["id"],
                "status": "created"
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            return
            
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DummyEtsyHandler) as httpd:
        print(f"Mock Etsy Server listening on port {PORT}")
        httpd.serve_forever()
