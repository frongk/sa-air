import pandas
import pickle

from tqdm import tqdm

INTERPOLATION_MAPPING_FILE = 'mapping_coordinates/energy_map_sa_100.pkl'

DATA_FILE = 'data/energy/energy_aggs/agg_agg_may_2017.csv'
GRID_FILE = 'data/interpolation_grid_100.csv'
GRID_INDEX = ['Index']
DATA_FIELDS = ['a.lp_value']
DATA_INDEX = ['b.u_id']

# time filters
DATE_NAME = 'date'
DATE_FILTER = 20170527

TIME_NAME = 'hour'
TIME_FILTER = 7

OUTPUT_DATA_PATH = 'data'
OUTPUT_DATA_SET_NAME = 'mapgen_energy.csv'

grid = pandas.read_csv(GRID_FILE,index_col = 0)
raw_data = pandas.read_csv(DATA_FILE)
data = raw_data[(raw_data[DATE_NAME]==DATE_FILTER) &
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
