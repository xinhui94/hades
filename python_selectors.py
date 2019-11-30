import selectors
import socket

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready  建立连接
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    # 注册到时间循环列表（不立刻收，客户端可能还没有发。）如果再有活动就调用read函数
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 8001))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)  # 先注册server对象。调用accept

while True:
    events = sel.select()  # 默认阻塞，有活动链接就返回活动列表
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
