#!/usr/bin/env python
import rospy 
import cv2
import cv_bridge
from sensor_msgs.msg import Image
import numpy as np
import sign_detector
import time

class arrow_detection():
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('usb_cam/image_raw', Image, self.image_callback)
        self.left_cascade = cv2.CascadeClassifier('haar_trained_xml/left/cascade.xml')
        self.right_cascade = cv2.CascadeClassifier('haar_trained_xml/right/cascade.xml')
        self.rate = rospy.Rate(20)

    def image_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data)
        left_signs = sign_detector.classify_signs(self.image, self.left_cascade)
        right_signs = sign_detector.classify_signs(self.image, self.right_cascade)
        
        sign_detector.show_box(self.image, left_signs)
        sign_detector.show_box(self.image, right_signs)

        if len(right_signs):
            print("right sign")
            x,y,w,h = right_signs[0]
            distance = self.distance_to_camera(8, 50, w)-1
            print(distance)
        
        elif len(left_signs):
            print("left sign")
            x,y,w,h = left_signs[0]
            distance = self.distance_to_camera(8, 50, w)-1
            print (distance)


        cv2.imshow("Frame", self.image)
        key = cv2.waitKey(0)

        self.rate.sleep()

    def distance_to_camera(self, knownWidth, focalLength, perWidth):
        return (knownWidth * focalLength) / perWidth



if __name__ == "__main__":
    rospy.init_node("arrow_detection")

    detection = arrow_detection()

    rospy.spin()