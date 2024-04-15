import cv2
from cvzone.FaceDetectionModule import FaceDetector
import serial
import numpy as np

cap = cv2.VideoCapture(1)
ws, hs = 640, 480  # Set resolution to 640x480
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Camera couldn't Access!!!")
    exit()


# ser = serial.Serial("/dev/cu.usbserial-1420", 9600, timeout=0.5)
detector = FaceDetector()
servoPos = [90, 90]  # initial servo position

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # get the coordinate
        fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
        pos = [fx, fy]
        # convert coordinat to servo degree
        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [0, 180])

        if servoX < 0:
            servoX = 0
        elif servoX > 180:
            servoX = 180
        if servoY < 0:
            servoY = 0
        elif servoY > 180:
            servoY = 180

        servoPos[0] = servoX
        servoPos[1] = servoY

        cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
        cv2.putText(
            img, str(pos), (fx + 15, fy - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )
        cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2)  # x line
        cv2.line(img, (fx, hs), (fx, 0), (0, 0, 0), 2)  # y line
        cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
        cv2.putText(
            img,
            "TARGET LOCKED",
            (100, 400),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (255, 0, 255),
            3,
        )

    else:
        cv2.putText(
            img, "NO TARGET", (100, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3
        )
        cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
        cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2)  # x line
        cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)  # y line

    cv2.putText(
        img,
        f"Servo X: {int(servoPos[0])} deg",
        (50, 50),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (255, 0, 0),
        2,
    )
    cv2.putText(
        img,
        f"Servo Y: {int(servoPos[1])} deg",
        (50, 100),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (255, 0, 0),
        2,
    )

    # ser.write(f"X{180 - int(servoPos[0])}Y{int(servoPos[1])}\n".encode())
    print(f"X{servoPos[0]}Y{servoPos[1]}\n")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
