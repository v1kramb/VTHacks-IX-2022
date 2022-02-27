import cv2
import mediapipe as mp
import numpy as np
import pose_base as pm
import pose_landmarks as pl
from datetime import datetime
import os
import sys

def get_pos_sec():
    return cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

# cap = cv2.VideoCapture(sys.argv[1])  # 0
cap = cv2.VideoCapture('short-pushup.mp4')

# Determine video attributes
fps = cap.get(cv2.CAP_PROP_FPS)
width  = cap.get(3)  # float `width`
height = cap.get(4)  # float `height`

# Set up output video writing
fourcc = cv2.VideoWriter_fourcc(*'H264')

# time_now = datetime.now()
# formatted_time = time_now.strftime("%m.%d.%Y_%H.%M.%S")
# out = cv2.VideoWriter(f"output/pushup_{formatted_time}.mp4", fourcc, int(fps), (int(width), int(height)))

path = os.path.join(os.path.dirname(__file__), "../output/")
out = cv2.VideoWriter(path + "pushup.mp4", fourcc, int(fps), (int(width), int(height)))

detector = pm.PoseDetector()
landmarks = pl.PoseLandmark()
count = 0
direction = 0
form = 0

print("Count:", count)
curr_count = count

maxElbow = 0
minElbow = 180

elbowColor = (255,255,255)
shoulderColor = (255,255,255)
hipColor = (255,255,255)

backArchStarted = False

frameCount = 0
videoSpeed = 1
waitKeyVal = 10
delay = int(fps/2)

while cap.isOpened():
    ret, img = cap.read()

    if img is None:
        break

    img = cv2.flip(img, 1)  # selfie view
    
    img = detector.findPose(img, True)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        elbow = detector.findAngle(img, landmarks.LEFT_SHOULDER, landmarks.LEFT_ELBOW, landmarks.LEFT_WRIST, color=elbowColor)
        shoulder = detector.findAngle(img, landmarks.LEFT_ELBOW, landmarks.LEFT_SHOULDER, landmarks.LEFT_HIP, color=shoulderColor)
        hip = detector.findAngle(img, landmarks.LEFT_SHOULDER, landmarks.LEFT_HIP, landmarks.LEFT_KNEE, color=hipColor)

        # Make sure the form is correct
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1
    
        # Then we can start evaluating the pushup
        if form == 1:
            # Hip arched at any point is bad
            if hip < 160:
                if not backArchStarted:
                    backArchStarted = True
                    hipColor = (0,0,255)
                    waitKeyVal = 50
                    print("Arching your back at %.2f seconds" % get_pos_sec())
            
            # getting the time frame where your back was arched
            if hip >= 160 and backArchStarted:  
                # backArchEnd = cap.get(cv2.CAP_PROP_POS_MSEC)
                # if backArchEnd == 0.0:  # back arched till end of video
                #     backArchEnd = cap.get(cv2.CAP_PROP_FRAME_COUNT) * 1000 / fps

                backArchStart = None

            # Pushing down
            if direction == 0:
                if elbow < minElbow:  # keep lowering minElbow
                    minElbow = elbow + 10  # adjust for frame bug
                else:  # we've found minElbow, you are pushing back up
                    if minElbow <= 90:  # good pushup (counted)
                        count += 0.5
                    else:
                        print("Elbow should be <= 90 degrees at %.2f seconds" % get_pos_sec())
                        elbowColor = (0,0,255)
                        waitKeyVal = 50
                    
                    minElbow = 180
                    direction = 1
            else:  # direction == 1, pushing up
                if elbow > maxElbow:
                    maxElbow = elbow 
                else:
                    if maxElbow >= 160:
                        count += 0.5
                    else:
                        print("Extend arms more as you're pushing up at %.2f seconds" % get_pos_sec())
                        elbowColor = (0,0,255)
                        waitKeyVal = 50
                    
                    maxElbow = 0
                    direction = 0

        if count > curr_count:
            print("Count:", count)
            curr_count = count        

        # Pushup counter
        cv2.rectangle(img, (0, 0), (150, 100), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(count), (5, 75), cv2.QT_FONT_NORMAL, 2.5,
                    (0, 0, 0), 5)

    cv2.imshow('Pushup counter', img)

    if waitKeyVal == 50:  # we want the angles to be highlighted for half a second
        for i in range(3):  # slow down VideoWriter
            out.write(img)
        frameCount += 1

        if frameCount == delay:  # reset the video speed and the angle highlights
            waitKeyVal = 10
            hipColor = (255,255,255)
            elbowColor = (255,255,255)
            frameCount = 0
    else:
        out.write(img)

    if cv2.waitKey(waitKeyVal) & 0xFF == ord('q'):
        break
        
cap.release()
out.release()
cv2.destroyAllWindows()

print("All done!")