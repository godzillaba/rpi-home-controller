function create(s, addr_self) {

    s.binaryType = "arraybuffer";
    
    s.onopen = function() {
        console.log("Connected!");
        Materialize.toast("Connected to " + s.url, 3000)
        
		
        
        if (s.url === sockets['self'].url) {
            query_object = {
                "MessageType": "Query",
                "Query": "People"
            }
            
            sockets['self'].send(JSON.stringify(query_object))
            
            query_object.Query = "Config"
            
            sockets['self'].send(JSON.stringify(query_object))    
        }

        get_switch_stats()
    }
    

    s.onmessage = function(e) {
        console.log("[" + s.url + "] Received: " + e.data);

        if (addr_self) {
            var addressdiv = document.getElementById('self')
        } else {
            var addressdiv = document.getElementById(s.url)
        }


        // parse received data
        recvd_data = JSON.parse(e.data)
        
        if (recvd_data.MessageType === "QueryReply") {
            
            if (recvd_data.Query === "pin_out") {
                
                var pin_number = recvd_data.pin_number
                var value = recvd_data.value
                
                // elms = all inputs of a certain address
                var elms = addressdiv.getElementsByTagName('input')

                // select input based on pin number
                for (var i = 0; i < elms.length; i++) {
                    if (elms[i].name == pin_number) {
                        var pin_switch = elms[i]
                    }
                }
                                
                pin_switch.checked = !(Boolean(value)) 
            }
            else if (recvd_data.Query === "Config") {
                
                json = recvd_data.ConfigData
                console.log(json)
                Materialize.toast("Received JSON data", 3000)
                
                
            }
            else if (recvd_data.Query === "People") {
                people_array = recvd_data.People

                for (var x = 0; x < people_array.length; x++) {
                    var person_name = people_array[x].name
                    
                    var person_status = people_array[x].online
         
                    var indicator = document.getElementById(person_name + "_io")
         
                    if (person_status) {
                        indicator.innerHTML = "online"
                    }
                    else {
                        indicator.innerHTML = "offline"
                    }
                }

            }
            
            
        }
        
//        if (e.data.split(" ")[0] === "PIN") {
//            var pin_number = e.data.split(" ")[1]
//            var pin_status = e.data.split(" ")[2]
//
//            // select checkbox pertaining to gpiopin and toggle
//            var elms = addressdiv.getElementsByTagName('input')
//
//
//            for (var i = 0; i < elms.length; i++) {
//                if (elms[i].name === pin_number) {
//                    var pin_switch = elms[i]
//                }
//            }
//
//            if (pin_status === "0") {
//                pin_switch.checked = true
//            } else if (pin_status === "1") {
//                pin_switch.checked = false
//            }
//        }
//		else if (e.data.split(" ")[0] === "PERSON") {
//			var person_name = e.data.split(",")[1]
//			var person_status = e.data.split(",")[2]
//			
//			var indicator = document.getElementById(person_name + "_io")
//			
//			indicator.innerHTML = person_status
//		}
//
//        if (e.data.split("----------")[0] === "JSON") {
//            data = e.data.split("----------")[1];
//            json = JSON.parse(data)
//            console.log(json)
//            Materialize.toast("Received JSON data", 3000)
//        }
        

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

var get_switch_stats = function() {
    addresses = document.getElementsByClassName('address')

    for (var x = 0; x < addresses.length; x++) {

        var boxes = addresses[x].getElementsByTagName('input')
        var sock = sockets[addresses[x].id]

        get_switch_stats_ofaddr(boxes, sock)
    }
}


var get_switch_stats_ofaddr = function(boxes, sock) {
    for (var x = 0; x < boxes.length; x++) {

//        sock.send("PIN=" + boxes[x].name + ",IN,0")
        var pnumber = boxes[x].name
        
        var query_object = {
            "MessageType": "Query",
            "Query": "pin_out",
            "pin_number": pnumber
        }
        
        var query_string = JSON.stringify(query_object)
        
        sock.send(query_string)
        
    }
}

var get_people_stats = function() {
    query_object = {
        "MessageType": "Query",
        "Query": "People"
    }
            
    sockets['self'].send(JSON.stringify(query_object))
}

var get_stats = function() {
    get_people_stats()
    get_switch_stats()
}

// get status at an interval
window.setInterval(function() {
    get_stats()
    
}, 10000);


// send command to ws server to toggle gpio pin when switch is clicked
var switch_onclick = function(box) {
    var sock_addr = box.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id
    var sock = sockets[sock_addr]

    if (sock.readyState != 1) {
        Materialize.toast("Not connected to WebSocket server", 5000)
    }
    
    ////////// new stuff
    
    var pnumber = box.name
    var pvalue = ( + !(box.checked) )
    
    command_object = {
        "MessageType": "Command",
        "Command": "pin_out",
        "pin_number": pnumber,
        "value": pvalue
    }
    
    command_string = JSON.stringify(command_object)
    
    sock.send(command_string)
    
}


// start


window.onload = function() {
    sockets = {}


    addresses = document.getElementsByClassName('address')

    for (var x = 0; x < addresses.length; x++) {
        var sock_addr = addresses[x].id

        if (sock_addr === "self") {

            var hostname = window.location.hostname
            var wsport = document.getElementById("wsport").content
            var sock = new WebSocket("ws://" + hostname + ":" + wsport);
            create(sock, true)

            sockets['self'] = sock
                        
        } else {
            var sock = new WebSocket(sock_addr)
            create(sock, false)
            sockets[sock.url] = sock
        }
    }
//    settings_onload()
	
};





////////////// settings js //////////////

var socket = null;
var isopen = false;

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

    config_object = {
        "MessageType": "Command",
        "Command": "SaveConfig",
        "ConfigData": json
    }
    
    
    jsonstring = JSON.stringify(config_object)
    console.log(jsonstring)
    sockets['self'].send(jsonstring)
    Materialize.toast("Sent JSON data", 3000)

}



//////////// nav stuff ////////////

hide = function (id) {
    document.getElementById(id).style.display = 'none';
}
show = function (id) {
    document.getElementById(id).style.display = 'block';
}

hideforms = function() {
    subforms = document.getElementsByClassName('subform')
    
    for (var x = 0; x < subforms.length; x++) {
        subforms[x].style.display = 'none'
    }
}

nav_deactivate_link = function (id) {
    document.getElementById(id).className =
    document.getElementById(id).className.replace(/\bactive\b/,'');
}

nav_activate_link = function (id) {
    document.getElementById(id).className += " active"
}

nav_activate = function (id) {
    nav_deactivate_link('topnav_home')
    nav_deactivate_link('topnav_settings')
    
    nav_activate_link(id)
}