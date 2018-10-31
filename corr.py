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


no_eg = country_data[country_data['country_name'] != 'Equatorial Guinea']



    
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
## access_to_electricity_rural
plt.subplot(2,2,1)
sns.distplot(country_data['access_to_electricity_rural'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Access to Electricity(Rural)')

## access_to_electricity_urban
plt.subplot(2,2,2)
sns.distplot(country_data['access_to_electricity_urban'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Access to Electricity(Urban)')

## CO2_emissions_per_capita)
plt.subplot(2,2,3)
sns.distplot(country_data['CO2_emissions_per_capita)'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('CO2 emissions per capita)')

##gni_index
plt.subplot(2,2,4)
sns.distplot(country_data['gni_index'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('GNI')

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
ele_r_lo = 9
ele_u_lo = 65
co2_hi = 1.2
gni_hi = 12746
gni_um = 4125
femploy_limit_hi = 45
memploy_limit_hi = 20
servemploy_lo = 15
gdp_usd_hi = 90000000000
adult_lit_lo = 45
airpoll_limit_lo = 22
tax_rev_limit = 30
exports_pct_gdp_limit = 30
fdi_pct_gdp_limit = 4.5
internet_usage_pct_up = 27
internet_usage_pct_low = 15
gni_index_limit = 1200


###############################################################################
# distplots with cutoff points
###############################################################################
"""
Outlier for exports_pct_gdp
"""

country_data[country_data['income_group'] == 'Low income']['exports_pct_gdp']
# flag: 30 is outlier threshold for low income country
country_data['out_exports_pct_gdp'] = 0
for index, value in enumerate(country_data['exports_pct_gdp']):
    if value > exports_pct_gdp_limit and country_data.loc[index, 'income_group'] == 'Low income':
        country_data.loc[index, 'out_exports_pct_gdp'] = 1

# histgram
sns.distplot(country_data['exports_pct_gdp']) 

plt.show()

# plot 

sns.pairplot(x_vars=['exports_pct_gdp'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = exports_pct_gdp_limit,
            label = 'Outlier Thresholds (low income countries)')
plt.title('Export of Goods and Services by Country')
plt.xlabel('Export of Goods and Services (% of GDP)')
plt.ylabel('')
plt.show()

# no Equatorial Guinea
sns.pairplot(x_vars=['exports_pct_gdp'],
             y_vars=['country_name'],
             data = no_eg,
             hue = 'income_group',
             size = 5)
plt.axvline(x = exports_pct_gdp_limit,
            label = 'Outlier Thresholds (low income countries)')
plt.title('Export of Goods and Services by Country (Equatorial Guinea excluded)')
plt.xlabel('Export of Goods and Services (% of GDP)')
plt.ylabel('')
plt.show()


"""
Outlier for fdi_pct_gdp
"""
# overview
country_data[country_data['income_group'] == 'Low income']['fdi_pct_gdp']

# flag: 4.5 is outlier threshold for low income country
country_data['out_fdi_pct_gdp'] = 0
for index, value in enumerate(country_data['fdi_pct_gdp']):
    if value > fdi_pct_gdp_limit and country_data.loc[index, 'income_group'] == 'Low income':
        country_data.loc[index, 'out_fdi_pct_gdp'] = 1
# histgram
sns.distplot(country_data['fdi_pct_gdp']) 

plt.show()

# plot 

sns.pairplot(x_vars=['fdi_pct_gdp'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = fdi_pct_gdp_limit,
            label = 'Outlier Thresholds (low income countries)')
plt.title('Foreign Derict Investment by Country')
plt.xlabel('Foreign Derict Investment (% of GDP)')
plt.ylabel('')
plt.show()


"""
Outlier for internet_usage_pct
"""
# overview
country_data[country_data['income_group'] == 'Lower middle income']['internet_usage_pct']

# flag: 27 is upper outlier threshold and 15 is lower outlier threshold for lower middle income country
country_data['out_internet_usage_pct'] = 0
for index, value in enumerate(country_data['internet_usage_pct']):
    if value > internet_usage_pct_up and country_data.loc[index, 'income_group'] == 'Lower middle income':
        country_data.loc[index, 'out_internet_usage_pct'] = 1
    elif value < internet_usage_pct_low and country_data.loc[index, 'income_group'] == 'Lower middle income':
        country_data.loc[index, 'out_internet_usage_pct'] = 1
        
        
# histgram
sns.distplot(country_data['internet_usage_pct']) 

plt.show()

# plot 
sns.pairplot(x_vars=['internet_usage_pct'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = internet_usage_pct_up,
            label = 'Upper Outlier Thresholds (Lower middle income countries)',
            color = 'orange')
plt.axvline(x = internet_usage_pct_low,
            label = 'Lower Outlier Thresholds (Lower middle income countries)',
            color = 'orange')
plt.title('Internet Usage by Country')
plt.xlabel('Internet Usage')
plt.ylabel('')
plt.show()

"""
Outlier for gni_index
"""
# overview
country_data[country_data['income_group'] == 'Low income']['gni_index']

# flag: 1200 is upper outlier threshold for low income country
country_data['out_gni_index'] = 0
for index, value in enumerate(country_data['gni_index']):
    if value > gni_index_limit and country_data.loc[index, 'income_group'] == 'Low income':
        country_data.loc[index, 'out_gni_index'] = 1
        
        
# histgram
sns.distplot(country_data['gni_index']) 


plt.show()

# plot 
sns.pairplot(x_vars=['gni_index'],
             y_vars=['country_name'],
             data = country_data,
             hue = 'income_group',
             size = 5)
plt.axvline(x = gni_index_limit,
            label = 'Outlier Thresholds (low income countries)')

plt.title('Gross National Income by Country')
plt.xlabel('Gross National Income ($ per capita)')
plt.ylabel('')
plt.show()

# no EG
sns.pairplot(x_vars=['gni_index'],
             y_vars=['country_name'],
             data = no_eg,
             hue = 'income_group',
             size = 5)
plt.axvline(x = gni_index_limit,
            label = 'Outlier Thresholds (low income countries)')

plt.title('Gross National Income by Country (Equatorial Guinea excluded)')
plt.xlabel('Gross National Income ($ per capita)')
plt.ylabel('')
plt.show()

## access_to_electricity_rural
plt.subplot(3,3,1)
sns.distplot(country_data['access_to_electricity_rural'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Access to Electricity(Rural)')
plt.axvline(x = ele_r_lo, label = 'Outlier Threshold', linestyle = '--', color = 'y')

## access_to_electricity_urban
plt.subplot(3,3,2)
sns.distplot(country_data['access_to_electricity_urban'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Access to Electricity(Urban)')
plt.axvline(x = ele_u_lo, label = 'Outlier Threshold', linestyle = '--', color = 'y')

## CO2_emissions_per_capita)
plt.subplot(3,3,3)
sns.distplot(country_data['CO2_emissions_per_capita)'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('CO2 emissions per capita)')
plt.axvline(x = co2_hi, label = 'Outlier Threshold', linestyle = '--', color = 'y')

##gni_index

plt.subplot(2,2,2)
sns.distplot(country_data['gni_index'], bins = 'fd', kde = False, rug = True, color = 'firebrick')

plt.subplot(3,3,4)
sns.distplot(country_data['gni_index'], bins = 'fd', kde = False, rug = True, color = 'firebrick')

plt.xlabel('GNI')
plt.axvline(x = gni_hi, label = 'Outlier Threshold', linestyle = '--', color = 'y')
plt.axvline(x = gni_um, label = 'Outlier Threshold', linestyle = '--', color = 'y')

## pct_female_employment
plt.subplot(3,3,5)
sns.distplot(country_data['pct_female_employment'], bins = 'fd', kde = False, rug = True, color = 'firebrick')
plt.xlabel('Female Employment')

plt.axvline(x = femploy_limit_hi, label = 'Outlier Threshold', linestyle = '--', color = 'y')


## pct_male_employment 
plt.subplot(3,3,6)
sns.distplot(country_data['pct_male_employment'], bins = 'fd', kde = False, rug = True, color = 'forestgreen')
plt.xlabel('Male Employment')

plt.axvline(x = memploy_limit_hi, label = 'Outlier Threshold', linestyle = '--', color = 'b')

## pct_services_employment 
plt.subplot(3,3,7)
sns.distplot(country_data['pct_services_employment'], bins = 'fd', kde = False, rug = True, color = 'cornflowerblue')
plt.xlabel('Services Employment')

plt.axvline(x = servemploy_lo, label = 'Outlier Thresholds', linestyle = '--', color = 'orangered')

##gdp_usd
plt.subplot(3,3,8)
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
## access_to_electricity_rural
country_data['out_access_to_electricity_rural'] = 0

for val in enumerate(country_data.loc[ : , 'access_to_electricity_rural']):
    if val[1] < ele_r_lo:
        country_data.loc[val[0], 'out_access_to_electricity_rural'] = 1

country_data['out_access_to_electricity_rural'].abs().sum()
check = (country_data.loc[ : , ['access_to_electricity_rural', 'out_access_to_electricity_rural']].sort_values('access_to_electricity_rural', ascending = False))

## access_to_electricity_urban
country_data['out_access_to_electricity_urban'] = 0

for val in enumerate(country_data.loc[ : , 'access_to_electricity_urban']):
    if val[1] < ele_u_lo:
        country_data.loc[val[0], 'out_access_to_electricity_urban'] = 1

country_data['out_access_to_electricity_urban'].abs().sum()
check = (country_data.loc[ : , ['access_to_electricity_urban', 'out_access_to_electricity_urban']].sort_values('access_to_electricity_urban', ascending = False))


## CO2_emissions_per_capita)
country_data['out_CO2_emissions_per_capita)'] = 0

for val in enumerate(country_data.loc[ : , 'CO2_emissions_per_capita)']):
    if val[1] > co2_hi:
        country_data.loc[val[0], 'out_CO2_emissions_per_capita)'] = 1

country_data['out_CO2_emissions_per_capita)'].abs().sum()
check = (country_data.loc[ : , ['CO2_emissions_per_capita)', 'out_CO2_emissions_per_capita)']].sort_values('CO2_emissions_per_capita)', ascending = False))


##gni_index
country_data['out_gni_index'] = 0

for val in enumerate(country_data.loc[ : , 'gni_index']):
    if val[1] > gni_hi:
        country_data.loc[val[0], 'out_gni_index'] = 1

country_data['out_gni_index'].abs().sum()
check = (country_data.loc[ : , ['gni_index', 'out_gni_index']].sort_values('gni_index', ascending = False))

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

###############################################################################
# corelation 
###############################################################################

"""
GNI vs CO2
"""
sns.lmplot(x = 'gni_index',
           y = 'CO2_emissions_per_capita)',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Gross National Income')
plt.ylabel('CO2 Emissions (per capita)')
plt.title('GNI vs CO2 Emissions')
plt.show()

# no EG
sns.lmplot(x = 'gni_index',
           y = 'CO2_emissions_per_capita)',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Gross National Income')
plt.ylabel('CO2 Emissions (per capita)')
plt.title('GNI vs CO2 Emissions (Equatorial Guinea excluded)')
plt.show()

"""
female vs male employment
(Kenya)
"""
sns.lmplot(x = 'pct_female_employment',
           y = 'pct_male_employment',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Female employment')
plt.ylabel('Male employment')
plt.title('Female vs Male Employment')
plt.show()

# no EG
#sns.lmplot(x = 'pct_female_employment',
#           y = 'pct_male_employment',
#           data = no_eg,
#           hue = 'income_group')
#plt.xlabel('Female employment')
#plt.ylabel('Male employment')
#plt.title('Female vs Male Employment (Equatorial Guinea excluded)')
#plt.show()

"""
service vs agriculture
"""
sns.lmplot(x = 'pct_agriculture_employment',
           y = 'pct_services_employment',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Agriculture Employment')
plt.ylabel('Services employment')
plt.title('Agriculture vs Services Employment')
plt.show()

# no EG
sns.lmplot(x = 'pct_agriculture_employment',
           y = 'pct_services_employment',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Agriculture Employment')
plt.ylabel('Services employment')
plt.title('Agriculture vs Services Employment (Equatorial Guinea excluded)')
plt.show()

"""
urban pop vs export gdp
"""
sns.lmplot(x = 'urban_population_pct',
           y = 'exports_pct_gdp',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Urban Population (% of total population)')
plt.ylabel('Export (% of GDP)')
plt.title('Urban Population vs Export')
plt.show()

# no EG
sns.lmplot(x = 'urban_population_pct',
           y = 'exports_pct_gdp',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Urban Population (% of total population)')
plt.ylabel('Export (% of GDP)')
plt.title('Urban Population vs Export (Equatorial Guinea excluded)')
plt.show()

"""
HIV vs GNI
"""
sns.lmplot(x = 'gni_index',
           y = 'incidence_hiv',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Gross National Income')
plt.ylabel('Incidence of HIV')
plt.title('GNI vs Incidence of HIV')
plt.show()

# no EG
sns.lmplot(x = 'gni_index',
           y = 'incidence_hiv',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Gross National Income')
plt.ylabel('Incidence of HIV')
plt.title('GNI vs Incidence of HIV (Equatorial Guinea excluded)')
plt.show()

"""
electricty rural vs GDP growth rate
"""
sns.lmplot(x = 'access_to_electricity_rural',
           y = 'gdp_growth_pct',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Access to electricity, rural (% of rural population)')
plt.ylabel('GDP growth (annual %)')
plt.title('Access to Electricity, Eural vs GDP Growth Rate')
plt.show()

# no EG
sns.lmplot(x = 'access_to_electricity_rural',
           y = 'gdp_growth_pct',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Access to electricity, rural (% of rural population)')
plt.ylabel('GDP growth (annual %)')
plt.title('Access to Electricity, Eural vs GDP Growth Rate (Equatorial Guinea excluded)')
plt.show()

"""
electricty pop vs internet usage
"""
sns.lmplot(x = 'access_to_electricity_pop',
           y = 'internet_usage_pct',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Access to electricity, population (% of population)')
plt.ylabel('Individuals using the Internet (% of population)')
plt.title('Access to Electricity, Population vs Individuals Using the Internet')
plt.show()

# no EG
sns.lmplot(x = 'access_to_electricity_pop',
           y = 'internet_usage_pct',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Access to electricity, population (% of population)')
plt.ylabel('Individuals using the Internet (% of population)')
plt.title('Access to Electricity, Population vs Individuals Using the Internet (Equatorial Guinea excluded)')
plt.show()

"""
fdi vs tax revenue
"""
sns.lmplot(x = 'fdi_pct_gdp',
           y = 'tax_revenue_pct_gdp',
           data = country_data,
           hue = 'income_group')
plt.xlabel('Access to electricity, population (% of population)')
plt.ylabel('Foreign direct investment (% of GDP)')
plt.title('Foreign Direct Investment vs Tax Revenue')
plt.show()

# no EG
sns.lmplot(x = 'fdi_pct_gdp',
           y = 'tax_revenue_pct_gdp',
           data = no_eg,
           hue = 'income_group')
plt.xlabel('Access to electricity, population (% of population)')
plt.ylabel('Foreign direct investment (% of GDP)')
plt.title('Foreign Direct Investment vs Tax revenue (Equatorial Guinea excluded)')
plt.show()



