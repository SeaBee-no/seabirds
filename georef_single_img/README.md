# README
The newest file is georefsingleimageGPSLOG.py, which is the one we will describe here. 
Currently it only takes the altitude from the drone, which is relative to take-off. We need real altitude to be integrated.

ChatGPTs explanaition of the code:

## Overview
This project is focused on georeferencing images from a drone using GPS logs. The newest file, `georefsingleimageGPSLOG.py`, is the main script that processes image files by extracting GPS coordinates, orientation data (yaw, pitch, and roll), and additional metadata, and uses these to georeference the images. The georeferenced images can then be used in GIS applications or mapping software.

## Description of `georefsingleimageGPSLOG.py`

### Key Features
- **GPS Data Extraction**: Extracts GPS coordinates, altitude, and yaw, pitch, and roll angles for each image from a GPS log file.
- **Field of View Calculation**: Computes the horizontal and vertical field of view (FoV) for each image based on sensor parameters.
- **Rotation Matrix Calculation**: Constructs a rotation matrix based on yaw, pitch, and roll to determine the orientation of the image.
- **Corner Position Calculation**: Calculates the georeferenced positions of the four corners of each image using the calculated rotation matrix and FoV.
- **Image Georeferencing**: Georeferences the image using GDAL, adding Ground Control Points (GCPs) based on the calculated corner positions in WGS84.

### How the Script Works

1. **Sensor Setup**: Sensor parameters for different cameras are defined, including focal length, sensor width, and height, which are used to calculate the field of view.
2. **Field of View Calculation**:
    - The field of view is calculated in radians for both horizontal and vertical axes based on the focal length and sensor dimensions.
3. **GPS Log Extraction**:
    - The script scans for a GPS log file in the input directory. This log file should contain image filenames, latitude, longitude, altitude, roll, pitch, and yaw values.
    - Each entry in the GPS log is loaded and stored in a list.
4. **Rotation Matrix and Position Calculation**:
    - For each image, the yaw, pitch, and roll values are adjusted based on drone orientation, and a rotation matrix is computed. This matrix is applied to align the image with global coordinates.
5. **Corner Georeferencing**:
    - Using the rotation matrix and field of view, the script calculates the projected positions of each corner in UTM.
    - These UTM coordinates are then converted back to latitude and longitude (WGS84) for use in the image georeferencing step.
6. **Georeferencing the Image**:
    - The image is loaded, and its corners are annotated with the calculated latitude and longitude GCPs.
    - The image is saved as a georeferenced TIFF file in the specified output folder.

### Code Walkthrough

#### Sensor Parameters
In the script, several sensors and their focal lengths, widths, and heights are defined in `mm`. These are used to set the correct field of view for each image.

#### Field of View Calculation
The `calculate_fov` function takes in the focal length and sensor dimension (width or height) to calculate the field of view for both horizontal and vertical axes, ensuring the image is correctly scaled in global coordinates.

#### GPS Log Parsing
The script reads a GPS log file, expected in CSV format, where each row contains:
   - **Filename**: The image name associated with the GPS coordinates.
   - **Latitude, Longitude, Altitude**: Geographic coordinates for the image location.
   - **Roll, Pitch, Yaw**: Orientation data for the image.

This information is stored in a list to be accessed later during image processing.

#### Georeferencing Process
For each image entry:
1. **Image Center and Orientation Calculation**: 
   - The latitude and longitude are converted to UTM, serving as the image center.
   - The yaw, pitch, and roll values are converted to a rotation matrix to properly orient the image.
2. **Corner Position Calculation**:
   - The script calculates the UTM positions of each corner based on the altitude, field of view, and orientation.
   - These UTM positions are converted back to latitude and longitude.
3. **Image Saving**:
   - Using GDAL, the image is loaded and the Ground Control Points (GCPs) are set for each corner using the calculated latitude and longitude values.
   - The georeferenced image is saved as a TIFF file.

### Example Usage
To run the script, place your images and GPS log file in the `inputfolder` directory. The script will generate georeferenced TIFF files in the `outputfolder`.

```bash
python georefsingleimageGPSLOG.py
```

## Customization
- **Sensor Parameters**: Adjust focal length and sensor dimensions in the `sensors` dictionary if you use different cameras.
- **Projection Systems**: Change the EPSG codes for UTM or WGS84 if your project requires different coordinate systems.

## Example Output from a Mission without RTK
![Animation](img/animation.gif?raw=true "Animation")
![Img0](img/img0.png?raw=true "Img0")
![Img1](img/img1.png?raw=true "Img1")
![Img2](img/img2.png?raw=true "Img2")
![Img3](img/img3.png?raw=true "Img3")

