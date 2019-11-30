import socket
import select

addr = ('127.0.0.1', 8001)
fd_sock = {}
# sock.setblocking(False)
epfd = select.epoll()

for i in range(10):
    sock = socket.socket()
    sock.connect(addr)
    fd_sock[sock.fileno()] = sock
    epfd.register(sock, select.EPOLLOUT)

def handle_read():
    pass

while True:
    events = epfd.poll()
    for fd, event in events:
        sock = fd_sock[fd]
        if event == select.EPOLLOUT:
            sock.send(b'hello world\r\n\r\n')
            epfd.modify(sock, select.EPOLLIN)
        elif event == select.EPOLLIN:
            v = sock.recv(1000)
            print(v)
            sock.close()
