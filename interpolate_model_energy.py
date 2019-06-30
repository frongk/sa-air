import pandas
import pickle
import os

from tqdm import tqdm

INTERPOLATION_MAPPING_FILE = 'mapping_coordinates/energy_map.pkl'

DATA_DIR = 'data/energy/energy_aggs'
DATA_KEY = 'b.u_id'

GRID_FILE = 'data/air_monitoring/Site_Censor_Model_Data.csv'
GRID_KEY = 'Site ID'

DATA_FIELDS = ['a.lp_value']
JOIN_CRITERIA = {
                 'DATA_FILE':['date', 'hour'],
                 'GRID_FILE':['Date', 'Time']
                }

OUTPUT_FILE_ID = 'data/model_data_w_energy.csv'

def dist_interpolate(dist_weights, values):
    return 1

grid = pandas.read_csv(GRID_FILE)
grid.set_index([GRID_KEY, *JOIN_CRITERIA['GRID_FILE']], inplace=True)

mapping_dict = pickle.load(open(INTERPOLATION_MAPPING_FILE,'rb'))

grid_interpolation_output = []
error_points = []
for file_id in tqdm(os.listdir(DATA_DIR), desc='file_level'):
    file_id = f'{DATA_DIR}/{file_id}'
    data = pandas.read_csv(file_id)
    data.set_index([DATA_KEY,*JOIN_CRITERIA['DATA_FILE']], inplace=True) 
    
    min_date = data.index.get_level_values(JOIN_CRITERIA['DATA_FILE'][0]).min()
    max_date = data.index.get_level_values(JOIN_CRITERIA['DATA_FILE'][0]).max()

    grid_filter = grid.query(f'{JOIN_CRITERIA["GRID_FILE"][0]} >= {min_date} and \
                               {JOIN_CRITERIA["GRID_FILE"][0]} <= {max_date}').index

    for point in tqdm(grid_filter, desc='grid_level'):
        site = point[0]
        day = point[1]
        time = point[2]
        
        weight_set = mapping_dict[site]['weight_vals']
        idx_set = mapping_dict[site]['triangle_idx']
        values = data.loc[idx_set,day,time][DATA_FIELDS].transpose()
        
        try:
            output_vals = list(point) + list((values*weight_set).sum(axis=1)/sum(weight_set))
            grid_interpolation_output.append(output_vals)
        except:
            error_points.append(point)

interp_df = pandas.DataFrame(grid_interpolation_output, 
                             columns=[GRID_KEY, *JOIN_CRITERIA['GRID_FILE'], *DATA_FIELDS])
interp_df.set_index([GRID_KEY, *JOIN_CRITERIA['GRID_FILE']], inplace=True)

interp_joined_data = grid.join(interp_df)
interp_joined_data.to_csv(OUTPUT_FILE_ID)
