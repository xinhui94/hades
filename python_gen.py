#!/usr/bin/env python
# encoding: utf-8

import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stopped = False
# urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}
urls_todo = {'/'}


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))

        global stopped
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            # send会进入到coro执行, 即fetch, 直到下次yield
            # next_future 为yield返回的对象
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


def loop():
    while not stopped:
        # 阻塞, 直到一个事件发生
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()


if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())  # 这里调用完所有协程都阻塞在yield f上面，之后事件循环发生，每次事件循环调用step程序前进
    loop()
    print(time.time() - start)
