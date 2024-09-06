import os
import random
import shutil

def select_and_copy_random_images(source_folder, destination_folder, num_images=30):
    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Get a list of all files in the source folder
    all_files = os.listdir(source_folder)
    
    # Filter the list to include only image files
    image_files = [file for file in all_files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]
    
    # Check if there are enough images in the source folder
    if len(image_files) < num_images:
        print(f"Not enough images in the folder. Only {len(image_files)} images found.")
        selected_images = image_files
    else:
        # Randomly select the specified number of images
        selected_images = random.sample(image_files, num_images)
    
    # Copy the selected images to the destination folder
    for image in selected_images:
        source_path = os.path.join(source_folder, image)
        destination_path = os.path.join(destination_folder, image)
        shutil.copy(source_path, destination_path)
        print(f"Copied {image} to {destination_folder}")

    return selected_images

# Example usage
source_folder = 'I:/rf'
destination_folder = 'I:/rfchoosen'
selected_images = select_and_copy_random_images(source_folder, destination_folder)

print("Selected and copied images:", selected_images)
