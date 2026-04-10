import socket
import json

SERVER_IP = "127.0.0.1"
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(3)

filename = "cn.png"   # ⚠️ MAKE SURE FILE EXISTS

# ---------------- RESUME ----------------
resume_req = {
    "type": "RESUME",
    "filename": filename
}

print("🔄 Checking for resume...")
client.sendto(json.dumps(resume_req).encode(), (SERVER_IP, PORT))

try:
    data, _ = client.recvfrom(4096)
    response = json.loads(data.decode())
    received_chunks = set(response.get("received", []))
    print("📥 Server already has:", received_chunks)
except:
    print("⚠ Starting fresh")
    received_chunks = set()

# ---------------- UPLOAD ----------------
with open(filename, "rb") as f:
    seq = 0

    while True:
        chunk = f.read(1024)
        if not chunk:
            break

        if seq in received_chunks:
            print(f"⏭ Skipping {seq}")
            seq += 1
            continue

        packet = {
            "type": "UPLOAD",
            "filename": filename,
            "seq": seq,
            "data": chunk.hex()
        }

        while True:
            print(f"📤 Sending {seq}")
            client.sendto(json.dumps(packet).encode(), (SERVER_IP, PORT))

            try:
                data, _ = client.recvfrom(1024)
                ack = json.loads(data.decode())

                if ack["seq"] == seq:
                    print(f"✅ ACK {seq}")
                    break

            except socket.timeout:
                print(f"❌ Retry {seq}")

        seq += 1

# ---------------- FINISH ----------------
client.sendto(json.dumps({
    "type": "FINISH",
    "filename": filename
}).encode(), (SERVER_IP, PORT))

print("🎉 Upload complete!")