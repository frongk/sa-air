# extract unique weather station coordinates by Site ID
# these will be loaded into triangulation mapping script
# *triangulate_dict.py* which will be used to ultimately
# interpolate values for where the stations are

import pandas

import plotly
import plotly.graph_objs as go

from SECRETS import mapbox_token

DATA_FILE_ID = 'data/air_monitoring/Site_Censor_Model_Data.csv'
OUTPUT_FILE_ID = 'data/weather_station_grid.csv'
KEY = 'Site ID'
LAT_NAME = 'Latitude'
LON_NAME = 'Longitude'
CENTER = (29.419795,-98.4978487)

weather_data = pandas.read_csv(DATA_FILE_ID)
weather_data = weather_data[[KEY, LAT_NAME, LON_NAME]].drop_duplicates()
weather_data.to_csv(OUTPUT_FILE_ID)


data = [
        go.Scattermapbox(
                         lat=weather_data[LAT_NAME].tolist(),
                         lon=weather_data[LON_NAME].tolist(),
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
plotly.offline.plot(fig, filename='plots/weather_station_locations.html')

