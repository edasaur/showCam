import cv2
import numpy as np
import os, os.path as osp
import sys
import argparse
import logging
import random

CAM_NUM = 1
log_format = '%(created)f:%(levelname)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)  # log to file filename='example.log',
TAG = "cam%s:" % CAM_NUM

def full_path(rel_path):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, rel_path)


def main():
    logging.debug(TAG + "inside main")
    rand = random.Random()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", help="capture from video file instead of from camera")
    args = parser.parse_args()

    logging.debug(TAG + "done parsing arguments")

    capture = cv2.VideoCapture()
    if args.video:
        capture.open(args.video)
    else:
        capture.open(0)
    if not capture.isOpened():
        # Failed to open camera
        return False
    logging.debug(TAG + "camera opened")

    average = None
    element = np.ones((3,3), np.uint8)
    while True:
        # logging.debug(TAG + "before reading frame")
        retval, frame = capture.read()
        if not retval:
            break  # end of video
        # logging.debug(TAG + "after reading frame")
        height, width, depth = frame.shape

        if average is None:
            average = np.float32(frame)
            avg_img = frame.copy()
        else:
            cv2.accumulateWeighted(frame, average, 0.01)
            avg_img = cv2.convertScaleAbs(average)

        difference = cv2.absdiff(frame, avg_img)
        gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        _, gray = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

        gray = cv2.dilate(gray, element, iterations=10)
        gray = cv2.erode(gray, element, iterations=13)

        contours, h = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        print len(contours)
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            cv2.circle(frame, (x+w/2,y+h/2), 5, (50,50,255), 10)

        cv2.imshow("cam%s" % CAM_NUM, frame)

        if cv2.waitKey(5) == 27:  # exit on escape
            logging.debug(TAG + "received escape key")
            capture.release()
            break

    return True

logging.debug(TAG + "starting module")
if __name__ == "__main__":
    logging.debug(TAG + "starting main")
    main()



