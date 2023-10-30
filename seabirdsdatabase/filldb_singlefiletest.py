import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys
import mimetypes
from datetime import datetime
import psycopg2

inputfolder = "shared-seabee-ns9879k/seabirds/"


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


filepath = "shared-seabee-ns9879k/seabirds/2022/Runde_niser_20220901/DJI_8673.MP4"
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
GPSStatus = None
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
        ExposureTime = exif["Exposure Time"]
        FNumber = exif["FNumber"]
        ISO = exif["ISO"]
        PixelXDimension = exif["PixelXDimension"]
        PixelYDimension = exif["PixelYDimension"]
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
        xmpfile = XMPFiles(file_path=inputfolder+filename, open_forupdate=False)

        # Get the XMP data
        xmp = xmpfile.get_xmp()
    except: 
        pass
    
    # Iterate over all namespaces and save what we want or need
    for ns in xmp:
        try:
            if(ns[1]=="drone-dji:AbsoluteAltitude"): AbsoluteAltitude = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:GPSStatus"): GPSStatus = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:RelativeAltitude"): RelativeAltitude = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:GimbalRollDegree"): GimbalRollDegree = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:GimbalYawDegree"): GimbalYawDegree = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:GimbalPitchDegree"): GimbalPitchDegree = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:FlightRollDegree"): FlightRollDegree = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:FlightYawDegree"): FlightYawDegree = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:FlightPitchDegree"): FlightPitchDegree = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:FlightXSpeed"): FlightXSpeed = float(ns[2])
        except:
            pass
        try:
            if(ns[1]=="drone-dji:FlightYSpeed"): FlightYSpeed = float(ns[2])
        except:
            pass
        try:
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
insert_query = "INSERT INTO files (rootdirectory, mission, subdirectory, filename, filemodifydate, datetimeoriginal, filetype, filesize, BodySerialNumber, geom, GPSStatus, AbsoluteAltitude, RelativeAltitude, GimbalRollDegree, GimbalYawDegree, GimbalPitchDegree, FlightRollDegree, FlightYawDegree, FlightPitchDegree, FlightXSpeed, FlightYSpeed, FlightZSpeed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
data = (rootdirectory, mission, subdirectory, filename, filemodifydate, datetimeoriginal, filetype, filesize, BodySerialNumber, geom, GPSStatus, AbsoluteAltitude, RelativeAltitude, GimbalRollDegree, GimbalYawDegree, GimbalPitchDegree, FlightRollDegree, FlightYawDegree, FlightPitchDegree, FlightXSpeed, FlightYSpeed, FlightZSpeed)

print(insert_query % data)        
