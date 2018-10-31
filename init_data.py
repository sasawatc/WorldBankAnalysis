# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018


For initializing datasets
"""

__version__ = '0.3.1'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')

from handy_func import *

from pathlib import Path

# Import libraries and base dataset (og_file); then filter out/subset central africa 1
import pandas as pd
import numpy as np

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


# processed_df = data_set  # Ham edit: trying to get the whole df instead of subsetting only ours
# fix typo from base file
data_set.loc[data_set.Hult_Team_Regions == "Central Aftica 1", 'Hult_Team_Regions'] = 'Central Africa 1'

"""
subset dataframe for central africa1 only
"""
# subset central_africa1
central_africa1 = data_set[data_set['Hult_Team_Regions'] == "Central Africa 1"].copy()

central_africa1_df = central_africa1.copy()

# flag columns with missing value
for col in central_africa1_df:

    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """

    if central_africa1_df[col].isnull().any():
        central_africa1_df['m_' + col] = central_africa1_df[col].isnull().astype(int)

# check if flag columns worked: shows missing values per column in absolute numbers; +1 for True (missing), +0 for False
# print(processed_df.isnull().sum())
# or
central_africa1_df['adult_literacy_pct'].isnull().sum() == central_africa1_df['m_adult_literacy_pct'].sum()

#########################################################################

extracted_df = extract_mdg_indicator(indicator_code="SE.ADT.LITR.ZS",
                                     indicator_title="adult_lit_rate",
                                     index_col="Country Code",
                                     mdg_file=base_folder / "MDGData.csv",
                                     year="2015")

central_africa1_df = replace_na(main_df=central_africa1_df,
                                sub_df=extracted_df,
                                target_main='adult_literacy_pct',
                                target_sub='adult_lit_rate',
                                index_main='country_code',
                                index_sub='Country Code')

# missing adult_lit_rate based on CIA World Factbook 2015 data
changes_dict = {"CPV": 86.8,  # (only 2016 data is available)
                "COM": 77.8,
                "COD": 77.0,
                "COG": 79.3,
                "GNQ": 95.3,
                "GHA": 76.6,
                "NGA": 59.6,
                "RWA": 70.5,
                "SEN": 57.7,
                "SDN": 75.9,
                "UGA": 78.4}

for country, val in changes_dict.items():
    central_africa1_df.at[central_africa1_df.country_code == country, 'adult_literacy_pct'] = val

# input missing HIV incidence value for Cabo Verde (only 2016 data is available)
central_africa1_df.at[central_africa1_df.country_code == 'CPV', 'incidence_hiv'] = 0.05

# input missing compulsory education for Burundi from Scholaro data
central_africa1_df.at[central_africa1_df.country_code == 'BDI', 'compulsory_edu_yrs'] = 6

# df = pd.DataFrame(dict(country=['A', 'B', 'C', 'D'], issuer=['Ai', np.nan, 'Ci', np.nan]))
# df2 = pd.DataFrame(dict(countries=['C', 'A', 'B', 'D'], test=['Ham', 'Win', 'Jacob', 'Masato']))

#########################################################################
#########################################################################

