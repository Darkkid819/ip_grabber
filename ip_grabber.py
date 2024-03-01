import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import argparse

parser = argparse.ArgumentParser(description='Simple HTTP server with logging and redirection.')
parser.add_argument('--url', type=str, help='Target URL for redirection', required=True)
parser.add_argument('--port', type=int, help='Port to run the HTTP server on', default=8080)
args = parser.parse_args()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        target_url = args.url

        ip = self.client_address[0]
        port = self.client_address[1]
        agent = self.headers['User-Agent']
        ref = self.headers.get('Referer', 'None')
        hostname = socket.getfqdn(ip)

        with open('log.txt', 'a') as log_file:
            log_file.write(f'IP Address: {ip}\n')
            log_file.write(f'Hostname: {hostname}\n')
            log_file.write(f'Port Number: {port}\n')
            log_file.write(f'User Agent: {agent}\n')
            log_file.write(f'HTTP Referer: {ref}\n\n')

        self.send_response(302)
        self.send_header('Location', target_url)
        self.end_headers()

def run(server_class, handler_class, port):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Starting httpd on port {port}...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    run(HTTPServer, RequestHandler, port=args.port)
