from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from libxmp import XMPFiles
from pyproj import Transformer
import numpy as np
from osgeo import gdal, osr
import matplotlib.pyplot as plt
import matplotlib.patches as patches

inputfolder = '/home/wigeon/Pictures/ntnu/trondelag-froan_smaavaeret_2024-05-30/'
outputfolder = '/home/wigeon/Pictures/ntnu/trondelag-froan_smaavaeret_2024-05-30_georef/'

# Define sensor parameters
# focal length, sensor width, sensor height
sensors = {
    "M3E-Wide": {"focal_length": 12.3, "sensor_width": 17.3, "sensor_height": 13},
    "P1 35mm": {"focal_length": 35, "sensor_width": 35.9, "sensor_height": 24},
    "H20T Thermal": {"focal_length": 13.5, "sensor_width": 7.68, "sensor_height": 6.144},
    "H20T Zoom 2x": {"focal_length": 10.14, "sensor_width": 7.41, "sensor_height": 5.56},
    "Sony ILX-LR1": {"focal_length": 24, "sensor_width": 35.7, "sensor_height": 23.8}
}
sensor = sensors["Sony ILX-LR1"]

def calculate_fov(focal_length, sensor_dimension):
    # Convert focal length and sensor dimensions from mm to meters
    focal_length_m = focal_length / 1000.0
    sensor_dimension_m = sensor_dimension / 1000.0
    # Calculate field of view in radians
    return 2 * np.arctan(sensor_dimension_m / (2 * focal_length_m))

# Calculate horizontal and vertical FoV
fov_x = calculate_fov(sensor["focal_length"], sensor["sensor_width"])
fov_y = calculate_fov(sensor["focal_length"], sensor["sensor_height"])

# Open gpslog file
gpslogfile = [filename for filename in os.listdir(inputfolder) if filename.startswith("gpslog")]
gpslogpath = os.path.join(inputfolder, gpslogfile[0])  # Use the first gpslog file

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
    def dms_to_dd(dms, ref):
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        dd = degrees + (minutes / 60) + (seconds / 3600)
        if ref in ['S', 'W']:
            dd *= -1
        return dd

    lat = geotags['GPSLatitude']
    lat_ref = geotags['GPSLatitudeRef']
    lon = geotags['GPSLongitude']
    lon_ref = geotags['GPSLongitudeRef']
    altitude = geotags.get('GPSAltitude', 0)
    heading = geotags.get('GPSImgDirection', 0)

    latitude = dms_to_dd(lat, lat_ref)
    longitude = dms_to_dd(lon, lon_ref)

    coordinates = {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "heading": heading
    }
    return coordinates

def get_xmp_data(filepath):
    xmpfile = XMPFiles(file_path=filepath, open_forupdate=False)
    xmp = xmpfile.get_xmp()
    xmp_data = {
        "absolute_altitude": None,
        "relative_altitude": None,
        "gimbal_yaw": None,
        "flight_yaw": None,
        "gimbal_pitch": None,
        "target_distance": None
    }
    
    # Extract desired XMP metadata
    for ns in xmp:
        if ns[1] == "drone-dji:AbsoluteAltitude":
            xmp_data["absolute_altitude"] = float(ns[2])
        elif ns[1] == "drone-dji:RelativeAltitude":
            xmp_data["relative_altitude"] = float(ns[2])
        elif ns[1] == "drone-dji:GimbalYawDegree":
            xmp_data["gimbal_yaw"] = float(ns[2])
        elif ns[1] == "drone-dji:FlightYawDegree":
            xmp_data["flight_yaw"] = float(ns[2])
        elif ns[1] == "drone-dji:GimbalPitchDegree":
            xmp_data["gimbal_pitch"] = float(ns[2])
        elif ns[1] == "drone-dji:LRFTargetDistance":
            xmp_data["target_distance"] = float(ns[2])

    xmpfile.close_file()
    return xmp_data

