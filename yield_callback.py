import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stopped = True
urls_to_do = ['/']


class Crawser(object):
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()

        try:
            self.sock.connect(('www.baidu.com', 80))
            self.sock.setblocking(False)
        except BlockingIOError as e:
            print(e)
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)
        global stopped
        while stopped:
            events = selector.select(timeout=3)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def connected(self, key, mask):
        selector.unregister(self.sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHOST: www.baidu.com\r\n\r\n'.format(
            self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(self.sock.fileno(), EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        try:
            chunk = self.sock.recv(4096)
            if chunk:
                self.response += chunk
            else:
                print(self.response)
                selector.unregister(self.sock.fileno())
                urls_to_do.remove(self.url)
                if not urls_to_do:
                    stopped = False
        except Exception as identifier:
            print(identifier)
            stopped = False


cr = Crawser('/')
cr.fetch()
