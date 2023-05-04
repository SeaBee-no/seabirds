# sdcard2sigma
# made to run on WSL/Linux
import argparse
import os
import sys
import shutil

parser = argparse.ArgumentParser(description='Copies files from DJI sd cards into SeaBee structure and pushes it to Sigma')

parser.add_argument('--grouping', help='first element in mission name/folder name')
parser.add_argument('--pilot', help='pilot to write to config file')
parser.add_argument('--sdcard', help='sd card root directory')
parser.add_argument('--backup', help='backup disk root directory')
parser.add_argument('--sigma', help='sigma root directory, usually something like seabirds/2023')

args = parser.parse_args()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(args.sdcard, "=>", args.backup, "=> sigma")

# mount the drive
try:
    os.system("sudo mkdir "+args.sdcard)
    os.system("sudo mount -t drvfs "+args.sdcard[-1:].upper()+": "+args.sdcard)
except:
    pass

# copy and rearrange to local disk
folders = os.listdir(args.sdcard+"/DCIM")
print(folders)
for folder in folders:
    temp = folder.split("_")
    if len(temp)==4:
        grouping = args.grouping
        missionname = temp[3]
        files = os.listdir(args.sdcard+"/DCIM/"+folder)
        for filename in files:
            if filename[-4:]==".JPG" or filename[-4:]==".jpg":
                datetime = filename.split("_")[1][:12]
                break
        newfoldername = grouping+"_"+missionname+"_"+datetime
        newfolder = args.backup+"/"+newfoldername
        print(newfolder)
        if not os.path.isdir(newfolder):
            print(bcolors.OKBLUE + folder, "=>", newfolder + bcolors.ENDC)
            os.makedirs(newfolder+"/images")
            os.system("rclone copy "+args.sdcard+"/DCIM/"+folder+" "+newfolder+"/images --progress")
            f = open(newfolder+"/config.yaml", "a")
            f.write("pilot: "+args.pilot+"\n")
            f.write("nfiles: "+str(len(files))+"\n")
            f.close()

# unmount the drive
try:
    os.system("sudo umount "+args.sdcard)
except:
    pass
print(bcolors.OKGREEN + "SAFE TO REMOVE SDCARD" + bcolors.ENDC)

# upload to sigma
print(bcolors.OKBLUE + args.backup, "=>", "minio:"+args.sigma + bcolors.ENDC)
os.system("rclone copy "+args.backup+" miniopilotnina:"+args.sigma+" --progress")