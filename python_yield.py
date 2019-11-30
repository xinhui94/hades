def yield_fun(n):
    for i in range(n):
        yield i


class Future(object):
    def __init__(self):
        self.result = None
        self._callback = []

    def set_result(self, result):
        self.result = result
        for fn in self._callback:
            fn()

    def add_done_callback(self, fn):
        self._callback.append(fn)


def gen_fun():
    print('hi')
    a = Future()
    s = yield a
    print(s)


class Task(object):
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            pass
        next_future.add_done_callback(self.step)


# gen = gen_fun()
# task = Task(gen)

def main():
    # yield from yield_fun(4)
    gen = yield_fun(4)
    # for it in gen:
    #     print(it)
    yield from gen


def f1():
    yield from Future()


def gen():
    yield from subgen()


def subgen():
    while True:
        x = yield
        yield x+1


def main1():
    g = gen()
    next(g)                # 驱动生成器g开始执行到第一个 yield
    retval = g.send(1)     # 看似向生成器 gen() 发送数据
    print(retval)          # 返回2
    # g.throw(StopIteration)  # 看似向gen()抛入异常


# 子生成器
def average_gen():
    total = 0
    count = 0
    average = 0
    while True:
        new_num = yield average
        count += 1
        total += new_num
        average = total/count

# 委托生成器


def proxy_gen():
    while True:
        yield from average_gen()

# 调用方


def main2():
    calc_average = proxy_gen()
    next(calc_average)            # 预激下生成器
    print(calc_average.send(10))  # 打印：10.0
    print(calc_average.send(20))  # 打印：15.0
    print(calc_average.send(30))  # 打印：20.0


if __name__ == "__main__":
    a = main2()
    print(a)
    # print(list(a))
