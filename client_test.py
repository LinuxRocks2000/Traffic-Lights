import socket
while 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", int(input("port> "))))
    sock.send(b"S" + bytes([3, 3, 0, 1]))
