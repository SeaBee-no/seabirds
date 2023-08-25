import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys
import mimetypes
from datetime import datetime
import psycopg2
import json
from libxmp import XMPFiles, consts

with open('credentials.json', 'r') as file:
    cred = json.load(file)

inputfolder = "shared-seabee-ns9879k/seabirds/"

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    dbname=cred["dbname"],
    user=cred["user"],
    password=cred["password"],
    host=cred["host"],
    port=cred["port"]
)

# Create a new cursor
cursor = connection.cursor()

def get_geotagging(img):
    exif = img._getexif()
    if exif is not None:
        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    raise ValueError("No EXIF geotagging found")

                for (t, value) in GPSTAGS.items():
                    if t in exif[idx]:
                        geotagging[value] = exif[idx][t]

        return geotagging
    else:
        raise ValueError("No EXIF metadata found")

def get_geotag_coordinates(geotags):
    lat = geotags['GPSLatitude']
    lon = geotags['GPSLongitude']

    lat_degrees = float(lat[0])
    lat_minutes = float(lat[1]) / 60
    lat_seconds = float(lat[2]) / 3600
    lon_degrees = float(lon[0])
    lon_minutes = float(lon[1]) / 60
    lon_seconds = float(lon[2]) / 3600

    return (lat_degrees + lat_minutes + lat_seconds, lon_degrees + lon_minutes + lon_seconds)


