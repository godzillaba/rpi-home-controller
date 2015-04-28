var socket = null;
var isopen = false;
var get_switch_stats = function () {
    var boxes = document.getElementsByTagName('input');
    for (var x = 0; x < boxes.length; x++) {
        socket.send("PIN=" + boxes[x].name + ",IN,0")
    }
}
window.setInterval(function () {
    get_switch_stats()
}, 3000);
window.onload = function() {
    hostname = window.location.hostname
	var wsport = document.getElementById("wsport").content
    socket = new WebSocket("ws://" + hostname + ":" + wsport);
    socket.binaryType = "arraybuffer";
    socket.onopen = function() {
        console.log("Connected!");
        isopen = true;
		Materialize.toast("Connected to ws://" + hostname + ":" + wsport, 3000)
        get_switch_stats()
    }
    socket.onmessage = function(e) {
        if (typeof e.data == "string") {
            console.log("Message received: " + e.data);
            if (e.data.split(" ")[0] === "PIN") {
                var pin_number = e.data.split(" ")[1]
                var pin_status = e.data.split(" ")[2]
                var pin_switch = (document.getElementsByName(pin_number)[0])
                if (pin_status === "0") {
                    pin_switch.checked = true
                } else if (pin_status === "1") {
                    pin_switch.checked = false
                }
            }
        }
    }
    socket.onclose = function(e) {
        console.log("Connection closed.");
		socket = null;
        isopen = false;
		Materialize.toast("Connection to ws://" + hostname + ":" + wsport + " closed.", 5000)
    }
};

//        begin custom stuff

var switch_onclick = function(box) {
    if (isopen === false) {
        Materialize.toast("Not connected to WebSocket server", 5000)
    }
    if (box.checked === true) {
        socket.send('PIN=' + box.name + ',OUT,0')
    } else if (box.checked === false) {
        socket.send('PIN=' + box.name + ',OUT,1')
    }
}
var master_switch_onclick = function(box) {
    if (box.checked === true) {
        socket.send('ALLRELAYS=0')
    } else if (box.checked === false) {
        socket.send('ALLRELAYS=1')
    }
    get_switch_stats()
}