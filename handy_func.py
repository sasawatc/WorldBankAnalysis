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


def extract_mdg_indicator(indicator_code: str, index_col: str, indicator_title: str, mdg_file_path: str,
                          year: str) -> pd.DataFrame:
    year = str(year)

    if str(mdg_file_path).lower().endswith('.csv'):
        df = pd.read_csv(mdg_file_path)
    elif str(mdg_file_path).lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(mdg_file_path)
    else:
        raise TypeError("Invalid File: File type not supported")

    selected_df = df[df['Indicator Code'] == indicator_code].copy()
    selected_df = selected_df[[index_col, year]].copy()

    selected_df.rename(columns={year: indicator_title},
                       inplace=True)

    return selected_df


def replace_na(main_df: pd.DataFrame, sub_df: pd.DataFrame, target_main: str, target_sub: str, index_main: str,
               index_sub: str) -> pd.DataFrame:
    main_df_copy = main_df.copy()
    missing_lst = main_df_copy.loc[main_df_copy[target_main].isnull(), index_main].tolist()

    for item in missing_lst:
        main_df_copy.at[main_df_copy[index_main] == item, target_main] = sub_df.loc[
            sub_df[index_sub] == item, target_sub].item()

    return main_df_copy


def replace_na_mean_median(col_series: pd.Series, mode: str = 'auto') -> pd.Series:

    if mode == 'auto':
        print("Skewness:", col_series.skew())
        if -0.2 <= col_series.skew() <= 0.2:
            print("Using MEAN")
            return col_series.fillna(col_series.mean())
        else:
            print("Using MEDIAN")
            return col_series.fillna(col_series.median())
    elif mode == 'mean':
        return col_series.fillna(col_series.mean())
    elif mode == 'median':
        return col_series.fillna(col_series.median())
    else:
        raise ValueError("invalid mode: only accepts 'auto', 'mean', 'median'")
