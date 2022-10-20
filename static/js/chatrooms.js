var ws = io()

var room
var username

ws.on("connect", function() {
    writeToLog("Connected to WebSocket server.")
})

ws.on("disconnect", function() {
    writeToLog("Disconnected from WebSocket server.")
    sendingDisabled(true)
})

ws.on("message", function(data) {
    writeToLog(data)
})

ws.on("chat", function(data) {
    writeToLog(data)
})

ws.on("history", function(data) {
    for (var i = 0; i < data.length; i++) {
        writeToLog(data[i])
    }
})

function writeToLog(text) {
    var logs = document.getElementById("logs")
    logs.innerHTML += text + "&#013;"
}

function clearLog() {
    var logs = document.getElementById("logs")
    logs.innerHTML = ""
}

function sendingDisabled(enabled) {
    document.getElementById("message").disabled = enabled
    document.getElementById("send-btn").disabled = enabled
    document.getElementById("disconnect-btn").disabled = enabled
    document.getElementById("connect-btn").disabled = !enabled
}

function attemptToJoinRoom() {
    var roomUsername = document.getElementById("username").value
    var roomId = document.getElementById("room-id").value
    if (roomUsername == ""|| roomId == "") {
        writeToLog("Please enter valid username and roomID to connect")
    } else {
        room = roomId
        username = roomUsername
        clearLog()
        writeToLog("Connecting to room '" + roomId + "'.")
        ws.emit("joinRoom", {"sid": ws.id, "username": roomUsername, "roomId": roomId})
        sendingDisabled(false)
    }
}

function attemptToLeaveRoom() {
    ws.emit("leaveRoom", {"username": username, "roomId": room})
    sendingDisabled(true)
    writeToLog("You have left the room")
}

function sendMessage() {
    var message = document.getElementById("message").value
    if (message !== "") {
        if (message === "/count") {
            ws.emit("incrementChat", {"roomId": room, "username": username})
        } else {
            ws.emit("chat", {"roomId": room, message: username + ": " + message})
        }
    } else {
        writeToLog("Please enter a message.")
    }

    document.getElementById("message").value = ""
}