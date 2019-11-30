import asyncio
import time

success = 0
fail = 0


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    # print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    # print(f'Received: {data.decode()!r}')

    # print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def main(message, count=100):
    print(f"started at {time.strftime('%X')}")
    # task = asyncio.create_task(tcp_echo_client(message))
    
    for i in range(count):
        await tcp_echo_client(message)
    print(f"stoped at {time.strftime('%X')}")
    print(f'call {count} times')

asyncio.run(main('Hello World!', 100))
