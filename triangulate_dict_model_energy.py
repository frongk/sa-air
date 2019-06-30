import pandas
import numpy
import os

from tqdm import tqdm

import pickle
import pdb

COORD_MAPPING_PATH = 'mapping_coordinates'
INTERPOLATION_GRID_FILE_ID = 'data/weather_station_grid.csv'
GRID_INDEX = 'Site ID'

DATASET_FILE_ID = 'data/energy_sites_grid.csv'
DATASET_INDEX = 'b.u_id'
LAT_NAME = 'b.lat'
LON_NAME = 'b.long'

NEAREST_COORDINATE_NO = 3

MAPPING_FILE_ID = f'{COORD_MAPPING_PATH}/energy_map_20.pkl'

# vectorized haversine function
def haversine(coord1, coord2, to_radians=True, earth_radius=6371):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    https://stackoverflow.com/questions/43577086/pandas-calculate-haversine-distance-within-each-group-of-rows
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    if to_radians:
        lat1, lon1, lat2, lon2 = numpy.radians([lat1, lon1, lat2, lon2])

    a = numpy.sin((lat2-lat1)/2.0)**2 + \
        numpy.cos(lat1) * numpy.cos(lat2) * numpy.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * numpy.arcsin(numpy.sqrt(a))

# generate weightings for interpolation
def weighting_generator(distance_set):
    """
    returns weights for making triangular interpolation calculations easier
    """
    weights = [1/dist for dist in distance_set]
    return weights

# generate weightings for interpolation
def weighting_generator(distance_set):
    """
    returns barycentric weights for making triangular interpolation calculations easier
    """
    weights = [1/dist for dist in distance_set]
    return weights

if not os.path.exists(COORD_MAPPING_PATH):
    os.mkdir(COORD_MAPPING_PATH)

grid = pandas.read_csv(INTERPOLATION_GRID_FILE_ID)
grid.set_index(GRID_INDEX, inplace=True)

data_set = pandas.read_csv(DATASET_FILE_ID)
data_locations = data_set[[DATASET_INDEX, LAT_NAME, LON_NAME]].drop_duplicates()
data_locations.set_index(DATASET_INDEX, inplace=True)


mapping_points = {}

for idx, point in tqdm(grid.iterrows(), desc='connecting points'):
    coord1 = tuple(point)[-2:]
    distances = data_locations.apply(lambda x: haversine(coord1, (x[LAT_NAME],x[LON_NAME]), to_radians=True), axis=1)

    closest_triangle = distances.sort_values(ascending=True).iloc[:NEAREST_COORDINATE_NO]
    triangle_idx = closest_triangle.index
    distances = closest_triangle.values
    weights = weighting_generator(distances)

    mapping_points[point.name] = {
                                'triangle_idx':triangle_idx.tolist(),
                                'distance_vals':distances.tolist(),
                                'weight_vals':weights,
                               }

with open(MAPPING_FILE_ID, 'wb') as map_file:
    pickle.dump(mapping_points, map_file)
