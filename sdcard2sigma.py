# sdcard2sigma
# sudo python3 seabirds/sdcard2sigma.py --grouping Team1 --collectedby "NINA (Sindre Molværsmyr)" --sdcard /mnt/j --backup1 /mnt/i --backup2 /mnt/g --sigma seabirds/2023
# made to run on WSL/Linux
import argparse
import os
import sys
import shutil

parser = argparse.ArgumentParser(description='Copies files from DJI sd cards into SeaBee structure and pushes it to Sigma')

parser.add_argument('--grouping', help='first element in mission name/folder name')
parser.add_argument('--collectedby', help='collectedby to write to config file')
parser.add_argument('--sdcard', help='sd card root directory')
parser.add_argument('--backup1', help='backup disk root directory - DJI format')
parser.add_argument('--backup2', help='backup disk root directory - Sigma format')
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

print(args.sdcard, "=>", args.backup1, "=>", args.backup2, "=> sigma")

# mount the drives
#try:
#    os.system("sudo mkdir "+args.sdcard)
#    os.system("sudo mount -t drvfs "+args.sdcard[-1:].upper()+": "+args.sdcard)
#except:
#    pass

try:
    os.system("sudo mkdir "+args.backup1)
    os.system("sudo mount -t drvfs "+args.backup1[-1:].upper()+": "+args.backup1)
except:
    pass

try:
    os.system("sudo mkdir "+args.backup2)
    os.system("sudo mount -t drvfs "+args.backup2[-1:].upper()+": "+args.backup2)
except:
    pass

# copy from sd to hard drive
#os.system("rclone copy "+args.sdcard+"/DCIM/ "+args.backup1+" --progress")

# unmount the drive
#try:
#    os.system("sudo umount "+args.sdcard)
#except:
#    pass
#print(bcolors.OKGREEN + "SAFE TO REMOVE SDCARD" + bcolors.ENDC)

# copy and rearrange to local disk
folders = os.listdir(args.backup1)
print(folders)
for folder in folders:
    temp = folder.split("_")
    if len(temp)==4:
        grouping = args.grouping
        missionname = temp[3]
        files = os.listdir(args.backup1+"/"+folder)
        for filename in files:
            if filename[-4:]==".JPG" or filename[-4:]==".jpg":
                datetime = filename.split("_")[1][:12]
                break
        finished = list()
        for thisfolder in os.listdir(args.backup2):
            x = thisfolder.split("_")
            if len(x)==3:
                finished.append(x[1]+"_"+x[2])
        if missionname+"_"+datetime not in finished:
            newfoldername = grouping+"_"+missionname+"_"+datetime
            newfolder = args.backup2+"/"+newfoldername
            print(newfolder)
            #if not os.path.isdir(newfolder):
            print(bcolors.OKBLUE + folder, "=>", newfolder + bcolors.ENDC)
            os.makedirs(newfolder+"/images")
            os.system("rclone copy "+args.backup1+"/"+folder+" "+newfolder+"/images --progress")
            f = open(newfolder+"/config.yaml", "a")
            f.write("nfiles: "+str(len(files))+"\n")
            f.write("collectedby: "+args.collectedby+"\n")
            f.close()
    else:
        os.system("rclone copy "+args.backup1+"/"+folder+" "+args.backup2+"/nonmission/"+folder+" --progress")


# upload to sigma
print(bcolors.OKBLUE + args.backup2, "=>", "minio:"+args.sigma + bcolors.ENDC)
os.system("rclone copy "+args.backup2+" miniopilotnina:"+args.sigma+" --progress")

# unmount the drive
try:
    os.system("sudo umount "+args.backup1)
except:
    pass
print(bcolors.OKGREEN + "SAFE TO REMOVE BACKUP1" + bcolors.ENDC)

# unmount the drive
try:
    os.system("sudo umount "+args.backup2)
except:
    pass
print(bcolors.OKGREEN + "SAFE TO REMOVE BACKUP2" + bcolors.ENDC)