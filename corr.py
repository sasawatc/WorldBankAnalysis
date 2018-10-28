import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

from pathlib import Path

# Import libraries and base dataset (og_file); then filter out/subset central africa 1
import pandas as pd

base_folder = Path('data/base')
processed_folder = Path('data/processed')
output_folder = Path('output')

#import clean data
clean_data = pd.read_excel(processed_folder / 'clean_data.xlsx', index='country_code')
country_data = clean_data.iloc[:, 2:]
print(country_data.head())

#check some data
print(country_data['income_group'])

list(country_data.columns.values)

data_describe = country_data.describe().round(2)
data_describe.loc['std',:].sort_values(ascending=False).round(2)



data_describe[['gdp_usd']].quantile([0.20,
                              0.40,
                              0.60,
                              0.80,
                              1.00])

data_describe[['gdp_usd']].quantile(1.00)-data_describe['gdp_usd'].quantile(0.8)

#plot outliers
country_data.boxplot(column=['gdp_usd'], by = 'income_group')

data_corr =country_data.corr().round(2)
print(data_corr)

sns.heatmap(data_corr, cmap='Blues',square = True,
            annot = False,
            linecolor = 'black',
            linewidths = 0.5)