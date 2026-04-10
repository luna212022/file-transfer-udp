# Reliable File Transfer using UDP with SSL Security

## Overview
This project implements a reliable file transfer system over UDP with custom reliability mechanisms and secure communication using SSL/TLS.

## Features
- UDP-based file transfer
- Chunk-based transmission
- Acknowledgment (ACK) system
- Resume interrupted transfers
- Missing packet detection
- Secure communication using SSL/TLS

## Technologies
- Python
- Socket Programming
- UDP Protocol
- TCP + SSL/TLS

## File Structure
- server.py → UDP server
- upload.py → Upload client
- download.py → Download client
- secure_server.py → SSL server
- secure_client.py → SSL client
- generate_cert.py → Generate certificate

## How to Run

### 1. Start Server
python server.py

### 2. Upload File
python upload.py

### 3. Download File
python download.py

### 4. SSL Demo
python secure_server.py
python secure_client.py

## Security
SSL/TLS is used to secure control communication.

## Conclusion
The project demonstrates reliable and secure file transfer over UDP using custom protocol design.
