import asyncio

lock = asyncio.Lock()


async def f1():
    await lock.acquire()
    global v1
    global v2
    print('f1')
    lock.release()


async def f2():
    await lock.acquire()
    print('f2')
    lock.release()


async def test_async_lock():
    t1 = asyncio.create_task(f1())
    t2 = asyncio.create_task(f2())
    await t2


async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')


async def main():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()

    # Wait until the waiter task is finished.
    await waiter_task


if __name__ == "__main__":
    asyncio.run(test_async_lock())
