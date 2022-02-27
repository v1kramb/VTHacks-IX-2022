
let socket = io();

const inputVideo = $("#video-input");

const videoPlayer = $("#video-player");
videoPlayer.get(0).play();

inputVideo.on('change', () => {
    $("#comment-section").css("display", "none");
    let files = inputVideo.prop('files');
    console.log("Uploaded a video");
    readURL(files);
});

let submittedFile = null;

function readURL(files) {
    if (files && files[0]) {
        var file = files[0];
        console.log(file);
        var url = URL.createObjectURL(file);
        
        var reader = new FileReader();
        reader.onload = function() {
            videoPlayer.attr("src", url);
            videoPlayer.attr("loop", true);
            videoPlayer.get(0).play();
        }
        submittedFile = file;
        reader.readAsDataURL(file);
        $("#submit").attr("disabled", false);
    }
}

function analyze() {
    if (submittedFile != null) {
        // send data to the server.
        // console.log(submittedFile);
        $("#loading-section").css("display", "block");
        const process = $("#exercise-select").val();
        console.log("Sending video to server to process as " + process);
        socket.emit("process-video", {file: submittedFile, process: process});
    }
}

socket.on('receive-video', data => {
    // now fetch the video from the stored database on the server
    $("#loading-section").css("display", "none");
    console.log(data);
    if (data[data.length - 1] == "") {
        data = data.slice(0, -1);
    }
    data = data.slice(0, -1); // remove 'all done'
    let display = "";
    if (data.length == 0) {
        display = "<span style='color: green; font-weight: bold; font-size: 1.4em'> Good form! </span><br>";
    }
    else {
        display = "<span style='color: rgb(232, 186, 0); font-weight: bold; font-size: 1.4em'> Check form! </span><br>"
    }
    for (let i = 0; i < data.length; i++) {
        display += data[i];
        if (i < data.length - 1) {
            display += "<br>"
        }
    }
    $("#comments").html(display);
    $("#comment-section").css("display", "block");
    fetch('/video')
    .then(data =>  {
        data.blob().then((file) => {
            file = new File([file], 'blah.mp4', {type: 'video/mp4'});
            var url = URL.createObjectURL(file);
        
            var reader = new FileReader();
            reader.onload = function() {
                videoPlayer.attr("src", url);
                videoPlayer.attr("loop", true);
                videoPlayer.get(0).play();
            }
            
            reader.readAsDataURL(file);
        });
    });

    $("#submit").attr("disabled", true);
})