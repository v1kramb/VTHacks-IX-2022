## Inspiration
A couple weeks ago, one of our team members strained their arm when they did an exercise incorrectly. It turns out that injuries like these are [far more common](https://askwonder.com/research/sports-pain-injury-statistics-6rxqus93o) than you’d expect. **8.6 million Americans are hurt annually by some form of physical activity.**<br><br>
Many of these injuries are [preventable]( https://opt.net.au/optimum-life/correct-technique-important/). A major reason for exercise-related injury is **improper exercise technique**.<br><br>
And especially during the pandemic era, when exercise is [critical]( https://medicine.umich.edu/dept/psychiatry/michigan-psychiatry-resources-covid-19/your-lifestyle/importance-physical-activity-exercise-during-covid-19-pandemic), isolation makes it challenging to evaluate your own exercise form. During Britain’s lockdown, around 7 million people had exercise-related injuries.<br><br>
We figured that an automated approach could work.

## What it does
FormFocus combines a web app with computer vision software. The web app allows users to upload videos of themselves doing an exercise. The app will analyze the video and automatically track your skeletal frame, no sensors needed.<br><br>
The app produces an annotated version of your video which will provide feedback on where you should be improving your exercises. It will highlight the body parts hindering your exercise and will slow down the video when you make a mistake. Currently, we have created classifiers for pushups and squats.

## How we built it
We utilize a Node.js Express web app to host the server, and use Socket.IO to communicate between the client and the server. The UI is designed with HTML/CSS and Bootstrap.<br><br>
After the user selects their exercise and uploads a video to the site locally, they'll click the "Analyze" button. This pushes the video data to the Node server, saves the file there locally.<br><br>
Then a Python script is executed based on the selected exercise. We use MediaPipe, a library which offers pose detection software, and have a class which will retrieve the angles between various joints in the body (e.g. knee, hip). The script makes heavy use of OpenCV. We read the video from the server and have custom logic to detect whether particular exercises are being performed, and if they're being performed correctly. For example, if you're doing a pushup and your arms don't reach 90 degrees or lower on the way down, the script will generate a critique and timestamp the point in the video when the user has made an error. The script generates an annotated video with a counter and the user's skeletal frame. It will also slow down the video and highlight the angles which need to be corrected, outputting an annotated video.<br><br>
The server now has the annotated video locally. Critiques from the Python script are sent to the client via Socket.IO. The client then makes an HTTP request for the annotated video from the server and streams it to the user. The user can now see the critiques as well as a judgment on whether their form is good or needs improvement.

## Challenges we ran into
- Determining the languages/platform to use. Our initial approach was to create a mobile app with Android Studio/Kotlin, making the frontend/backend locally. However, only one team member had experience with Kotlin. 
  - Our slow development prompted us to pivot to a web app, which we realized could be a more scalable solution for users who want to log their process over time.
  - We also realized that users could simply access the web app from their phone.
- Making an aesthetically pleasing UI. As a team, our frontend experience is quite limited, so a good portion of our time was spent researching user interface design fundamentals.
- We ran into a frustrating bug which took 3 hours to resolve. One line of code encoded the video incorrectly.

## Accomplishments that we're proud of
- Creating a clean pipeline; in particular, being able to integrate Node with the Python AI script.
- Creating a working application of computer vision in a hackathon.

## What's next for FormFocus
- Build classifiers for a wider range of exercises and subdivide them into the muscle groups they target (e.g. lats, biceps, shoulders, etc.).
- Implement live submission for the exercises in addition to the upload system.
- Incorporate risk-of-injury for different exercises and user attributes (age, weight, height, etc.).
- Create a recommendation system for workout plans based on your target goals, desired workout split, risk-of-injury, and past exercise performance.
- Create a mobile app which works in unison with the web app. The mobile app would support live exercise submission and the web app would be used to track past workouts/plan new ones.