def calculate_image_position(latitude, longitude, altitude, roll, pitch, yaw, focal_length, sensor_width, sensor_height):
    # so the yaw is simple, it is degrees from north, going with the clock to 360. roll is also okay as it is degrees away 
    # from flat (camera pointing straigt down) with positive values is the drone turning to the right, meaning the camera 
    # points to the left of the position. pitch is a bit more tricky. 90 is the drone being flat, and the camera pointing 
    # straight down. above 90 is the camera pitching forward in degrees, while negative is the camera pointing backwards. 
    # correct the funciton taking this into account
    
    # Convert geographic coordinates to UTM projection
    transformer = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)
    x, y = transformer.transform(longitude, latitude)
    
    # Convert roll, pitch, yaw from degrees to radians
    roll = np.radians(roll)
    pitch = np.radians(-(pitch - 90))  # Adjust pitch by 90 to align it to pointing down
    yaw = np.radians(-yaw + 90)  # Align yaw with east and going counter-clockwise
    
    # Define individual rotation matrices
    R_yaw = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])
    
    R_roll = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])
    
    R_pitch = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    
    # Combine the rotations in the order Yaw -> Roll -> Pitch
    rotation_matrix = R_yaw @ R_roll @ R_pitch

    return x, y, rotation_matrix



def calculate_corner_positions(center_x, center_y, altitude, rotation_matrix, fov_x, fov_y):
    # Define half-angle offsets based on FoV and altitude to get distance to corners
    half_width = altitude * np.tan(fov_y / 2)
    half_height = altitude * np.tan(fov_x / 2)
    print("Half-width:", half_width)
    print("Half-height:", half_height)

    # Define corner offsets in the image plane (relative to center) with a z-axis of 0
    corners = [
        np.array([-half_width, -half_height, -altitude]),  # Bottom-left
        np.array([half_width, -half_height, -altitude]),   # Bottom-right
        np.array([half_width, half_height, -altitude]),    # Top-right
        np.array([-half_width, half_height, -altitude])    # Top-left
    ]
    
    # Debugging: print shapes to confirm
    print("Rotation matrix shape:", rotation_matrix.shape)
    print("Corner vector shape:", corners[0].shape)
    
    # Apply rotation matrix to each corner to transform to world coordinates
    corner_positions = []
    for corner in corners:
        # Ensure corner is a 3D vector
        corner = np.reshape(corner, (3, 1))
        
        # Transform corner
        transformed_corner = rotation_matrix @ corner  # Perform matrix multiplication
        
        # Extract transformed x and y and add to center
        corner_x = center_x + transformed_corner[0, 0]
        corner_y = center_y + transformed_corner[1, 0]
        corner_positions.append((corner_x, corner_y))
    
    return corner_positions

def create_georeferenced_tiff(filename, topleft, topright, bottomleft, bottomright):
    # Output filename setup
    outputfilename = os.path.join(outputfolder, filename.replace('JPG', 'TIF'))

    # Check if TIFF version exists; if not, create from JPG
    if os.path.exists(inputfolder + filename.replace('JPG', 'tif')):
        georeffilepath = inputfolder + filename.replace('JPG', 'tif')
        im = Image.open(georeffilepath)
        im.save(outputfilename, 'TIFF', compression='tiff_deflate')
    else:
        georeffilepath = inputfolder + filename
        im = Image.open(georeffilepath)
        im = im.convert('RGBA')  # Convert to RGBA to handle transparency if needed
        data = np.array(im)      # Convert to numpy array for manipulation
        im2 = Image.fromarray(data)
        im2.save(outputfilename, 'TIFF', compression='tiff_deflate')

    # Open the saved TIFF file for updating with GDAL
    ds = gdal.Open(outputfilename, gdal.GA_Update)

    # Set spatial reference to WGS84
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)

    # Define GCPs for georeferencing
    width, height = im.size
    gcps = [
        gdal.GCP(topleft[1], topleft[0], 0, 0, 0),
        gdal.GCP(topright[1], topright[0], 0, width, 0),
        gdal.GCP(bottomleft[1], bottomleft[0], 0, 0, height),
        gdal.GCP(bottomright[1], bottomright[0], 0, width, height)
    ]
    ds.SetGCPs(gcps, sr.ExportToWkt())

    # Set NoData value on the first band (assuming a single-band image)
    band = ds.GetRasterBand(1)
    nodata_value = 0
    band.SetNoDataValue(nodata_value)

    # Close the dataset to finalize changes
    ds = None

