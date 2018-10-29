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


def extract_mdg_indicator(indicator_code, index_col, indicator_title, mdg_file, year):
    year = str(year)

    if str(mdg_file).lower().endswith('.csv'):
        df = pd.read_csv(mdg_file)
    elif str(mdg_file).lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(mdg_file)
    else:
        raise TypeError("Invalid File: File type not supported")

    gni_df = df[df['Indicator Code'] == indicator_code].copy()
    gni_2014_df = gni_df[[index_col, year]].copy()

    gni_2014_df.rename(columns={year: indicator_title},
                       inplace=True)

    return gni_2014_df


def replace_na(main_df, sub_df, target_main, target_sub, index_main, index_sub):
    main_df_copy = main_df.copy()
    missing_lst = main_df_copy.loc[main_df_copy[target_main].isnull(), index_main].tolist()

    for item in missing_lst:
        main_df_copy.at[main_df_copy[index_main] == item, target_main] = sub_df.loc[sub_df[index_sub] == item, target_sub].item()

    return main_df_copy