import socket
import ssl

HOST = "0.0.0.0"
PORT = 6000

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("server.crt", "server.key")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Secure Server started...")

while True:
    conn, addr = server.accept()
    secure_conn = context.wrap_socket(conn, server_side=True)

    data = secure_conn.recv(1024).decode()
    print("Secure message:", data)

    secure_conn.send(b"SECURE ACK")

    secure_conn.close()