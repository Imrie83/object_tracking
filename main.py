import cv2
import sys

(major_ver, minor_ver, subminor_ver) = cv2.__version__.split(".")

if __name__ == '__main__':

    # Set up tracker.
    # Instead of CSRT, you can also use

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]

    if int(minor_ver) == 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()

    # video = cv2.VideoCapture("name.mp4")
    video = cv2.VideoCapture(0)

    # Close if video not opened.
    if not video.isOpened():
        print('Could not open video')
        sys.exit()

    # Read first frame
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Initial bounding box
    box = (287, 23, 86, 320)
    box = cv2.selectROI(frame, False)

    # Init tracker with first frame and bounding box.
    ok = tracker.init(frame, box)

    while True:
        # read a new frame.
        ok, frame = video.read()

        if not ok:
            break

        # Start timer.
        timer = cv2.getTickCount()

        # Update tracker.
        ok, box = tracker.update(frame)

        # Calculate FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw b-box.
        if ok:
            # tracking success
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, 'Tracking failure detected', (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)

        # Display tracker type
        cv2.putText(frame, tracker_type + 'Tracker', (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        # Display fps
        cv2.putText(frame, 'FPS: ' + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit on ESC
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
