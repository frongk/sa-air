import pandas
import requests
from bs4 import BeautifulSoup

from tqdm import tqdm
import time

GRID_FILE_ID = 'data/interpolation_grid_100.csv'
OUTPUT_FILE_ID = 'data/elevation_100.csv'

grid_points = pandas.read_csv(GRID_FILE_ID)

elevation_list = []
for _, row in tqdm(grid_points.iterrows()):
    lat = row['Latitude']
    lon = row['Longitude']
    idx = row['Index']

    url = f'https://ned.usgs.gov/epqs/pqs.php?x={lon}&y={lat}&units=Meters&output=xml'

    
    resp = requests.get(url)
    while not resp.ok:
        print("bad response")
        print(resp)
        time.sleep(10)
        resp = requests.get(url)

    soup = BeautifulSoup(resp.text, "xml")
    elevation = float(soup.Elevation.text)
    elevation_list.append((idx, lat, lon, elevation))
    time.sleep(1)

df_elevation = pandas.DataFrame(elevation_list, columns=['Index','Latitude','Longitude','Elevation'])
df_elevation.to_csv(OUTPUT_FILE_ID)

