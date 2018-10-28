# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018


For initializing datasets
"""

__version__ = '0.2.0'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')

from pathlib import Path

# Import libraries and base dataset (og_file); then filter out/subset central africa 1
import pandas as pd

base_folder = Path('data/base')
processed_folder = Path('data/processed')
output_folder = Path('output')

og_file = base_folder / 'world_data_hult_regions.xlsx'
data_set = pd.read_excel(og_file)
file2 = base_folder / 'API_VC.IHR.PSRC.P5_DS2_en_excel_v2_10181485.xls'
homi_set = pd.read_excel(file2)

# Ying's originals
########################################################################
# df_data_set = pd.DataFrame.copy(data_set)
#
# # locate the values in the data_set, where column 'Team Regions' == "Central Aftica"
# central_africa1 = data_set[data_set['Hult_Team_Regions'] == "Central Aftica 1"]
#
# # within the new dataframe 'central_africa1', locate its 'hult team regions' column, and replace the values '...Aftica 1' with '...Africa 1'. Reflect the changes back in the dataframe 'central_africa1'
# central_africa1.loc[:, 'Hult_Team_Regions'] = 'Central Africa 1'
#
# print(central_africa1.head())
########################################################################

central_africa1 = data_set  # Ham edit: trying to get the whole df instead of subsetting only ours
central_africa1.loc[
    central_africa1.Hult_Team_Regions == "Central Aftica 1", 'Hult_Team_Regions'] = 'Central Africa 1'  # fix typo from base file

# flag columns with missing value
for col in central_africa1:

    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """

    if central_africa1[col].isnull().any():
        central_africa1['m_' + col] = central_africa1[col].isnull().astype(int)

# check if flag columns worked: shows missing values per column in absolute numbers; +1 for True (missing), +0 for False
print(central_africa1.isnull().sum())
# or
central_africa1['adult_literacy_pct'].isnull().sum() == central_africa1['m_adult_literacy_pct'].sum()

# Import supplementary data set
extra_file = base_folder / 'MDGEXCEL.xlsx'
extra_data = pd.read_excel(extra_file)

# create an adult literacy rate dataframe
# make a list (Series) with the country_code
country_list = central_africa1['country_code']
country_name_list = central_africa1['country_name']
country_name_list.to_excel(output_folder / 'country_name_list.xlsx')
# create a variable (var1) that equals rows that contain this string about adult literacy rate
vari1 = "Literacy rate, adult total (% of people ages 15 and above)"

# from the supplementary data set, filter out data under the "indicator name" column that contains the string in vari1
indicators1 = extra_data.loc[extra_data["Indicator Name"] == vari1]

# create adult literacy rate empty list
alrate = []
# for loop to add the data in the indicators1 dataframe that match our central africa 1 countries, into our empty list: alrate
for i in country_list:
    countryinfo = indicators1.loc[indicators1[
                                      "Country Code"] == i]  # find all the corresponding data who's country codes match the country code in our Central Africa 1 datafram
    alrate.append(countryinfo)

# turn alrate from List to DataFrame
alrate = pd.concat(alrate)

