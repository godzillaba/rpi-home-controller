function create(s) {

    s.binaryType = "arraybuffer";
    
    s.sendMessage = function(string) {
        
        if (sock.readyState != 1) {
            
            // errmsg = "Not connected to WebSocket server. readyState: " + sock.readyState
            // Materialize.toast(errmsg, 5000)
            // console.log(errmsg)
            alert_closed()

        } else {
            
            s.send(string)
            console.log("[" + s.url + "] Sent: " + string)

        }

        
    }

    s.onopen = function() {
        console.log("Connected!");
        Materialize.toast("Connected to " + s.url, 3000)

        get_stats()
        get_config()

        // $('#main_section').show()
    }
    

    s.onmessage = function(e) {
        console.log("[" + s.url + "] Received: " + e.data);

        // if (addr_self) {
        //     var addressdiv = document.getElementById('self')
        // } else {
        //     var addressdiv = document.getElementById(s.url)
        // }


        // parse received data
        recvd_data = JSON.parse(e.data)
        
        if (recvd_data.MessageType === "QueryReply") {
            
            if (recvd_data.Query === "pin_out") {
                
                var pin_number = recvd_data.pin_number
                var value = recvd_data.value
                
                var addressdiv = document.getElementById(recvd_data.Sender)
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
                    var indicator2= document.getElementById(person_name + "_io2")

                    var last_seen_span = document.getElementById(people_array[x].hostname + '_lastseen')

                    last_seen_span.innerHTML = people_array[x].last_seen

                    if (person_status) {
                        indicator.innerHTML = "online"
                        indicator2.innerHTML = "true"
                    }
                    else {
                        indicator.innerHTML = "offline"
                        indicator2.innerHTML= "false"
                    }
                }

            }
            else if (recvd_data.Query === "ThermostatData") {
                
                actual_temp_p = document.getElementById("actual_temp_" + recvd_data.Sender)

                target_temp_p = document.getElementById("target_temp_" + recvd_data.Sender)

                actual_temp_p.innerHTML = recvd_data.Data.actual_temp
                target_temp_p.innerHTML = recvd_data.Data.target_temp

                document.getElementById("fan_"+recvd_data.Data.fan+"_"+recvd_data.Sender).checked = true

                document.getElementById("compressor_"+recvd_data.Data.system+"_"+recvd_data.Sender).checked = true


            }
            else if (recvd_data.Query === "Log") {
                console.log("received log data")
                logarray = recvd_data.Data

                $("#log p").remove();

                logobj = $("#log")

                for (var x = 0; x < logarray.length; x++) {
                    loglvl = get_loglevel(logarray[x])

                    logobj.append("<p class='logentry " + loglvl + "'>" + logarray[x] + "</p>")
                }

                filterchange()
            }
            
            
        } else if (recvd_data.MessageType === "ErrorMessage") {
            Materialize.toast(recvd_data.Error, 5000)
        }
    }

    s.onclose = function(e) {
        console.log("Connection closed.");
        // Materialize.toast("<span>Connection to " + s.url + " closed.<a href='#!' class='btn-flat red-text' onclick='window.onload()'><i class='material-icons'>refresh</i></a></span>")
        alert_closed()
    }
}

alert_closed = function () {
    $("#sock-readyState").html(sock.readyState)
    $("#connection_closed_modal").openModal()
}

var get_config = function () {
    obj = {
        "Sender": "WebClient",
        "DestinationAddress": "self",
        "MessageType": "Query",
        "Query": "Config"
    }

    sock.sendMessage(JSON.stringify(obj))

}

var get_switch_stats = function() {
    addresses = document.getElementsByClassName('address')

    for (var x = 0; x < addresses.length; x++) {

        var boxes = addresses[x].getElementsByTagName('input')
        // var sock = sockets[addresses[x].id]
        var addr = addresses[x].id

        get_switch_stats_ofaddr(boxes, addr)
    }
}


var get_switch_stats_ofaddr = function(boxes, addr) {
    // var sock = sockets['self']
    for (var x = 0; x < boxes.length; x++) {

        var pnumber = boxes[x].name
        
        var query_object = {
            "Sender": "WebClient",
            "DestinationAddress": addr,
            "MessageType": "Query",
            "Query": "pin_out",
            "pin_number": pnumber
        }
        
        var query_string = JSON.stringify(query_object)
        
        sock.sendMessage(query_string)
        
    }
}

var get_people_stats = function() {
    query_object = {
        "Sender": "WebClient",
        "DestinationAddress": "self",
        "MessageType": "Query",
        "Query": "People"
    }
            
    sock.sendMessage(JSON.stringify(query_object))
}

get_log = function () {
    query_object = {
        "Sender": "WebClient",
        "DestinationAddress": "self",
        "MessageType": "Query",
        "Query": "Log"
    }
    sock.sendMessage(JSON.stringify(query_object))
}

var get_stats = function() {
    get_people_stats()
    get_switch_stats()
    get_hvac_data()
}

// get status at an interval
window.setInterval(function() {
    if (sock.readyState == 1) {
        get_stats()
    }
    else {
        console.log("readyState != 1 setInterval doing nothing.")
    }

}, 30000);


// send command to ws server to toggle gpio pin when switch is clicked
var switch_onclick = function(box) {
    var sock_addr = box.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id
    
    // var sock = sockets[sock_addr]
    
    // var sock = sockets['self']

    
    ////////// new stuff
    
    var pnumber = box.name
    var pvalue = ( + !(box.checked) )
    
    command_object = {
        "Sender": "WebClient",
        "DestinationAddress": sock_addr,
        "MessageType": "Command",
        "Command": "pin_out",
        "pin_number": pnumber,
        "value": pvalue
    }
    
    command_string = JSON.stringify(command_object)
    
    sock.sendMessage(command_string)
    
}


