import pandas as pd
from geopy.distance import geodesic
from datetime import datetime, timedelta
import plotly.express as px
import os

def hi():
    print('hi 1205')

def calculate_distance(lat, lon, df_deviceid_file_path, distance, row_lat='lat', row_lon='lon', deviceid='device_id'):
    # Read the device data from the CSV file
    df_deviceid = pd.read_csv(df_deviceid_file_path)
    
    # Drop rows with missing lat or lon values
    df_deviceid = df_deviceid.dropna(subset=[row_lat, row_lon], how='all')
    
    # Ensure latitude and longitude values are within valid ranges
    min_lat = -90
    max_lat = 90
    min_lon = -180
    max_lon = 180
    df_deviceid[row_lat] = df_deviceid[row_lat].apply(lambda x: min(max(min_lat, x), max_lat))
    df_deviceid[row_lon] = df_deviceid[row_lon].apply(lambda x: min(max(min_lon, x), max_lon))

    # Create a function to calculate the distance
    def calculate_distance_row(row):
        device_location = (row[row_lat], row[row_lon])
        target_location = (lat, lon)
        distance = geodesic(device_location, target_location).kilometers
        return distance

    # Add a column to store the distances
    df_deviceid['distance_km'] = df_deviceid.apply(calculate_distance_row, axis=1)

    # Filter out data within one kilometer
    filtered_df = df_deviceid[df_deviceid['distance_km'] <= distance]

    # Get the list of device IDs
    lst_device_id = filtered_df[deviceid].to_list()

    return lst_device_id


if __name__ == '__main__':
    # Example of calculate_distance usage:
    lon = 121.4471
    lat = 25.0669
    df_deviceid_file_path = '/Users/apple/Downloads/project_device_table_20231017.csv'
    result_lst_device_id = calculate_distance(lat, lon, df_deviceid_file_path, 1)
    print(result_lst_device_id)
    