# Set up transformer for UTM to WGS84 conversion
utm_to_wgs84 = Transformer.from_crs("epsg:32632", "epsg:4326", always_xy=True)  # Replace 32632 with your UTM zone

# Initialize an empty list to store the GPS data
gpslog = []

# Open and read the GPS log line by line
with open(gpslogpath, 'r') as file:
    for line in file:
        values = line.strip().split(',')
        filename = values[0]
        latitude = float(values[1])
        longitude = float(values[2])
        altitude = float(values[3])
        roll = float(values[4])
        pitch = float(values[5])
        yaw = float(values[6])
        
        gps_entry = {
            "filename": filename,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw
        }
        gpslog.append(gps_entry)

# Example usage for each image entry
for entry in gpslog:
    latitude = entry["latitude"]
    longitude = entry["longitude"]
    altitude = entry["altitude"]
    roll = entry["roll"]
    pitch = entry["pitch"]
    yaw = entry["yaw"]

    # Get image center position and rotation matrix
    center_x, center_y, rotation_matrix = calculate_image_position(
        latitude, longitude, altitude, roll, pitch, yaw,
        sensor["focal_length"], sensor["sensor_width"], sensor["sensor_height"]
    )

    print(f"Center: X={center_x}, Y={center_y}")
    print(f"Rotation matrix:\n{rotation_matrix}")
    print(f"Altitude: {altitude}")
    print(f"Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}")
    print(f"FoV: {fov_x}° x {fov_y}°")

    # Calculate corner positions
    # Calculate corner positions in UTM
    utm_corner_positions = calculate_corner_positions(center_x, center_y, altitude, rotation_matrix, fov_x, fov_y)

    # Plot setup
    fig, ax = plt.subplots()
    ax.add_patch(patches.Circle((center_x, center_y), 5, color='blue', label="Center"))

    # Plot each corner with a circle marker
    for i, (x, y) in enumerate(utm_corner_positions, start=1):
        ax.add_patch(patches.Circle((x, y), 4, color='red', label=f"Corner {i}" if i == 1 else ""))
        ax.text(x, y, f"{i}", color="black", fontsize=12, ha='center', va='center')

    # Draw lines between corners to form the rectangle
    for i in range(4):
        x0, y0 = utm_corner_positions[i]
        x1, y1 = utm_corner_positions[(i + 1) % 4]  # Connect back to the first point
        ax.plot([x0, x1], [y0, y1], 'r--')

    # Labels and adjustments
    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_title("2D Plot of Image Center and Corners")
    ax.legend(loc="upper right")
    ax.grid(True)
    plt.show()

    # Convert UTM corners back to latitude and longitude
    wgs84_corner_positions = []
    for i, (utm_x, utm_y) in enumerate(utm_corner_positions, start=1):
        lon, lat = utm_to_wgs84.transform(utm_x, utm_y)
        wgs84_corner_positions.append((lat, lon))
        print(f"Corner {i} (WGS84): Latitude={lat}, Longitude={lon}")

    # Now you have the corner positions in WGS84 for creating the georeferenced TIFF
    create_georeferenced_tiff(
        entry["filename"],
        topleft=wgs84_corner_positions[2],
        topright=wgs84_corner_positions[1],
        bottomleft=wgs84_corner_positions[3],
        bottomright=wgs84_corner_positions[0]
    )