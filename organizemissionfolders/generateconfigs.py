import os
import yaml
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def extract_info_from_filename(filename):
    parts = filename.split('_')
    grouping = parts[0].lower()
    area = parts[1].lower() if len(parts) > 1 else 'Unknown'

    # Specific replacements for 'grouping'
    if grouping == 'troendelag-froeya':
        grouping = 'Trøndelag-Frøya'
    elif grouping == 'troendelag-oerland':
        grouping = 'Trøndelag-Ørland'
    else:
        grouping = grouping.replace('ae', 'æ').replace('oe', 'ø').replace('aa', 'å').title()#.replace('-', ' ')

    # Capitalize first letter of area, replace 'ae', 'oe', 'aa', and hyphens
    area = area.replace('ae', 'æ').replace('oe', 'ø').replace('aa', 'å').title().replace('-', ' ')
    
    return grouping, area

def get_first_timestamp(images_folder):
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    if not image_files:
        return 'Unknown'
    
    image_files.sort()  # Sort the files to get the earliest one
    first_image = image_files[0]
    first_image_path = os.path.join(images_folder, first_image)
    
    # Extracting datetime from the first image's EXIF data
    try:
        with Image.open(first_image_path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        datetime_str = value.replace(':', '').replace(' ', '')
                        return datetime_str[:12]
    except Exception as e:
        print(f"Could not extract date from {first_image}: {e}")
    
    return 'Unknown'

def count_files_in_folder(folder):
    return len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])

def create_config_file(root_folder):
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        
        if os.path.isdir(folder_path):
            images_folder = os.path.join(folder_path, 'images')
            
            if not os.path.exists(images_folder):
                print(f"No images folder found in {folder}. Skipping...")
                continue

            grouping, area = extract_info_from_filename(folder)
            datetime_str = get_first_timestamp(images_folder)
            nfiles = count_files_in_folder(images_folder)

            config_data = {
                'grouping': grouping,
                'area': area,
                'datetime': datetime_str,
                'nfiles': nfiles,
                'organisation': 'Karmøy Ringmerkingsgruppe',
                'creator_name': 'Oskar Bjørnstad',
                'mosaic': True,
                'classify': True,
                'publish': True,
                'theme': 'Seabirds'
                # 'odm_options': {
                #     'fast-orthophoto': True,
                # }
            }

            config_file_path = os.path.join(folder_path, 'config.seabee.yaml')
            with open(config_file_path, 'w', encoding='utf-8') as config_file:
                yaml.dump(config_data, config_file, default_flow_style=False, indent=2, allow_unicode=True)

            print(f"Created/Updated config file at {config_file_path}")

# Example usage
root_folder = 'I:/oskar'
create_config_file(root_folder)
