"""
for connecting to WebSocket use command
uvicorn main:app --reload

"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Messages</title>
        <style>
        li {
        list-style-type: none;
        }
        </style>
    </head>
    <body>
        <h1>Form with text field</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                message_json = JSON.parse(event.data)
                message_num = message_json['message_number']
                message_out = message_json['send_message']
                var content = document.createTextNode(message_num + ". " + message_out)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                let message_data = {send_message: input.value};
                let json_message = JSON.stringify(message_data);
                ws.send(json_message)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def root():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    message_number = 0
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        message_number += 1
        message = json.loads(data)
        message['message_number'] = message_number
        await websocket.send_text(json.dumps(message))
