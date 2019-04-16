import argparse
import cv2

from video import VideoStream
from gui import Window, wait_for_key

if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video file or directory with video files')
    args = parser.parse_args()

    stream = VideoStream(args.input)
    
    window = Window('video')
    window.show(640, 480)
    
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

        window.display_frame(frame)

    stream.close()
    window.dispose()
