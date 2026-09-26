import socket  # noqa: F401
import threading

def handle_client(conn):
    while True:
        data = conn.recv(1024)
        if data == b"":
            print("Client closed the connection")
            break

        print("Received:", data)
        conn.send(b"+PONG\r\n")


def main():
    with socket.create_server(("localhost", 6379), reuse_port=True) as server_socket:
        while True:
            print("Waiting for connection...")
            conn, addr = server_socket.accept()  # wait for client
            print(f"Connected by {addr}")
            thread = threading.Thread(
                target=handle_client,
                args=(conn,)
            )
            thread.start()


if __name__ == "__main__":
    main()
