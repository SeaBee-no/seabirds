import os
import yaml

# Define the root folder where the mission folders are stored
root_folder = "/home/notebook/shared-seabee-ns9879k/seabirds/2024"

# List to hold the missions with the "habitat" theme
missions_with_habitat = []

# Traverse the directory
for root, dirs, files in os.walk(root_folder):
    if "config.seabee.yaml" in files:
        config_path = os.path.join(root, "config.seabee.yaml")
        try:
            with open(config_path, 'r') as file:
                config_data = yaml.safe_load(file)
                if config_data.get('theme') == "Habitat":
                    missions_with_habitat.append(root)
        except Exception as e:
            print(f"Error reading {config_path}: {e}")

# Display missions with the habitat theme
print("Missions with the 'habitat' theme:")
for mission in missions_with_habitat:
    print(mission)