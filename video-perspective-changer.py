import os, argparse, glob
import cv2
import numpy as np
from threading import Thread

from video import VideoStream, OutputVideoFile
from gui import Window, wait_for_key

class VideoController:
    def __init__(self, video_path):
        self._stream = VideoStream(video_path)
        self._focused_area_vertices = None
        self._original_frame = None

        self.name = os.path.splitext(os.path.basename(video_path))[0]
        self.current_frame = self._stream.next_frame()

    def fetch_next_frame(self):
        self._original_frame = self._stream.next_frame()

        if self._original_frame is None:
            self.current_frame = None
            return

        if self._focused_area_vertices is not None:
            self.current_frame = self._original_frame.copy()
            self.current_frame.focus_on_area(self._focused_area_vertices)
        else:
            self.current_frame = self._original_frame

    def set_focus_area(self, vertices, top_left_vertex_idx):
        # Make sure the first vertex is the top left vertex 
        self._focused_area_vertices = np.roll(
            vertices, 
            -top_left_vertex_idx, 
            axis=0
        )

    def reset_focus_area(self):
        self._focused_area_vertices = None
        self.current_frame = self._original_frame
    
    def record(self, output_dir):
        if self.current_frame is None:
            return

        # TODO: Data hardcoded for testing purposes
        out = OutputVideoFile('{0}/{1}.out.avi'.format(output_dir, self.name), self.current_frame.width, self.current_frame.height)
        while self.current_frame is not None:
            out.add_frame(self.current_frame)
            self.fetch_next_frame()
        out.save()
        print('saved')

    def dispose(self):
        self._stream.close()

def main_loop(controllers):
    current_video_idx = 0
    paused = True 
    window = None
    
    def show_window_for_video(idx):
        nonlocal window
        if window is not None:
            window.dispose()
        window = Window(controllers[idx].name)
        window.show(640, 480)

    show_window_for_video(current_video_idx)
    
    threads = []

    while current_video_idx < len(controllers):
        current_video = controllers[current_video_idx]
        key_pressed = wait_for_key(1)
        
        # <SPACE>: Pause
        if key_pressed == ord(' '):
            paused = not paused
        # <q>: Quit 
        elif key_pressed == ord('q'):
            break
        # <RETURN>: Change perspective
        elif key_pressed == 13 and window.selection is not None:
            current_video.set_focus_area(
                window.selection.vertices, 
                window.selection.top_left_vertex_idx
            )
            current_video.fetch_next_frame() 
            t = Thread(target=current_video.record, args=('out/', ))
            threads.append(t)
            t.start()

            current_video_idx += 1
            if current_video_idx < len(controllers):
                show_window_for_video(current_video_idx)
            print(current_video_idx)
            continue
        # <u>: Undo the perspective transformation
        elif key_pressed == ord('u'):
            current_video.reset_focus_area()

        if not paused:
            current_video.fetch_next_frame()
        if current_video.current_frame is not None:
            window.display_frame(current_video.current_frame)
    
    print("left the loop")
    for t in threads:
        t.join()

    if window is not None:
        window.dispose()
    for video in controllers:
        video.dispose()

def find_video_files_in_directory(directory, recursive_search=False):
    VIDEO_FILE_EXT = ['*.mp4', '*.mov', '*.avi']
    video_files_paths = []
    for ext in VIDEO_FILE_EXT:
        pattern = os.path.join(
            directory, 
            ('**/' + ext) if recursive_search else ext
        )
        video_files_paths.extend(glob.glob(pattern, recursive=recursive_search))
    return video_files_paths

if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video file or directory with video files.')
    parser.add_argument(
        '-d', 
        '--dir', 
        action='store_true', 
        help='The input argument is treated as a directory containing input video files.'
    )
    args = parser.parse_args()
    
    controllers = []

    if args.dir:
        video_files_paths = find_video_files_in_directory(args.input)
        for path in video_files_paths:
            controllers.append(VideoController(path))
    else:
        controllers.append(VideoController(args.input))

    main_loop(controllers)
