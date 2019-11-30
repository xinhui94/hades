import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")


async def main1():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


async def fun1():
    return 10


async def main2():
    task = asyncio.create_task(fun1())

    def f(future):
        print('hello world')

    task.add_done_callback(f)
    await task
    print(task.result())
    print(task.print_stack())
    print(task.get_name())
    print(task.all_tasks())


@asyncio.coroutine
def old_style_coroutine():
    yield from asyncio.sleep(1)


async def main3():
    await old_style_coroutine()
    print(1)

if __name__ == "__main__":
    print(asyncio.iscoroutine(main3()))
    print(asyncio.iscoroutine(old_style_coroutine()))
    asyncio.run(main3())
