# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018

For initializing datasets
"""

from pandas import DataFrame

__version__ = '0.5.0'
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
data_set: DataFrame = pd.read_excel(og_file)

# fix typos from base file
data_set.loc[data_set.Hult_Team_Regions == "Central Aftica 1", 'Hult_Team_Regions'] = 'Central Africa 1'
data_set.rename(columns={'CO2_emissions_per_capita)': 'CO2_emissions_per_capita'}, inplace=True)

# flag columns with missing value
""" Create columns that are 0s if a value was not missing and 1 if
a value is missing. """
for col in data_set:
    if data_set[col].isnull().any():
        data_set['m_' + col] = data_set[col].isnull().astype(int)

##############################################################################################
# extract gni_index and add gni_index
extracted_df = extract_mdg_indicator(indicator_code='NY.GNP.PCAP.CD',
                                     indicator_title='gni_index',
                                     index_col="Country Code",
                                     mdg_file_path=base_folder / 'MDGData.csv',
                                     year='2014')

data_set = pd.merge(extracted_df, data_set,
                    left_on='Country Code',
                    right_on='country_code').copy()

data_set = data_set.drop(columns=['Country Code'])

##############################################################################################
# drop bad columns
data_set.drop(columns=['adult_literacy_pct', 'homicides_per_100k', 'tax_revenue_pct_gdp'])

##############################################################################################
# fill in the remaining NAs with mean/median based on skewness
for col in data_set.select_dtypes(include=['float64', 'int']).columns:
    data_set[col] = replace_na_mean_median(col_series=data_set[col])

##############################################################################################
# reorder gni_index to be right before gdp_usd
data_set = data_set[['country_index', 'Hult_Team_Regions', 'country_name',
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
data_set.to_excel(output_folder / 'clean_data.xlsx')

# subset central_africa1 and export
central_africa1_df: DataFrame = data_set[data_set['Hult_Team_Regions'] == "Central Africa 1"].copy()
central_africa1_df.to_excel(output_folder / "clean_data_central_africa.xlsx")
