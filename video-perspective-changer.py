import argparse
import cv2

from video import VideoStream

if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video file or directory with video files')
    args = parser.parse_args()

    stream = VideoStream(args.input)
    
    cv2.namedWindow('window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('window', 640, 480)

    while(True):
        frame = stream.next_frame()

        if cv2.waitKey(1) & 0xFF == ord('q') or frame is None:
            break

        cv2.imshow('window', frame.cv_image)

    stream.close()
        





