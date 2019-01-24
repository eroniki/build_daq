import cv2
import numpy as np
import os
import glob
from natsort import natsorted

def convert_frames_to_video(pathIn,pathOut,fps=3):
    files = glob.glob(pathIn + "*.jpg")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, fps, (640,480))

    print files
    #for sorting the file names properly
    files = natsorted(files)
    for file in files:
        print file

    print len(files)
    for i in range(len(files)):
        filename= files[i]
        #reading each files
        print filename
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        #inserting the frames into an image array
        out.write(img)

    out.release()

def main():
    pathIn= '/home/immersivemidiaopenposeclone/build_daq/data/1544470391975/6/'
    pathOut = 'video.avi'
    convert_frames_to_video(pathIn, pathOut)

if __name__=="__main__":
    main()
