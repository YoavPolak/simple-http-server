from threading import Thread
from http_server_handler import HTTPServerHandler, HTTPServer

def main():
    HOST, PORT = "localhost", 80

    server = HTTPServer((HOST, PORT), HTTPServerHandler)
    with server:
        server.serve_forever()
if __name__ == "__main__":
    main()