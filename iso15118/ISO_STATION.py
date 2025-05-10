import socket
import threading
import json

def authenticate_token(token):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as auth_sock:
            auth_sock.connect(("localhost", 8080))
            auth_sock.sendall(json.dumps({"auth_token": token}).encode())
            response = auth_sock.recv(1024).decode()
            return json.loads(response)
    except Exception as e:
        print(f"[Station] Error connecting to Auth Server: {e}")
        return {"status": "error"}

def handle_ev_request(conn, addr):
    try:
        data = conn.recv(1024).decode()
        request = json.loads(data)
        token = request.get("auth_token")
        print(f"[Station] Received request from EV: {token}")

        auth_result = authenticate_token(token)
        print(f"[Station] Auth result: {auth_result}")

        conn.sendall(json.dumps(auth_result).encode())
        conn.close()
    except Exception as e:
        print(f"[Station] Error handling EV: {e}")

def start_station_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9090))
    server.listen(5)
    print("[Station] Listening on port 9090...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_ev_request, args=(conn, addr)).start()

if __name__ == "__main__":
    start_station_server()
