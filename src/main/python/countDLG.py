#python3 countDLG.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel 

from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
#from datetime import datetime
import time
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import requests

def getY(width, H, W):
     return (-4.0/15) * (H/W) * width + (0.6 * H - 20)

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
# ap.add_argument("-i", "--input", type=str,
#    help="path to optional input video file")
# ap.add_argument("-o", "--output", type=str,
#   help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
    help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=15,
    help="# of skip frames between detections")
args = vars(ap.parse_args())


#stream = requests.get(url, stream=True)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# if not args.get("input", False):
#    print("[INFO] starting video stream...")
#    vs = VideoStream(src=0).start()
#    time.sleep(2.0)

# else:
#    print("[INFO] opening video file...")
#    vs = cv2.VideoCapture(args["input"])

url = "https://api.ucsb.edu/dining/cams/v2/stream/de-la-guerra?ucsb-api-key=RWNmwapAJVigtDphtVjipbv2Rrqfulik"
vs = VideoStream(src=url).start()
time.sleep(2.0)

writer = None

W = None
H = None

ct = CentroidTracker(maxDisappeared=50, maxDistance=50)
trackers = []
trackableObjects = {}
waitTimes = []
counter = 0

totalFrames = 0
totalDown = 0
totalUp = 0
#inLine = 0

inDH = 0
tracking = 0

fps = FPS().start()
#printHello()

now = datetime.datetime.now()
interval = datetime.timedelta(minutes=1)

while True:
    frame = vs.read()

    # frame = frame[1] if args.get("input", False) else frame

    # if args["input"] is not None and frame is None:
    #     break
####################################################################################################################
    # resize the frame to have a maximum width of 500 pixels (the
    # less data we have, the faster we can process it), then convert
    # the frame from BGR to RGB for dlib
    frame = imutils.resize(frame, width=500)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]
####################################################################################################################

    # WE WILL NOT NEED THIS SEGMENT OF CODE

    # if we are supposed to be writing a video to disk, initialize
    # the writer
    # if args["output"] is not None and writer is None:
    #   fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    #   writer = cv2.VideoWriter(args["output"], fourcc, 30,
    #       (W, H), True)

####################################################################################################################

    status = "Waiting"
    rects = []

    if totalFrames % args["skip_frames"] == 0:
        status = "Detecting"
        trackers = []

        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > args["confidence"]:
                idx = int(detections[0, 0, i, 1])

                if CLASSES[idx] != "person":
                    continue

                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")

                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(startX, startY, endX, endY)
                tracker.start_track(rgb, rect)

                trackers.append(tracker)

    else:

        for tracker in trackers:
            status = "Tracking"
            tracker.update(rgb)
            pos = tracker.get_position()

            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())

            rects.append((startX, startY, endX, endY))

    #cv2.line(frame, (0, (3*H)//5 - 20), (W, H // 3 - 20), (0, 255, 255), 2)

    objects = ct.update(rects)

    for (objectID, centroid) in objects.items():
        to = trackableObjects.get(objectID, None)

        if to is None:
            to = TrackableObject(objectID, centroid)
            y = getY(centroid[0],H, W)
            if centroid[1] < y:
                to.start = 1
                #inLine += 1
            elif centroid[1] > y:
                to.start = 0

        else:
            y = [c[1] for c in to.centroids]
            direction = centroid[1] - np.mean(y)
            to.centroids.append(centroid)

            if not to.counted:
                    h = getY(centroid[0], H, W)
                    if centroid[1] < h:
                        if direction < 0 and to.start == 0:
                            totalUp += 1
                            to.counted = True
                            inDH -= 1
                            print("In Dining Hall: " + str(inDH))
                            print("Left: " + str(totalUp))


                    elif centroid[1] > h:
                        if direction > 0 and to.start == 1:
                            totalDown += 1
                            to.counted = True
                            inDH += 1
                            print("In Dining Hall: " + str(inDH))
                            print("Arrived: " + str(totalDown))

        trackableObjects[objectID] = to

        # draw both the ID of the object and the centroid of the
        # object on the output frame
        # text = "ID {}".format(objectID)
        # cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
        #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

    deregistered = ct.notRegistered

    for x in deregistered:
        obj = trackableObjects.get(x, None)
        if obj.counted and obj.start == 1:
            counter += 1
            obj.endTime = time.time()
            waitTimes.append(obj.endTime - obj.startTime)
        ct.remove(x)

    tracking = ct.tracking

    info = [
        ("Left", totalUp),
        ("Arrived", totalDown),
        ("Status", status),
        ("Population", inDH),
        ("Tracking", tracking),
        ("Counter", counter)
    ]

    current = datetime.datetime.now()
    if current > now + interval:
        database.updateCapacity("dlg", inDH)
        print("---- UPDATED DATABASE -----")
        now = current

    #("In Line", inLine)

    # loop over the info tuples and draw them on our frame
    # for (i, (k, v)) in enumerate(info):
    #     text = "{}: {}".format(k, v)
    #     cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
    #         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # check to see if we should write the frame to disk
    if writer is not None:
        writer.write(frame)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    totalFrames += 1
    fps.update()


fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
for x in waitTimes:
    string = time.strftime("%H:%M:%S", time.gmtime(x))
    print(string + " ")


# check to see if we need to release the video writer pointer
if writer is not None:
    writer.release()

# if we are not using a video file, stop the camera video stream
if not args.get("input", False):
    vs.stop()

# otherwise, release the video file pointer
else:
    vs.release()

cv2.destroyAllWindows()