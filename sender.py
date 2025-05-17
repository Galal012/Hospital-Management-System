import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

local_ip = "0.0.0.0"
local_port = 12345

sock.bind((local_ip, local_port))
print(f"Socket bound to {local_ip}:{local_port}")

destination_ip = "127.0.0.1"
destination_port = 54321

def send_message(message):
    sock.sendto(message.encode(), (destination_ip, destination_port))
    print("Message sent successfully!")