import argparse
import os
import sys
import shutil

# try:
#     os.system("sudo mkdir /mnt/d/")
#     os.system("sudo mount -t drvfs D: /mnt/d")
# except:
#     pass

rootfolder = "/mnt/c/Users/sindre.molvarsmyr/Downloads/til_sindre"
folders = os.listdir(rootfolder)
print(folders)
for folder in folders:
    if(folder != "nonmission"):
        nfiles = len(os.listdir(rootfolder+"/"+folder+"/images/"))
        print(folder + " " + str(nfiles))
        try:
            os.remove(rootfolder+"/"+folder+"/config.yaml")
        except:
            pass
        f = open(rootfolder+"/"+folder+"/config.yaml", "a")
        f.write("nfiles: "+str(nfiles)+"\n")
        f.write("organisation: NINA\n")
        f.write("creator_name: Sine Dagsdatter Hagestad\n")
        f.write("mosaic: true\n")
        f.write("publish: true\n")
        f.write("theme: Seabirds\n")
        f.close()