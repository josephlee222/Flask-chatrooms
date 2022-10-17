var ws = io()

ws.on("connect", function() {
    console.log("Connected.")
})

function increaseCount() {
    console.log("Button pressed")
    ws.emit("increment")
}

ws.on("update", function(count) {
    document.getElementById("count").innerHTML = count
})