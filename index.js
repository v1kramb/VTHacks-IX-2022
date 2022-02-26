const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server, Socket } = require("socket.io");
const io = new Server(server);

app.use(express.static(__dirname + '/public_html'))

const fs = require("fs");

const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["path/to/script.py", arg1, arg2, ...]);

io.on('connection', socket => {
    console.log(socket.id + " connected");
    socket.on('process-video', file => { 
        console.log(file);
        fs.writeFile('./toprocess.mp4', file, err => {
            if (err) {
                console.error(err);
                return;
            }
            // file written
        });
    })
});

let port = process.env.PORT || 80;
server.listen(process.env.PORT || 80, () => {
    console.log("listening on *:" + port);
})