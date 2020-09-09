var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var spawn = require('child_process').spawn;
app.use(express.static(__dirname + '/public'));

io.on('connection', function(socket){
  console.log('Socket.io connected');
  var  py    = spawn('python',['-u', 'test.py']);
  socket.on('pohyb', function(data) {
    //console.log(data);
    py.stdin.write(data+"\n");
  });
  py.stdout.on('data', function (data) {
        console.log('stdout: ' + data);
  });
});

app.get('/', function(req, res) {
  res.sendfile('horizon.html');
});

imu = spawn('python',['imu.py']);

imu.stdout.on('data', function (data) {
        //console.log('stdout: ' + data);
	io.emit('data', data);
});

http.listen(8090, function(){
  console.log('Listening');
});
