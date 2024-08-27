import os
import geopandas as gpd
import psycopg2
from psycopg2 import sql
from dbconnection import *
import shapely.wkb
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def process_gpkg_file(gpkg_file):
    comment = ''
    modelversion = '20240131-nina_seabirds_rgb_20240130'

    logger.info(f"Reading file: {gpkg_file}")
    gdf = gpd.read_file(gpkg_file)
    logger.info(f"File read successfully with {len(gdf)} records")

    # Transform geometries to WGS84 (EPSG:4326)
    gdf = gdf.to_crs(epsg=4326)

    # Check the structure of the GeoDataFrame
    logger.info(f"Columns in the GeoDataFrame: {gdf.columns}")

    # Connect to the database
    conn = psycopg2.connect(**db_params)

    # Step 3: Insert data into PostgreSQL
    cur = conn.cursor()

    for index, row in gdf.iterrows():
        try:
            # Convert geometry to WKB format
            geom_wkb = shapely.wkb.dumps(row.geometry, hex=True)

            # Prepare the SQL query. You'll need to modify this based on your table structure and data
            insert_query = sql.SQL("""
                INSERT INTO detections (geom, filename, species, activity, sex, age, visibleonimage, modelversion, score_species, manuallyverified, comment)
                VALUES (ST_GeomFromWKB(%s::geometry), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)

            # Extract the desired filename part
            full_filename = row['TEMP_image_filename']
            filename = os.path.basename(full_filename)
            filename = os.path.splitext(filename)[0]  # Remove the file extension

            # Log the row data
            logger.info(f"Processing row {index}: filename={filename}, species={row['species']}")

            # Values to insert - adjusting for potential non-existent columns
            values = (
                geom_wkb, 
                filename, 
                row['species'] if 'species' in row and pd.notnull(row['species']) and row['species'] != '' else 0, # species
                0, #row['activity'] if 'activity' in row and pd.notnull(row['activity']) and row['activity'] != '' else 0, # activity
                0, # sex
                0, # age
                True, 
                modelversion,
                row['score_species'] if 'score_species' in row and pd.notnull(row['score_species']) else 0,
                False,
                comment
            )

            # Log the SQL query and values
            logger.debug(f"SQL query: {cur.mogrify(insert_query, values)}")

            cur.execute(insert_query, values)

        except Exception as e:
            logger.error(f"Error inserting row {index} from file {gpkg_file}: {e}")
            logger.debug(f"SQL query: {cur.mogrify(insert_query, values)}")

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def add_from_gpkg_folder_or_file(gpkg_input):
    if os.path.isfile(gpkg_input):
        # If the input is a single file, process that file
        process_gpkg_file(gpkg_input)
    elif os.path.isdir(gpkg_input):
        # If the input is a directory, process all GPKG files in that directory and its subdirectories
        for root, dirs, files in os.walk(gpkg_input):
            for file in files:
                if file.endswith('.gpkg'):
                    logger.info(f"Found file: {os.path.join(root, file)}")
                    process_gpkg_file(os.path.join(root, file))
    else:
        raise ValueError("The input should be either a GPKG file or a directory containing GPKG files.")

# Example usage for a single file
#gpkg_file = '/mnt/data/out.gpkg'
# Example usage for a folder
gpkg_folder = 'C:/detections'

# To process a single file
#add_from_gpkg_folder_or_file(gpkg_file)

# To process all GPKG files in a folder
add_from_gpkg_folder_or_file(gpkg_folder)
