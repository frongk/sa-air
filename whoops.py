# i need to add a weekday field to the model data after 
# i spent hours interpolating over the energy data
# this is a datathon and revisions are low priority (shrug)

import pandas
from datetime import datetime

INPUT_FILE_ID = 'data/model_data_w_energy.csv'
OUTPUT_FILE_ID = 'data/model_data_w_energy.csv'

def weekday_maker(date_int):
    date_obj = datetime.strptime(str(date_int), '%Y%m%d')
    return date_obj.weekday()

df = pandas.read_csv(INPUT_FILE_ID)
df['Weekday'] = df['Date'].apply(weekday_maker)
df.to_csv(OUTPUT_FILE_ID)
