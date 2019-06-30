import pandas

import plotly
import plotly.graph_objs as go
from SECRETS import mapbox_token

TRAFFIC_FILE_ID = 'data/traffic/traffic_data.csv'
FILTER_FIELDS = ['AssetNum','Latitude','Longitude']
LAT_NAME = 'Latitude'
LON_NAME = 'Longitude'
CENTER = (29.419795,-98.4978487)

OUTPUT_FILE_ID = 'data/traffic_grid.csv'


PLOT_OUTPUT_NAME = 'plots/traffic_measurements.html'

# for plotting geographic data
def plot_gps_points(lat, lon):
    data = [
            go.Scattermapbox(
                             lat=lat,
                             lon=lon,
                             mode='markers',
                             marker=go.scattermapbox.Marker(size=24)
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
 
raw_df = pandas.read_csv(TRAFFIC_FILE_ID)
grid = raw_df[FILTER_FIELDS].drop_duplicates()
grid.to_csv(OUTPUT_FILE_ID)

plot_gps_points(grid[LAT_NAME], grid[LON_NAME])
