import exiftool
import os

dir = "P:/22660210_droner_sjofugl/2022/Bergen_Haholmen_20220526/images/"
files = os.listdir(dir)
with exiftool.ExifToolHelper() as et:
    metadata = et.get_metadata(dir+files)
    for d in metadata:
        print("{:20.20} {:20.20}".format(d["SourceFile"],
                                         d["EXIF:DateTimeOriginal"]))0