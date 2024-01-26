import geopandas as gpd
import psycopg2
from psycopg2 import sql
from dbconnection import *
import shapely.wkb

# Step 1: Read GPKG file
gpkg_file = 'C:/Users/sindre.molvarsmyr/Downloads/out_VAL.gpkg'
#gpkg_file = 'C:/dronedetections/per20230925.gpkg'
gdf = gpd.read_file(gpkg_file)

# Connect to the database
conn = psycopg2.connect(**db_params)

# Step 3: Insert data into PostgreSQL
cur = conn.cursor()

for index, row in gdf.iterrows():
    # Convert geometry to WKB format
    geom_wkb = shapely.wkb.dumps(row.geometry, hex=True)

    # Prepare the SQL query. You'll need to modify this based on your table structure and data
    insert_query = sql.SQL("""
        INSERT INTO detections (geom, filename, species, activity, sex, age, visibleonimage, modelversion, score_species, score_activity, score_sex, score_age, manuallyverified, comment)
        VALUES (ST_GeomFromWKB(%s::geometry), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
    insert_query = sql.SQL("""
        INSERT INTO detections (geom, filename, species, activity, sex, age, visibleonimage, modelversion, score_species, manuallyverified, comment)
        VALUES (ST_GeomFromWKB(%s::geometry), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)

    filename = row['TEMP_image_filename']
    filename = filename.replace("2022/","")
    filename = filename.replace("2023/","")
    filename = filename.replace("seabirds/","")
    filename = filename.replace("/orthophoto/odm_orthophoto.original.tif","")
    filename = filename.replace("/odm_orthophoto/odm_orthophoto.original.tif","")
    
    # Values to insert - replace 'row.<fieldname>' with actual field names from your GPKG file
    values = (
        geom_wkb, 
        filename, 
        0, #row['species'], # species
        0,
        0,
        0,
        True, 
        '20240126',
        row['score_species'],
        False,
        'val'
    )

    cur.execute(insert_query, values)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
