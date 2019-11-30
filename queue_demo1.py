import queue
import threading


def f(q):
    q.put(1)
    print('sub thread')


if __name__ == "__main__":
    q = queue.Queue()
    t = threading.Thread(target=f, args=(q,))
    t.start()
    print(q.get())
    q.task_done()
    t.join()
