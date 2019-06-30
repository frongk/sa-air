import pandas

import plotly
import plotly.graph_objs as go
from SECRETS import mapbox_token

MAP_DATA_FILE = 'data/map_data.csv'

LAT_NAME = 'Latitude'
LON_NAME = 'Longitude'
CENTER = (29.419795,-98.4978487)

X_DIFF = 
Y_DIFF = 0.018435000000000

PLOT_OUTPUT_NAME = 'plots/test_map.html'

def make_boxes(idx, gps_coord, x_diff, y_diff):
    lat = gps_coord[0]
    lon = gps_coord[1]
    a = [lat-0.5*y_diff, lon-0.5*x_diff]
    b = [lat-0.5*y_diff, lon+0.5*x_diff]
    c = [lat+0.5*y_diff, lon-0.5*x_diff]
    d = [lat+0.5*y_diff, lon+0.5*x_diff]
    name = idx
    return {idx:[a,b,c,d]}

def color_map(input_val, min_=20, max_=37):
    range_ = max_-min_
    value = max((input_val-min_)/range_ ,0)
    #return f'rgb({value*255},{value*255},{value*255})'
    return f'rgb({255-value*255}, 0, 0)'

# for plotting geographic data
def plot_gps_points(lat, lon, vals):
    data = [
            go.Scattermapbox(
                             lat=lat,
                             lon=lon,
                             mode='markers',
                             marker=go.scattermapbox.Marker(
                                      color=list(map(color_map, vals)),
                                      opacity=0.5,
                                      size=20)
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

map_data = pandas.read_csv(MAP_DATA_FILE)
plot_gps_points(map_data[LAT_NAME], map_data[LON_NAME], map_data['PM2.5'])