# # Import supplementary data set
# extra_file = base_folder / 'MDGEXCEL.xlsx'
# extra_data = pd.read_excel(extra_file)
#
# # create an adult literacy rate dataframe
# # make a list (Series) with the country_code
# country_list = central_africa1_df['country_code']
# country_name_list = central_africa1_df['country_name']
# country_name_list.to_excel(output_folder / 'country_name_list.xlsx')
# # create a variable (var1) that equals rows that contain this string about adult literacy rate
# vari1 = "Literacy rate, adult total (% of people ages 15 and above)"
#
# # from the supplementary data set, filter out data under the "indicator name" column that contains the string in vari1
# indicators1 = extra_data.loc[extra_data["Indicator Name"] == vari1]
#
#
# # create adult literacy rate empty list
# alrate = []
# # for loop to add the data in the indicators1 dataframe that match our central africa 1 countries, into our empty list: alrate
# for i in country_list:
#     countryinfo = indicators1.loc[indicators1[
#                                       "Country Code"] == i]  # find all the corresponding data who's country codes match the country code in our Central Africa 1 datafram
#     alrate.append(countryinfo)
#
# # turn alrate from List to DataFrame
# alrate = pd.concat(alrate)
#
# # flag columns with null values
# for col in alrate:
#
#     """ Create columns that are 0s if a value was not missing and 1 if
#     a value is missing. """
#
#     if alrate[col].isnull().any():
#         alrate['m_' + col] = alrate[col].isnull().astype(int)
#
# # manually input missing values based on CIA World Factbook data into alrate
# # input missing adult literacy rate for Comoros (2015)
# alrate.loc[11812, '2015'] = 77.8
# # input missing adult literacy rate for Congo Dem Rep (2015)
# alrate.loc[11944, '2015'] = 77.0
# # input missing adult literacy rate for Congo Rep (2015)
# alrate.loc[12076, '2015'] = 79.3
# # input missing adult literacy rate for Equatorial Guinea (2015)
# alrate.loc[14056, '2015'] = 95.3
# # input missing adult literacy rate for Ghana (2015)
# alrate.loc[15904, '2015'] = 76.6
# # input missing adult literacy rate for Nigeria (2015)
# alrate.loc[25276, '2015'] = 59.6
# # input missing adult literacy rate for Rwanda (2015)
# alrate.loc[27520, '2015'] = 70.5
# # input missing adult literacy rate for Senegal (2015)
# alrate.loc[28180, '2015'] = 57.7
# # input missing adult literacy rate for Sudan (2015)
# alrate.loc[30556, '2015'] = 75.9
# # input missing adult literacy rate for Uganda (2015)
# alrate.loc[32800, '2015'] = 78.4
#
# ##########put missing rates into its own list/dataframe###########
# ##########call all of our country's rows into one list/dataframe###########
# # then use alrate.loc[list of country's rows, '2015' = [list of found missing values]]
# # alrate.loc[[values]]
#
#
# ###now add missing values to central_africa1
# ##from CIA World Factbook data
#
# # input missing HIV incidence value for Cabo Verde (only 2016 data is available)
# central_africa1_df.loc[16, 'incidence_hiv'] = 0.05
# # input missing adult literacy rate for Cabo Verde
# central_africa1_df.loc[16, 'adult_literacy_pct'] = 86.8
# # input missing adult literacy rate for Comoros
# central_africa1_df.loc[27, 'adult_literacy_pct'] = 77.8
# # input missing adult literacy rate for Congo dem rep
# central_africa1_df.loc[28, 'adult_literacy_pct'] = 77.0
# # input missing Hadult literacy rate for Congo rep
# central_africa1_df.loc[26, 'adult_literacy_pct'] = 79.3
# # input missing adult literacy rate for Equatorial Guinea
# central_africa1_df.loc[21, 'adult_literacy_pct'] = 95.3
# # input missing adult literacy rate for Ghana
# central_africa1_df.loc[17, 'adult_literacy_pct'] = 76.6
# # input missing adult literacy rate for Nigeria
# central_africa1_df.loc[19, 'adult_literacy_pct'] = 59.6
# # input missing adult literacy rate for Rwanda
# central_africa1_df.loc[25, 'adult_literacy_pct'] = 70.5
# # input missing adult literacy rate for Senegal
# central_africa1_df.loc[22, 'adult_literacy_pct'] = 57.7
# # input missing adult literacy rate for Sudan
# central_africa1_df.loc[18, 'adult_literacy_pct'] = 75.9
# # input missing adult literacy rate for Uganda
# central_africa1_df.loc[23, 'adult_literacy_pct'] = 78.4
#
# # from Scholaro data, input missing Burundi compulsory education
# central_africa1_df.loc[29, 'compulsory_edu_yrs'] = 6

################################################################################################
# input tax_revenue_pct_gdp data

