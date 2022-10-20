from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit, send
import shelve

app = Flask(__name__)
socketio = SocketIO(app)
appdata = shelve.open("appdata", writeback=True)

@app.route('/')
def counter():
    return render_template("home.html", count=appdata["count"])

@app.route('/chatrooms')
def chatrooms():
    if "chatHistory" not in appdata:
        appdata["chatHistory"] = {}

    if "count" not in appdata:
        appdata["count"] = 0

    appdata.sync()
    return  render_template("chatrooms.html")


@socketio.on("increment")
def handleIncrement():
    appdata["count"] += 1
    print("Incremented to " + str(appdata["count"]) + ".")
    socketio.emit("update", appdata["count"])
    appdata.sync()

@socketio.on("joinRoom")
def joinRoom(data):
    global chatLog
    join_room(data["roomId"])
    print(data)
    message = data["username"] + " has entered the room '" + data["roomId"] + "'"
    updateLog(message, data["roomId"])
    try:
        emit("history", appdata["chatHistory"][data["roomId"]], to=data["sid"])
    except:
        print("No history for specified room '" + data["roomId"] + "'.")

@socketio.on("leaveRoom")
def leaveRoom(data):
    leave_room(data["roomId"])
    message = data["username"] + " has left the room '" + data["roomId"] + "'"
    updateLog(message, data["roomId"])
    send(message, to=data["roomId"])

@socketio.on("chat")
def chat(data):

    updateLog(data["message"], data["roomId"])
    emit("chat", data["message"], to=data["roomId"])

@socketio.on("incrementChat")
def handleIncrementChat(data):
    appdata["count"] += 1
    print("Incremented to " + str(appdata["count"]) + ".")
    emit("chat", data["username"] + " has incremented the counter to " + str(appdata["count"]), to=data["roomId"])
    emit("update", appdata["count"], broadcast=True)
    appdata.sync()

def updateLog(text, room):
    try:
        appdata["chatHistory"][room].append(text)
    except:
        appdata["chatHistory"][room] = [text]

    appdata.sync()
    print(text)

if __name__ == '__main__':
    socketio.run(app)
