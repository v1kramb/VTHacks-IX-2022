const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server, Socket } = require("socket.io");
const io = new Server(server);

app.use(express.static(__dirname + '/public_html'))

// const fs = require("fs");

io.on('connection', socket => {

});