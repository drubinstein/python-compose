import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    print(args)
    server_address = ("", args.port)
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    httpd.serve_forever()
