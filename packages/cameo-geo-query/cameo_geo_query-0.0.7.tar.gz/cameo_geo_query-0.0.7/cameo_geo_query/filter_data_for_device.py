import pandas as pd
from geopy.distance import geodesic
from datetime import datetime, timedelta
import plotly.express as px
import os

def filter_data_for_device(result_lst_device_id, time, df_device_file_path, row_time='localTime', row_deviceid='deviceId',sensor='PM2.5'):
    def get_date_hour_min(time2minus, now, str_time):
        str_date = str_time.split(' ')[0]
        str_hour = str_time.split(' ')[1].split(':')[0]
        str_minute = str_time.split(' ')[1].split(':')[1][0]
        if str_minute == '0':
            if str_hour == '00':
                str_time = now - timedelta(minutes=time2minus + 10)
                str_time = str_time.strftime("%Y-%m-%d %H:%M:%S")
                str_date = str_time.split(' ')[0]
                str_hour = str_time.split(' ')[1].split(':')[0]
                str_minute = str_time.split(' ')[1].split(':')[1][0]
            else:
                str_hour = str(int(str_hour) - 1).zfill(2)
                str_minute = '5'
        else:
            str_minute = str(int(str_minute) - 1)

        return str_date, str_hour, str_minute
    
    def filter_time(df, time):
        user_input_time = pd.to_datetime(time)
        half_hour_offset = pd.DateOffset(minutes=30)
        start_time = user_input_time - half_hour_offset
        end_time = user_input_time + half_hour_offset
        df[row_time] = pd.to_datetime(df[row_time])
        filtered_data = df[(df[row_time] >= start_time) & (df[row_time] <= end_time)].reset_index(drop = True)
        return filtered_data
    
    def filter_deviceid(df, result_lst_device_id):
        df = df[df[row_deviceid].isin(result_lst_device_id)].reset_index(drop = True)
        return df
    
    df_all = pd.DataFrame()

    get_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

    for i in range(-40, 40, 10):
        str_time = get_time - timedelta(minutes=i)
        str_time = str_time.strftime("%Y-%m-%d %H:%M:%S")
        str_date, str_hour, str_minute = get_date_hour_min(i, time, str_time)
        str_url = f'{df_device_file_path}/{str_date}/10mins_{str_date} {str_hour}_{str_minute}.csv.gz'
        try:
            str_url = f'{df_device_file_path}/{str_date}/10mins_{str_date} {str_hour}_{str_minute}.csv.gz'
            df = pd.read_csv(str_url, compression='gzip')
            df_all = df_all.append(df, ignore_index=True)
        except:
            pass
    df_all = filter_time(df_all, time)
    df_all = filter_deviceid(df_all, result_lst_device_id)
    df_all = df_all[df_all['sensorId']=='pm2_5'].reset_index(drop = True)
    
    return df_all



if __name__ == '__main__':

    # Example of filter_data_for_device_time usage:
    df_device_file_path = '/Users/apple/Desktop/iot_data'
    time = '2023-11-03 08:35:00'
    df = filter_data_for_device(result_lst_device_id, time,df_device_file_path)
    print(df.localTime.min())
    print(df.localTime.max())
