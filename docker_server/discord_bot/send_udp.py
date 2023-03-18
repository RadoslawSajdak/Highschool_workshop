import socket

def send_udp(message):
    IP_ADDRESS = "127.0.0.1"
    UDP_PORT = 8888

    print("UDP target IP: ", IP_ADDRESS)
    print("UDP target port: ", UDP_PORT)
    print("message: ", message)

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (IP_ADDRESS, UDP_PORT))

    data, addr = sock.recvfrom(1500) # buffer size is 1500 bytes
    print("Got: ", data)
    sock.close()

if __name__ == "__main__":
    send_udp("Hello world")