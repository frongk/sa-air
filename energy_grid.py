import pandas
import os

import plotly
import plotly.graph_objs as go
from SECRETS import mapbox_token

FILE_DIR = 'data/energy/energy_aggs'
OUTPUT_FILE_ID = 'data/energy_sites_grid.csv'

KEY = 'b.u_id'
LAT_NAME = 'b.lat'
LON_NAME = 'b.long'


CENTER = (29.419795,-98.4978487)
PLOT_OUTPUT_NAME = 'plots/energy measurements.html'

# for plotting geographic data
def plot_gps_points(lat, lon):
    data = [
            go.Scattermapbox(
                             lat=lat,
                             lon=lon,
                             mode='markers',
                             marker=go.scattermapbox.Marker(size=15)
                            )
           ]
    layout = go.Layout(
                autosize=True,
                hovermode='closest',
                    mapbox=go.layout.Mapbox(
                        accesstoken=mapbox_token,
                        bearing=0,
                        center=go.layout.mapbox.Center(
                            lat=CENTER[0],
                            lon=CENTER[1]
                        ),
                        pitch=0,
                        zoom=10
                    ),
                )
    
    
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=PLOT_OUTPUT_NAME)
 
# iterate through all files to make sure all sites are captured
inconsistent_sites = pandas.DataFrame()
for idx, file_id in enumerate(os.listdir(FILE_DIR)):
    file_id = f'{FILE_DIR}/{file_id}'
    print(file_id)
    if idx == 0:
        unique_sites = pandas.read_csv(file_id)[[KEY, LAT_NAME, LON_NAME]].drop_duplicates()
        
    new_data = pandas.read_csv(file_id)[[KEY, LAT_NAME, LON_NAME]].drop_duplicates()

    new_sites = new_data[~new_data[KEY].isin(unique_sites[KEY])]
    missing_sites = unique_sites[~unique_sites[KEY].isin(new_data[KEY])]

    unique_sites = pandas.concat((unique_sites, new_sites), axis=0)
    inconsistent_sites = pandas.concat((inconsistent_sites, missing_sites), axis=0)
    
# filter out inconsistent sites
best_sites = unique_sites[~unique_sites[KEY].isin(inconsistent_sites[KEY])]

# generate output file
best_sites.to_csv(OUTPUT_FILE_ID)

# plot 
plot_gps_points(best_sites[LAT_NAME], best_sites[LON_NAME])
