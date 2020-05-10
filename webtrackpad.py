import asyncio
import websockets
from pymouse import PyMouse
from http import HTTPStatus

mouse = PyMouse()
f = open("index.html", "rb")
byte = f.read()
f.close()

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

async def process_request(path, request_headers):
    if request_headers['Connection'] == 'keep-alive':
        return (HTTPStatus.OK, [('Content-Type', 'text/html')], byte)
    else:
        return None;
            
asyncio.get_event_loop().run_until_complete(
    websockets.serve(server, '0.0.0.0', 80, process_request = process_request))
asyncio.get_event_loop().run_forever()