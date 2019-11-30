import threading

lock = threading.Lock()


def job1():
    global n
    for i in range(10):
        n += 1
        print('job1', n)


def job2():
    global n
    for i in range(10):
        n += 10
        print('job2', n)


n = 0
t1 = threading.Thread(target=job1)
t2 = threading.Thread(target=job2)
t1.start()
t2.start()
t1.join()
t2.join()
