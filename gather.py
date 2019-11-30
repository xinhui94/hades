import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )


async def fun(i):
    return i


async def main1():

    rs = await asyncio.gather(
        fun(1),
        fun(2),
    )
    print(rs)


async def main2():

    task = asyncio.create_task(fun(1))
    done, pending = await asyncio.wait({task})
    if task in done:
        print('done')


async def main3():
    await asyncio.gather(fun(1), factorial('A', 3))
    print(asyncio.current_task())
    print(asyncio.all_tasks())

if __name__ == "__main__":
    asyncio.run(main3())