for (root,dirs,files) in os.walk(inputfolder, topdown=True):
    print(root)
    if "/other" not in root:
        allfiles = [root + "/" + item for item in files]
        filepathstring = "','".join(allfiles)
        if filepathstring=="": # if there is no files in the folder just skip it
            continue
        else: 
            filepathstring = "'" + filepathstring + "'"
            # search for all files in that directory
            select_query = "SELECT filename FROM files WHERE concat_ws('/', rootdirectory, mission, subdirectory, filename) IN (%s)"
            cursor.execute(select_query % filepathstring)
            records = cursor.fetchall()
            # and reduce the number of files so that we dont look at them again if they exist
            records2 = []
            for item in records:
                records2.append(item[0])
            files = [item for item in files if item not in records2]
            for file in sorted(files):
                filepath = os.path.join(root, file)
                print(filepath)
                
                # Get FileModifyDate
                timestamp = os.path.getmtime(filepath)
                filemodifydate = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                # Get FileType
                mime_type, _ = mimetypes.guess_type(filepath)
                filetype = mime_type or "Unknown"

                # Get file size
                filesize = os.path.getsize(filepath)

                # Create directory and mission
                # shared-seabee-ns9879k/seabirds/2022/Oslo_NorskGjenvinningWEBODM_20220528/entwine_pointcloud/ept-data/6-51-31-33.laz
                directory = filepath.replace(inputfolder, "")
                directory = directory.split("/")
                rootdirectory = inputfolder+directory[0]
                mission = directory[1]
                subdirectory = "/".join(directory[2:-1])
                if subdirectory == "":
                    subdirectory = None
                filename = directory[-1]
                if filename == mission: 
                    mission = None
                BodySerialNumber = None
                datetimeoriginal = None
                Make = None
                Model = None
                width = None
                height = None
                ExposureTime = None
                FNumber = None
                ISO = None
                PixelXDimension = None
                PixelYDimension = None
                GpsStatus = None
                AbsoluteAltitude = None
                RelativeAltitude = None
                GimbalRollDegree = None
                GimbalYawDegree = None
                GimbalPitchDegree = None
                FlightRollDegree = None
                FlightYawDegree = None
                FlightPitchDegree = None
                FlightXSpeed = None
                FlightYSpeed = None
                FlightZSpeed = None
                # special functions for jpg
                if(filetype == "image/jpeg" and not filename.startswith(".") and filesize != 0):
                    img = Image.open(filepath)
                    
                    width, height = img.size

                    try:
                        # pulls exif for image files
                        exif_data = img._getexif()
                        exif = {
                            TAGS[k]: v
                            for k, v in img._getexif().items()
                            if k in TAGS
                        }
                        BodySerialNumber = exif["BodySerialNumber"].rstrip('\x00')
                        datetimeoriginal = exif["DateTimeOriginal"]
                        datetimeoriginal = datetime.strptime(datetimeoriginal, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                        ISO = int(exif["ISOSpeedRatings"])
                        FNumber = float(exif["FNumber"])
                        Model = exif["Model"].rstrip('\x00')
                        Make = exif["Make"].rstrip('\x00')
                        ExposureTime = float(exif["ExposureTime"])
                    except:
                        pass

                    try:
                        geotags = get_geotagging(img)
                        coordinates = get_geotag_coordinates(geotags)
                        geom = f"POINT({coordinates[1]} {coordinates[0]})"
                    except:
                        geom = None
                    
                    try:
                        # Load the XMP data from the file
                        xmpfile = XMPFiles(file_path=filepath, open_forupdate=False)

                        # Get the XMP data
                        xmp = xmpfile.get_xmp()

                        # Iterate over all namespaces and save what we want or need
                        for ns in xmp:
                            if(ns[1]=="drone-dji:AbsoluteAltitude"): AbsoluteAltitude = float(ns[2])
                            if(ns[1]=="drone-dji:GpsStatus"): GpsStatus = ns[2].rstrip('\x00')
                            if(ns[1]=="drone-dji:RelativeAltitude"): RelativeAltitude = float(ns[2])
                            if(ns[1]=="drone-dji:GimbalRollDegree"): GimbalRollDegree = float(ns[2])
                            if(ns[1]=="drone-dji:GimbalYawDegree"): GimbalYawDegree = float(ns[2])
                            if(ns[1]=="drone-dji:GimbalPitchDegree"): GimbalPitchDegree = float(ns[2])
                            if(ns[1]=="drone-dji:FlightRollDegree"): FlightRollDegree = float(ns[2])
                            if(ns[1]=="drone-dji:FlightYawDegree"): FlightYawDegree = float(ns[2])
                            if(ns[1]=="drone-dji:FlightPitchDegree"): FlightPitchDegree = float(ns[2])
                            if(ns[1]=="drone-dji:FlightXSpeed"): FlightXSpeed = float(ns[2])
                            if(ns[1]=="drone-dji:FlightYSpeed"): FlightYSpeed = float(ns[2])
                            if(ns[1]=="drone-dji:FlightZSpeed"): FlightZSpeed = float(ns[2])
                    except: 
                        pass

                    try:
                        xmpfile.close_file()
                    except:
                        pass
                else:
                    geom = None
                
                # Insert data into the table
                insert_query = "INSERT INTO files (rootdirectory, mission, subdirectory, filename, filemodifydate, datetimeoriginal, filetype, filesize, geom, ExposureTime, FNumber, ISO, width, height, Make, Model, BodySerialNumber, GpsStatus, AbsoluteAltitude, RelativeAltitude, GimbalRollDegree, GimbalYawDegree, GimbalPitchDegree, FlightRollDegree, FlightYawDegree, FlightPitchDegree, FlightXSpeed, FlightYSpeed, FlightZSpeed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (rootdirectory, mission, subdirectory, filename, filemodifydate, datetimeoriginal, filetype, filesize, geom, ExposureTime, FNumber, ISO, width, height, Make, Model, BodySerialNumber, GpsStatus, AbsoluteAltitude, RelativeAltitude, GimbalRollDegree, GimbalYawDegree, GimbalPitchDegree, FlightRollDegree, FlightYawDegree, FlightPitchDegree, FlightXSpeed, FlightYSpeed, FlightZSpeed)
                cursor.execute(insert_query, data)
                connection.commit()


# Close the cursor and connection
cursor.close()
connection.close()