import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

from pathlib import Path

# Import libraries and base dataset (og_file); then filter out/subset central africa 1

base_folder = Path('data/base')
processed_folder = Path('data/processed')
output_folder = Path('output')

#import clean data
clean_data = pd.read_excel(output_folder / 'clean_data.xlsx', index='country_code')
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
for col in country_data.select_dtypes(include=['float64', 'int']):
    country_data.boxplot(column = col, by = 'income_group')
    plt.title(col)
    plt.suptitle("")
    plt.tight_layout()
    plt.show()
<<<<<<< Updated upstream
    

=======

"""
Outlier for exports_pct_gdp
"""

country_data[country_data['income_group'] == 'Low income']['exports_pct_gdp']
# flag: 30 is outlier threshold for low income country
country_data['out_exports_pct_gdp'] = 0
for index, value in enumerate(country_data['exports_pct_gdp']):
    if value > 30 and country_data.loc[index, 'income_group'] == 'Low income':
        country_data.loc[index, 'out_exports_pct_gdp'] = 1

# histgram
sns.distplot(country_data['exports_pct_gdp']) 
plt.axvline(x = 30,
            label = 'Outlier Thresholds (low income countries)')
plt.show()

# plot 

sns.pairplot(x_vars=['exports_pct_gdp'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = 30,
            label = 'Outlier Thresholds (low income countries)')
plt.show()
"""
Outlier for fdi_pct_gdp
"""
# overview
country_data[country_data['income_group'] == 'Low income']['fdi_pct_gdp']

# flag: 4.5 is outlier threshold for low income country
country_data['out_fdi_pct_gdp'] = 0
for index, value in enumerate(country_data['fdi_pct_gdp']):
    if value > 4.5 and country_data.loc[index, 'income_group'] == 'Low income':
        country_data.loc[index, 'out_fdi_pct_gdp'] = 1
# histgram
sns.distplot(country_data['fdi_pct_gdp']) 
plt.axvline(x = 4.5,
            label = 'Outlier Thresholds (low income countries)')
plt.show()

# plot 

sns.pairplot(x_vars=['fdi_pct_gdp'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = 4.5,
            label = 'Outlier Thresholds (low income countries)')

plt.show()


"""
Outlier for internet_usage_pct
"""
# overview
country_data[country_data['income_group'] == 'Lower middle income']['internet_usage_pct']

# flag: 27 is upper outlier threshold and 15 is lower outlier threshold for lower middle income country
country_data['out_internet_usage_pct'] = 0
for index, value in enumerate(country_data['internet_usage_pct']):
    if value > 27 and country_data.loc[index, 'income_group'] == 'Lower middle income':
        country_data.loc[index, 'out_internet_usage_pct'] = 1
    elif value < 15 and country_data.loc[index, 'income_group'] == 'Lower middle income':
        country_data.loc[index, 'out_internet_usage_pct'] = 1
        
        
# histgram
sns.distplot(country_data['internet_usage_pct']) 
plt.axvline(x = 27,
            label = 'Upper Outlier Thresholds (low income countries)')
plt.axvline(x = 15,
            label = 'Lower Outlier Thresholds (low income countries)')
plt.show()

# plot 


sns.pairplot(x_vars=['internet_usage_pct'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = 27,
            label = 'Upper Outlier Thresholds (low income countries)',
            color = 'orange')
plt.axvline(x = 15,
            label = 'Lower Outlier Thresholds (low income countries)',
            color = 'orange')

plt.show()


    
>>>>>>> Stashed changes
country_data.boxplot(column=['gdp_usd'], by = 'income_group')
country_data.boxplot(column=['gni_index'], by = 'income_group')

###############################################################################
# Correlation Matrix for all variables   --->>> how to take out the missing values
###############################################################################    
data_corr =country_data.corr().round(2)
print(data_corr)

sns.heatmap(data_corr, cmap='Blues',square = True,
            annot = False,
            linecolor = 'black',
            linewidths = 0.5)

###############################################################################
# Distplots (without cutoffs)
###############################################################################

## pct_female_employment
plt.subplot(2,2,1)
sns.distplot(country_data['pct_female_employment'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Female Employment')

## pct_male_employment 
plt.subplot(2,2,2)
sns.distplot(country_data['pct_male_employment'], bins = 'fd', kde = False, rug = True, color = 'forestgreen')
plt.xlabel('Male Employment')

## pct_services_employment 
plt.subplot(2,2,3)
sns.distplot(country_data['pct_services_employment'], bins = 'fd', kde = False, rug = True, color = 'cornflowerblue')
plt.xlabel('Services Employment')

##gdp_usd
plt.subplot(2,2,4)
sns.distplot(country_data['gdp_usd'], bins = 'fd', kde = False, rug = True, color = 'slategrey')
plt.xlabel('GDP (USD)')

plt.tight_layout()
plt.savefig('4 5 6 10 Histograms w/o cutoffs.png')
plt.show()


##adult_literacy_pct
plt.subplot(2,2,1)
sns.distplot(country_data['adult_literacy_pct'], bins = 'fd', kde = False, rug = True, color = 'coral')
plt.xlabel('Adult Literacy Rate')

## avg_air_pollution
plt.subplot(2,2,2)
sns.distplot(country_data['avg_air_pollution'], bins = 'fd', kde = False, rug = True, color = 'plum')
plt.xlabel('Avg Air Pollution')

##tax_revenue_pct_gdp
plt.subplot(2,2,3)
sns.distplot(country_data['tax_revenue_pct_gdp'], bins = 'fd', kde = False, rug = True, color = 'orange')
plt.xlabel('Tax Revenue PCT GDP')

plt.tight_layout()
plt.savefig('12, 13, 14 Histograms w/o cutoffs.png')
plt.show()

###############################################################################
# outlier cutoffs
###############################################################################

femploy_limit_hi = 45
memploy_limit_hi = 20
servemploy_lo = 15
gdp_usd_hi = 90000000000
adult_lit_lo = 45
airpoll_limit_lo = 22
tax_rev_limit = 30


###############################################################################
# distplots with cutoff points
###############################################################################

## pct_female_employment
plt.subplot(2,2,1)
sns.distplot(country_data['pct_female_employment'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Female Employment')

plt.axvline(x = femploy_limit_hi, label = 'Outlier Threshold', linestyle = '--', color = 'y')


## pct_male_employment 
plt.subplot(2,2,2)
sns.distplot(country_data['pct_male_employment'], bins = 'fd', kde = False, rug = True, color = 'forestgreen')
plt.xlabel('Male Employment')

plt.axvline(x = memploy_limit_hi, label = 'Outlier Threshold', linestyle = '--', color = 'b')

## pct_services_employment 
plt.subplot(2,2,3)
sns.distplot(country_data['pct_services_employment'], bins = 'fd', kde = False, rug = True, color = 'cornflowerblue')
plt.xlabel('Services Employment')

plt.axvline(x = servemploy_lo, label = 'Outlier Thresholds', linestyle = '--', color = 'orangered')

##gdp_usd
plt.subplot(2,2,4)
sns.distplot(country_data['gdp_usd'], bins = 'fd', kde = False, rug = True, color = 'slategrey')
plt.xlabel('GDP (USD)')

plt.axvline(x = gdp_usd_hi, label = 'Outlier Thresholds', linestyle = '--', color = 'green')

plt.tight_layout()
plt.savefig('4 5 6 10 Histograms with cutoffs.png')
plt.show()

##adult_literacy_pct
plt.subplot(2,2,1)
sns.distplot(country_data['adult_literacy_pct'], bins = 'fd', kde = False, rug = True, color = 'coral')
plt.xlabel('Adult Literacy Rate')

plt.axvline(x = adult_lit_lo, label = 'Outlier Thresholds', linestyle = '--', color = 'darkmagenta')

## avg_air_pollution
plt.subplot(2,2,2)
sns.distplot(country_data['avg_air_pollution'], bins = 'fd', kde = False, rug = True, color = 'plum')
plt.xlabel('Avg Air Pollution')

plt.axvline(x = airpoll_limit_lo, label = 'Outlier Thresholds', linestyle = '--', color = 'darkturquoise')

##tax_revenue_pct_gdp
plt.subplot(2,2,3)
sns.distplot(country_data['tax_revenue_pct_gdp'], bins = 'fd', kde = False, rug = True, color = 'orange')
plt.xlabel('Tax Revenue PCT GDP')

plt.axvline(x = tax_rev_limit, label = 'Outlier Thresholds', linestyle = '--', color = 'k')

plt.tight_layout()
plt.savefig('12 13 14 Histograms with cutoffs.png')
plt.show()


###############################################################################
# Flagging Outliers
###############################################################################

## pct_female_employment
country_data['out_pct_female_employment'] = 0

for val in enumerate(country_data.loc[ : , 'pct_female_employment']):
    if val[1] > femploy_limit_hi:
        country_data.loc[val[0], 'out_pct_female_employment'] = 1

country_data['out_pct_female_employment'].abs().sum()
check = (country_data.loc[ : , ['pct_female_employment', 'out_pct_female_employment']].sort_values('pct_female_employment', ascending = False))

## pct_male_employment 
country_data['out_pct_male_employment'] = 0

for val in enumerate(country_data.loc[ : , 'pct_male_employment']):
    if val[1] > memploy_limit_hi:
        country_data.loc[val[0], 'out_pct_male_employment'] = 1

country_data['out_pct_male_employment'].abs().sum()
check = (country_data.loc[ : , ['pct_male_employment', 'out_pct_male_employment']].sort_values('pct_male_employment', ascending = False))

## pct_services_employment 
country_data['out_pct_services_employment'] = 0

for val in enumerate(country_data.loc[ : , 'pct_services_employment']):
    if val[1] < servemploy_lo:
        country_data.loc[val[0], 'out_pct_services_employment'] = 1

country_data['out_pct_services_employment'].abs().sum()
check = (country_data.loc[ : , ['pct_services_employment', 'out_pct_services_employment']].sort_values('pct_services_employment', ascending = False))

## gdp_usd
country_data['out_gdp_usd'] = 0

for val in enumerate(country_data.loc[ : , 'gdp_usd']):
    if val[1] > gdp_usd_hi:
        country_data.loc[val[0], 'out_gdp_usd'] = 1

country_data['out_gdp_usd'].abs().sum()
check = (country_data.loc[ : , ['gdp_usd', 'out_gdp_usd']].sort_values('gdp_usd', ascending = False))

## adult_literacy_pct
country_data['out_adult_literacy_pct'] = 0

for val in enumerate(country_data.loc[ : , 'adult_literacy_pct']):
    if val[1] < adult_lit_lo:
        country_data.loc[val[0], 'out_adult_literacy_pct'] = 1

country_data['out_adult_literacy_pct'].abs().sum()
check = (country_data.loc[ : , ['adult_literacy_pct', 'out_adult_literacy_pct']].sort_values('adult_literacy_pct', ascending = False))

## avg_air_pollution
country_data['out_avg_air_pollution'] = 0

for val in enumerate(country_data.loc[ : , 'avg_air_pollution']):
    if val[1] < airpoll_limit_lo:
        country_data.loc[val[0], 'out_avg_air_pollution'] = 1

country_data['out_avg_air_pollution'].abs().sum()
check = (country_data.loc[ : , ['avg_air_pollution', 'out_avg_air_pollution']].sort_values('avg_air_pollution', ascending = False))

## tax_revenue_pct_gdp
country_data['out_tax_revenue_pct_gdp'] = 0

for val in enumerate(country_data.loc[ : , 'tax_revenue_pct_gdp']):
    if val[1] > tax_rev_limit:
        country_data.loc[val[0], 'out_tax_revenue_pct_gdp'] = 1

country_data['out_tax_revenue_pct_gdp'].abs().sum()
check = (country_data.loc[ : , ['tax_revenue_pct_gdp', 'out_tax_revenue_pct_gdp']].sort_values('tax_revenue_pct_gdp', ascending = False))

###############################################################################
# Analyze Outliers
###############################################################################
#country_data['out_sum'] = (country_data['out_1'] + country_data['out_2'] + country_data['out_3'] + country_data['out_pct_female_employment'] + country_data['out_male_employment'] + country_data['out_pct_services_employment'] + country_data['out_7'] + country_data['out_8'] + country_data['out_9'] + country_data['out_gdp_usd'] + country_data['out_11'] + country_data['out_adult_literacy_pct'] + country_data['out_avg_air_pollution'] + country_data['out_tax_revenue_pct_gdp'])

#check = (country_data.loc[ : , ['out_1'] + ['out_2'] + ['out_3'] +['out_pct_female_employment'] +['out_pct_male_employment'] + ['out_pct_services_employment'] + ['out_7'] + ['out_8'] + ['out_9'] +['out_gdp_usd'] + ['out_11'] + ['out_adult_literacy_pct'] +['out_avg_air_pollution'] +['out_tax_revenue_pct_gdp']].sort_values(['out_sum'], ascending = False))