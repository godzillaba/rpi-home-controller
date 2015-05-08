var socket = null;
var isopen = false;

var get_json_data = function() {
    socket.send("GETJSON")
}

var send_json_data = function() {
    json.HTTP.port = document.getElementById("HTTP_Port").value
    json.WebSocket.port = document.getElementById("WebSocket_Port").value
    json.TCP.port = document.getElementById("TCP_Port").value

    json.Web.UI.NavColor = document.getElementById("NavColor").value
    json.Web.UI.BodyColor = document.getElementById("BodyColor").value
    json.Web.UI.ChromeHeaderColor = document.getElementById("ChromeHeaderColor").value

    json.Web.UI.LabelColor = document.getElementById("LabelColor").value
    json.Web.UI.WaveType = document.getElementById("WaveType").value
    json.Web.UI.CardColor = document.getElementById("CardColor").value

    json.Web.UI.SwitchKnobColorOff = document.getElementById("SwitchKnobColorOff").value
    json.Web.UI.SwitchKnobColorOn = document.getElementById("SwitchKnobColorOn").value
    json.Web.UI.SwitchBGColorOff = document.getElementById("SwitchBGColorOff").value
    json.Web.UI.SwitchBGColorOn = document.getElementById("SwitchBGColorOn").value

    json.Web.UI.SettingsFontColor = document.getElementById("SettingsFontColor").value
    json.Web.UI.FontWeight = document.getElementById("FontWeight").value

    json.Web.UI.DropDownColor = document.getElementById("DropDownColor").value
    json.Web.UI.DropDownText = document.getElementById("DropDownText").value


    var addressdivs = document.getElementsByClassName('address_group')
    var GroupInputs = document.getElementById('GroupsForm').getElementsByClassName('switchgroupdata')
    json.Web.Groups = []

    for (var x = 0; x < addressdivs.length; x++) {

        var addr = addressdivs[x].getElementsByClassName('addr')[0].value
        console.log(addr)


        var addr_groups = addressdivs[x].getElementsByClassName('switchgroupdata')

        if (addr_groups.length > 0 && addr) {
            json.Web.Groups[x] = []
            json["Web"]["Groups"][x].push(addr)

            console.log(addr_groups)

            for (var i = 0; i < addr_groups.length; i++) {
                var d = addr_groups[i]
                console.log(d)
                var inputs = d.getElementsByTagName("input")
                var desc = inputs[0].value
                var gpin = inputs[1].value
                if (desc && gpin) {
                    json["Web"]["Groups"][x].push({
                        "description": desc,
                        "gpiopin": gpin
                    })
                }
            }
        }
    }



    console.log(json)

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