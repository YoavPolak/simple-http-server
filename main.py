from threading import Thread
from server import ThreadedTCPRequestHandler, ThreadedTCPServer

def main():
    HOST, PORT = "localhost", 80

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        server.serve_forever()
if __name__ == "__main__":
    main()