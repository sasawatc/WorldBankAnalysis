# from pathlib import Path
#
# # Import libraries and base dataset (og_file); then filter out/subset central africa 1
# import pandas as pd
#
# base_folder = Path('data/base')
# processed_folder = Path('data/processed')
# output_folder = Path('output')
#
# file_name = base_folder / 'MDGData.csv'
# df = pd.read_csv(file_name)
#
# gni_df = df[df['Indicator Name'] == 'GNI per capita, Atlas method (current US$)'].copy()
# gni_2014_df = gni_df[['Country Code', '2014']].copy()
# gni_2014_df.to_excel(output_folder / 'gni_2014_df.xlsx')
#
# ###################################################################
#
# file_name = processed_folder / 'clean_data.xlsx'
# clean_df = pd.read_excel(file_name)
#
# output = pd.merge(gni_2014_df, clean_df, left_on='Country Code', right_on='country_code')

import pandas as pd


def extract_mdg_indicator(indicator_val, indicator_title, mdg_file, year='2014'):
    df = pd.read_csv(mdg_file)
    gni_df = df[df['Indicator Name'] == indicator_val].copy()
    gni_2014_df = gni_df[['Country Code', year]].copy()
    gni_2014_df.rename(columns={year: indicator_title},
                       inplace=True)
    return gni_2014_df

