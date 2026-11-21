"""
Smart Calculator PWA Local Web Server
Serves the web/ directory with proper MIME types, service worker headers,
and displays local and network IP addresses for phone/tablet testing.
"""

import http.server
import socket
import socketserver
import os
import sys

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


def get_local_ip() -> str:
    """Attempts to find the LAN IP address of this device."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class PWAHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving the web/ directory with no-cache headers for PWA."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # Allow Service Worker caching, but avoid proxy caching
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def run_server():
    local_ip = get_local_ip()

    with ReusableTCPServer(("", PORT), PWAHTTPRequestHandler) as httpd:
        print("=" * 65)
        print("         🧮 SMART CALCULATOR - PROGRESSIVE WEB APP (PWA)        ")
        print("=" * 65)
        print(f" [*] Local PC URL:       http://localhost:{PORT}")
        print(f" [*] Mobile / LAN URL:   http://{local_ip}:{PORT}")
        print("-" * 65)
        print(" Features active:")
        print("  - Progressive Web App (PWA) Installable")
        print("  - Offline Service Worker active")
        print("  - Touch & Desktop Keyboard support")
        print("  - Standard & Scientific Modes")
        print("  - Dark & Light Themes with History persistence")
        print("-" * 65)
        print(" Press Ctrl+C in this terminal to stop the server.")
        print("=" * 65)

        # Open in default browser automatically
        try:
            import webbrowser
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    run_server()
