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

Step 1) identify your video 
    ex: ~/Downloads/video_to_merge.mp4

Step 2) Look at this script. Change the globals you might be using
    ex: set speed_mult to 2, opening_size to 5 

Step 3) Run this script
    ex: ./videomerge ~/Downloads/video_to_merge.mp4

Step 4) Find your starting frame

'''

#globals

#play video at X times speed
speed_mult = 4

#Used for 
#may have to play with with
# (Reccomend ~4-7, but some might need to go as low as 2)
# (Probably don't go above ~9)
opening_size = 5 

from sys import argv
import os, os.path
import numpy as np
import cv2


def click_callback(event, x, y, flags, param):
    #record a click happening
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x,y
        print("CLICK")


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
            running != running
            #print("SPACE")
      

        elif mouseX >0 and mouseY >0: #click happened
            #print("CLICK HAPPENED!")
            running = True
            break   #storing click in mouseX/Y, using current frame as start frame
    
    #end while
    #print("STARTING MERGE")

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
            running != running
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
