import select
import socket

sock = socket.socket()
sock.bind(('0.0.0.0', 8001))
rlist = [sock]
wlist = []
xlist = []

sock.listen()
sock.setblocking(False)
while True:
    rl, wl, xl = select.select(rlist, wlist, xlist)
    for fd in rl:
        if fd == sock:
            new_sock, addr = sock.accept()
            print('get req from {addr}'.format(addr=addr))
            new_sock.setblocking(False)
            rlist.append(new_sock)
        else:
            data = fd.recv(4096)
            print(data)
            fd.close()
            rlist.remove(fd)
    
        