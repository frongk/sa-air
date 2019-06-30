import pandas 
import numpy
import pickle

DATA_DIR = 'data'
MAP_FILES = [
             'elevation_100.csv',
             'mapgen_weather.csv',
             'mapgen_energy.csv',
             'mapgen_traffic.csv'
            ]

WEEKDAY = 5
MONTH = 5
TIME = 7

DATA_INDEX = 'Index'

MODEL_FILE = 'model/xgboost_PM2.5.pkl'
MAP_DATA_FILE_ID = 'data/map_data_traffic_scenario.csv'

data_load = []
for file_ in MAP_FILES:
    data_load.append(pandas.read_csv(f'{DATA_DIR}/{file_}'))
    
dataset = pandas.concat(data_load, axis=1)
# dataset.set_index(DATA_INDEX, inplace=True)

dataset = dataset.assign(Weekday = numpy.ones(dataset.shape[0])*WEEKDAY)
dataset = dataset.assign(Month = numpy.ones(dataset.shape[0])*MONTH)
dataset = dataset.assign(Time = numpy.ones(dataset.shape[0])*TIME)

dataset['t'] = (dataset['t']-273.15)*9/5+32

dataset.rename(columns={'t':'Outdoor Temperature',
                        'gust':'Wind Speed - Scalar'
                       },
               inplace=True)

dataset[['Volume','Occupancy','Speed']] = 1.2*dataset[['Volume','Occupancy','Speed']]

model, model_input_vars = pickle.load(open(MODEL_FILE,'rb'))
input_data = dataset[model_input_vars].copy()
pollution_prediction = model.predict(input_data)

map_data = dataset[['Latitude', 'Longitude']]
map_data['PM2.5'] = pollution_prediction  

map_data.to_csv(MAP_DATA_FILE_ID)
