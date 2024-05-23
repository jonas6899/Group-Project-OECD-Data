# %% Function: get basic OECD data

#First piece: Get the not live data into a dataframe

def load_basic_oecd_data(): 
    
    import pandas as pd
    import datetime

    # List of OECD countries and their ISO country codes
    oecd_countries = {
        "Australia": "AUS",
        "Belgium": "BEL",
        "Chile": "CHL",
        "Costa Rica": "CRI",
        "Denmark": "DNK",
        "Germany": "DEU",
        "Estonia": "EST",
        "Finland": "FIN",
        "France": "FRA",
        "Greece": "GRC",
        "Ireland": "IRL",
        "Iceland": "ISL",
        "Israel": "ISR",
        "Italy": "ITA",
        "Japan": "JPN",
        "Canada": "CAN",
        "Colombia": "COL",
        "Korea": "KOR",
        "Latvia": "LVA",
        "Lithuania": "LTU",
        "Luxembourg": "LUX",
        "Mexico": "MEX",
        "New Zealand": "NZL",
        "Netherlands": "NLD",
        "Norway": "NOR",
        "Austria": "AUT",
        "Poland": "POL",
        "Portugal": "PRT",
        "Sweden": "SWE",
        "Switzerland": "CHE",
        "Slovak Republic": "SVK",
        "Slovenia": "SVN",
        "Spain": "ESP",
        "Czech Republic": "CZE",
        "Turkey": "TUR",
        "Hungary": "HUN",
        "United Kingdom": "GBR",
        "United States": "USA"
    }

    # Dictionary for languages and currencies of the countries, wasn't able to find any api that has pop data newer then 2020, pop Data in Millions
    country_info = {
        "Australia": {"Population": 25.979, "Language": "English", "Currency": "Australian Dollar"},
        "Belgium": {"Population": 11.641, "Language": "Dutch, French, German", "Currency": "Euro"},
        "Chile": {"Population": 19.829, "Language": "Spanish", "Currency": "Chilean Peso"},
        "Costa Rica": {"Population": 5.213, "Language": "Spanish", "Currency": "Costa Rican Colón"},
        "Denmark": {"Population": 5.911, "Language": "Danish", "Currency": "Danish Krone"},
        "Germany": {"Population": 83.798, "Language": "German", "Currency": "Euro"},
        "Estonia": {"Population": 1.349, "Language": "Estonian", "Currency": "Euro"},
        "Finland": {"Population": 5.556, "Language": "Finnish, Swedish", "Currency": "Euro"},
        "France": {"Population": 67.943, "Language": "French", "Currency": "Euro"},
        "Greece": {"Population": 10.361, "Language": "Greek", "Currency": "Euro"},
        "Ireland": {"Population": 5.100, "Language": "Irish, English", "Currency": "Euro"},
        "Iceland": {"Population": 0.382, "Language": "Icelandic", "Currency": "Icelandic Króna"},
        "Israel": {"Population": 9.529, "Language": "Hebrew, Arabic", "Currency": "New Israeli Shekel"},
        "Italy": {"Population": 58.940, "Language": "Italian", "Currency": "Euro"},
        "Japan": {"Population": 124.947, "Language": "Japanese", "Currency": "Japanese Yen"},
        "Canada": {"Population": 38.930, "Language": "English, French", "Currency": "Canadian Dollar"},
        "Colombia": {"Population": 51.683, "Language": "Spanish", "Currency": "Colombian Peso"},
        "Korea": {"Population": 51.628, "Language": "Korean", "Currency": "South Korean Won"},
        "Latvia": {"Population": 1.879, "Language": "Latvian", "Currency": "Euro"},
        "Lithuania": {"Population": 2.833, "Language": "Lithuanian", "Currency": "Euro"},
        "Luxembourg": {"Population": 0.653, "Language": "Luxembourgish, French, German", "Currency": "Euro"},
        "Mexico": {"Population": 130.118, "Language": "Spanish", "Currency": "Mexican Peso"},
        "New Zealand": {"Population": 5.124, "Language": "English, Māori", "Currency": "New Zealand Dollar"},
        "Netherlands": {"Population": 17.703, "Language": "Dutch", "Currency": "Euro"},
        "Norway": {"Population": 5.457, "Language": "Norwegian", "Currency": "Norwegian Krone"},
        "Austria": {"Population": 9.053, "Language": "German", "Currency": "Euro"},
        "Poland": {"Population": 37.827, "Language": "Polish", "Currency": "Polish Złoty"},
        "Portugal": {"Population": 10.444, "Language": "Portuguese", "Currency": "Euro"},
        "Sweden": {"Population": 10.487, "Language": "Swedish", "Currency": "Swedish Krona"},
        "Switzerland": {"Population": 8.776, "Language": "German, French, Italian, Romansh", "Currency": "Swiss Franc"},
        "Slovak Republic": {"Population": 5.432, "Language": "Slovak", "Currency": "Euro"},
        "Slovenia": {"Population": 2.109, "Language": "Slovenian", "Currency": "Euro"},
        "Spain": {"Population": 47.615, "Language": "Spanish", "Currency": "Euro"},
        "Czech Republic": {"Population": 10.760, "Language": "Czech", "Currency": "Czech Koruna"},
        "Turkey": {"Population": 84.980, "Language": "Turkish", "Currency": "Turkish Lira"},
        "Hungary": {"Population": 9.643, "Language": "Hungarian", "Currency": "Hungarian Forint"},
        "United Kingdom": {"Population": 67.299, "Language": "English", "Currency": "British Pound"},
        "United States": {"Population": 333.288, "Language": "English", "Currency": "US Dollar"}
    }

    # Create the DataFrame
    df = pd.DataFrame.from_dict(oecd_countries, orient='index', columns=['ISO Code'])

    # Add columns for Language, Currency, and Population
    df['Language'] = df.index.map(lambda x: country_info[x]['Language'])
    df['Currency'] = df.index.map(lambda x: country_info[x]['Currency'])
    df['Population'] = df.index.map(lambda x: country_info[x]['Population'])


    #second piece: Get the Data for GDP and GDP per Capita from Worldbank API 
    import requests

    # Function to get GDP and GDP per capita for OECD countries
    def get_oecd_data():
        # Dictionary of OECD countries and their ISO codes
        oecd_countries = {
            "Australia": "AUS",
            "Belgium": "BEL",
            "Chile": "CHL",
            "Costa Rica": "CRI",
            "Denmark": "DNK",
            "Germany": "DEU",
            "Estonia": "EST",
            "Finland": "FIN",
            "France": "FRA",
            "Greece": "GRC",
            "Ireland": "IRL",
            "Iceland": "ISL",
            "Israel": "ISR",
            "Italy": "ITA",
            "Japan": "JPN",
            "Canada": "CAN",
            "Colombia": "COL",
            "Korea": "KOR",
            "Latvia": "LVA",
            "Lithuania": "LTU",
            "Luxembourg": "LUX",
            "Mexico": "MEX",
            "New Zealand": "NZL",
            "Netherlands": "NLD",
            "Norway": "NOR",
            "Austria": "AUT",
            "Poland": "POL",
            "Portugal": "PRT",
            "Sweden": "SWE",
            "Switzerland": "CHE",
            "Slovak Republic": "SVK",
            "Slovenia": "SVN",
            "Spain": "ESP",
            "Czech Republic": "CZE",
            "Turkey": "TUR",
            "Hungary": "HUN",
            "United Kingdom": "GBR",
            "United States": "USA"
        }

        #set period of retrieved data (last completed year) 
        current_year = datetime.datetime.now().year

        # get the last completed year
        last_completed_year = current_year - 1

        # Convert the last completed year to a string
        last_completed_year_str = str(last_completed_year)

        # URL for GDP and GDP per capita data
        url_gdp = 'https://www.imf.org/external/datamapper/api/v1/NGDPD'
        url_gdp_per_capita = 'https://www.imf.org/external/datamapper/api/v1/NGDPDPC'

        # Make GET requests to the URLs
        response_gdp = requests.get(url_gdp)
        response_gdp_per_capita = requests.get(url_gdp_per_capita)

        # Check if the requests were successful
        if response_gdp.status_code == 200 and response_gdp_per_capita.status_code == 200:
            # Parse the JSON responses
            data_gdp = response_gdp.json()
            data_gdp_per_capita = response_gdp_per_capita.json()

            # Create an empty DataFrame to store combined data
            df = pd.DataFrame(columns=['GDP (bn USD)', 'GDP per Capita (USD)'])

            # Iterate over OECD countries
            for country, iso_code in oecd_countries.items():
                # Get GDP for the current year and the country
                gdp = data_gdp['values']['NGDPD'].get(iso_code, {}).get(str(last_completed_year_str), None)
                # Get GDP per capita for the current year and the country
                gdp_per_capita = data_gdp_per_capita['values']['NGDPDPC'].get(iso_code, {}).get(str(current_year), None)

                if gdp is not None and gdp_per_capita is not None:
                    
                    # new data 
                    new_data = {'GDP (bn USD)': gdp, 'GDP per Capita (USD)': gdp_per_capita}
                    new_data = pd.DataFrame([new_data])
                    
                    # concate with df
                    df = pd.concat([df, new_data], ignore_index=True)
                    
            # Set country names as index
            df.index = oecd_countries.keys()

            return df
        else:
            print("Failed to fetch data from the API.")


    # Get GDP and GDP per capita data for OECD countries for the current year
    oecd_data_df = get_oecd_data()

    #third piece: merge the two together 
    basic_oecd_data = pd.merge(df, oecd_data_df, left_index = True, right_index = True)
    
    return basic_oecd_data

