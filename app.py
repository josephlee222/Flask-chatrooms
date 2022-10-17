import socketio
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit, send

app = Flask(__name__)
socketio = SocketIO(app)
count = 0
chatLog = {}


@app.route('/')
def hello_admin():
    return render_template("home.html", count=count)

@app.route('/chatrooms')
def chatrooms():
    return  render_template("chatrooms.html")


@socketio.on("increment")
def handleIncrement():
    global count
    count += 1
    print("Incremented to " + str(count) + ".")
    socketio.emit("update", count)

@socketio.on("joinRoom")
def joinRoom(data):
    global chatLog
    join_room(data["roomId"])
    print(data)
    send(data["username"] + " has entered the room '" + data["roomId"] + "'", to=data["roomId"])
    try:
        emit("history", chatLog[data["roomId"]], to=data["sid"])
    except:
        print("No history for specified room '" + data["roomId"] + "'.")

@socketio.on("leaveRoom")
def leaveRoom(data):
    leave_room(data["roomId"])
    send(data["username"] + " has left the room '" + data["roomId"] + "'", to=data["roomId"])

@socketio.on("chat")
def chat(data):
    global chatLog
    try:
        chatLog[data["roomId"]].append(data["message"])
    except:
        logList = [data["message"]]
        chatLog[data["roomId"]] = logList


    print(str(chatLog[data["roomId"]]))
    emit("chat", data["message"], to=data["roomId"])

@socketio.on("incrementChat")
def handleIncrementChat(data):
    global count
    count += 1
    print("Incremented to " + str(count) + ".")
    emit("chat", data["username"] + " has incremented the counter to " + str(count), to=data["roomId"])
    emit("update", count, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
