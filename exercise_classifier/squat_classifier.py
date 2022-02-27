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
cap = cv2.VideoCapture('input-squat.mp4')

# Determine video attributes
fps = cap.get(cv2.CAP_PROP_FPS)
width  = cap.get(3)  # float `width`
height = cap.get(4)  # float `height`

# Set up output video writing
fourcc = cv2.VideoWriter_fourcc(*'H264')
path = os.path.join(os.path.dirname(__file__), "../output/")
out = cv2.VideoWriter(path + "squat.mp4", fourcc, int(fps), (int(width), int(height)))

detector = pm.PoseDetector()
landmarks = pl.PoseLandmark()
count = 0
direction = 0
form = 0

print("Count:", count)
curr_count = count

maxKnee = 0
minKnee = 180

kneeColor = (255,255,255)
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
        hip = detector.findAngle(img, landmarks.LEFT_KNEE, landmarks.LEFT_HIP, landmarks.LEFT_SHOULDER, color=hipColor)
        knee = detector.findAngle(img, landmarks.LEFT_ANKLE, landmarks.LEFT_KNEE, landmarks.LEFT_HIP, color=kneeColor)

        # Make sure the form is correct
        if hip > 160 and knee > 160:  # standing position
            form = 1
    
        # Start evaluating
        if form == 1:
            # TODO: add something to keep your back straight

            # Go down
            print(direction)
            if direction == 0:
                if knee < minKnee:  # keep lowering
                    minKnee = knee + 7  # + 10  # adjust for frame bug
                else:
                    if minKnee <= 90:  # good
                        count += 0.5
                    else:
                        print("Squat lower at %.2f seconds" % get_pos_sec())
                        kneeColor = (0,0,255)
                        waitKeyVal = 50

                    minKnee = 180
                    direction = 1
            else:  # direction == 1, go up
                if knee > maxKnee:
                    maxKnee = knee
                else:
                    if maxKnee >= 160:
                        count += 0.5
                    else:
                        print("Stand up straight at %.2f seconds" % get_pos_sec())
                        kneeColor = (0,0,255)
                        waitKeyVal = 50
                    # print("WENT UP")
                    maxKnee = 0
                    direction = 0

        if count > curr_count:
            print("Count:", count)
            curr_count = count        

        # Counter
        cv2.rectangle(img, (0, 0), (100, 100), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(count)), (5, 75), cv2.QT_FONT_NORMAL, 2.5,
                    (0, 0, 0), 5)

    cv2.imshow('Squat counter', img)

    if waitKeyVal == 50:  # we want the angles to be highlighted for half a second
        for i in range(3):  # slow down VideoWriter
            out.write(img)
        frameCount += 1

        if frameCount == delay:  # reset the video speed and the angle highlights
            waitKeyVal = 10
            hipColor = (255,255,255)
            kneeColor = (255,255,255)
            frameCount = 0
    else:
        out.write(img)

    if cv2.waitKey(waitKeyVal) & 0xFF == ord('q'):
        break
        
cap.release()
out.release()
cv2.destroyAllWindows()

print("All done!")