# %% Function: get medical OECD data

def load_oecd_med_data():
    
    import pandas as pd
    import numpy as np
    
    # set working directory to file location
    import os
    dir_path = os.path.dirname(__file__)
    os.chdir(dir_path)
    
    # download life data
    
    # [CHART] Expenditure in healthcare across countries and areas of care 
    HC_EXP_since2015 = pd.read_csv("https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.0/.A.EXP_HEALTH.XDC._T..HC3+HC0+HC52+HC513+HC512+HC511+HC7+HC6+HC1HC2+HC4._T._T...V?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels")

    # [TABLE] Input costs of Medical goods providers across countries
    HC_IC_since2015 = pd.read_csv("https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA_FP,1.0/.A..XDC.....HP5._T..V?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels")

    # [CHART] Number of doctors per region
    DOCTORS_since2015 = pd.read_csv("https://sdmx.oecd.org/public/rest/data/OECD.CFE.EDS,DSD_REG_HEALTH@DF_CARE,1.0/A.TL2+CTRY.MLT+MT00+BGR+BG31+BG32+BG33+BG34+BG41+BG42+SRB+RS11+RS12+RS21+RS22+GBR+UKC+UKD+UKE+UKF+UKG+UKH+UKI+UKJ+UKK+UKL+UKM+UKN+ROU+RO11+RO12+RO21+RO22+RO31+RO32+RO41+RO42+TUR+TR10+TR21+TR22+TR31+TR32+TR33+TR41+TR42+TR51+TR52+TR61+TR62+TR63+TR71+TR72+TR81+TR82+TR83+TR90+TRA1+TRA2+TRB1+TRB2+TRC1+TRC2+TRC3+SVK+SK01+SK02+SK03+SK04+SVN+SI03+SI04+ESP+ES11+ES12+ES13+ES21+ES22+ES23+ES24+ES30+ES41+ES42+ES43+ES51+ES52+ES53+ES61+ES62+ES63+ES70+SWE+SE11+SE12+SE21+SE22+SE23+SE31+SE32+SE33+CHE+CH01+CH02+CH03+CH04+CH05+CH06+CH07+NLD+NL11+NL12+NL13+NL21+NL22+NL23+NL31+NL32+NL33+NL34+NL41+NL42+NZL+NZ11+NZ12+NZ13+NZ14+NZ15+NZ16+NZ17+NZ18+NZ19+NZ21+NZ22+NZ23+NZ24+NZ25+NOR+NO02+NO06+NO07+NO08+NO09+POL+PL21+PL22+PL41+PL42+PL43+PL51+PL52+PL61+PL62+PL63+PL71+PL72+PL81+PL82+PL84+PL91+PL92+PRT+PT11+PT15+PT16+PT17+PT18+PT20+PT30+JPN+JPA+JPB+JPC+JPD+JPE+JPF+JPG+JPH+JPI+JPJ+KOR+KR01+KR02+KR03+KR04+KR05+KR06+KR07+LVA+LV00+LTU+LT01+LT02+LUX+LU00+MEX+ME01+ME02+ME03+ME04+ME05+ME06+ME07+ME08+ME09+ME10+ME11+ME12+ME13+ME14+ME15+ME16+ME17+ME18+ME19+ME20+ME21+ME22+ME23+ME24+ME25+ME26+ME27+ME28+ME29+ME30+ME31+ME32+HUN+HU11+HU12+HU21+HU22+HU23+HU31+HU32+HU33+ISL+IRL+ISR+IL01+IL02+IL03+IL04+IL05+IL06+ITA+ITC1+ITC2+ITC3+ITC4+ITF1+ITF2+ITF3+ITF4+ITF5+ITF6+ITG1+ITG2+ITH1+ITH2+ITH3+ITH4+ITH5+ITI1+ITI2+ITI3+ITI4+FRA+FR1+FRB+FRC+FRD+FRE+FRF+FRG+FRH+FRI+FRJ+FRK+FRL+FRM+FRY+DEU+DE1+DE2+DE3+DE4+DE5+DE6+DE7+DE8+DE9+DEA+DEB+DEC+DED+DEE+DEF+DEG+GRC+EL30+EL41+EL42+EL43+EL51+EL52+EL53+EL54+EL61+EL62+EL63+EL64+EL65+DNK+DK01+DK02+DK03+DK04+DK05+EST+EE00+FIN+FI19+FI1B+FI1C+FI1D+FI20+CHL+CL01+CL02+CL03+CL04+CL05+CL06+CL07+CL08+CL09+CL10+CL11+CL12+CL13+CL14+CL15+CL16+COL+CO05+CO08+CO11+CO13+CO15+CO17+CO18+CO19+CO20+CO23+CO25+CO27+CO41+CO44+CO47+CO50+CO52+CO54+CO63+CO66+CO68+CO70+CO73+CO76+CO81+CO85+CO86+CO88+CO91+CO94+CO95+CO97+CO99+CZE+CZ01+CZ02+CZ03+CZ04+CZ05+CZ06+CZ07+CZ08+CAN+CA10+CA11+CA12+CA13+CA24+CA35+CA46+CA47+CA48+CA59+CA60+CA61+CA62+AT11+AT12+AT13+AT21+AT22+AT31+AT32+AT33+AT34+BEL+BE1+BE2+BE3+AUT+AU1+AU2+AU3+AU4+AU5+AU6+AU7+AU8+AUS..DOC...PS?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels")

    # [CHART] Expenditure for prescription (Rx) and over-the-counter (OTC) medicine across countries
    Rx_OTC_EXP_since2015 = pd.read_csv("https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.0/.A.EXP_HEALTH.XDC._T..HC512+HC511._T._T...V?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels")

    # [CHART] Sales and volumes penetration (in %) of Generic drugs (Gx) across countries
    Gx_SALES_since2015 = pd.read_csv("https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,HEALTH_PHMC@DF_GEN_MRKT,1.0/..PT_SL_VOL_M+PT_SL_VAL_M._T.?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels")

    # [TABLE] Pharmaceutcal sales across countries
    PHARMA_SALES_since2015 = pd.read_csv("https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,HEALTH_PHMC@DF_KEY_INDIC,1.0/.PH_SALES.XDC._Z+_T._T?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels")

    
    # 1: HC EXP
    
    # get necessary columns
    HC_EXP_since2015 = HC_EXP_since2015[["REF_AREA", "Reference area", "FUNCTION", "Health function", "TIME_PERIOD", "OBS_VALUE", "UNIT_MULT" ]]
    
    # remove duplicates
    HC_EXP_since2015 = HC_EXP_since2015.drop_duplicates()
    
    # get the real number of (by multiplying with )
    HC_EXP_since2015.UNIT_MULT = 10**HC_EXP_since2015.UNIT_MULT
    HC_EXP_since2015['TOTAL_EXP'] = HC_EXP_since2015.OBS_VALUE * HC_EXP_since2015.UNIT_MULT
    
    # put the expenditure value for each category in the column
    HC_EXP_wide = HC_EXP_since2015.pivot_table(index= ['REF_AREA', 'TIME_PERIOD'], columns='FUNCTION', values='TOTAL_EXP', aggfunc='first')
    HC_EXP_wide = HC_EXP_wide.reset_index()
    
    
    # 2: HC input costs
    
    # get necessary columns
    HC_IC_since2015 = HC_IC_since2015[["REF_AREA", "TIME_PERIOD", "OBS_VALUE", "UNIT_MULT" ]]
    
    # remove duplicates
    HC_IC_since2015 = HC_IC_since2015.drop_duplicates()
    
    # get the real number of (by multiplying with )
    HC_IC_since2015.UNIT_MULT = 10**HC_IC_since2015.UNIT_MULT
    HC_IC_since2015['TOTAL_COST'] = HC_IC_since2015.OBS_VALUE * HC_IC_since2015.UNIT_MULT
    HC_IC_since2015 = HC_IC_since2015[["REF_AREA", "TIME_PERIOD", "TOTAL_COST"]]
    
    
    
    # 3: Rx and OTC
    
    # get necessary columns
    Rx_OTC_EXP_since2015 = Rx_OTC_EXP_since2015[["REF_AREA", "Reference area", "FUNCTION", "Health function", "TIME_PERIOD", "OBS_VALUE", "CURRENCY", "UNIT_MULT" ]]
    
    # remove duplicates
    Rx_OTC_EXP_since2015 = Rx_OTC_EXP_since2015.drop_duplicates()
    
    # get the real number of (by multiplying with 10^MULT)
    Rx_OTC_EXP_since2015.UNIT_MULT = 10**Rx_OTC_EXP_since2015.UNIT_MULT
    Rx_OTC_EXP_since2015['TOTAL_EXP'] = Rx_OTC_EXP_since2015.OBS_VALUE * Rx_OTC_EXP_since2015.UNIT_MULT
    
    # put the expenditure value for each category in the column
    Rx_OTC_EXP_wide = Rx_OTC_EXP_since2015.pivot_table(index= ['REF_AREA', 'TIME_PERIOD'], columns='FUNCTION', values='TOTAL_EXP', aggfunc='first')
    Rx_OTC_EXP_wide = Rx_OTC_EXP_wide.reset_index()
    
    
    # 4: Gx
    
    # get necessary columns
    Gx_SALES_since2015 = Gx_SALES_since2015[["REF_AREA", "Reference area", "UNIT_MEASURE", "Unit of measure", "TIME_PERIOD", "OBS_VALUE"]]
    
    # remove duplicates
    Gx_SALES_since2015 = Gx_SALES_since2015.drop_duplicates()
    
    # get the real share as decimal
    Gx_SALES_since2015['SHARE'] = Gx_SALES_since2015.OBS_VALUE / 100
    
    # put the share for each category in the column
    Gx_SALES_wide = Gx_SALES_since2015.pivot_table(index= ['REF_AREA', 'TIME_PERIOD'], columns='UNIT_MEASURE', values='SHARE', aggfunc='first')
    Gx_SALES_wide = Gx_SALES_wide.reset_index()
    
    
    # 5: Pharma sales
    
    # get necessary columns
    PHARMA_SALES_since2015 = PHARMA_SALES_since2015[["REF_AREA", "Reference area", "TIME_PERIOD", "OBS_VALUE", "UNIT_MULT"]]
    
    # remove duplicates
    PHARMA_SALES_since2015 = PHARMA_SALES_since2015.drop_duplicates()
    
    # get the real number of (by multiplying with 10^MULT )
    PHARMA_SALES_since2015.UNIT_MULT = 10**PHARMA_SALES_since2015.UNIT_MULT
    PHARMA_SALES_since2015['TOTAL_PHARM'] = PHARMA_SALES_since2015.OBS_VALUE * PHARMA_SALES_since2015.UNIT_MULT
    
    # put the share for each category in the column
    PHARMA_SALES = PHARMA_SALES_since2015[["REF_AREA","Reference area","TIME_PERIOD", "TOTAL_PHARM"]]
    
    
    # FINAL: combine all tables together
    
    # combine all data frames together
    TOTAL_df = pd.merge(HC_EXP_wide,Rx_OTC_EXP_wide, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    TOTAL_df = pd.merge(TOTAL_df,Gx_SALES_wide, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    TOTAL_df = pd.merge(TOTAL_df,PHARMA_SALES, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    TOTAL_df = pd.merge(TOTAL_df,HC_IC_since2015, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    
    
    # add the OECD basic data to df
    basicoecddata = load_basic_oecd_data()
    
    # add to TOTAL data frame
    TOTAL_df = pd.merge(TOTAL_df,basicoecddata, left_on='REF_AREA', right_on="ISO Code", how='left')
    
    
    # get a legend for all the meanings
    # get df with translation for different names
    measuremeaning = HC_EXP_since2015[['FUNCTION', 'Health function']]
    measuremeaning = measuremeaning.drop_duplicates()
    measuremeaning.columns = ["Column name", "Meaning"]
    
    # append Gx shares
    temp = Gx_SALES_since2015[['UNIT_MEASURE', 'Unit of measure']]
    temp = temp.drop_duplicates()
    temp.columns = ["Column name", "Meaning"]
    measuremeaning = pd.concat([measuremeaning, temp], ignore_index=True)
    
    # append pharma info
    measuremeaning.loc[len(measuremeaning)] = {"Column name": 'TOTAL_PHARM', "Meaning": 'Pharmaceutical Sales'}
    measuremeaning.loc[len(measuremeaning)] = {"Column name": 'TOTAL_COST', "Meaning": 'Total Healthcare Input Cost'}
    
    
    
    
    # No of physicians per region:
    
    # get necessary columns
    DOCTORS_since2015 = DOCTORS_since2015[["TERRITORIAL_LEVEL", "REF_AREA", "Reference area", "TIME_PERIOD", "OBS_VALUE", "COUNTRY"]]
    
    
    
    
    
    
    # import exchange rates
    exchanges = pd.read_excel('Data/Exchange data.xlsx', skiprows=6, skipfooter=2)
    # remove first row
    exchanges = exchanges[1:len(exchanges)]
    # change to long format
    exchanges = exchanges.melt(id_vars="Time period")
    # remove nans 
    exchanges = exchanges.replace('nan', np.nan)
    exchanges = exchanges.dropna()
    # remove further unnecessary columns
    exchanges = exchanges[exchanges.variable != "Time period.1"]
    # rename columns
    exchanges = exchanges.rename({"Time period": "Country", "variable": "year", "value":"forexrate"}, axis = 1)
    exchanges.Country = exchanges["Country"].str.replace("·  ","") # remove certain weird strings
        
    
    # convert value into integer
    exchanges.forexrate = pd.to_numeric(exchanges.forexrate)
    exchanges.year = pd.to_numeric(exchanges.year)
    
    # get iso3 codes
    countrynames = load_basic_oecd_data()
    countrynames = countrynames.reset_index()
    
    # merge data 
    exchanges = pd.merge(exchanges,countrynames, left_on=['Country'], right_on=['index'], how='left')
    
    # only keep data that without does not have nans
    exchanges = exchanges.dropna()
    
    # only keep necessary columns
    exchanges = exchanges[["ISO Code", "year", "forexrate"]]
    
    # merge with total data
    TOTAL_df = pd.merge(TOTAL_df, exchanges, left_on=["REF_AREA", "TIME_PERIOD"], right_on=["ISO Code", "year"], how="right")
    
    # compute values for each category 
    TOTAL_df["HC0"] = TOTAL_df["HC0"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC1HC2"] = TOTAL_df["HC1HC2"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC3"] = TOTAL_df["HC3"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC511_x"] = TOTAL_df["HC511_x"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC512_x"] = TOTAL_df["HC512_x"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC52"] = TOTAL_df["HC52"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC513"] = TOTAL_df["HC513"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC6"] = TOTAL_df["HC6"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC7"] = TOTAL_df["HC7"] / TOTAL_df["forexrate"] 
    TOTAL_df["HC511_y"] = TOTAL_df["HC511_y"] / TOTAL_df["forexrate"] 
    TOTAL_df["TOTAL_PHARM"] = TOTAL_df["TOTAL_PHARM"] / TOTAL_df["forexrate"] 
    TOTAL_df["TOTAL_COST"] = TOTAL_df["TOTAL_COST"] / TOTAL_df["forexrate"] 
    
    # remove years before 2015
    TOTAL_df = TOTAL_df[TOTAL_df.TIME_PERIOD >= 2015]


    # save csv files locally
    TOTAL_df.to_csv("Data/HC_Market.csv", index=False)
    measuremeaning.to_csv("Data/HC_Market_meaning.csv", index=False)
    DOCTORS_since2015.to_csv("Data/Doctors_Region.csv", index=False)














