import sys
import http.server as s

LISTEN_ADDRESS = '0.0.0.0'
LISTEN_PORT = int(sys.argv[1])

class ServerHandler(s.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("{} {} {}<br>\n".format(self.command, self.path, self.request_version).encode())
        for h in self.headers:
            self.wfile.write("{}: {}<br>\n".format(h, self.headers[h]).encode())
        self.wfile.write("<a href='http://localhost:8080/app/callback?logout=backchannel'>Logout</a>\n".format().encode())
        self.wfile.write("<a href='http://localhost:8180/realms/demo/protocol/openid-connect/logout?post_logout_redirect_uri={}&client_id={}&id_token_hint={}'>Logout 2</a>\n".format('http%3A%2F%2Flocalhost%3A8080%2F', 'reverse-proxy-app', self.headers['OIDC_id_token']).encode())

httpd = s.HTTPServer((LISTEN_ADDRESS, LISTEN_PORT), ServerHandler)
httpd.serve_forever()

