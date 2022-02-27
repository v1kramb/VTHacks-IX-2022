
let socket = io();

const inputVideo = $("#video-input");

const videoPlayer = $("#video-player");
videoPlayer.get(0).play();

inputVideo.on('change', () => {
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
        
        console.log(url);
        
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
        console.log(submittedFile);
        socket.emit("process-video", submittedFile);
    }
}

fetch('/video')
    .then(data =>  {
        data.blob().then((file) => {
            file = new File([file], 'blah.mp4', {type: 'video/mp4'});
            // console.log(f);

            console.log(file);
            
            var url = URL.createObjectURL(file);
        
            console.log(url);

            var reader = new FileReader();
            reader.onload = function() {
                videoPlayer.attr("src", url);
                videoPlayer.attr("loop", true);
                videoPlayer.get(0).play();
            }
            
            console.log(url);
            reader.readAsDataURL(file);
        });
    });

socket.on('receive-video', data => {
    fetch('/video')
    .then(data =>  {
        data.blob().then((file) => {
            const f = new File([file], 'blah.mp4', {type: 'video/mp4'});

            console.log(file);
            
            var url = URL.createObjectURL(file);
        
            console.log(url);
            
            var reader = new FileReader();
            reader.onload = function() {
                videoPlayer.attr("src", url);
                videoPlayer.attr("loop", true);
                videoPlayer.get(0).play();
            }
            
            console.log(url);
            videoPlayer.get(0).crossorigin = 'anonymous'
            reader.readAsDataURL(file);
        });
    });

    $("#submit").attr("disabled", true);
})