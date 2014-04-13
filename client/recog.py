#! /usr/bin/env python
import cv2
import numpy as np
import os, os.path as osp
import sys
import argparse
import logging
import random
import urllib2
import boto
import time


CAM_NUM = 1
log_format = '%(created)f:%(levelname)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)  # log to file filename='example.log',
TAG = "cam%s" % CAM_NUM

def main():
    logging.debug(TAG + "inside main")

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", help="capture from video file instead of from camera")
    args = parser.parse_args()

    logging.debug(TAG + "done parsing arguments")
    get_config()
    print len(Settings.username)

    capture = cv2.VideoCapture()
    if args.video:
        capture.open(args.video)
    else:
        capture.open(0)
    if not capture.isOpened():
        # Failed to open camera
        return False
    logging.debug(TAG + "camera opened")

    process_video(capture)

    return True

class Settings:
    # Please don't steal my keys :/
    key = 'AKIAIXFZWTTMOPWRMN7Q'
    secret = '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'
    threshold = 6
    alert_level = 50

    @classmethod
    def set_threshold(cls, new):
        print new + 3
        cls.threshold = new + 3

    @classmethod
    def set_alert_level(cls, new):
        print new + 2
        cls.alert_level = new + 2

def get_config():
    config = open('config.txt', 'r')
    while True:
        line = config.readline()
        if not line:
            break
        line = line.split(':')
        setattr(Settings, line[0], line[1].rstrip())

def process_video(capture):
    rand = random.Random()
    average = None
    element = np.ones((3,3), np.uint8)
    cv2.namedWindow(TAG)
    cv2.createTrackbar('Disturbance threshold', TAG, 3, 8, Settings.set_threshold)
    cv2.createTrackbar('Alert level', TAG, 48, 48, Settings.set_alert_level)
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
            cv2.accumulateWeighted(frame, average, (2**Settings.threshold)/7000.0)
            avg_img = cv2.convertScaleAbs(average)

        difference = cv2.absdiff(frame, avg_img)
        gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        _, gray = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

        gray = cv2.dilate(gray, element, iterations=10)
        gray = cv2.erode(gray, element, iterations=13)

        contours, h = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        num_contours = len(contours)

        if num_contours >= Settings.alert_level:
            PictureTaker.picture(frame.copy(), num_contours)
        else:
            PictureTaker.tick()

        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            cv2.circle(frame, (x+w/2,y+h/2), 5, (50,50,255), 10)

        cv2.imshow(TAG, frame)

        if cv2.waitKey(5) == 27:  # exit on escape
            logging.debug(TAG + "received escape key")
            capture.release()
            break


class PictureTaker:
    MAX_TIME_TIL_UPLOAD = 300
    best_frame = None
    best_frame_count = 0
    time_til_upload = MAX_TIME_TIL_UPLOAD

    @classmethod
    def picture(self, frame, disturbance_count):
        if disturbance_count < Settings.alert_level:
            return
        if disturbance_count > self.best_frame_count:
            self.best_frame = frame
            self.best_frame_count = disturbance_count
            self.time_til_upload = self.MAX_TIME_TIL_UPLOAD
            return

    @classmethod
    def tick(self):
        if self.best_frame is not None:
            self.time_til_upload -= 1
        if self.time_til_upload == 0:
            self.upload()

    @classmethod
    def upload(self):
        frame = self.best_frame
        self.best_frame_count = 0
        self.best_frame = None
        self.time_til_upload = self.MAX_TIME_TIL_UPLOAD
        url = self.upload_s3(frame)
        logging.info(url)
        

    @classmethod
    def upload_s3(self, frame):
        TEMP_FILE_NAME = 'temp.png'
        cv2.imwrite(TEMP_FILE_NAME, frame)
        conn = boto.connect_s3(Settings.key, Settings.secret)
        bucket = conn.get_bucket('showcam.photos')
        name = Settings.username + time.strftime("-%Y%m%d-%H%M%S")
        key = bucket.new_key(name)
        key.set_contents_from_filename(TEMP_FILE_NAME)
        os.remove(TEMP_FILE_NAME)
        return "https://s3-us-west-1.amazonaws.com/showcam.photos/%s" % name


logging.debug(TAG + "starting module")
if __name__ == "__main__":
    logging.debug(TAG + "starting main")
    main()



