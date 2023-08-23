# need to install this:
# cv2
# py -m pip install imutils

# q = quit
# r = rotate
# z = clear crop region
# s = skip photo
# c = crop/copy

import cv2
from PIL import Image
import os
import sys
import imutils

dir = "shared-seabee-ns9879k/seabirds/2023/Bergen_Realfagstaket_20230530/images/"
files = os.listdir(dir)
files.sort()
print(files)
mouseX = 0
mouseY = 0
gcpNumber = 0
max_size = 500*940

def click(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        mouseX = int(x/scaling)
        mouseY = int(y/scaling)

gcpoutfile = open('seabirds/manualgcp/gcp_list.txt', 'a')
gcpfile = open('seabirds/manualgcp/gcp_listPOINTSRealfag.txt', 'r')
lines = gcpfile.readlines()
gcpoutfile.writelines(lines[0].strip()+'\n')
gcp = []
for line in lines[1:]:
    temp = line.strip().split(" ")
    gcp.append(temp)

for file in files:
    if(file[-4:] in [".jpg",".JPG"]):
        skip = False
        filename = dir + file
        img = Image.open(filename)
        width, height = img.size
        img.close()
        if width > height:
            scaling = (1024*1.2/float(width)) # max width
        else:
            scaling = (800*1.2/float(height)) # max height
        image_original = cv2.imread(filename)
        image = cv2.resize(image_original, (0,0), fx=scaling, fy=scaling, interpolation = cv2.INTER_CUBIC) 
        clone = image.copy()
        cv2.namedWindow(file)
        cv2.setMouseCallback(file, click)
        # wait for 
        while True:
                # display the image and wait for a keypress
                cv2.imshow(file, image)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord("1"):
                    print(1)
                    gcpNumber = 1
                elif key == ord("2"):
                    print(2)
                    gcpNumber = 2
                elif key == ord("3"):
                    print(3)
                    gcpNumber = 3
                elif key == ord("4"):
                    print(4)
                    gcpNumber = 4
                elif key == ord("n"): # write and next
                    break
                elif key == ord("s"): # skip
                    skip = True
                    break
                elif key == ord("q"): # quit
                    cv2.destroyAllWindows()
                    sys.exit("Quit")
        cv2.destroyAllWindows()
        if not skip:
            #352150.64	6777351.46	694.3730469	1984.79	2849.43	DJI_5686.JPG	gcp01
            gcpline = str(gcp[gcpNumber-1][1])+" "+str(gcp[gcpNumber-1][2])+" "+str(gcp[gcpNumber-1][3])+" "+str(mouseX)+" "+str(mouseY)+" "+str(file)+" gcp"+str(gcp[gcpNumber-1][0])
            gcpoutfile.writelines(gcpline+'\n')
            print(gcpline)

gcpoutfile.close()
