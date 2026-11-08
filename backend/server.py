"""
KisanSamvaad - Autonomous Indic Agricultural AI Server
Unified launcher running on Python standard library for ultra-lightweight execution (<100MB RAM).
Integrates Sarvam AI Sovereign Models (Saaras, Bulbul, Sarvam-1, Document Vision, Mayura).
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

# Ensure local backend imports resolve properly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

from app.api.routes import APIRouter
from app.core.config import settings

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class KisanSamvaadHandler(SimpleHTTPRequestHandler):
    """Handles KisanSamvaad API requests with full CORS support and PWA assets."""

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, api-subscription-key, Authorization")

    def _send_json_response(self, data: dict, status_code: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _serve_static_file(self, file_path: str, content_type: str):
        if os.path.exists(file_path):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self._send_cors_headers()
            with open(file_path, "rb") as f:
                content = f.read()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        else:
            self._send_json_response({"error": f"File not found: {os.path.basename(file_path)}"}, 404)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Frontend web routes & PWA manifest / service worker
        if path in ("/", "/index.html", "/interactive_kisan_hub.html"):
            index_path = os.path.join(PROJECT_ROOT, "frontend", "index.html")
            return self._serve_static_file(index_path, "text/html; charset=utf-8")

        elif path == "/manifest.json":
            manifest_path = os.path.join(PROJECT_ROOT, "frontend", "manifest.json")
            return self._serve_static_file(manifest_path, "application/manifest+json")

        elif path == "/sw.js":
            sw_path = os.path.join(PROJECT_ROOT, "frontend", "sw.js")
            return self._serve_static_file(sw_path, "application/javascript")

        elif path == "/presentation.html":
            pres_path = os.path.join(PROJECT_ROOT, "presentation.html")
            return self._serve_static_file(pres_path, "text/html; charset=utf-8")

        elif path.startswith("/api/"):
            data, status = APIRouter.handle_get(path, query)
            return self._send_json_response(data, status_code=status)

        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        headers_dict = {k: v for k, v in self.headers.items()}
        data, status = APIRouter.handle_post(path, body, headers_dict)
        self._send_json_response(data, status_code=status)


def run_server(port: int = 8000, host: str = "127.0.0.1"):
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, KisanSamvaadHandler)
    print(f"🌾 KisanSamvaad Sovereign Agri AI Server running at http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down KisanSamvaad server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    port_to_use = int(sys.argv[1]) if len(sys.argv) > 1 else settings.port
    run_server(port=port_to_use, host=settings.host)
