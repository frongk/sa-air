# CivTechSA Datathon - Team Jellyfish 

## File Descriptions
sa_grid.py
for generating a grid of points in SA area that defines the GPS points from which future maps will be calculated.

triangulate_dict.py
for generating a mapping file that finds nearest 3 points using simple Euclidean distance metric

interpolate.py
performs triangular interpolation for estimating the value of a certain point based on the 3 nearest datapoints

elevation.py
for calling USGS elevation service for elevation info at a certain GPS coordinate.

## links
Datathon Datasets:
https://sites.google.com/respec.com/smartsa-datathon-2019/home

For bulk download of air quality information
https://www17.tceq.texas.gov/tamis/index.cfm

For weather model data
http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_script_tips.html

SA Trip Data for Intersection Traffic Information (need to script a pull)
https://gis.sanantonio.gov/Satrip/satripdata.html

### TODO
- add weekday whoops.py to air_monitoring preprocessing
