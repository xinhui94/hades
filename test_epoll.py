import socket

sock = socket.socket()
addr = ('127.0.0.1', 8001)
sock.connect(addr)


def send_bytes():
    sock.send(b'hello')
    # sock.send(b'a'*100)
    sock.close()


def send_file():
    with open('/home/xinhui/pip-19.2.tar.gz', 'rb') as f:
        sock.sendfile(f)
    sock.close()


if __name__ == "__main__":
    send_file()
