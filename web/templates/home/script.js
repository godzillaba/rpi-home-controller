function create (s, addr_self) {

	s.binaryType = "arraybuffer";
	
	s.onopen = function() {
	    console.log("Connected!");
		Materialize.toast("Connected to " + s.url, 3000)
	    get_switch_stats()
	}
	
	s.onmessage = function(e) {
	        console.log("[" + s.url + "] Received: " + e.data);
	        
			if (addr_self) {
				var addressdiv = document.getElementById('self')
			}
			else {
				var addressdiv = document.getElementById(s.url)
			}
			
			
	        // parse received data
	        if (e.data.split(" ")[0] === "PIN") {
	            var pin_number = e.data.split(" ")[1]
	            var pin_status = e.data.split(" ")[2]
	            
	            // select checkbox pertaining to gpiopin and toggle
	            var elms = addressdiv.getElementsByTagName('input')
				
				
				for (var i = 0; i < elms.length; i++) {
					if (elms[i].name === pin_number){
						var pin_switch = elms[i]
					}
				}
				
	            if (pin_status === "0") {
	                pin_switch.checked = true
	            } else if (pin_status === "1") {
	                pin_switch.checked = false
	            }
	        }
	    
	}
	
	s.onclose = function(e) {
	    console.log("Connection closed.");
		Materialize.toast("Connection to " + s.url + " closed.", 5000)
	}
}



// get status of each switch's gpiopin
// var get_switch_stats = function () {
//     var boxes = document.getElementsByTagName('input');
//     for (var x = 0; x < boxes.length; x++) {
//         socket.send("PIN=" + boxes[x].name + ",IN,0")
//     }
// }

var get_switch_stats = function () {
	addresses = document.getElementsByClassName('address')

    for (var x = 0; x < addresses.length; x++) {
        
		var boxes = addresses[x].getElementsByTagName('input')
		var sock = sockets[addresses[x].id]
		
		get_switch_stats_ofaddr(boxes, sock)
    }
}


var get_switch_stats_ofaddr = function (boxes, sock) {
	for (var x = 0; x < boxes.length; x++) {
		sock.send("PIN=" + boxes[x].name + ",IN,0")
	}
}


// get status at an interval
window.setInterval(function () {
    get_switch_stats()
}, 10000);


// send command to ws server to toggle gpio pin when switch is clicked
var switch_onclick = function(box) {
    var sock_addr = box.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id
	var sock = sockets[sock_addr]
	
	if (sock.readyState != 1) {
        Materialize.toast("Not connected to WebSocket server", 5000)
    }
    if (box.checked === true) {
        sock.send('PIN=' + box.name + ',OUT,0')
    } else if (box.checked === false) {
        sock.send('PIN=' + box.name + ',OUT,1')
    }
}


// start


window.onload = function() {
    sockets = {}

	
	addresses = document.getElementsByClassName('address')
	
	for (var x = 0; x < addresses.length ; x++) {
		var sock_addr = addresses[x].id
		
		if (sock_addr === "self") {
			
			var hostname = window.location.hostname
			var wsport = document.getElementById("wsport").content
			var sock = new WebSocket("ws://" + hostname + ":" + wsport);
			create(sock, true)
			
			sockets['self'] = sock
		}
		
		else {
			var sock = new WebSocket(sock_addr)
			create(sock, false)
			sockets[sock.url] = sock
		}
	}
};



