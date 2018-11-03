# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018

Contains customized functions to make the lives of this project coders much better...
"""

__version__ = '1.0.0'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')

import pandas as pd
import re


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


def replace_na_skewness(col_series: pd.Series, skew_threshold: float = 0.2, mode: str = 'auto') -> pd.Series:
    if mode == 'auto':
        # print("Skewness:", col_series.skew())
        if -skew_threshold <= col_series.skew() <= skew_threshold:
            # print("Using MEAN")
            return col_series.fillna(col_series.mean())
        else:
            # print("Using MEDIAN")
            return col_series.fillna(col_series.median())
    elif mode == 'mean':
        return col_series.fillna(col_series.mean())
    elif mode == 'median':
        return col_series.fillna(col_series.median())
    else:
        raise ValueError("invalid mode: only accepts 'auto', 'mean', 'median'")


def replace_na_skewness_by_group(df: pd.DataFrame, by: str, skew_threshold: float = 0.2,
                                 mode: str = 'auto') -> pd.DataFrame:
    grouped_df_lst = list()
    for group in df[by].unique():
        grouped_df_lst.append(df[df[by] == group].copy())

    for each_df in grouped_df_lst:
        for col in each_df.select_dtypes(include=['float64', 'int']).columns:
            each_df.loc[:, col] = replace_na_skewness(col_series=each_df.loc[:, col])

    return pd.concat(grouped_df_lst, ignore_index=True)


def generate_title(txt: str) -> str:
    special_txt = {'Pct': '%', 'Vs': 'vs', 'Hiv': 'HIV', 'Gni': 'GNI', 'Co2': 'CO2', 'Gdp': 'GDP', 'Usd': 'USD',
                   'Fdi': 'FDI', 'Avg': 'AVG'}
    txt = txt.replace('_', ' ')
    txt = txt.title()

    pattern = re.compile('|'.join(special_txt.keys()))
    result = pattern.sub(lambda x: special_txt[x.group()], txt)

    return result
