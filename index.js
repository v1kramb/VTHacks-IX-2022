const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server, Socket } = require("socket.io");
const io = new Server(server);

app.use(express.static(__dirname + '/public_html'))

const fs = require("fs");

const spawn = require("child_process").spawn;

// app.put('/upload-video', (req, res) => {
//     console.log("uploaded something");
//     console.log(req);
//     req.
// });

app.get('/video', (req, res) => {
    const url = "output/output.mp4"
    const rs = fs.createReadStream(url);    
    const { size } = fs.statSync(url);

    res.setHeader("Content-Type", "video/mp4");
    res.setHeader("Content-Length", size);

    rs.pipe(res);
});

io.on('connection', socket => {
    console.log(socket.id + " connected");
    socket.on('process-video', data => {
        let file = data.file;
        let exercise = data.process; 
        console.log(file);
        fs.writeFile('./toprocess.mp4', file, err => {
            if (err) {
                console.error(err);
                return;
            }
            console.log("Wrote MP4 from client.")
            console.log("Proceeding with processing...")
            // file written, now process it
            const pythonProcess = spawn('python',["exercise_classifier/" + exercise + "_classifier.py", './toprocess.mp4']);
            pythonProcess.stdout.on('data', (data) => {
                // this let's us know the python script has terminated!
                const messages = data.toString().split("\n")
                console.log('Completed processing')
                io.to(socket.id).emit('receive-video', messages);
                // fs.readFile('./output/pushup.mp4', 'hex', (err, data) => {
                //     if (err) {
                //         console.log(err); 
                //         return;
                //     }
                //     // now send that data back to the client
                //     console.log("Reading from python output")
                //     console.log("Sending back to client");
                    
                //     // io.to(socket.id).emit('receive-video', Buffer.from(data, 'hex'));
                //     io.to(socket.id)
                // });
            });
        });
    });
});



let port = process.env.PORT || 80;
server.listen(process.env.PORT || 80, () => {
    console.log("listening on *:" + port);
})