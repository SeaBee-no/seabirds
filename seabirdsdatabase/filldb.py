import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys
import mimetypes
from datetime import datetime
import psycopg2
import json

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
    if "/other" not in root:
        for file in sorted(files):
            filepath = os.path.join(root, file)
            # Execute the SELECT query
            select_query = "SELECT * FROM files WHERE concat_ws('/', rootdirectory, mission, subdirectory, filename) = %s"
            cursor.execute(select_query, (filepath,))
            records = cursor.fetchall()
            if(len(records)==0):
                print(filepath)
                
                # Get FileModifyDate
                timestamp = os.path.getmtime(filepath)
                filemodifydate = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                # Get FileType
                mime_type, _ = mimetypes.guess_type(filepath)
                filetype = mime_type or "Unknown"

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
                bodyserialnumber = None
                datetimeoriginal = None
                # special functions for jpg
                if(filetype == "image/jpeg" and not filename.startswith(".")):
                    img = Image.open(filepath)
                    
                    try:
                        # pulls exif for image files
                        exif_data = img._getexif()
                        exif = {
                            TAGS[k]: v
                            for k, v in img._getexif().items()
                            if k in TAGS
                        }
                        bodyserialnumber = exif["BodySerialNumber"].rstrip('\x00')
                        datetimeoriginal = exif["DateTimeOriginal"]
                        datetimeoriginal = datetime.strptime(datetimeoriginal, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        pass

                    try:
                        geotags = get_geotagging(img)
                        coordinates = get_geotag_coordinates(geotags)
                        geom = f"POINT({coordinates[1]} {coordinates[0]})"
                    except:
                        geom = None
                else:
                    geom = None
                
                # Insert data into the table
                insert_query = "INSERT INTO files (rootdirectory, mission, subdirectory, filename, filemodifydate, datetimeoriginal, filetype, bodyserialnumber, geom) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326))"
                data = (rootdirectory, mission, subdirectory, filename, filemodifydate, datetimeoriginal, filetype, bodyserialnumber, geom)
                cursor.execute(insert_query, data)
                connection.commit()


# Close the cursor and connection
cursor.close()
connection.close()