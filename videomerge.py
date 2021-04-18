#! /usr/bin/env python

# Author: Alex Johnson, modified version of Hunter Damron's framemerge
# Purpose: takes a sequence of images and a pixel location of the robot then merges into one image
#   Does this online on a video to make results easier

#########################
#                       #
#       TUTORIAL        #
#                       #
#########################
'''
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


'''

#globals

#play video at X times speed
speed_mult = 3

#Used for 
#may have to play with with
# (Reccomend ~4-7, but some might need to go as low as 2)
# (Probably don't go above ~9)
opening_size = 2 

from sys import argv
import os, os.path
import numpy as np
import cv2


def click_callback(event, x, y, flags, param):
    #record a click happening
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x,y
        #print("CLICK")


def main():
    if len(argv) != 2:
        print("Usage: videomerge.py <video_name>")
        return
    vid_name = argv[1]


    cap = cv2.VideoCapture(vid_name)

    fps = cap.get(cv2.CAP_PROP_FPS)  * speed_mult
    msec_per_frame = int(1000/fps)

    windowName = 'Videomerge : ' + vid_name
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(windowName, click_callback)

    global mouseX, mouseY
    mouseX, mouseY = -1, -1

    # Capture frame-by-frame
    ret, base_img = cap.read()


    running = False
    writefile = True
    while ret:
        

        # Display the resulting frame
        cv2.imshow(windowName,base_img)

        if running:
            #print("new frame")
            ret, base_img = cap.read()


        k = cv2.waitKey(msec_per_frame) & 0xFF

        if k  == 27: #esc
            writefile = False #quit
            running = False
            break

        elif k == 32: # space   
            running = not running
            #print("SPACE")
      

        elif mouseX >0 and mouseY >0: #click happened
            #print("CLICK HAPPENED!")
            break   #storing click in mouseX/Y, using current frame as start frame
    
    #end while
    print("Starting frame found, beginning merge")

    startcenter = (int(mouseX), int(mouseY))
    
    base_gray = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    composite_img = base_img.copy()
    h, w = base_img.shape[:2]

    ret, above_img = cap.read()
    if not ret: #video finished
        running = False
                

    while ret and writefile:
        global opening_size

        if running:
            ret, above_img = cap.read()
            if not ret: #video finished
                running = False
                break


        above_gray = cv2.cvtColor(above_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(np.abs(above_gray - base_gray),20,255,cv2.THRESH_BINARY)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((opening_size,opening_size),np.uint8))
        cv2.floodFill(thresh, np.zeros((h + 2, w + 2), np.uint8), startcenter, 0)
        composite_img = cv2.bitwise_and(base_img, base_img, mask=cv2.bitwise_not(thresh))
        composite_img += cv2.bitwise_or(above_img, above_img, mask=thresh)

        # Display the resulting frame
        cv2.imshow(windowName,composite_img)

        k = cv2.waitKey(msec_per_frame) & 0xFF
        if k  == 27: #esc
            writefile = False
            running = False #quit

        elif k == 13: # enter
            # we want to save this composite as the new base   
            base_img = composite_img.copy()

        elif k == 32: # space   
            running = not running
            #print("SPACE")

        elif k == ord('+'): #increase opening size
            opening_size+=1

        elif k == ord('-'): #decrease opening size, min 1
            opening_size = 1 if opening_size==1 else opening_size-1

        elif k == ord('d'): #done! save
            running = False
            break

    #end while
    

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


    if writefile: #if we finished correctly
        im_name = os.path.splitext(vid_name)[0]+'.png'
        cv2.imwrite(im_name, base_img)



    

if __name__ == "__main__":
    main()
