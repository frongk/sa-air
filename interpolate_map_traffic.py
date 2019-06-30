import pandas
import pickle

from tqdm import tqdm

INTERPOLATION_MAPPING_FILE = 'mapping_coordinates/traffic_map_sa_100.pkl'

DATA_FILE = 'data/traffic/traffic_data.csv'
GRID_FILE = 'data/interpolation_grid_100.csv'
GRID_INDEX = ['Index']
DATA_FIELDS = ['Volume', 'Occupancy', 'Speed']
DATA_INDEX = ['AssetNum']

# time filters
WEEKDAY_NAME = 'Weekday'
WEEKDAY_FILTER = 5

TIME_NAME = 'Time'
TIME_FILTER = 7

OUTPUT_DATA_PATH = 'data'
OUTPUT_DATA_SET_NAME = 'mapgen_traffic.csv'

grid = pandas.read_csv(GRID_FILE,index_col = 0)
raw_data = pandas.read_csv(DATA_FILE)
data = raw_data[(raw_data[WEEKDAY_NAME]==WEEKDAY_FILTER) &
                (raw_data[TIME_NAME]==TIME_FILTER)]
data.set_index(DATA_INDEX, inplace=True)

mapping_dict = pickle.load(open(INTERPOLATION_MAPPING_FILE,'rb'))

grid_interpolation_output = []
for point in tqdm(grid.index):
    weight_set = mapping_dict[point]['weight_vals']
    idx_set = mapping_dict[point]['triangle_idx']
    values = data[DATA_FIELDS].loc[idx_set].transpose()
    
    output_vals = [point] + list((values*weight_set).sum(axis=1)/sum(weight_set))
    grid_interpolation_output.append(output_vals)
    
    
out_df = pandas.DataFrame.from_records(grid_interpolation_output, columns=GRID_INDEX + DATA_FIELDS)

out_df.set_index(*GRID_INDEX,inplace=True)
out_df.to_csv(f'{OUTPUT_DATA_PATH}/{OUTPUT_DATA_SET_NAME}.csv')
