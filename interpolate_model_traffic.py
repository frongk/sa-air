import pandas
import pickle
import os

from tqdm import tqdm

INTERPOLATION_MAPPING_FILE = 'mapping_coordinates/traffic_map.pkl'

DATA_FILE = 'data/traffic/traffic_data.csv'
DATA_KEY = 'AssetNum'
EXTRA_INDEX = ['Date']

GRID_FILE = 'data/model_data_w_energy.csv'
GRID_KEY = 'Site ID'

DATA_FIELDS = ['Volume','Occupancy','Speed']
JOIN_CRITERIA = {
                 'DATA_FILE':['Weekday', 'Time'],
                 'GRID_FILE':['Weekday', 'Time']
                }

FINAL_JOIN = ['Date', 'Time']
OUTPUT_FILE_ID = 'data/model_data_w_energy_traffic.csv'

grid = pandas.read_csv(GRID_FILE)
grid.set_index([GRID_KEY, *EXTRA_INDEX, *JOIN_CRITERIA['GRID_FILE']], inplace=True)

mapping_dict = pickle.load(open(INTERPOLATION_MAPPING_FILE,'rb'))

data = pandas.read_csv(DATA_FILE)
data.set_index([DATA_KEY,*JOIN_CRITERIA['DATA_FILE']], inplace=True) 

grid_interpolation_output = []
error_points = []
for point in tqdm(grid.index, desc='grid_level'):
    try:
        site = point[0]
        day = point[1+len(EXTRA_INDEX)] 
        time = point[2+len(EXTRA_INDEX)]
        
        weight_set = mapping_dict[site]['weight_vals']
        idx_set = mapping_dict[site]['triangle_idx']
        values = data.loc[idx_set,day,time][DATA_FIELDS].transpose()
        
        output_vals = list(point) + list((values*weight_set).sum(axis=1)/sum(weight_set))
        grid_interpolation_output.append(output_vals)
    except:
        error_points.append(point)

interp_df = pandas.DataFrame(grid_interpolation_output, 
                             columns=[GRID_KEY, *EXTRA_INDEX, *JOIN_CRITERIA['GRID_FILE'], *DATA_FIELDS])
interp_df.set_index([GRID_KEY, *EXTRA_INDEX, *JOIN_CRITERIA['GRID_FILE']], inplace=True)

interp_joined_data = grid.join(interp_df)

interp_joined_data.to_csv(OUTPUT_FILE_ID)
