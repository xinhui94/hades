import select
import socket
import re

sock = socket.socket()
sock.bind(('0.0.0.0', 8001))
sock.listen()
sock.setblocking(False)
ep_fd = select.epoll()
ep_fd.register(sock, select.EPOLLIN)

fd_sock = {}
fd_read_data = {}
fd_write_data = {}
tasks = []


def on_read(fd):
    # while True:
    #     try:
    #         d = fd_sock[fd].recv(10)
    #         req += d
    #     except BlockingIOError as identifier:
    #         print(identifier)
    #         break
    d = fd_sock[fd].recv(10)
    req = fd_read_data[fd]
    req += d
    fd_read_data[fd] = req
    if b'\r\n\r\n' in req:
        print(req)
        ep_fd.unregister(fd_sock[fd])
        ep_fd.register(fd, select.EPOLLOUT)
        fd_write_data[fd] = req
        # fd_sock[fd].close()
        # fd_sock.pop(fd)


def on_read_v2(fd):
    # 循环读取数据
    # todo 避免一种情况，某个用户一次性发送过大数据包，导致cpu一直处理这个用户，其他用户无法被处理
    # todo 发送不符合格式的数据包，导致系统一直在处理这个用户 用户层进行处理 可以设置最大缓冲区长度
    while True:
        try:
            req = fd_read_data[fd]
            d = fd_sock[fd].recv(1500)
            req += d
            fd_read_data[fd] = req
            # handle_read_file(fd, req)
            if len(d) == 0:
                handle_close(fd)
                ep_fd.unregister(fd)
                break
            # handle_read_file(fd, req)
            handle_read(fd, req)
            # handle_read_termi(fd, req)
            # if b'\r\n\r\n' in req:
            #     print(req)
            #     ep_fd.unregister(fd_sock[fd])
            #     ep_fd.register(fd, select.EPOLLOUT)
            #     fd_write_data[fd] = req
            #     break
        except BlockingIOError as identifier:
            print(identifier)
            break


def on_read_file(fd):
    try:
        f = open('output', 'ab')
    except Exception as identifier:
        print(identifier)
        new_sock = fd_sock[fd]
        new_sock.close()
        return
    while True:
        try:
            data = fd_sock[fd].recv(4096)
            if len(data) == 0:
                f.close()
                handle_close(fd)
                ep_fd.unregister(fd)
                break
            f.write(data)
        except Exception as identifier:
            f.close()
            print(identifier)
            break


def on_write(fd):
    # 对写缓冲区进行操作
    new_sock = fd_sock[fd]
    data = fd_write_data[fd]
    n = new_sock.send(data)
    if n < len(data):
        fd_write_data[fd] = data[n:]
    else:
        fd_write_data[fd] = b''
        ep_fd.unregister(fd)
        # new_sock.close() # 应该用户层关闭连接


def on_write_v2(fd):
    # 基本不需要应用层操心，自动完成
    new_sock = fd_sock[fd]
    data = fd_write_data[fd]
    while True:
        try:
            n = new_sock.send(data)
            if n < len(data):
                data = data[n:]
            else:
                # ep_fd.unregister(fd)  # 导致读取也失败了
                ep_fd.modify(fd, select.EPOLLIN)
                fd_write_data[fd] = b''
                # new_sock.close() #  连接关闭是应用层考虑的事 handle_write
                handle_write(fd)
                # handle_write_termi(fd)
                break
        except Exception as identifier:
            fd_write_data[fd] = data
            print(identifier)
            break


def on_error(fd):
    handle_error(fd)
    fd_sock[fd].close()


def on_connect():
    new_sock, address = sock.accept()
    new_sock.setblocking(False)
    fd_sock[new_sock.fileno()] = new_sock
    fd_read_data[new_sock.fileno()] = b''
    handle_connect(new_sock.fileno(), address)


def handle_connect(fd, address):
    # 可以设置直接关闭连接，或者读取数据，或者打印消息等。
    new_sock = fd_sock[fd]
    ep_fd.register(new_sock, select.EPOLLIN)
    print('get req from {addr}'.format(addr=address))


def handle_read(fd, data):
    # 应用层接口,处理粘包以及数据处理
    # 一条消息完整时才进行处理
    # 处理可以选择长连接或者短链接
    # 注意越过边界的数据不要要放回去
    # 本例为echo例子，返回对方发送的消息
    if b'\r\n\r\n' in data:
        print(data)
        # ep_fd.unregister(fd_sock[fd])  # 短连接
        fd_read_data[fd] = b''
        send_data(fd, data)


def handle_read_termi(fd, data):
    x = re.search('xin', data.decode())
    if x:
        end = x.end()
        value = data[:end]
        fd_read_data[fd] = data[end:]
        print('get message {msg}'.format(msg=value))
        send_data(fd, value)


def handle_write_termi(fd):
    print('close short connection')


def handle_write(fd):
    new_sock = fd_sock[fd]
    new_sock.close()
    print('close short connection')


def send_data(fd, data):
    # 将数据送到发送缓冲区，并设置可写
    # 如果第一次发送数据，直接修改发送缓冲区以及改状态可写，每次发送之后设置为不可写
    # 第二次发送，注意一个fd只能register一次，如果要监听只能调用modify函数
    fd_write_data[fd] = data
    # ep_fd.register(fd, select.EPOLLOUT)  # 重复注册
    ep_fd.modify(fd, select.EPOLLIN | select.EPOLLOUT)


def handle_read_file(fd, req):
    # 一边上传一遍写入
    # 磁盘文件没有阻塞非阻塞概念，只有网络io由非阻塞
    # 缺点 频繁打开关闭文件导致
    with open('output', 'ab') as f:
        f.write(req)
        fd_read_data[fd] = b''


def handle_close(fd):
    print('connect closed by remote')


def handle_error(fd):
    print('remote error')


def read_buff_peek(fd, n):
    data = fd_read_data[fd]
    fd_read_data[fd] = data[n:]


def buff_add_data(fd, data):
    pass


while True:
    events = ep_fd.poll()
    for task in tasks:
        task()
    for fd, event in events:
        if fd == sock.fileno():
            on_connect()
        else:
            if event == select.EPOLLIN:
                on_read_v2(fd)
                # on_read_file(fd)
            elif event == select.EPOLLOUT:
                on_write_v2(fd)
            else:
                on_error(fd)

# 接口 handle_connect, handle_read, handle_close， handle_write
# 网络编程的三个半事件
# 不能滥用register/unregister
