import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime

def get_live_data():

    snowbird_bigroundup_url = "https://snowbirdskipatrol.com/Wx/BIGROUNDUP.HTM"
    response2 = requests.get(snowbird_bigroundup_url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    #print(str(soup).split('<pre>')[1].split('</pre>')[0],str(soup2).split('<pre>')[1].split('</pre>')[0])

    # Table String Lengths:
    #sinners_tablestring = str(soup).split('<pre>')[1].split('</pre>')[0]
    bigroundup_tablestring = str(soup2).split('<pre>')[1].split('</pre>')[0]

    # sinnersdf = pd.read_fwf(StringIO(sinners_tablestring))
    bigroundupdf = pd.read_fwf(StringIO(bigroundup_tablestring))

    current_year = datetime.now().year

    b_cols = bigroundupdf.columns[0].split()
    b_cols2 = bigroundupdf.values.tolist()[0]

    b_cols2 = b_cols2[0].split()

    # New Dataframe for SBigroundup that has cleaned columns in the right order:


    # Put which station is what where it needs to go:
    for i in range(len(b_cols2)):
        # Hardcoding Table column name assignment since they are not in a structured order:
        if i >= 2 and i < 8:
            b_cols2[i] = b_cols[0] + "_" + b_cols2[i]
        if i >= 8 and i < 10:
            b_cols2[i] = b_cols[2] + "_" + b_cols2[i]
        if i >= 10 and i < 13:
            b_cols2[i] = b_cols[4] + "_" + b_cols2[i]
        if i >= 13 and i < 15:
            b_cols2[i] = b_cols[6] + "_" + b_cols2[i]
        if i >= 15 and i < 19:
            if i == 18:
                b_cols2[i] = b_cols[8] + "_" + b_cols2[i] + '_DIR'
            else:
                b_cols2[i] = b_cols[8] + "_" + b_cols2[i]
        if i >= 19 and i < len(b_cols2):
            if i == len(b_cols2)-1:
                b_cols2[i] = b_cols[10] + "_" + b_cols2[i] + '_DIR'
            else:
                b_cols2[i] = b_cols[10] + "_" + b_cols2[i]


    # Asssign the new column set to brdf:
    brdf = pd.DataFrame(columns=b_cols2)
    # Assign the rows of sinnersdf to sdf by splitting by spaces into new columns:
    for i in range(3,len(bigroundupdf)):
        splitrow = str(bigroundupdf.iloc[i][0]).split()

        #values = splitrow[12:13]
        date = str(current_year) + '-' + splitrow[0] + '-' + splitrow[1]
        splitrow[1] = date
        #print(splitrow, len(splitrow))

        brdf.loc[i] = splitrow[1:]
    brdf.reset_index(drop=True,inplace=True)

    # Datetime conversions
    brdf['TIME'] = brdf['TIME'].astype(str).str.zfill(4)
    #brdf['TIME'] = pd.to_datetime(brdf['TIME'],format='%H:%M').dt.time 
    brdf.sort_values('TIME')
    brdf['DATETIME_STR'] = brdf['DATE'].astype(str) + ' ' + brdf['TIME'].astype(str)
    brdf['DATETIME'] = pd.to_datetime(brdf['DATETIME_STR'],format='%Y-%m-%d %H%M', errors='coerce')
    brdf['BASE_TEMP'] = brdf['BASE_TEMP'].astype(int)
    brdf.sort_values('BASE_TEMP')

    brdf.to_csv('data/latest.csv', index=False)
    return brdf 