# data from ...
changes_dict = {"CPV": 25.3,
                "GHA": 20.3,
                "SDN": 6.9,
                "NGA": 3.5,
                "UGA": 19.7,
                "COG": 32.3,
                "COM": 22.6,
                "COD": 8,
                "BDI": 17.9}

for country, val in changes_dict.items():
    central_africa1_df.at[central_africa1_df.country_code == country, 'tax_revenue_pct_gdp'] = val

##############################################################################################

##############################################################################################
# homicides_per_100k
extracted_df = extract_mdg_indicator(indicator_code="VC.IHR.PSRC.P5",
                                     indicator_title="homicides_per_100k",
                                     index_col="Country Code",
                                     mdg_file=base_folder / "API_VC.IHR.PSRC.P5_DS2_en_excel_v2_10181485.xls",
                                     year="2015")

central_africa1_df = replace_na(main_df=central_africa1_df,
                                sub_df=extracted_df,
                                target_main='homicides_per_100k',
                                target_sub='homicides_per_100k',
                                index_main='country_code',
                                index_sub='Country Code')

    


##############################################################################################

##############################################################################################
# extract gni_index

extracted_df = extract_mdg_indicator(indicator_code='NY.GNP.PCAP.CD',
                                     indicator_title='gni_index',
                                     index_col="Country Code",
                                     mdg_file=base_folder / 'MDGData.csv',
                                     year='2014')

central_africa1_df = pd.merge(extracted_df, central_africa1_df,
                              left_on='Country Code',
                              right_on='country_code').copy()

central_africa1_df = central_africa1_df.drop(columns=['Country Code'])

# reorder gni_index to be right before gdp_usd
central_africa1_df = central_africa1_df[['country_index', 'Hult_Team_Regions', 'country_name',
                                         'country_code', 'income_group', 'access_to_electricity_pop',
                                         'access_to_electricity_rural', 'access_to_electricity_urban',
                                         'CO2_emissions_per_capita)', 'compulsory_edu_yrs', 'pct_female_employment',
                                         'pct_male_employment', 'pct_agriculture_employment',
                                         'pct_industry_employment', 'pct_services_employment',
                                         'exports_pct_gdp', 'fdi_pct_gdp', 'gni_index', 'gdp_usd', 'gdp_growth_pct',
                                         'incidence_hiv', 'internet_usage_pct', 'homicides_per_100k',
                                         'adult_literacy_pct', 'child_mortality_per_1k', 'avg_air_pollution',
                                         'women_in_parliament', 'tax_revenue_pct_gdp', 'unemployment_pct',
                                         'urban_population_pct', 'urban_population_growth_pct', 'm_compulsory_edu_yrs',
                                         'm_incidence_hiv', 'm_homicides_per_100k', 'm_adult_literacy_pct',
                                         'm_tax_revenue_pct_gdp']]
if central_africa1['homicides_per_100k'].isnull().any():
        col_median = central_africa1['homicides_per_100k'].median()
        central_africa1['homicides_per_100k'] = central_africa1['homicides_per_100k'].fillna(col_median)
# export
central_africa1_df.to_excel(output_folder / 'clean_data.xlsx')

##############################################################################################
# alrate_transpose = alrate.transpose()


##find list of country with empty literacy rate
# alrate_list = alrate[["Country Code",'2014']]
# alrate_nalist = alrate_list[alrate_list['2014'].isnull()].drop('2014', axis=1)
# alrate_nalist = list(alrate_nalist['Country Code'])
# print(alrate_nalist)


# fillment1:fill missing data by 2013 or 2015 data

# fillment2: fill by regression model
# extra2 = extra_data[extra_data["Country Name"]=="Cabo Verde"]
# extra2 = pd.pivot_table(extra2, index='Indicator Name')
# corr = extra2.corr(method='pearson', min_periods=1)
# print(corr)

# # fillment3: homicede missing data
# data_set = data_set.set_index('country_code')
# data_set.update(homi_set.set_index('Country Code')
#                 .rename(columns={'2014': 'homicides_per_100k'}))

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