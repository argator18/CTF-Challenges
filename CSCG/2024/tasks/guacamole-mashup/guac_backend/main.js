const GuacamoleLite = require('guacamole-lite');

const websocketOptions = {
    port: 8082 // WebSocket server port
};

var guacd_hostname = "";

if(process.env.SESSIONID) { 
    guacd_hostname = "localhost";
    console.log("Prod environment");
}
else {
    guacd_hostname = "guac-guacd";
    console.log("Local environment");
}
const guacdOptions = {
    host: guacd_hostname,
    port: 4822 // guacd server port
};

const clientOptions = {
    
    crypt: {
        cypher: 'AES-256-CBC',
        key: 'x9h9Ab3Bhz0LTleMygDVQQvkqWocr5EV'
    }
};

const guacServer = new GuacamoleLite(websocketOptions, guacdOptions, clientOptions);
guacServer.on('error', (clientConnection, error) => {
    console.error(`Error on connection ID: ${clientConnection.connectionId}`, error);
    // Additional error handling logic...
});