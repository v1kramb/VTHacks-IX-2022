const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server, Socket } = require("socket.io");
const io = new Server(server);

app.use(express.static(__dirname + '/public_html'))

const fs = require("fs");

const spawn = require("child_process").spawn;

io.on('connection', socket => {
    console.log(socket.id + " connected");
    socket.on('process-video', file => { 
        console.log(file);
        fs.writeFile('./toprocess.mp4', file, err => {
            if (err) {
                console.error(err);
                return;
            }
            console.log("Wrote MP4 from client.")
            console.log("Proceeding with processing...")
            // file written, now process it
            const pythonProcess = spawn('python',["exercise_classifier/pushup_classifier.py", './toprocess.mp4']);
            pythonProcess.stdout.on('data', (data) => {
                // this let's us know the python script has terminated!
                console.log(data);
                console.log('Completed processing')
                fs.readFile('./output/pushup.mp4', 'hex', (err, data) => {
                    if (err) {
                        console.log(err); 
                        return;
                    }
                    // now send that data back to the client
                    console.log("Reading from python output")
                    console.log("Sending back to client");
                    io.to(socket.id).emit('receive-video', Buffer.from(data, 'hex'));
                });
            });
        });
    })
});

let port = process.env.PORT || 80;
server.listen(process.env.PORT || 80, () => {
    console.log("listening on *:" + port);
})