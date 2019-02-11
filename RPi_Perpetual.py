# This Program runs prepetually on Raspberry Pi
#
# Work Flow:-
# 1) image_capture() function captures an image at every 30 seconds and invokes s3_upload() thread 
# 2) s3_upload() uploads the image to AWS S3 bucket and invokes face_recognition() thread
# 3) face_recognition() gets response of all facial attributes(for all faces detetcted in image) from AWS rekognition and invokes mongodb_upload() thread

import os
import datetime
import time
import boto3
from threading import Thread
import json
from picamera import PiCamera


def face_recognition(image_name):
    print("Indexing faces")
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": BUCKET,
                "Name": image_name
            }
        },
        Attributes=["ALL"],
    )
    print("Indexing faces completed")


def s3_upload(image_name):
    data = open(image_name,"rb")
    print("Uploading to S3 bucket")
    s3.Bucket(BUCKET).put_object(Key=image_name, Body=data)
    print("Uploaded to S3 bucket")
    image_analysis = Thread(target=face_recognition,args=[image_name])
    image_analysis.start()


def image_capture():
    image_name = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")
    camera.start_preview()
    time.sleep(2)
    camera.capture(image_name+'.jpeg')
    camera.stop_preview()
    image_upload = Thread(target=s3_upload,args=[image_name+".jpeg"])
    image_upload.start()


s3 = boto3.resource("s3")
rekognition = boto3.client("rekognition", "us-east-2")
BUCKET = "cromdev"

camera = PiCamera()
camera.resolution = (640,480)
t=5
i=1    

while True:
    init=Thread(target=image_capture)
    init.start()
    print (i)
    i=i+1
    time.sleep(t)   
