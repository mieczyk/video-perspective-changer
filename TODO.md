# To be implemented

* `python video-perspective-changer <INPUT>` - \<INPUT\> may be a video file, list of video files or a directory containing video files (-d,--dir option).
* When the `--dir` option is given, a user can pass the `-r,--recursive` option as well, turning on the recursive search within the given directory.
* ``-o,--output-dir`` - where the output video files will be saved. All output files will have the same name as the input files, but the "out" suffix will be added.
* The preview of the first video (paused by default) is displayed in the GUI window (first frame by default). User can navigate the video with the following keys: 
    * <-, ->, [, ] - next; previous frame(s).
    * <SPACE> - pause.
    * <ENTER> - change the perspective of the current video.
* A user can "draw" a rectangle with mouse and manipulate its vertices (the rectangle will be transformed into an irregular quandrange during the manipulation).
* Multiple video files are processed simultaneously.
* Separate configuration file + README.
