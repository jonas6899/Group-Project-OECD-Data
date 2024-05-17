
# %% prepare and import


import os
import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import ssl

# magic
ssl._create_default_https_context = ssl._create_unverified_context

# set working directory to file location
dname = os.getcwd()
os.chdir(dname)


# %% Dowload live data

def display_data():
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

    # %% Create summary table for HC expenditure

    # get necessary columns
    HC_EXP_since2015 = HC_EXP_since2015[["REF_AREA", "Reference area", "FUNCTION", "Health function", "TIME_PERIOD", "OBS_VALUE", "CURRENCY", "UNIT_MULT" ]]

    # remove duplicates
    HC_EXP_since2015 = HC_EXP_since2015.drop_duplicates()

    # get the real number of (by multiplying with )
    HC_EXP_since2015.UNIT_MULT = 10**HC_EXP_since2015.UNIT_MULT
    HC_EXP_since2015['TOTAL_EXP'] = HC_EXP_since2015.OBS_VALUE * HC_EXP_since2015.UNIT_MULT

    # put the expenditure value for each category in the column
    HC_EXP_wide = HC_EXP_since2015.pivot_table(index= ['REF_AREA', 'TIME_PERIOD', 'CURRENCY'], columns='FUNCTION', values='TOTAL_EXP', aggfunc='first')
    HC_EXP_wide = HC_EXP_wide.reset_index()


    # %% Create a summary table for expenditure Rx and OTC

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


    # %% Create a summary table for Gx

    # get necessary columns
    Gx_SALES_since2015 = Gx_SALES_since2015[["REF_AREA", "Reference area", "UNIT_MEASURE", "Unit of measure", "TIME_PERIOD", "OBS_VALUE"]]

    # remove duplicates
    Gx_SALES_since2015 = Gx_SALES_since2015.drop_duplicates()

    # get the real share as decimal
    Gx_SALES_since2015['SHARE'] = Gx_SALES_since2015.OBS_VALUE / 100

    # put the share for each category in the column
    Gx_SALES_wide = Gx_SALES_since2015.pivot_table(index= ['REF_AREA', 'TIME_PERIOD'], columns='UNIT_MEASURE', values='SHARE', aggfunc='first')
    Gx_SALES_wide = Gx_SALES_wide.reset_index()


    # %% Create a summary table for pharmaceutcal sales

    # get necessary columns
    PHARMA_SALES_since2015 = PHARMA_SALES_since2015[["REF_AREA", "Reference area", "TIME_PERIOD", "OBS_VALUE", "UNIT_MULT"]]

    # remove duplicates
    PHARMA_SALES_since2015 = PHARMA_SALES_since2015.drop_duplicates()

    # get the real number of (by multiplying with 10^MULT )
    PHARMA_SALES_since2015.UNIT_MULT = 10**PHARMA_SALES_since2015.UNIT_MULT
    PHARMA_SALES_since2015['TOTAL_PHARM'] = PHARMA_SALES_since2015.OBS_VALUE * PHARMA_SALES_since2015.UNIT_MULT

    # put the share for each category in the column
    PHARMA_SALES = PHARMA_SALES_since2015[["REF_AREA", "TIME_PERIOD", "TOTAL_PHARM"]]


    # %% Combine all tables together

    # combine all data frames together
    TOTAL_df = pd.merge(HC_EXP_wide,Rx_OTC_EXP_wide, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    TOTAL_df = pd.merge(TOTAL_df,Gx_SALES_wide, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    TOTAL_df = pd.merge(TOTAL_df,PHARMA_SALES, on=['REF_AREA', 'TIME_PERIOD'], how='outer')

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





    # %% get number of physicians in correct data format

    # get necessary columns
    DOCTORS_since2015 = DOCTORS_since2015[["TERRITORIAL_LEVEL", "REF_AREA", "Reference area", "TIME_PERIOD", "OBS_VALUE", "COUNTRY"]]

    # define country and filter df
    country = "CHE"
    filtered_doctors = DOCTORS_since2015[DOCTORS_since2015.COUNTRY == country]
    filtered_doctors = filtered_doctors[filtered_doctors.TERRITORIAL_LEVEL == "TL2" ]

    # Create a new figure explicitly
    fig, ax = plt.subplots()

    # get regions
    regions = filtered_doctors["Reference area"].drop_duplicates()

    # Plot each region separately
    for region in regions:
        region_data = filtered_doctors[filtered_doctors['Reference area'] == region]
        ax.plot(region_data['TIME_PERIOD'], region_data['OBS_VALUE'], label=region)

        # Add annotations for the first and last data points
        #plt.text(region_data['TIME_PERIOD'].iloc[0], region_data['OBS_VALUE'].iloc[0], str(region_data['OBS_VALUE'].iloc[0]), ha='right')
        #plt.text(region_data['TIME_PERIOD'].iloc[-1], region_data['OBS_VALUE'].iloc[-1], str(region_data['OBS_VALUE'].iloc[-1]), ha='left')

    # Add labels and legend
    ax.set_xlabel('Year')  # Changed plt.xlabel() to ax.set_xlabel()
    ax.set_ylabel('# physicians')  # Changed plt.ylabel() to ax.set_ylabel()
    ax.set_title('Number of physicians per region over the years')  # Changed plt.title() to ax.set_title()
    ax.legend()

    # return plot
    return fig







































