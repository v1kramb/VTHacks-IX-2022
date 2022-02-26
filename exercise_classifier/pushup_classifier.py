import cv2
import mediapipe as mp
import numpy as np
import pose_base as pm
import pose_landmarks as pl
from datetime import datetime
import os
import sys

# cap = cv2.VideoCapture(sys.argv[1])  # 0
cap = cv2.VideoCapture('short-pushup.mp4')

# Determine video attributes
fps = cap.get(cv2.CAP_PROP_FPS)
width  = cap.get(3)  # float `width`
height = cap.get(4)  # float `height`

# Set up output video writing
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# time_now = datetime.now()
# formatted_time = time_now.strftime("%m.%d.%Y_%H.%M.%S")
# out = cv2.VideoWriter(f"output/pushup_{formatted_time}.mp4", fourcc, int(fps), (int(width), int(height)))

path = os.path.join(os.path.dirname(__file__), "../output/")
# out = cv2.VideoWriter(path + "pushup_2.mp4", fourcc, int(fps), (int(width), int(height)))

detector = pm.PoseDetector()
landmarks = pl.PoseLandmark()
count = 0
direction = 0
form = 0
feedback = "Fix Form"

print("Count:", count)
curr_count = count

while cap.isOpened():
    ret, img = cap.read()

    if img is None:
        break

    img = cv2.flip(img, 1)  # selfie view
    
    img = detector.findPose(img, True)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(img, landmarks.LEFT_SHOULDER, landmarks.LEFT_ELBOW, landmarks.LEFT_WRIST)
        shoulder = detector.findAngle(img, 13, 11, 23)
        hip = detector.findAngle(img, 11, 23,25)
        
        #Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
        
        #Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1
    
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0

        if count > curr_count:
            print("Count:", count)
            curr_count = count        

        #Draw Bar
        # if form == 1:
        #     cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        #     cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
        #                 (255, 0, 0), 2)


        #Pushup counter
        # cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
        #             (255, 0, 0), 5)
        
        #Feedback 
        # cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        # cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
        #             (0, 255, 0), 2)

        
    cv2.imshow('Pushup counter', img)
    # out.write(img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
# out.release()
cv2.destroyAllWindows()

print("All done!")