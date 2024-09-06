import os
import shutil

def move_images_to_subfolder(root_folder):
    # Iterate over each subfolder in the root folder
    for subdir, _, files in os.walk(root_folder):
        # Skip if the subfolder is already named 'images'
        if os.path.basename(subdir) == 'images':
            continue
        
        # Create the 'images' subfolder if it doesn't exist
        images_folder = os.path.join(subdir, 'images')
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        
        # Move each image file to the 'images' subfolder
        for file in files:
            # Check if the file is an image (you can add more extensions if needed)
            if file.lower().endswith(('.dng')):
                #move to other folder
                raw_folder = os.path.join(subdir, 'other/raw')
                if not os.path.exists(raw_folder):
                    os.makedirs(raw_folder)
                src_file = os.path.join(subdir, file)
                dst_file = os.path.join(raw_folder, file)
                shutil.move(src_file, dst_file)
                print(f"Moved {file} to {raw_folder}")
            else:
                src_file = os.path.join(subdir, file)
                dst_file = os.path.join(images_folder, file)
                shutil.move(src_file, dst_file)
                print(f"Moved {file} to {images_folder}")

# Example usage
root_folder = 'I:/oskar'
move_images_to_subfolder(root_folder)
