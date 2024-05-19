import React from 'react';
import Guacamole from 'guacamole-common-js';
import crypto from "crypto";
import { Buffer } from 'buffer';
import './App.css';

const CIPHER = 'aes-256-cbc';
const KEY = 'x9h9Ab3Bhz0LTleMygDVQQvkqWocr5EV';



function encryptToken(value) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(CIPHER, Buffer.from(KEY), iv);

  let encrypted = cipher.update(JSON.stringify(value), 'utf8', 'base64');
  encrypted += cipher.final('base64');

  const data = {
    iv: iv.toString('base64'),
    value: encrypted
  };

  const json = JSON.stringify(data);
  return Buffer.from(json).toString('base64');
}


const GuacamoleApp = () => {
  var guac_backend_host = process.env.REACT_APP_GUAC_BACKEND_HOSTNAME;
  var win_server_host = process.env.REACT_APP_WIN_SERVER_HOSTNAME;

  const handleSelectSSH = (event) => {
    document.getElementById("port").value = "50022";
    document.getElementById("ssh").checked = true;
  }

  const handleSelectRDP = (event) => {
    document.getElementById("port").value = "3389";
    document.getElementById("rdp").checked = true;
  }

  const handleSelectVNC = (event) => {
    document.getElementById("port").value = "5900";
    document.getElementById("vnc").checked = true;
  }

  const openGc = async () => {
    window.Buffer = Buffer;
    try {
      var ele = document.getElementsByTagName('input');
      var protocol_type = "";
      var port = document.getElementById("port").value;
      for (var i = 0; i < ele.length; i++) {
        if (ele[i].type === "radio") {
          if (ele[i].checked)
            protocol_type = ele[i].value;
        }
      }
      const tokenObject = {
        connection: {
          type: protocol_type,
          settings: {
            "hostname": win_server_host,
            "username": "Administrator",
            "port": port,
            "password": "vagrant",
            "security": "any",
            "ignore-cert": true,
            "enable-wallpaper": true
          }
        }
      };

      const token = encryptToken(tokenObject);
      var wsurl = guac_backend_host;

      

      console.log(wsurl);
      const gc = await new Guacamole.Client(new Guacamole.WebSocketTunnel(wsurl));
      const display = document.getElementById('gcdisplay');
      const element = gc.getDisplay().getElement();

      if (display) {
        display?.appendChild(element);
      }

      gc.connect(`token=${token}&height=800&width=` + document.getElementById("gcdisplay").offsetWidth.toString());

      // Error handler
      gc.onerror = (error) => console.log(error.message);
      window.onunload = () => gc.disconnect();

      // Mouse
      const mouse = new Guacamole.Mouse(gc.getDisplay().getElement());


      // Forward all mouse interaction over Guacamole connection
      mouse.onEach(['mousedown', 'mousemove', 'mouseup'], function sendMouseEvent(e) {
        gc.sendMouseState(e.state, true);
      });


      // Hide software cursor when mouse leaves display
      mouse.on('mouseout', function hideCursor() {
        gc.getDisplay().showCursor(false);
      });
      const keyboard = new Guacamole.Keyboard(document);
      keyboard.onkeydown = (keysym) => gc.sendKeyEvent(1, keysym);
      keyboard.onkeyup = (keysym) => gc.sendKeyEvent(0, keysym);

    } catch (error) {
      console.log("GC Error", error);
    }
  }
  return <div style={{ width: '100%' }}>
    <h1>Guacamole Connect RDP/SSH/VNC</h1>
    <fieldset width="100px">
      <legend>Select your connection method</legend>

      <div>
        <input type="radio" id="ssh" name="connection_type" value="ssh" onChange={handleSelectSSH} />
        <label htmlFor="SSH">SSH</label>
      </div>

      <div>
        <input type="radio" id="rdp" name="connection_type" value="rdp" onChange={handleSelectRDP} />
        <label htmlFor="RDP">RDP</label>
      </div>

      <div>
        <input type="radio" id="vnc" name="connection_type" value="vnc" onChange={handleSelectVNC} />
        <label htmlFor="VNC">VNC</label>
      </div>

    </fieldset>
    <div>
      Port:
      <input type="text" id="port" name="port" defaultValue="3389" />
    </div>
    <br></br>
    <button onClick={openGc}>Open Guacamole</button>
    <br />
    <div className="box">
      <div id='gcdisplay' className="content"><p>content</p></div>
    </div>
  </div>
}
export default GuacamoleApp;

