import asyncio
import websockets
from pymouse import PyMouse

mouse = PyMouse()

def move(x, y):
    pos = mouse.position()
    mouse.move(pos[0] + x, pos[1] + y)

def click():
    pos = mouse.position()
    mouse.click(pos[0], pos[1])

async def server(websocket, path):
    async for message in websocket:
        if message == 'c':
            click();
        else: 
            coordinate = [float(x) for x in message.split(',')]
            move(coordinate[0], coordinate[1])
            
asyncio.get_event_loop().run_until_complete(
    websockets.serve(server, '0.0.0.0', 8080))
asyncio.get_event_loop().run_forever()
