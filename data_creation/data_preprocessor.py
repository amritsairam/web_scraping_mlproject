import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

def aqicsvcleaner():
    average_values = []
    
    for i in range(2013, 2019):
        df = pd.read_csv('uncleaned_aqi/AQI/aqi{}.csv'.format(i))
        # Rest of the code for processing the file

        df[['date', 'time']] = df['Date'].str.split(n=1, expand=True)
        df['final_time'] = df['Time'].fillna('') + df['time'].fillna('')
        df.drop(['Date', 'Time', 'time'], axis=1, inplace=True)
        df['Time'] = df['final_time']
        df.drop(['final_time'], axis=1, inplace=True)
        df = df[['date', 'Time', 'PM2.5']]
        if i==2015:
          df.loc[df['date'].str.endswith('/201'), 'date'] = df.loc[df['date'].str.endswith('/201'), 'date'].str.replace('/201', '/2015')
        
        if 'PM2.5 AQI' in df.columns:
            df.drop(['PM2.5 AQI'], axis=1, inplace=True)
        
        invalid_values = ['NoData', 'PwrFail', '---', 'InVld']
        df['PM2.5'] = df['PM2.5'].replace(invalid_values, 0)

        df['PM2.5'] = df['PM2.5'].astype(float)
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce').dt.time

        # Replace '24:00 AM' with '00:00 AM' and adjust the date
        df.loc[df['Time'] == datetime.time(0, 0), 'Time'] = datetime.time(0, 0)
        from pandas.core.arrays.datetimelike import NaT
        df['Time'] = df['Time'].replace(NaT, '00:00:00')
        
        average = df.groupby('date')['PM2.5'].mean()
        average_values.append(average)



        if not os.path.exists('Data/cleaned_aqi/{}'.format(i)):
            os.makedirs('Data/cleaned_aqi/{}'.format(i))

        cleaned_filename = 'aqi{}final.csv'.format(i)
        cleaned_filepath = os.path.join('Data', 'cleaned_aqi', str(i), cleaned_filename)
        average.to_csv(cleaned_filepath)
    
    return average_values

if __name__ == "__main__":
    aqicsvcleaner()
    