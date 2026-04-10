import socket
import json

SERVER_IP = "127.0.0.1"
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)   # ⚠ prevents infinite hang

filename = "test.txt"

# ---------------- REQUEST ----------------
request = {
    "type": "DOWNLOAD",
    "filename": filename
}

print(f"📤 Requesting '{filename}' from server...")
client.sendto(json.dumps(request).encode(), (SERVER_IP, PORT))

file_data = {}
expected_seq = 0

# ---------------- RECEIVE ----------------
while True:
    try:
        data, _ = client.recvfrom(4096)
    except socket.timeout:
        print("❌ Timeout: Server not responding")
        break

    try:
        msg = json.loads(data.decode())
    except:
        print("❌ Invalid packet")
        continue

    msg_type = msg.get("type")
    print("📥 Packet:", msg_type)

    # END signal
    if msg_type == "END":
        print("✅ All chunks received")
        break

    # DATA packet
    if msg_type == "DATA":
        seq = msg["seq"]

        try:
            chunk = bytes.fromhex(msg["data"])
        except:
            print("❌ Corrupt chunk")
            continue

        print(f"📦 Received chunk {seq}")
        file_data[seq] = chunk

# ---------------- REBUILD FILE ----------------
if not file_data:
    print("❌ No data received. File not created.")
    exit()

output_file = "downloaded_" + filename

with open(output_file, "wb") as f:
    for i in sorted(file_data):
        f.write(file_data[i])

print(f"\n🎉 Download complete! Saved as '{output_file}'")