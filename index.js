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
    
    const url = "toprocess.mp4"
    const rs = fs.createReadStream(url);    
    const { size } = fs.statSync(url);

    res.setHeader("Content-Type", "video/mp4");
    res.setHeader("Content-Length", size);

    rs.pipe(res);
});
// app.get('/video', function (req, res) {

//     const path = 'toprocess.mp4';

//     var stat = fs.statSync(path);
//     var total = stat.size;
  
//     if (req.headers.range) {
  
//       // meaning client (browser) has moved the forward/back slider
//       // which has sent this request back to this server logic ... cool
  
//       var range = req.headers.range;
//       var parts = range.replace(/bytes=/, "").split("-");
//       var partialstart = parts[0];
//       var partialend = parts[1];
  
//       var start = parseInt(partialstart, 10);
//       var end = partialend ? parseInt(partialend, 10) : total-1;
//       var chunksize = (end-start)+1;
//       console.log('RANGE: ' + start + ' - ' + end + ' = ' + chunksize);
  
//       var file = fs.createReadStream(path, {start: start, end: end});
//       res.writeHead(206, { 'Content-Range': 'bytes ' + start + '-' + end + '/' + total, 'Accept-Ranges': 'bytes', 'Content-Length': chunksize, 'Content-Type': 'video/mp4' });
//       file.pipe(res);
  
//     } else {
  
//       console.log('ALL: ' + total);
//       res.writeHead(200, { 'Content-Length': total, 'Content-Type': 'video/mp4' });
//       fs.createReadStream(path).pipe(res);
//     }
//   }
// );

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
                io.to(socket.id).emit('receive-video', "Knowledge");
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