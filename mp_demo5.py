from multiprocessing import Process, Queue
import time


def f(q):
    time.sleep(2)
    q.put([42, None, 'hello'])


if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()

# 线程进程安全，既多个线程同时访问不出错
