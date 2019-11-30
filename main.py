#!/usr/bin/env python
# author: chenxinhui
import asyncio


async def f1():
    print('f1 s')
    await asyncio.sleep(10)
    print('f1 e')


async def f2():
    print('f2 s')
    await asyncio.sleep(10)
    print('f2 e')

async def main():
    
    print('main')
    task2 = asyncio.create_task(f2())
    task1 = asyncio.create_task(f1())

    # await f1()
    # await task1
    print('middle')
    await task1
    # await f2()

if __name__ == "__main__":
    asyncio.run(f1())
