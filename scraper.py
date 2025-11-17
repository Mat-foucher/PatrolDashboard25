import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime
from collections import Counter
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

def send_wind_alert(message):
    webhook_url = os.getenv('TEAMS_WEBHOOK')
    payload = {
        "text": message
    }
    requests.post(webhook_url, json=payload)
    

def get_live_data(dummy_buster = None):
    
    ################################################################
    # SCRAPING LOGIC 
    ################################################################

    snowbird_sinners_url = "https://snowbirdskipatrol.com/Wx/SIN.HTM"
    snowbird_bigroundup_url = "https://snowbirdskipatrol.com/Wx/BIGROUNDUP.HTM"
    snowbird_bigsnow = "https://snowbirdskipatrol.com/Wx/BIGSNOW3.HTM"
    response = requests.get(snowbird_sinners_url)
    response2 = requests.get(snowbird_bigroundup_url)
    response3 = requests.get(snowbird_bigsnow)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    soup3 = BeautifulSoup(response3.text, 'html.parser')
    #print(str(soup).split('<pre>')[1].split('</pre>')[0],str(soup2).split('<pre>')[1].split('</pre>')[0])

    # Table String Lengths:
    sinners_tablestring = str(soup).split('<pre>')[1].split('</pre>')[0]
    bigroundup_tablestring = str(soup2).split('<pre>')[1].split('</pre>')[0]
    bigsnow_tablestring = str(soup3).split('<pre>')[1].split('</pre>')[0]

    sinnersdf = pd.read_fwf(StringIO(sinners_tablestring))
    bigroundupdf = pd.read_fwf(StringIO(bigroundup_tablestring))
    bigsnowdf = pd.read_fwf(StringIO(bigsnow_tablestring))

    current_year = datetime.now().year

    #############################################
    # SINNERS
    #############################################

    # Split the dataframe:


    s_cols = sinnersdf.columns[0].split()
    #print(s_cols)

    # New Dataframe for Sinners that has cleaned columns:
    sdf = pd.DataFrame(columns=s_cols)

    # Assign the rows of sinnersdf to sdf by splitting by spaces into new columns:
    for i in range(len(sinnersdf)):
        if i > 1:
            splitrow = str(sinnersdf.iloc[i]).split()
            #print(splitrow[6:13])
            #values = splitrow[6:13]
            date = str(current_year) + '-' + splitrow[6] + '-' + splitrow[7]
            #print(date)
            splitrow[7] = date
            sdf.loc[i] = splitrow[7:13]
        sdf.reset_index(drop=True,inplace=True)
    #sdf.head(100)

    #############################################
    # BIGROUNDUP
    #############################################

    b_cols = bigroundupdf.columns[0].split()
    b_cols2 = bigroundupdf.values.tolist()[0]

    s_cols = bigsnowdf.columns[0].split()
    s_cols2 = bigsnowdf.values.tolist()[0]

    b_cols2 = b_cols2[0].split()
    s_cols2 = s_cols2[0].split()

    # New Dataframe for SBigroundup that has cleaned columns in the right order:

    # Assume Date / time are always the first two: 
    date_s = 'DATE'
    time_s = 'TIME'

    #date_time_good = False
    date_i = b_cols2.index(date_s)
    time_i = b_cols2.index(time_s)

    # print(date_i, time_i)

    if date_i < 2 and time_i < 2:
        print('Date and time are at their proper location (https://snowbirdskipatrol.com/Wx/BIGROUNDUP.HTM)')
    #date_time_good = True 

    for i in b_cols:
        try:
            float(i)
            print(i + " is a number")
            b_cols.remove(i)
        except ValueError:
            print(i + " is not a number")
            # take out the elevations (for now)


    # identify where each weather station's TEMP is (always assume that the weather station has TEMP).
    # this will fail if a weather station does not pipe it's TEMP (unlikely).

    temp_indices = [i for i, item in enumerate(b_cols2) if item == 'TEMP']

    #print(temp_indices)

    # New clean column set up method:

    for i in range(len(temp_indices)):
        
        if i < len(temp_indices)-1:
            #print(i, temp_indices[i], temp_indices[i+1])
            for j in range(temp_indices[i], temp_indices[i+1]):
                b_cols2[j] = b_cols[i] + "_" + b_cols2[j]

        else:
            #print(i, temp_indices[i], temp_indices[len(temp_indices) - 1])
            for j in range(temp_indices[i], len(b_cols2)):
                b_cols2[j] = b_cols[i] + "_" + b_cols2[j]

    # add wind direction:
    element_counts = Counter(b_cols2)
    duplicate_indices = {
        element: [i for i, x in enumerate(b_cols2) if x == element]
        for element, count in element_counts.items()
        if count > 1
    }
    #print(duplicate_indices)
    # make wind and wind direction distinct: 
    for i in duplicate_indices:
        b_cols2[max(duplicate_indices[i])] = b_cols2[max(duplicate_indices[i])] + '_DIR'


    # Asssign the new column set to brdf:
    brdf = pd.DataFrame(columns=b_cols2)
    # Assign the rows of sinnersdf to sdf by splitting by spaces into new columns:
    for i in range(3,len(bigroundupdf)):
        splitrow = str(bigroundupdf.iloc[i][0]).split()

        #values = splitrow[12:13]
        date = str(current_year) + '-' + splitrow[0] + '-' + splitrow[1]
        splitrow[1] = date
        #print(splitrow[1:], len(splitrow[1:]))
        if len(splitrow)-1 == len(b_cols2):
            brdf.loc[i] = splitrow[1:]
    brdf.reset_index(drop=True,inplace=True)

    # AI summary (for fun):
    # ai_summary = AISummary(brdf)

    ####################
    ## big snow table ##
    #################### 
    # Assume Date / time are always the first two:
    date_s = 'DATE'
    time_s = 'TIME'

    #date_time_good = False
    date_i = s_cols2.index(date_s)
    time_i = s_cols2.index(time_s)

    # print(date_i, time_i)

    if date_i < 2 and time_i < 2:
        print('Date and time are at their proper location (https://snowbirdskipatrol.com/Wx/BIGSNOW3.HTM)')
        date_time_good = True

    # Squash s_cols & s_cols2 together:
    for i in range(len(s_cols2)):
        if i>1:
            s_cols2[i] = s_cols[i-2] + '_' + s_cols2[i]

    # bsdf = big snow dataframe:

    bsdf = pd.DataFrame(columns=s_cols2)

    ## Assign the row values of bigsnow to the bsdf column (bsdf has the right column titles):

    for i in range(3,len(bigsnowdf)):
        splitrow = str(bigsnowdf.iloc[i][0]).split()

        #values = splitrow[12:13]
        date = str(current_year) + '-' + splitrow[0] + '-' + splitrow[1]
        splitrow[1] = date



        if len(splitrow)-1 == len(s_cols2):
            bsdf.loc[i] = splitrow[1:]


    bsdf.reset_index(drop=True,inplace=True)
    # print(s_cols)
    # print(s_cols2)
    # bsdf.head(100)


    #############################################
    # Stuff for sending the data to google sheets
    #############################################

    # creds_path = '/etc/secrets/creds.json'
    # scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    # client = gspread.authorize(creds)

    # Fetch on cron run:
    # df = get_live_data()

    # sheet = client.open("snowbird_bigroundup_log").sheet1

    # sheet.append_row(df.iloc[0].tolist())

    # Bigroundup: 

    brdf['TIME'] = brdf['TIME'].astype(str).str.zfill(4)
    #brdf['TIME'] = pd.to_datetime(brdf['TIME'],format='%H:%M').dt.time 
    brdf.sort_values('TIME')
    brdf['DATETIME_STR'] = brdf['DATE'].astype(str) + ' ' + brdf['TIME'].astype(str)
    brdf['DATETIME'] = pd.to_datetime(brdf['DATETIME_STR'],format='%Y-%m-%d %H%M', errors='coerce')
    brdf['BASE_TEMP'] = brdf['BASE_TEMP'].astype(int)
    brdf.sort_values('BASE_TEMP')

    # BigSnow: 
    bsdf['TIME'] = bsdf['TIME'].astype(str).str.zfill(4)
    #brdf['TIME'] = pd.to_datetime(brdf['TIME'],format='%H:%M').dt.time
    bsdf.sort_values('TIME')
    bsdf['DATETIME_STR'] = bsdf['DATE'].astype(str) + ' ' + bsdf['TIME'].astype(str)
    bsdf['DATETIME'] = pd.to_datetime(bsdf['DATETIME_STR'],format='%Y-%m-%d %H%M', errors='coerce')
    bsdf['BASE_HS'] = bsdf['BASE_HS'].astype(float)
    bsdf['SIN_HS'] = bsdf['SIN_HS'].astype(float)
    bsdf['PH1_HS'] = bsdf['PH1_HS'].astype(float)
    bsdf['G2_HS'] = bsdf['G2_HS'].astype(float)
    bsdf.sort_values('DATE')

    # BigSnow - Anomaly Detection for heights (basic):

    for i in range(len(s_cols2)):
        for j in range(len(bsdf[s_cols2[i]])):
            #print(bsdf[s_cols2[i]].loc[j])
            if isinstance(bsdf[s_cols2[i]].loc[j], float):
                if bsdf[s_cols2[i]].loc[j] < 0:
                    bsdf[s_cols2[i]].loc[j] = 0.0


    # Wind Alerts to teams: 

    # Check to see if wind at any station is high (>20 mph) :
    latest_df = brdf[brdf['DATETIME'] == brdf['DATETIME'].max()]
    max_peak_wind = int(latest_df['PEAK_WIND'].iloc[0])
    max_redstack_wind = int(latest_df['REDSTACK_WIND'].iloc[0])
    
    if max_peak_wind > 20:
        send_wind_alert(f"ALERT: PEAK WINDS OVER 20 MPH [LAST RECORDED: {max_peak_wind}] @Mathieu Foucher") 
    if max_redstack_wind > 20:
        send_wind_alert(f"ALERT: REDSTACK WINDS OVER 20 MPH [LAST RECORDED: {max_redstack_wind}] @Mathieu Foucher") 

    if max_peak_wind > 40:
        send_wind_alert(f"DANGER: PEAK WINDS OVER 40 MPH [LAST RECORDED: {max_peak_wind}]. STAY CLEAR OF RIDGELINES. @Mathieu Foucher") 
    if max_redstack_wind > 40:
        send_wind_alert(f"DANGER: REDSTACK WINDS OVER 40 MPH [LAST RECORDED: {max_redstack_wind}]. STAY CLEAR OF RIDGELINES. @Mathieu Foucher") 

    #brdf.to_csv('data/latest.csv', index=False)
    return brdf, bsdf





