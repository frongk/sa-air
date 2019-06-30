# goal - define coordinate locations for further analysis
# how - use san antonio traffic intersection coordinates to define a box and center point
#       use box to define radius and draw a circle around the city area
# creates a plot to check

import pandas
import numpy

from itertools import product
from tqdm import tqdm

import plotly
import plotly.graph_objs as go

from SECRETS import mapbox_token

def boundary(center, radius, coords):
    xx = (coords[0] - center[0])**2 
    yy = (coords[1] - center[1])**2 
    dd = (xx+yy)**0.5

    if dd < radius:
        return True
    else:
        return False

DIVISION_NS = 20
DIVISION_EW = 20 

traffic = pandas.read_csv('SATRIP_detectionsummary.csv')
intersections = traffic[['LocationName', 'Latitude', 'Longitude']].drop_duplicates()

TOP = intersections['Latitude'].max()
BOTTOM = intersections['Latitude'].min()
LEFT = intersections['Longitude'].max()
RIGHT = intersections['Longitude'].min()

CENTER = ((LEFT+RIGHT)/2, (TOP+BOTTOM)/2)
RADIUS = max((TOP-BOTTOM)/2, (LEFT-RIGHT)/2)/17

lat_axis = numpy.linspace(LEFT,RIGHT,DIVISION_EW)
long_axis = numpy.linspace(BOTTOM,TOP,DIVISION_NS)

final_set = []
x = []
y = []

for cc in tqdm(product(lat_axis, long_axis)):
    # close_tests = intersections.apply(lambda x: boundary(x[['Longitude','Latitude']], RADIUS, cc), axis=1).tolist()
    idx = 0
    maxidx = intersections.shape[0]
    state = False

    while not state:
        point = intersections[['Longitude','Latitude']].iloc[idx]
        state = boundary(point, RADIUS, cc)

        if state:
            final_set.append(cc)
            x.append(cc[0])
            y.append(cc[1])

        if idx < maxidx-1:
            idx += 1
        else:
            state = True

data = [
        go.Scattermapbox(
                         lat=y,
                         lon=x,
                         mode='markers',
                         marker=go.scattermapbox.Marker(size=3)
                        ),
        go.Scattermapbox(
                         lat=intersections.Latitude.tolist(),
                         lon=intersections.Longitude.tolist(),
                         mode='markers',
                         marker=go.scattermapbox.Marker(size=5)
                        )
       ]
layout = go.Layout(
            autosize=True,
            hovermode='closest',
                mapbox=go.layout.Mapbox(
                    accesstoken=mapbox_token,
                    bearing=0,
                    center=go.layout.mapbox.Center(
                        lat=CENTER[1],
                        lon=CENTER[0]
                    ),
                    pitch=0,
                    zoom=10
                ),
            )


fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='plots/grid_tt.html')

#save final groups of points
pandas.DataFrame(final_set, columns=['Longitude','Latitude'])[['Latitude','Longitude']].to_csv(f'data/interpolation_grid_{DIVISION_NS}.csv')
