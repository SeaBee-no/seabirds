from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import psycopg2
import json

with open('/home/sindre.molvarsmyr/credentials.json', 'r') as file:
    cred = json.load(file)

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    dbname=cred["dbname"],
    user=cred["user"],
    password=cred["password"],
    host=cred["host"],
    port=cred["port"]
)

# Create a new cursor
cursor = connection.cursor()
select_query = "SELECT * FROM annoteringer"
cursor.execute(select_query)
records = cursor.fetchall()

# Close the cursor and connection
cursor.close()
connection.close()

data = records[1][3]

def index(request):
    return HttpResponse("Hello, world. You're at the polls index."+str(data))