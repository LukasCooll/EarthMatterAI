import pandas as pd


df = pd.read_csv("Koeppen-Geiger-ASCII.txt", sep=r"\s+")

def get_climate_data(lat, lon):

    df['lat_diff'] = abs(df['Lat'] - lat)
    df['lon_diff'] = abs(df['Lon'] - lon)
    df['total_diff'] = df['lat_diff'] + df['lon_diff']


    closest_row = df.loc[df['total_diff'].idxmin()]
    climate_code = closest_row['Cls']

    return "Climate code at location:", climate_code