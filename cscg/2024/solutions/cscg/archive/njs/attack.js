var request = require('request');
var url ='https://requestbin.kanbanbox.com/1j1csvk1'
request(url, function (error, response, body) {
  if (!error) {
    console.log(body);
  }
});