# flag columns with null values
for col in alrate:

    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """

    if alrate[col].isnull().any():
        alrate['m_' + col] = alrate[col].isnull().astype(int)

# manually input missing values based on CIA World Factbook data into alrate
# input missing adult literacy rate for Comoros (2015)
alrate.loc[11812, '2015'] = 77.8
# input missing adult literacy rate for Congo Dem Rep (2015)
alrate.loc[11944, '2015'] = 77.0
# input missing adult literacy rate for Congo Rep (2015)
alrate.loc[12076, '2015'] = 79.3
# input missing adult literacy rate for Equatorial Guinea (2015)
alrate.loc[14056, '2015'] = 95.3
# input missing adult literacy rate for Ghana (2015)
alrate.loc[15904, '2015'] = 76.6
# input missing adult literacy rate for Nigeria (2015)
alrate.loc[25276, '2015'] = 59.6
# input missing adult literacy rate for Rwanda (2015)
alrate.loc[27520, '2015'] = 70.5
# input missing adult literacy rate for Senegal (2015)
alrate.loc[28180, '2015'] = 57.7
# input missing adult literacy rate for Sudan (2015)
alrate.loc[30556, '2015'] = 75.9
# input missing adult literacy rate for Uganda (2015)
alrate.loc[32800, '2015'] = 78.4

##########put missing rates into its own list/dataframe###########
##########call all of our country's rows into one list/dataframe###########
# then use alrate.loc[list of country's rows, '2015' = [list of found missing values]]
# alrate.loc[[values]]


###now add missing values to central_africa1
##from CIA World Factbook data

# input missing HIV incidence value for Cabo Verde (only 2016 data is available)
central_africa1.loc[16, 'incidence_hiv'] = 0.05
# input missing adult literacy rate for Cabo Verde
central_africa1.loc[16, 'adult_literacy_pct'] = 86.8
# input missing adult literacy rate for Comoros
central_africa1.loc[27, 'adult_literacy_pct'] = 77.8
# input missing adult literacy rate for Congo dem rep
central_africa1.loc[28, 'adult_literacy_pct'] = 77.0
# input missing Hadult literacy rate for Congo rep
central_africa1.loc[26, 'adult_literacy_pct'] = 79.3
# input missing adult literacy rate for Equatorial Guinea
central_africa1.loc[21, 'adult_literacy_pct'] = 95.3
# input missing adult literacy rate for Ghana
central_africa1.loc[17, 'adult_literacy_pct'] = 76.6
# input missing adult literacy rate for Nigeria
central_africa1.loc[19, 'adult_literacy_pct'] = 59.6
# input missing adult literacy rate for Rwanda
central_africa1.loc[25, 'adult_literacy_pct'] = 70.5
# input missing adult literacy rate for Senegal
central_africa1.loc[22, 'adult_literacy_pct'] = 57.7
# input missing adult literacy rate for Sudan
central_africa1.loc[18, 'adult_literacy_pct'] = 75.9
# input missing adult literacy rate for Uganda
central_africa1.loc[23, 'adult_literacy_pct'] = 78.4

# from Scholaro data, input missing Burundi compulsory education
central_africa1.loc[29, 'compulsory_edu_yrs'] = 6

################################################################################################
# input tax_revenue_pct_gdp data

# data from ...
changes_dict = {"Cabo Verde": 25.3,
                "Ghana": 20.3,
                "Sudan": 6.9,
                "Nigeria": 3.5,
                "Uganda": 19.7,
                "Congo, Rep.": 32.3,
                "Comoros": 22.6,
                "Congo, Dem. Rep.": 8,
                "Burundi": 17.9}

for country, val in changes_dict.items():
    central_africa1.at[central_africa1.country_name == country, 'tax_revenue_pct_gdp'] = val
# tax_data = pd.read_excel(processed_folder / 'world_data_hult.xlsx')
# tax_data = tax_data.loc[tax_data['Hult_Team_Regions'] == "Central Aftica 1", ['tax_revenue_pct_gdp']]
# central_africa1.update(tax_data, overwrite=True)

##############################################################################################
# alrate_transpose = alrate.transpose()


##find list of country with empty literacy rate
# alrate_list = alrate[["Country Code",'2014']]
# alrate_nalist = alrate_list[alrate_list['2014'].isnull()].drop('2014', axis=1)
# alrate_nalist = list(alrate_nalist['Country Code'])
# print(alrate_nalist)


# fillment1:fill missing data by 2013 or 2015 data

alrate.ix[10360, '2014'] = alrate.ix[10360, '2015']
alrate.ix[28180, '2014'] = alrate.ix[28180, '2013']

# fillment2: fill by regression model
# extra2 = extra_data[extra_data["Country Name"]=="Cabo Verde"]
# extra2 = pd.pivot_table(extra2, index='Indicator Name')
# corr = extra2.corr(method='pearson', min_periods=1)
# print(corr)

# fillment3: homicede missing data
data_set = data_set.set_index('country_code')
data_set.update(homi_set.set_index('Country Code')
                .rename(columns={'2014': 'homicides_per_100k'}))

##substract school enrollment rate
#
# vari2 = "School enrollment, primary (% net)"
# indicators2 = extra_data.loc[extra_data["Indicator Name"]==vari2]
# schrate=[]
# for i in country_list:
#    countryinfo = indicators2.loc[indicators2["Country Code"]==i]
#    schrate.append(countryinfo)
#
# schrate = pd.concat(schrate)


central_africa1.to_excel(output_folder / 'clean_data.xlsx')
