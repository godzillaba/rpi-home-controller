var net = require('net');

var HOST = '127.0.0.1';
var PORT = 5432;

var tcp = new net.Socket();


var WebSocketServer = require('ws').Server
  , wss = new WebSocketServer({port: 8080});
wss.on('connection', function(ws) {
    
    ws.on('message', function(message) {
        console.log('received: %s', message);
        tcp.connect(PORT, HOST, function() {

    		console.log('CONNECTED TO: ' + HOST + ':' + PORT);
    		// Write a message to the socket as soon as the client is connected, the server will receive it as message from the client 
    		tcp.write(message);
			tcp.on('data', function(data) {
			    
			    console.log('DATA: ' + data);
			    ws.send('' + data)
			    // Close the client socket completely
			    
			});
		});
    });
    
});




	

// // Add a 'data' event handler for the client socket
// // data is what the server sent to this socket
// client.on('data', function(data) {
    
//     console.log('DATA: ' + data);
//     // Close the client socket completely
//     client.destroy();
    
// });

// // Add a 'close' event handler for the client socket
// client.on('close', function() {
//     console.log('Connection closed');
// });