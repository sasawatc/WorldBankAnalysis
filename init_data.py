# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018

For initializing datasets
"""

__version__ = '1.0.0'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')


def init_data():
    from pandas import DataFrame
    from pathlib import Path

    # Import libraries and base dataset (og_file); then filter out/subset central africa 1
    import pandas as pd

    from handy_func import extract_mdg_indicator, replace_na_skewness_by_group

    ##############################################################################################
    # declare directory paths
    base_folder = Path('data/base')
    processed_folder = Path('data/processed')

    og_file = base_folder / 'world_data_hult_regions.xlsx'
    data_set: DataFrame = pd.read_excel(og_file)

    ##############################################################################################
    # fix typos from base file
    data_set.loc[data_set.Hult_Team_Regions == "Central Aftica 1", 'Hult_Team_Regions'] = 'Central Africa 1'
    data_set.rename(columns={'CO2_emissions_per_capita)': 'CO2_emissions_per_capita'}, inplace=True)

    ##############################################################################################
    # drop unwanted row
    data_set = data_set.drop(data_set.loc[data_set.country_name == 'World'].index).copy()

    ##############################################################################################
    # flag columns with missing value
    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """
    for col in data_set:
        if data_set[col].isnull().any():
            data_set['m_' + col] = data_set[col].isnull().astype(int)

    ##############################################################################################
    # drop bad columns
    data_set = data_set.drop(columns=['adult_literacy_pct', 'homicides_per_100k', 'tax_revenue_pct_gdp']).copy()

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
    # separate by income_group and replace NA by mean/median according to skewness

    data_set = replace_na_skewness_by_group(df=data_set,
                                            by='income_group').copy()

    ##############################################################################################
    # reorder gni_index to be right before gdp_usd
    data_set = data_set[['country_index', 'Hult_Team_Regions', 'country_name', 'country_code',
                         'income_group', 'access_to_electricity_pop', 'access_to_electricity_rural',
                         'access_to_electricity_urban', 'CO2_emissions_per_capita', 'compulsory_edu_yrs',
                         'pct_female_employment', 'pct_male_employment', 'pct_agriculture_employment',
                         'pct_industry_employment', 'pct_services_employment', 'exports_pct_gdp',
                         'fdi_pct_gdp', 'gni_index', 'gdp_usd', 'gdp_growth_pct', 'incidence_hiv',
                         'internet_usage_pct', 'child_mortality_per_1k',
                         'avg_air_pollution', 'women_in_parliament', 'unemployment_pct',
                         'urban_population_pct', 'urban_population_growth_pct', 'm_access_to_electricity_pop',
                         'm_access_to_electricity_rural', 'm_access_to_electricity_urban',
                         'm_CO2_emissions_per_capita', 'm_compulsory_edu_yrs', 'm_pct_female_employment',
                         'm_pct_male_employment', 'm_pct_agriculture_employment', 'm_pct_industry_employment',
                         'm_pct_services_employment', 'm_exports_pct_gdp', 'm_fdi_pct_gdp', 'm_gdp_usd',
                         'm_gdp_growth_pct', 'm_incidence_hiv', 'm_internet_usage_pct', 'm_child_mortality_per_1k',
                         'm_avg_air_pollution', 'm_women_in_parliament', 'm_unemployment_pct', 'm_urban_population_pct',
                         'm_urban_population_growth_pct', 'm_adult_literacy_pct', 'm_homicides_per_100k',
                         'm_tax_revenue_pct_gdp']]

    ##############################################################################################
    # export
    data_set.to_excel(processed_folder / 'clean_data.xlsx')

    # subset central_africa1 and export
    central_africa1_df: DataFrame = data_set[data_set['Hult_Team_Regions'] == "Central Africa 1"]
    central_africa1_df.reset_index(drop=True, inplace=True)
    central_africa1_df.to_excel(processed_folder / "clean_data_central_africa.xlsx")

    ##############################################################################################
