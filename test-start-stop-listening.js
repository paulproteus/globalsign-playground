var http = require('http');

var howManySoFar = 0;

var app = http.createServer(function(req, res) {
  howManySoFar = howManySoFar + 1;
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('OK\n');

  if (howManySoFar > 3) {
    app.close();
    console.log('closed');
    howManySoFar = 0;
    console.log('reset the counter!');
  }
});

var x = app.listen(3000);

console.log(app.listen(3000));
