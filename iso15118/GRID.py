import socket
import threading
import json

VALID_TOKENS = {"EV1234", "EV5678", "EV9999"}

def handle_station_request(conn, addr):
    data = conn.recv(1024).decode()
    request = json.loads(data)
    token = request.get("auth_token")

    print(f"[AuthServer] Received token from {addr}: {token}")

    if token in VALID_TOKENS:
        response = {"status": "authorized"}
    else:
        response = {"status": "unauthorized"}

    conn.sendall(json.dumps(response).encode())
    conn.close()

def start_auth_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8080))
    server.listen(5)
    print("[AuthServer] Listening on port 8080...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_station_request, args=(conn, addr)).start()

if __name__ == "__main__":
    start_auth_server()
