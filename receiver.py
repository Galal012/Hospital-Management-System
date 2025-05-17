import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

local_ip = "127.0.0.1"
local_port = 54321

sock.bind((local_ip, local_port))
print(f"Socket bound to {local_ip}:{local_port}")

while True:
    data, address = sock.recvfrom(1024)
    if data.decode() == "None":
        break
    print(f"Received message from {address}: {data.decode()}")

sock.close()