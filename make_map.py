import pandas

import plotly
import plotly.graph_objs as go
from SECRETS import mapbox_token

MAP_DATA_FILE = 'data/map_data.csv'

LAT_NAME = 'Latitude'
LON_NAME = 'Longitude'
CENTER = (29.419795,-98.4978487)

PLOT_OUTPUT_NAME = 'plots/test_map_tr_ctrl.html'

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
                                      size=20),
                            text = ['PM2.5: ' + str(x) for x in vals]
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
                        zoom=10.5
                    ),
                margin=go.layout.Margin(
                    l=10,
                    r=10,
                    b=10,
                    t=20,
                    pad=4
                            )
                  )
    
    
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=PLOT_OUTPUT_NAME)

map_data = pandas.read_csv(MAP_DATA_FILE)
plot_gps_points(map_data[LAT_NAME], map_data[LON_NAME], map_data['PM2.5'])
