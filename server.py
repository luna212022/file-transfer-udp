import socket
import json
import os

HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("✅ Server started on port", PORT)

files = {}

while True:
    try:
        data, addr = server.recvfrom(BUFFER_SIZE)
    except Exception as e:
        print("❌ Receive error:", e)
        continue

    print("\n📥 Packet from:", addr)

    try:
        message = json.loads(data.decode())
    except:
        print("❌ Invalid JSON")
        continue

    print("📨 Message type:", message.get("type"))

    # ---------------- RESUME ----------------
    if message["type"] == "RESUME":

        filename = message["filename"]
        print(f"🔄 Resume request for {filename}")

        if filename in files:
            received = set(files[filename].keys())
        else:
            received = set()

        response = {
            "type": "MISSING",
            "received": list(received)
        }

        server.sendto(json.dumps(response).encode(), addr)

    # ---------------- UPLOAD ----------------
    elif message["type"] == "UPLOAD":

        filename = message["filename"]
        seq = message["seq"]

        try:
            chunk = bytes.fromhex(message["data"])
        except Exception as e:
            print("❌ Decode error:", e)
            continue

        if filename not in files:
            files[filename] = {}

        files[filename][seq] = chunk

        print(f"📦 Received chunk {seq}")

        ack = {"type": "ACK", "seq": seq}
        server.sendto(json.dumps(ack).encode(), addr)

    # ---------------- FINISH ----------------
    elif message["type"] == "FINISH":

        filename = message["filename"]
        print(f"✅ FINISH for {filename}")

        chunks = files.get(filename, {})

        if not chunks:
            print("❌ No data received")
            continue

        ordered = [chunks[i] for i in sorted(chunks)]

        output_file = "server_" + filename

        try:
            with open(output_file, "wb") as f:
                for c in ordered:
                    f.write(c)

            print(f"💾 File saved as {output_file}")
        except Exception as e:
            print("❌ File write error:", e)

    # ---------------- DOWNLOAD ----------------
    elif message["type"] == "DOWNLOAD":

        filename = message["filename"]
        filepath = "server_" + filename

        print(f"📤 Download request for {filename}")

        if not os.path.exists(filepath):
            print("❌ File not found")
            continue

        with open(filepath, "rb") as f:
            seq = 0
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break

                packet = {
                    "type": "DATA",
                    "seq": seq,
                    "data": chunk.hex()
                }

                server.sendto(json.dumps(packet).encode(), addr)
                seq += 1

        server.sendto(json.dumps({"type": "END"}).encode(), addr)
        print("✅ Download complete")