// start


window.onload = function() {


    var hostname = window.location.hostname
    var wsport = document.getElementById("wsport").content
    sock = new WebSocket("ws://" + hostname + ":" + wsport);
    create(sock)

    $("#address_in_modal").html("ws://" + hostname + ":" + wsport)

};





////////////// settings js //////////////

var socket = null;
var isopen = false;

var send_json_data = function() {
    
    // Network
    json.HTTP.port = document.getElementById("HTTP_Port").value
    json.WebSocket.port = document.getElementById("WebSocket_Port").value
    json.TCP.port = document.getElementById("TCP_Port").value

    // UI
    $("#UIForm input[type='text']").each( function () {
        json.Web.UI[this.id] = this.value
    })

    // People
    json.Web.People = []
    peeps = json.Web.People
    
    $("#PeopleForm div.row.person").each( function () {
        
        name = $(this).find('#name').val()
        hostname = $(this).find('#hostname').val()

        if (name && hostname) {
            
            person_object = {
                "name": name,
                "hostname": hostname
            }
            peeps.push(person_object)

        }

    })

    // Groups
    var addressdivs = document.getElementsByClassName('address_group')

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


    // Get ready to send
    config_object = {
        "Sender": "WebClient",
        "DestinationAddress": "self",
        "MessageType": "Command",
        "Command": "SaveConfig",
        "ConfigData": json
    }
    
    
    jsonstring = JSON.stringify(config_object)
    console.log(json)
    sock.sendMessage(jsonstring)
    Materialize.toast("Sent JSON data", 3000)

}



//////////// hvac ////////////

// target_temp_span = document.getElementById("target_temp")
// actual_temp_span = document.getElementById("actual_temp")
// fan_span = document.getElementById("fan")
// system_span = document.getElementById("system")

var get_hvac_data = function () {
    
    thermostats = document.getElementsByClassName("thermostat")

    for (var x = 0; x < thermostats.length; x++) {
        console.log(thermostats[x].id)
        query_object = {
            "Sender": "WebClient",
            "DestinationAddress": thermostats[x].id.split("_")[0],
            "MessageType": "Query",
            "Query": "ThermostatData"
        }

        sock.sendMessage(JSON.stringify(query_object))
    }
}

var send_hvac_data = function (thermostat_addr) {
    command_object = {
        "Sender": "WebClient",
        "DestinationAddress": thermostat_addr,
        "MessageType": "Command",
        "Command": "TempConfig",
        "target_temp": (document.getElementById("target_temp_" + thermostat_addr)).innerHTML,
        "fan": $("input[type='radio'][name='fan_"+ thermostat_addr +"']:checked")[0].getAttribute('data-jsonval'),
        "system": $("input[type='radio'][name='compressor_"+ thermostat_addr +"']:checked")[0].getAttribute('data-jsonval')
    }

    console.log(command_object)

    sock.sendMessage(JSON.stringify(command_object))
}

var lower_target = function (thermostat_addr) {

    target_temp_elm = document.getElementById("target_temp_" + thermostat_addr)
    current_target = parseInt(target_temp_elm.innerHTML)
    new_target = current_target - 1
    target_temp_elm.innerHTML = new_target

    send_hvac_data(thermostat_addr)

}

var raise_target = function (thermostat_addr) {
    target_temp_elm = document.getElementById("target_temp_" + thermostat_addr)
    current_target = parseInt(target_temp_elm.innerHTML)
    new_target = current_target + 1
    target_temp_elm.innerHTML = new_target

    send_hvac_data(thermostat_addr)
}

//////////// nav stuff ////////////

nav_activate = function (id) {
    $('.topnavli').removeClass('active')
    $('#'+id).addClass('active')

    // nav_activate_link(id)
}

get_loglevel = function (str) {
    try {
        loglvl = str.split("]")[2].split("[")[1]
    } catch (err) {
        loglvl = "LVLundefined"
    }

    if (!(loglvl in levels)) {
        loglvl = "LVLundefined"
    }

    return loglvl
}

levels = {
    "DEBUG": 1,
    "INFO": 2,
    "WARNING": 3,
    "ERROR": 4,
    "CRITICAL": 5,
    "LVLundefined": 6
}

filterchange = function () {
    filterstr = $("#filter").val()

    if (filterstr == "") {
        $("#log p").each(function () {
            $(this).show()
        })
    }


    else {
        $("#log p").each(function () {
            if ( $(this).html().indexOf(filterstr) < 0 ) {
                $(this).hide()
            } else {
                $(this).show()
            }
        })
    }

    minlevel = $("#loglevelfilter").val()

    for (var key in levels) {
        if (levels[key] < minlevel){
            $("."+key).hide()
        }
    }

    $("#logcard")[0].scrollTop = $("#logcard")[0].scrollHeight;
}
$(document).ready( function () {
    $("#refresh_logs").click(function() {
        
        w = $(this).width() + 60

        $(this).css("width", w)
        $(this).children().hide()

        $(this).parent().children().animate({
            height: 0,
            width: 0,
        }, 50);



        window.setTimeout(function() {
            $("#refresh_logs").hide().parent().removeClass("valign-wrapper")
        }, 600);


        get_log(); 
        window.setInterval(function(){get_log()}, 30000)

    })
})

$(document).ready(function () {
    $("#topnav_dev, #sidenav_dev").on("click", function(){
        $('ul.tabs').tabs('select_tab', 'logdevsection');
    });
})
