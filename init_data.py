# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018

For initializing datasets
"""

__version__ = '0.3.1'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')

from pathlib import Path

# Import libraries and base dataset (og_file); then filter out/subset central africa 1
import pandas as pd

from handy_func import *

base_folder = Path('data/base')
processed_folder = Path('data/processed')
output_folder = Path('output')

og_file = base_folder / 'world_data_hult_regions.xlsx'
data_set = pd.read_excel(og_file)
file2 = base_folder / 'API_VC.IHR.PSRC.P5_DS2_en_excel_v2_10181485.xls' #homicide rate database
homi_set = pd.read_excel(file2)

# processed_df = data_set  # Ham edit: trying to get the whole df instead of subsetting only ours

# fix typos from base file
data_set.loc[data_set.Hult_Team_Regions == "Central Aftica 1", 'Hult_Team_Regions'] = 'Central Africa 1'
data_set.rename(columns ={'CO2_emissions_per_capita)' : 'CO2_emissions_per_capita'}, inplace = True)

# subset central_africa1
central_africa1 = data_set[data_set['Hult_Team_Regions'] == "Central Africa 1"].copy()

central_africa1_df = central_africa1.copy()

# flag columns with missing value
""" Create columns that are 0s if a value was not missing and 1 if
a value is missing. """
for col in central_africa1_df:
    if central_africa1_df[col].isnull().any():
        central_africa1_df['m_' + col] = central_africa1_df[col].isnull().astype(int)

# check if flag columns worked: shows missing values per column in absolute numbers; +1 for True (missing), +0 for False
# print(processed_df.isnull().sum())
# or
central_africa1_df['adult_literacy_pct'].isnull().sum() == central_africa1_df['m_adult_literacy_pct'].sum()

################################################################################################

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
changes_dict = {"CPV": 86.8,  # (only 2015 data is available)
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

# fill in the remaining NAs with median
central_africa1_df.homicides_per_100k = central_africa1_df.homicides_per_100k.fillna(central_africa1_df.homicides_per_100k.median())

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

##############################################################################################
# reorder gni_index to be right before gdp_usd
central_africa1_df = central_africa1_df[['country_index', 'Hult_Team_Regions', 'country_name',
                                         'country_code', 'income_group', 'access_to_electricity_pop',
                                         'access_to_electricity_rural', 'access_to_electricity_urban',
                                         'CO2_emissions_per_capita', 'compulsory_edu_yrs', 'pct_female_employment',
                                         'pct_male_employment', 'pct_agriculture_employment',
                                         'pct_industry_employment', 'pct_services_employment',
                                         'exports_pct_gdp', 'fdi_pct_gdp', 'gni_index', 'gdp_usd', 'gdp_growth_pct',
                                         'incidence_hiv', 'internet_usage_pct', 'homicides_per_100k',
                                         'adult_literacy_pct', 'child_mortality_per_1k', 'avg_air_pollution',
                                         'women_in_parliament', 'tax_revenue_pct_gdp', 'unemployment_pct',
                                         'urban_population_pct', 'urban_population_growth_pct', 'm_compulsory_edu_yrs',
                                         'm_incidence_hiv', 'm_homicides_per_100k', 'm_adult_literacy_pct',
                                         'm_tax_revenue_pct_gdp']]
# export
central_africa1_df.to_excel(output_folder / 'clean_data.xlsx')
