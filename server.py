from asyncio import sleep
from sanic import Sanic
from sanic.response import text

app = Sanic()


@app.route('/')
async def test(request):
    await sleep(5)
    return text("Hello world!")


@app.websocket("ws/")
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Sending: ' + data)
        await sleep(5)
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
