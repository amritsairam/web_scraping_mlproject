import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

# Create "Data/Real_Data" directory if it doesn't exist
if not os.path.exists("Data/Real_Data"):
    os.makedirs("Data/Real_Data")


for year in range(2013, 2019):
    concatenated_df = pd.DataFrame()
    folder_name = "Data/Real_Data/{}".format(year)
    # Create year-specific folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i in range(1, 13):
        file_html = open('Data/Html_Data/{}/{}.html'.format(year, i), 'rb')
        plain_text = file_html.read()

        tempD = []
        finalD = []

        soup = BeautifulSoup(plain_text, "lxml")
        for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
            for tbody in table:
                for tr in tbody:
                    a = tr.get_text()
                    tempD.append(a)
        rows = len(tempD) / 15

        for times in range(round(rows)):
            newtempD = []
            for i in range(15):
                newtempD.append(tempD[0])
                tempD.pop(0)
            finalD.append(newtempD)

        length = len(finalD)

        finalD.pop(length - 1)
        finalD.pop(0)

        for a in range(len(finalD)):
            finalD[a].pop(6)
            finalD[a].pop(13)
            finalD[a].pop(12)
            finalD[a].pop(11)
            finalD[a].pop(10)
            finalD[a].pop(9)
            finalD[a].pop(0)

        df = pd.DataFrame(finalD, columns=['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM'])

        concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
    concatenated_df.to_csv('{}/concatenated_{}.csv'.format(folder_name, year), index=False)

combined_df = pd.DataFrame()
for year in range(2013, 2019):
    df4 = pd.read_csv('Data/Real_Data/{}/concatenated_{}.csv'.format(year, year))
    df5 = pd.read_csv('Data/cleaned_aqi/{}/aqi{}final.csv'.format(year, year))
    final_year = pd.concat([df4, df5], axis=1)
    combined_df = combined_df.append(final_year)

combined_df.to_csv('Data/Real_Data/Real_Combine.csv', index=False)
