import time
from threading import Thread


def fun1(name=''):
    for i in range(2):
        print('hello world, {name}'.format(name=name))
        time.sleep(1)


def main():
    thread1 = Thread(target=fun1, args=('xinhui', ))
    thread1.start()

    thread2 = Thread(target=fun1)
    thread2.start()

    thread1.join()
    thread2.join()
    print('main finished')


if __name__ == "__main__":
    print(time.ctime())
    main()
    print(time.ctime())
