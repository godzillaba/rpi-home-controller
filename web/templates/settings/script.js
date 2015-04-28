var socket = null;
var isopen = false;

var get_json_data = function () {
	socket.send("GETJSON")
}

var send_json_data = function () {
	json.HTTP.port = document.getElementById("HTTP_Port").value
	json.WebSocket.port = document.getElementById("WebSocket_Port").value
	json.TCP.port = document.getElementById("TCP_Port").value
	
	json.Web.UI.NavColor = document.getElementById("NavColor").value
	json.Web.UI.BodyColor = document.getElementById("BodyColor").value
	json.Web.UI.ChromeHeaderColor = document.getElementById("ChromeHeaderColor").value
	
	json.Web.UI.SwitchKnobColorOff = document.getElementById("SwitchKnobColorOff").value
	json.Web.UI.SwitchKnobColorOn = document.getElementById("SwitchKnobColorOn").value
	json.Web.UI.SwitchBGColorOff = document.getElementById("SwitchBGColorOff").value
	json.Web.UI.SwitchBGColorOn = document.getElementById("SwitchBGColorOn").value
	
	var GroupInputs = document.getElementById('GroupsForm').getElementsByClassName('switchgroupdata')
	
	
	
	json.Web.Groups = []
	
	for (var i=0; i<GroupInputs.length; i++) {
	    var d = GroupInputs[i]
		console.log(d)
		var inputs = d.getElementsByTagName("input")
		var desc = inputs[0].value
		var gpin = inputs[1].value
		if (desc && gpin){
			json["Web"]["Groups"].push({"description":desc, "gpiopin":gpin})
		}
	}
		
	
	jsonstring = JSON.stringify(json)
	console.log(jsonstring)
	socket.send("SAVEJSON=" + jsonstring)
	Materialize.toast("Sent JSON data", 3000)

}

window.onload = function() {
    hostname = window.location.hostname
	var wsport = document.getElementById("wsport").content
    
	socket = new WebSocket("ws://" + hostname + ":" + wsport);
    socket.binaryType = "arraybuffer";

    socket.onopen = function() {
	    console.log("Connected!");
        isopen = true;
		Materialize.toast("Connected to ws://" + hostname + ":" + wsport, 3000)
		get_json_data()
    }

    socket.onmessage = function(e) {
        if (typeof e.data == "string") {
            console.log("Message received: " + e.data);
            
			if (e.data.split("----------")[0] === "JSON") {
				data = e.data.split("----------")[1];
				json = JSON.parse(data)
				console.log(json)
				Materialize.toast("Received JSON data", 3000)
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
