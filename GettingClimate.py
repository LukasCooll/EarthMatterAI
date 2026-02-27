import pandas as pd


df = pd.read_csv("Koeppen-Geiger-ASCII.txt", delim_whitespace=True)


def get_climate_data(lat, lon):

    df['lat_diff'] = abs(df['Lat'] - lat)
    df['lon_diff'] = abs(df['Lon'] - lon)
    df['total_diff'] = df['lat_diff'] + df['lon_diff']


    closest_row = df.loc[df['total_diff'].idxmin()]
    climate_code = closest_row['Cls']

    print("Climate code at location:", climate_code)