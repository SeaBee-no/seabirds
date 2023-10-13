# This script takes a folder of JPG files captured with a DJI drone and converts them into georeferenced TIF files.
# The script used relativeheight (+3 meters) as height above the ground. There is a commented loop that uses online elevation and gps altitude,
# but it was found unreliable in many areas. 
# Currently it also uses flightyaw as direction. One should potentially swap to using gimbalyaw, but this was found to be unreliable as the values
# provided by DJI varied a lot (on a M3E in summer 2023). This means that gimbal should always point forward when capturing data intended for this use. 
# The script could also easily be ported to other drones as long as there is a way to figure out flightaltitude, yaw/heading, and which sensor was used.

# import all our packages
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json
import requests
import urllib
from libxmp import XMPFiles, consts
import pygeodesy
import math
from pyproj import CRS, Transformer
import utm
import shutil
from osgeo import gdal, osr
import os
import numpy as np

# sets variables needed, like input and output
#img = Image.open('/data/P-Prosjekter2/22660210_droner_sjofugl/test/input/DJI_6688.JPG')
#filename = '/mnt/nas/drone/test/DJI_20230520132711_0063_V.JPG'
#filename = '/mnt/nas/drone/test/DJI_20230418090059_0056_V.JPG'
inputfolder = '/data/P-Prosjekter2/412338_fjellrypetaksering_med_drone/test/t/'
#inputfolder = 'shared-seabee-ns9879k/seabirds/2022/Runde_imagesforannotation/unused/'
#inputfolder = 'shared-seabee-ns9879k/seabirds/test'

#outputfolder = 'shared-seabee-ns9879k/seabirds/test/'
outputfolder = '/data/P-Prosjekter2/412338_fjellrypetaksering_med_drone/test/t_georef/'

# focal length, sensor width, sensor height
sensors = [("M3E-Wide", 12.3, 17.3, 13), ("P1 35mm", 35, 35.9, 24), ("H20T Thermal", 13.5, 7.68, 6.144), ("H20T Zoom 2x", 10.14, 7.41, 5.56)]
sensor = sensors[2]

# defines functions for online altitude api and exif extraction
def get_elevation(x):
    url = 'https://api.opentopodata.org/v1/eudem25m?'
    #url = 'https://api.open-elevation.com/api/v1/lookup?'
    params = {'locations': f"{x[0]},{x[1]}"}
    result = requests.get((url + urllib.parse.urlencode(params)))
    return result.json()['results'][0]['elevation']

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

