import pandas as pd
from geopy.distance import geodesic
from datetime import datetime, timedelta
import plotly.express as px
import os

def create_custom_color_scale(color_dict):
    scale = []
    max_value = max(item['v'] for item in color_dict)  # 獲取最大數值
    for item in color_dict:
        # 將每個色彩值對應到其數值範圍（從0到1之間），並反轉色彩順序
        scale.append([item['v'] / max_value, item['color']])
    return scale[::-1]  # 反轉色彩尺度列表
    
    
def create_pm25_map(df, lat, lon, file_path, row_value='value', row_deviceId='deviceId', row_lat='lat', row_lon='lon',
                    row_time='localTime'):
    # Filter data
    df[row_value] = df[row_value].astype(float)
    df = df.loc[df.groupby(row_deviceId)[row_value].idxmax()]

    pm2_5_color_dict = [
        {"v": 500.4, "color": "#000000"},
        {"v": 450.5, "color": "#301E12"},
        {"v": 400.5, "color": "#3C230F"},
        {"v": 350.5, "color": "#49280D"},
        {"v": 300.5, "color": "#552E0A"},
        {"v": 250.5, "color": "#623307"},
        {"v": 230.5, "color": "#682c1f"},
        {"v": 210.5, "color": "#6d2537"},
        {"v": 190.5, "color": "#731d4e"},
        {"v": 170.5, "color": "#781666"},
        {"v": 150.5, "color": "#7e0f7e"},
        {"v": 131.3, "color": "#970f6a"},
        {"v": 112.1, "color": "#b10f56"},
        {"v": 92.9, "color": "#ca0e43"},
        {"v": 73.7, "color": "#e30e30"},
        {"v": 54.5, "color": "#fc0e1c"},
        {"v": 50.7, "color": "#fc241d"},
        {"v": 46.9, "color": "#fc3b1f"},
        {"v": 43.1, "color": "#fd5220"},
        {"v": 39.3, "color": "#fd6822"},
        {"v": 35.5, "color": "#fd7e23"},
        {"v": 31.5, "color": "#fd9827"},
        {"v": 27.5, "color": "#feb12b"},
        {"v": 23.5, "color": "#fecb30"},
        {"v": 19.5, "color": "#ffe534"},
        {"v": 15.5, "color": "#fffd38"},
        {"v": 12.4, "color": "#d4fd36"},
        {"v": 9.3, "color": "#a9fd34"},
        {"v": 6.2, "color": "#7EFD32"},
        {"v": 3.1, "color": "#53FD30"},
        {"v": 0, "color": "#29fd2e"}
    ]
    custom_color_scale = create_custom_color_scale(pm2_5_color_dict)

    # Create scatter mapbox
    fig = px.scatter_mapbox(df, lat=row_lat, lon=row_lon, color=row_value, range_color=(0, 500.4),
                            hover_data=[row_time, row_deviceId, row_value], zoom=7, size=[15] * len(df[row_lat]),
                            size_max=15, color_continuous_scale=custom_color_scale)

    fig.update_layout(mapbox_style='open-street-map')  # carto-positron

    initial_center = {"lat": lat, "lon": lon}  # Example coordinates
    initial_zoom = 14  # Example zoom level
    fig.update_layout(mapbox_center=initial_center, mapbox_zoom=initial_zoom)

    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


    # Save to html
    fig.write_html(file_path, include_plotlyjs=True)

    return file_path

if __name__ == '__main__':

    # Example of create_pm25_map usage:
    file_path = '/Users/apple/Desktop/test.html'
    url = create_pm25_map(df,lat, lon, file_path, row_value='value', row_deviceId='deviceId', row_lat='lat', row_lon='lon', row_time='localTime')
    print(url)
