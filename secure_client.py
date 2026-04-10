import socket
import ssl

HOST = "127.0.0.1"
PORT = 6000

context = ssl._create_unverified_context()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client, server_hostname=HOST)

secure_client.connect((HOST, PORT))

secure_client.send(b"HELLO SECURE SERVER")

response = secure_client.recv(1024)
print("Server:", response.decode())

secure_client.close()