# loop through the input folder
files = sorted(os.listdir(inputfolder))
for filename in files:
    print(filename)
    # Load image using PIL
    img = Image.open(inputfolder+filename)
    width, height = img.size

    # Get geotagging info
    geotags = get_geotagging(img)

    # Get geotag coordinates
    coordinates = get_geotag_coordinates(geotags)
    latitude = coordinates[0]
    longitude = coordinates[1]

    # Load the XMP data from the file
    xmpfile = XMPFiles(file_path=inputfolder+filename, open_forupdate=False)

    # Get the XMP data
    xmp = xmpfile.get_xmp()

    # Iterate over all namespaces and save what we want or need
    for ns in xmp:
        #print(ns[1], ns[2])
        # if(ns[1]=="drone-dji:GpsLatitude"):
        #     latitude = float(ns[2])
        # if(ns[1]=="drone-dji:GpsLongitude"):
        #     longitude = float(ns[2])
        if(ns[1]=="drone-dji:AbsoluteAltitude"):
            absolutealtitude = float(ns[2])
        if(ns[1]=="drone-dji:RelativeAltitude"):
            relativealtitude = float(ns[2])
        if(ns[1]=="drone-dji:GimbalYawDegree"):
            gimbalyaw = float(ns[2])
        if(ns[1]=="drone-dji:FlightYawDegree"):
            flightyaw = float(ns[2])
        if(ns[1]=="drone-dji:GimbalPitchDegree"):
            pitch = float(ns[2])

    xmpfile.close_file()

    # old tries to figure out the gimbalyaw. could be ignored
    # the gimbal will move seperatly from the drone, and are stored in seperate values. flightyaw is drone direction, while gimbal yaw seems to be 
    # 180/-180 when pointing forwards (on a M3E), but there are some values that swap 180 degrees, so lets swap values below 90 to be on top still
    # starts by making the gimbal yaw around 0 degrees
    # new theory: the gimbalyaw is allways correct, but sometimes its turned 180 degrees on its head (on the M3E)
    # the solution should be to correct so that if its more then 90 degrees away from the flightyaw we turn it around
    # print("flightyaw",flightyaw, "gimbalyaw", gimbalyaw)
    # if(abs(flightyaw - gimbalyaw) > 90):
    #     yaw = gimbalyaw + 180
    # else:
    #     yaw = gimbalyaw
    # dont really understand the varations in the gimbalyaw. might not be reliable, so we go for only flightyaw so far..
    yaw = flightyaw

    # Section that uses online elevation and absolutealtitude
    # print(yaw, pitch)
    # groundaltitude = get_elevation((latitude, longitude))
    # if groundaltitude == None:
    #     flightheight = relativealtitude + 3 #?
    # else:
    #     flightheight = absolutealtitude - groundaltitude
    # unreliable (potensially the online service that gives "wrong" results)
    flightheight = relativealtitude + 3

    # calculate the width and height of the view on the image
    alpha = math.degrees(math.atan((sensor[2]/2)/sensor[1]))
    distancex = abs(math.tan(math.radians(alpha))*flightheight)

    alpha = math.degrees(math.atan((sensor[3]/2)/sensor[1]))
    distancey = abs(math.tan(math.radians(alpha))*flightheight)

    # create the corner coordinates
    utmcoord = utm.from_latlon(latitude, longitude)
    # print(utmcoord)
    x1 = utmcoord[0]
    y1 = utmcoord[1]
    # print(yaw)
    #https://math.stackexchange.com/questions/143932/calculate-point-given-x-y-angle-and-distance
    distancetocorner = math.sqrt(distancex**2 + distancey**2)
    # print(distancey, distancex, distancetocorner)
    angletocorner = math.degrees(math.sin(distancey / distancex))

    angles = (angletocorner, angletocorner+(90-angletocorner)*2, angletocorner+(90-angletocorner)*2+angletocorner*2, 360-angletocorner)
    angles = [x-yaw for x in angles]
    newpoints = []
    for a in angles:
        x2 = x1 + distancetocorner*math.cos(math.radians(a))
        y2 = y1 + distancetocorner*math.sin(math.radians(a))
        # print(x1, "+", distancetocorner*math.cos(math.radians(a)), y1, "+", distancetocorner*math.sin(math.radians(a)))
        newpoints.append(utm.to_latlon(x2, y2, utmcoord[2], utmcoord[3]))

    # print(newpoints)
    topright = newpoints[0]
    topleft = newpoints[1]
    bottomleft = newpoints[2]
    bottomright = newpoints[3]

    # we can try to georef the file based on the corner coordinates
    # Create a copy of the original file and save it as the output filename:
    outputfilename = outputfolder+filename.replace('JPG','TIF')
    im = Image.open(inputfolder+filename)
    im = im.convert('RGBA')
    data = np.array(im)   # "data" is a height x width x 4 numpy array
    im2 = Image.fromarray(data)
    im2.save(outputfilename, 'TIFF')
    output_fn = outputfilename

    # Open the output file for writing:
    ds = gdal.Open(output_fn, gdal.GA_Update)
    # Set spatial reference:
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326) # set used projection

    # Enter the GCPs
    #   Format: [map x-coordinate(longitude)], [map y-coordinate (latitude)], [elevation],
    #   [image column index(x)], [image row index (y)]
    gcps = [gdal.GCP(topleft[1], topleft[0], 0, 0, 0),
    gdal.GCP(topright[1], topright[0], 0, width, 0),
    gdal.GCP(bottomleft[1], bottomleft[0], 0, 0, height),
    gdal.GCP(bottomright[1], bottomright[0], 0, width, height)]

    # Apply the GCPs to the open output file:
    ds.SetGCPs(gcps, sr.ExportToWkt())

    # Close the output file in order to be able to work with it in other programs:
    ds = None