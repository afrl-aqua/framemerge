# framemerge
Merges multiple images which contain a single moving object



#       TUTORIAL  FOR   VIDEOMERGE      


This script opens up a video and dynamically creates a merged image with
the frames of a video. FOr use with the Aqua2 robot at AFRL, but I'm sure it
could be used for other purposes

Users click on the aqua to identify their starting frame, then
press space to unpause the video.

As the video plays, it will dynamically merge the current frame with all 
currently saved frames. At the start, the only saved frame is the starting frame

Once a starting frame is identified, users can press enter to add a frame to the 
full image. 

Pressing Esc will quit the application
When you are done, press 'd' to save the image. 
    Alternatively, let the video end.
    Saved images will have the same name as the video. 

Full Process:

Step 1) identify your video 
    ex: ~/Downloads/video_to_merge.mp4

Step 2) Look at this script. Change the globals you might be using
    ex: set speed_mult to 2, opening_size to 5 

Step 3) Run this script
    ex: ./videomerge ~/Downloads/video_to_merge.mp4

Step 4) Find your starting frame
    In the video, click on the Aqua. This will make sure it doesn't get erased
    The video will start paused. Press space to unpause, or pause again.
    You can also press escape to quit the application

Step 5) Select your merged frames
    Once you have cicked on the aqua and pressed space to play the video,
    the application will begin dynamically merging the current frame.

    If you like the location of the aqua, press enter. 
        This will add it to the base frame

Step 6) Finish
    If you ware satisfied, press 'd' to save the image, or let the video end
        The file will be saved in the same location as the video, with the same name,  as a png
    If you were not satisfied, press 'esc' to quit. 

