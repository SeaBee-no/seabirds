import os
import yaml
import requests
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Get embedded EXIF data from image file."""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
    return exif_data

def get_gps_info(exif_data):
    """Extract GPS information from EXIF data."""
    if 'GPSInfo' not in exif_data:
        return None
    
    gps_info = {}
    for key in exif_data['GPSInfo'].keys():
        decode = GPSTAGS.get(key, key)
        gps_info[decode] = exif_data['GPSInfo'][key]
    
    if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info and \
       'GPSLatitudeRef' in gps_info and 'GPSLongitudeRef' in gps_info:
        lat = gps_info['GPSLatitude']
        lon = gps_info['GPSLongitude']
        lat_ref = gps_info['GPSLatitudeRef']
        lon_ref = gps_info['GPSLongitudeRef']
        
        lat = convert_to_degrees(lat)
        lon = convert_to_degrees(lon)
        
        if lat_ref != 'N':
            lat = -lat
        if lon_ref != 'E':
            lon = -lon
        
        return lat, lon
    return None

def convert_to_degrees(value):
    """Convert GPS coordinates to degrees in float format."""
    d = float(value[0].numerator) / float(value[0].denominator)
    m = float(value[1].numerator) / float(value[1].denominator)
    s = float(value[2].numerator) / float(value[2].denominator)
    return d + (m / 60.0) + (s / 3600.0)

def get_average_gps_and_first_timestamp(folder_path):
    latitudes = []
    longitudes = []
    first_timestamp = None

    images_folder = os.path.join(folder_path, 'images')
    if not os.path.exists(images_folder):
        print(f"No images folder found in {folder_path}. Skipping...")
        return None, None, None

    for root, _, files in os.walk(images_folder):
        files = sorted(files)  # Ensure files are processed in a consistent order
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg')):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        exif_data = get_exif_data(img)
                        gps_info = get_gps_info(exif_data)
                        if gps_info:
                            latitudes.append(gps_info[0])
                            longitudes.append(gps_info[1])
                        if not first_timestamp and ('DateTimeOriginal' in exif_data or 'DateTime' in exif_data):
                            timestamp = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
                            first_timestamp = timestamp
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    if latitudes and longitudes:
        avg_latitude = sum(latitudes) / len(latitudes)
        avg_longitude = sum(longitudes) / len(longitudes)
    else:
        avg_latitude = None
        avg_longitude = None

    formatted_timestamp = None
    if first_timestamp:
        try:
            date_time_obj = datetime.strptime(first_timestamp, '%Y:%m:%d %H:%M:%S')
            formatted_timestamp = date_time_obj.strftime('%Y%m%d%H%M')
        except Exception as e:
            print(f"Error formatting timestamp: {e}")

    return avg_latitude, avg_longitude, formatted_timestamp

def get_place_name(lat, lon):
    """Use Kartverket's API to get place name based on latitude and longitude."""
    url = f"https://ws.geonorge.no/stedsnavn/v1/punkt?nord={lat}&ost={lon}&koordsys=4326&radius=500&treffPerSide=500"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and 'navn' in data:
            closest = min(data['navn'], key=lambda x: x['meterFraPunkt'])
            place_name = closest['stedsnavn'][0]['skrivemåte']
            return place_name
    return None

def get_municipality_and_county(lat, lon):
    """Use Kartverket's API to get municipality and county based on latitude and longitude."""
    url = f"https://ws.geonorge.no/kommuneinfo/v1/punkt?nord={lat}&ost={lon}&koordsys=4326"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        municipality = data.get('kommunenavn', 'Unknown')
        county = data.get('fylkesnavn', 'Unknown')
        return municipality, county
    return None, None

def check_image_count(folder_path):
    """Check if the number of image files matches the count in config.seabee.yaml."""
    yaml_file = os.path.join(folder_path, 'config.seabee.yaml')
    if not os.path.exists(yaml_file):
        print(f"config.seabee.yaml not found in {folder_path}")
        return False

    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    expected_count = config.get('nfiles')
    if expected_count is None:
        print(f"nfiles not specified in {yaml_file}")
        return False

    images_folder = os.path.join(folder_path, 'images')
    image_files = [file for file in os.listdir(images_folder) if file.lower().endswith(('jpg', 'jpeg'))]
    actual_count = len(image_files)

    if actual_count == expected_count:
        return True
    else:
        print(f"Image count mismatch in {folder_path}: expected {expected_count}, found {actual_count}")
        return True

def replace_norwegian_chars(name):
    """Replace Norwegian characters æ, ø, å with ae, oe, aa."""
    name = name.replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
    name = name.replace('Æ', 'Ae').replace('Ø', 'Oe').replace('Å', 'Aa')
    return name

def rename_folders_based_on_image_data(directory):
    folders = os.listdir(directory)
    for folder in folders:
        folder_path = os.path.join(directory, folder)
        if not os.path.isdir(folder_path):
            continue
        if not check_image_count(folder_path):
            continue  # Skip folders where image count does not match the config

        avg_lat, avg_lon, first_timestamp = get_average_gps_and_first_timestamp(folder_path)
        if avg_lat is not None and avg_lon is not None:
            place_name = get_place_name(avg_lat, avg_lon)
            municipality, county = get_municipality_and_county(avg_lat, avg_lon)
            if place_name and municipality and county and first_timestamp:
                new_folder_name = f"{county}-{municipality}_{place_name}_{first_timestamp}"
                new_folder_name = replace_norwegian_chars(new_folder_name)
                new_folder_path = os.path.join(directory, new_folder_name)
                os.rename(folder_path, new_folder_path)
                print(f"Renamed {folder} to {new_folder_name}")
            else:
                print(f"Could not retrieve full data to rename folder {folder}")
        else:
            print(f"No GPS data found in the images for folder {folder}")

# Example usage:
directory = 'I:/oskar'
rename_folders_based_on_image_data(directory)
