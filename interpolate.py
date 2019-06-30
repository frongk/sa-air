import pandas
import pickle

INTERPOLATION_MAPPING_FILE = 'mapping_coordinates/traffic_map_20.pkl'

DATA_FILE = 'data/SATRIP_detectionsummary.csv'
GRID_FILE = 'data/interpolation_grid_20.csv'

GROUP_FIELDS = ['AssetNum']
DATA_FIELDS = ['Volume', 'Occupancy', 'Speed']

OUTPUT_DATA_PATH = 'data'
OUTPUT_DATA_SET_NAME = 'mean_traffic.csv'

ADDITIONAL_JOIN_CRITERIA = []
def dist_interpolate(dist_weights, values):
    return 1

grid = pandas.read_csv(GRID_FILE,index_col = 0)
data_raw = pandas.read_csv(DATA_FILE)
data_sum = data_raw.groupby(GROUP_FIELDS).sum()[DATA_FIELDS]
data_mean = data_raw.groupby(GROUP_FIELDS).mean()[DATA_FIELDS]

mapping_dict = pickle.load(open(INTERPOLATION_MAPPING_FILE,'rb'))

grid_interpolation_output = []
for point in grid.index:
    weight_set = mapping_dict[point]['weight_vals']
    idx_set = mapping_dict[point]['triangle_idx']
    values = data_sum.loc[idx_set].transpose()
    
    output_vals = [point] + list((values*weight_set).sum(axis=1)/sum(weight_set))
    grid_interpolation_output.append(output_vals)
    
    
out_df = pandas.DataFrame.from_records(grid_interpolation_output, columns=['Index'] + DATA_FIELDS)

out_df.set_index('Index',inplace=True)
out_df.to_csv(f'{OUTPUT_DATA_PATH}/{OUTPUT_DATA_SET_NAME}.csv')
