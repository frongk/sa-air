import pandas

def dist_calc(df_row, coordinate):
    lat_dist2 = (df_row['Latitude'] - coordinate[0])**2
    long_dist2 = (df_row['Longitude'] - coordinate[1])**2
    return (lat_dist2 + long_dist2)**0.5

traffic = pandas.read_csv('SATRIP_detectionsummary.csv')
signals = traffic.groupby(['LocationName', 'Latitude', 'Longitude']).sum()
signals.reset_index(inplace=True)

test_coord = (29.5498886, -98.5952193)
distances = signals.apply(lambda row: dist_calc(row, test_coord), axis=1)
closest = distances.sort_values().index[:10]
print(signals.loc[closest])
