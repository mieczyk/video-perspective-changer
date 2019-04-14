import argparse
import cv2

from video import VideoStream

def wait_for_key(miliseconds):
    # '& 0xFF' because we're interested in the last 8 bits only.
    return cv2.waitKey(miliseconds) & 0xFF

if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video file or directory with video files')
    args = parser.parse_args()

    stream = VideoStream(args.input)

    cv2.namedWindow('window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('window', 640, 480)

    while(True):
        frame = stream.next_frame()
        key_pressed = wait_for_key(1)

        # Pause the video
        if key_pressed == ord(' '):
            while(True):
                key_pressed = wait_for_key(0)
                if  key_pressed == ord(' ') or key_pressed == ord('q'):
                    break

        if frame is None or key_pressed == ord('q'):
            break

        cv2.imshow('window', frame.cv_image)

    stream.close()
