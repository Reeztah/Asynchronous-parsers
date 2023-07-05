import asyncio
import time


async def fun1(x):
    print(f"x ** 2 = {x ** 2} быстрая часть функции fun1")  # находим квадрат от x
    await asyncio.sleep(3)  # засыпаем на 3 секунды
    print('...fun1 очнулась и завершена')  # выводим сообщение


async def fun2(x):
    print(f"x ** 0.5 = {x ** 0.5} быстрая часть функции fun2")  # находим квадрат 0.5 от x
    await asyncio.sleep(3)  # засыпаем на 3 секунды
    print('...fun2 очнулась и завершена')  # выводим сообщение


print(time.strftime('%X'))

loop = asyncio.get_event_loop()
task1 = loop.create_task(fun1(4))
task2 = loop.create_task(fun2(4))
loop.run_until_complete(asyncio.wait([task1, task2]))

print(time.strftime('%X'))
