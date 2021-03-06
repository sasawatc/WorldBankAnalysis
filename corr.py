# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:43:31 2018

For running all correlation analysis and saving graphs
"""

__version__ = '1.0.0'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')


def corr():
    from adjustText import adjust_text  # requires package installation (conda install -c phlya adjusttext)

    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    from pathlib import Path
    from handy_func import generate_title

    # Import libraries and base dataset (og_file); then filter out/subset central africa 1

    base_folder = Path('data/base')
    processed_folder = Path('data/processed')
    figs_folder = Path('figs')
    boxplot_folder = Path('figs/box_plot')
    distplot_folder = Path('figs/dist_plot')
    pairplot_folder = Path('figs/pair_plot')
    scatterplot_folder = Path('figs/scatter_plot')
    swarmplot_folder = Path('figs/swarm_plot')
    pie_folder = Path('figs/pie')

    # import clean data
    clean_data = pd.read_excel(processed_folder / 'clean_data.xlsx', index='country_code')
    world_data = clean_data.iloc[:, 2:]

    world_data.loc[world_data.country_name == 'Congo, Dem. Rep.', 'income_group'] = 'Low income'
    world_data.loc[world_data.country_name == 'Congo, Rep.', 'income_group'] = 'Lower middle income'
    """
    subset dataset
    """
    # low income worldwide
    low_income_world = world_data[world_data.income_group == 'Low income']
    low_income_world.reset_index(drop=True, inplace=True)

    # lower middle income worldwide
    lower_middle_income_world = world_data[world_data.income_group == 'Lower middle income']
    lower_middle_income_world.reset_index(drop=True, inplace=True)

    # upper middle income worldwide
    upper_middle_income_world = world_data[world_data.income_group == 'Upper middle income']
    upper_middle_income_world.reset_index(drop=True, inplace=True)

    # Central Africa 1
    df = clean_data[clean_data.Hult_Team_Regions == 'Central Africa 1']
    country_data = df.iloc[:, 2:]
    country_data.reset_index(drop=True, inplace=True)

    print(country_data.head())

    # check some data
    print(country_data['income_group'])

    list(country_data.columns.values)

    data_describe = country_data.describe().round(2)
    data_describe.loc['std', :].sort_values(ascending=False).round(2)

    data_describe[['gdp_usd']].quantile([0.20,
                                         0.40,
                                         0.60,
                                         0.80,
                                         1.00])

    data_describe[['gdp_usd']].quantile(1.00) - data_describe['gdp_usd'].quantile(0.8)

    ###############################################################################
    # Plot pie charts for missing data report
    ###############################################################################
    homicides_mp = country_data['m_homicides_per_100k'].sum() / len(country_data)
    print(homicides_mp)

    literacy_mp = country_data['m_adult_literacy_pct'].sum() / len(country_data)
    print(literacy_mp)

    tax_revenue_mp = country_data['m_tax_revenue_pct_gdp'].sum() / len(country_data)
    print(tax_revenue_mp)

    fig1, ax1 = plt.subplots()
    plt.pie([homicides_mp, 1 - homicides_mp],
            labels=['Missing data', 'Reported'],
            autopct='%1.1f%%',
            shadow=False,
            colors=['#B60020', '#7FA2FE'])
    ax1.axis('equal')
    plt.title('Homicides Missing Data Percentage')
    plt.tight_layout()
    plt.savefig(pie_folder / 'Homicides pie.png')
    # plt.show()

    fig2, ax2 = plt.subplots()
    plt.pie([literacy_mp, 1 - literacy_mp],
            labels=['Missing data', 'Reported'],
            autopct='%1.1f%%',
            shadow=False,
            colors=['#B60020', '#7FA2FE'])
    ax2.axis('equal')
    plt.title('Adult Literacy Data Percentage')
    plt.tight_layout()
    plt.savefig(pie_folder / 'Adult literacy pie.png')
    # plt.show()

    fig3, ax3 = plt.subplots()
    plt.pie([tax_revenue_mp, 1 - tax_revenue_mp],
            labels=['Missing data', 'Reported'],
            autopct='%1.1f%%',
            shadow=False,
            colors=['#B60020', '#7FA2FE'])
    ax3.axis('equal')
    plt.title('Tax Revenue Missing Data Percentage')
    plt.tight_layout()
    plt.savefig(pie_folder / 'Tax Revenue pie.png')
    # plt.show()

    ###############################################################################
    # Plot boxplots for all indicators to find potential outliers
    ###############################################################################
    for col in country_data.select_dtypes(include=['float64', 'int']):
        country_data.boxplot(column=col, by='income_group')
        title = generate_title(str(col))
        plt.title(col)
        plt.suptitle("")
        plt.tight_layout()
        plt.savefig(boxplot_folder / f'{col}')
        # plt.show()

    country_data.boxplot(column=['gdp_usd'], by='income_group')

    country_data.boxplot(column=['gni_index'], by='income_group')
    """Use gni instead of gdp because gni correlates more with the corresponding income groups; it has less extreme 
    outliers """

    # Distplots (without cutoffs)
    ###############################################################################
    # access_to_electricity_rural
    plt.subplot(2, 2, 1)
    sns.distplot(country_data['access_to_electricity_rural'], bins='fd', kde=False, rug=True, color='lightseagreen')
    plt.xlabel('Access to Electricity(Rural)')

    # access_to_electricity_urban
    plt.subplot(2, 2, 2)
    sns.distplot(country_data['access_to_electricity_urban'], bins='fd', kde=False, rug=True, color='dodgerblue')
    plt.xlabel('Access to Electricity(Urban)')

    # CO2_emissions_per_capita
    plt.subplot(2, 2, 3)
    sns.distplot(country_data['CO2_emissions_per_capita'], bins='fd', kde=False, rug=True, color='gold')
    plt.xlabel('CO2 emissions per capita')

    # avg_air_pollution
    plt.subplot(2, 2, 4)
    sns.distplot(country_data['avg_air_pollution'], bins='fd', kde=False, rug=True, color='plum')
    plt.xlabel('Avg Air Pollution')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'electricity & pollution Histograms without cutoffs.png')
    # plt.show()

    # pct_female_employment
    plt.subplot(2, 2, 1)
    sns.distplot(country_data['pct_female_employment'], bins='fd', kde=False, rug=True, color='firebrick')
    plt.xlabel('Female Employment')

    # pct_male_employment
    plt.subplot(2, 2, 2)
    sns.distplot(country_data['pct_male_employment'], bins='fd', kde=False, rug=True, color='forestgreen')
    plt.xlabel('Male Employment')

    # pct_services_employment
    plt.subplot(2, 2, 3)
    sns.distplot(country_data['pct_services_employment'], bins='fd', kde=False, rug=True, color='cornflowerblue')
    plt.xlabel('Services Employment')

    # adult_literacy_pct
    # plt.subplot(2,2,4)
    # sns.distplot(country_data['adult_literacy_pct'], bins = 'fd', kde = False, rug = True, color = 'coral')
    # plt.xlabel('Adult Literacy Rate')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'Employment & Literacy Histograms without cutoffs.png')
    # plt.show()

    # tax_revenue_pct_gdp
    # plt.subplot(2,2,1)
    # sns.distplot(country_data['tax_revenue_pct_gdp'], bins = 'fd', kde = False, rug = True, color = 'orange')
    # plt.xlabel('Tax Revenue PCT GDP')

    # gni_index

    plt.subplot(2, 2, 1)
    sns.distplot(country_data['gni_index'], bins='fd', kde=False, rug=True, color='cadetblue')
    plt.xlabel('Gross National Income ($ per capita)')

    # gdp_usd
    plt.subplot(2, 2, 2)
    sns.distplot(country_data['gdp_usd'], bins='fd', kde=False, rug=True, color='slategrey')
    plt.xlabel('Gross Domestic Product ($)')

    # exports_pct_gdp
    plt.subplot(2, 2, 3)
    sns.distplot(country_data['exports_pct_gdp'], bins='fd', kde=False, rug=True, color='green')
    plt.xlabel('Exports')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'Money Histograms without cutoffs.png')
    # plt.show()

    # fdi_pct_gdp
    plt.subplot(1, 2, 1)
    sns.distplot(country_data['fdi_pct_gdp'], bins='fd', kde=False, rug=True, color='c')
    plt.xlabel('Foreign Direct Investment, net inflows (% of GDP)')

    # internet_usage_pct
    plt.subplot(1, 2, 2)
    sns.distplot(country_data['internet_usage_pct'], bins='fd', kde=False, rug=True, color='indigo')
    plt.xlabel('Individuals using the Internet (% of population)')

    plt.savefig(distplot_folder / 'FDI & Internet Histograms without cutoffs.png')
    # plt.show()

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

    # access_to_electricity_rural
    plt.subplot(2, 2, 1)
    sns.distplot(country_data['access_to_electricity_rural'], bins='fd', kde=False, rug=True, color='lightseagreen')
    plt.xlabel('Access to Electricity(Rural)')
    plt.axvline(x=ele_r_lo, label='Outlier Threshold', linestyle='--', color='y')

    # access_to_electricity_urban
    plt.subplot(2, 2, 2)
    sns.distplot(country_data['access_to_electricity_urban'], bins='fd', kde=False, rug=True, color='dodgerblue')
    plt.xlabel('Access to Electricity(Urban)')
    plt.axvline(x=ele_u_lo, label='Outlier Threshold', linestyle='--', color='r')

    # CO2_emissions_per_capita
    plt.subplot(2, 2, 3)
    sns.distplot(country_data['CO2_emissions_per_capita'], bins='fd', kde=False, rug=True, color='gold')
    plt.xlabel('CO2 emissions per capita')
    plt.axvline(x=co2_hi, label='Outlier Threshold', linestyle='--', color='g')

    # avg_air_pollution
    plt.subplot(2, 2, 4)
    sns.distplot(country_data['avg_air_pollution'], bins='fd', kde=False, rug=True, color='plum')
    plt.xlabel('Avg Air Pollution')
    plt.axvline(x=airpoll_limit_lo, label='Outlier Thresholds', linestyle='--', color='darkturquoise')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'electricity & pollution Histograms with cutoffs.png')
    # plt.show()

    # pct_female_employment
    plt.subplot(2, 2, 1)
    sns.distplot(country_data['pct_female_employment'], bins='fd', kde=False, rug=True, color='firebrick')
    plt.xlabel('Female Employment')
    plt.axvline(x=femploy_limit_hi, label='Outlier Threshold', linestyle='--', color='y')

    # pct_male_employment
    plt.subplot(2, 2, 2)
    sns.distplot(country_data['pct_male_employment'], bins='fd', kde=False, rug=True, color='forestgreen')
    plt.xlabel('Male Employment')
    plt.axvline(x=memploy_limit_hi, label='Outlier Threshold', linestyle='--', color='b')

    # pct_services_employment
    plt.subplot(2, 2, 3)
    sns.distplot(country_data['pct_services_employment'], bins='fd', kde=False, rug=True, color='cornflowerblue')
    plt.xlabel('Services Employment')
    plt.axvline(x=servemploy_lo, label='Outlier Thresholds', linestyle='--', color='orangered')

    # adult_literacy_pct
    # plt.subplot(2,2,4)
    # sns.distplot(country_data['adult_literacy_pct'], bins = 'fd', kde = False, rug = True, color = 'coral')
    # plt.xlabel('Adult Literacy Rate')
    # plt.axvline(x = adult_lit_lo, label = 'Outlier Thresholds', linestyle = '--', color = 'darkmagenta')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'Employment & Literacy Histograms with cutoffs.png')
    # # plt.show()

    # tax_revenue_pct_gdp
    # plt.subplot(2,2,1)
    # sns.distplot(country_data['tax_revenue_pct_gdp'], bins = 'fd', kde = False, rug = True, color = 'orange')
    # plt.xlabel('Tax Revenue PCT GDP')
    # plt.axvline(x = tax_rev_limit, label = 'Outlier Thresholds', linestyle = '--', color = 'k')

    # gni_index

    plt.subplot(2, 2, 1)

    sns.distplot(country_data['gni_index'], bins='fd', kde=False, rug=True, color='cadetblue')
    plt.xlabel('GNI')
    plt.axvline(x=gni_hi, label='Outlier Threshold', linestyle='--', color='r')
    plt.axvline(x=gni_um, label='Outlier Threshold', linestyle='--', color='r')

    # gdp_usd
    plt.subplot(2, 2, 2)
    sns.distplot(country_data['gdp_usd'], bins='fd', kde=False, rug=True, color='slategrey')
    plt.xlabel('GDP (USD)')
    plt.axvline(x=gdp_usd_hi, label='Outlier Thresholds', linestyle='--', color='green')

    # exports_pct_gdp
    plt.subplot(2, 2, 3)
    sns.distplot(country_data['exports_pct_gdp'], bins='fd', kde=False, rug=True, color='green')
    plt.xlabel('Exports')
    plt.axvline(x=exports_pct_gdp_limit, label='Outlier Thresholds', linestyle='--', color='b')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'Money Histograms with cutoffs.png')
    # # plt.show()

    # fdi_pct_gdp
    plt.subplot(2, 1, 1)
    sns.distplot(country_data['fdi_pct_gdp'], bins='fd', kde=False, rug=True, color='c')
    plt.xlabel('Foreign Direct Investment, net inflows (% of GDP)')
    plt.axvline(x=tax_rev_limit, label='Outlier Thresholds', linestyle='--', color='b')

    # internet_usage_pct
    plt.subplot(2, 1, 2)
    sns.distplot(country_data['internet_usage_pct'], bins='fd', kde=False, rug=True, color='indigo')
    plt.xlabel('Individuals using the Internet (% of population)')
    plt.axvline(x=internet_usage_pct_up, label='Outlier Thresholds', linestyle='--', color='r')
    plt.axvline(x=internet_usage_pct_low, label='Outlier Thresholds', linestyle='--', color='r')

    plt.tight_layout()
    plt.savefig(distplot_folder / 'FDI & Internet Histograms with cutoffs.png')
    # # plt.show()

    ###############################################################################
    # Flagging Outliers
    ###############################################################################
    # access_to_electricity_rural
    country_data['out_access_to_electricity_rural'] = 0

    for val in enumerate(country_data.loc[:, 'access_to_electricity_rural']):
        if val[1] < ele_r_lo:
            country_data.loc[val[0], 'out_access_to_electricity_rural'] = 1

    country_data['out_access_to_electricity_rural'].abs().sum()
    check = (country_data.loc[:, ['access_to_electricity_rural', 'out_access_to_electricity_rural']].sort_values(
        'access_to_electricity_rural', ascending=False))

    # access_to_electricity_urban
    country_data['out_access_to_electricity_urban'] = 0

    for val in enumerate(country_data.loc[:, 'access_to_electricity_urban']):
        if val[1] < ele_u_lo:
            country_data.loc[val[0], 'out_access_to_electricity_urban'] = 1

    country_data['out_access_to_electricity_urban'].abs().sum()
    check = (country_data.loc[:, ['access_to_electricity_urban', 'out_access_to_electricity_urban']].sort_values(
        'access_to_electricity_urban', ascending=False))

    # CO2_emissions_per_capita)
    country_data['out_CO2_emissions_per_capita'] = 0

    for val in enumerate(country_data.loc[:, 'CO2_emissions_per_capita']):
        if val[1] > co2_hi:
            country_data.loc[val[0], 'out_CO2_emissions_per_capita'] = 1

    country_data['out_CO2_emissions_per_capita'].abs().sum()
    check = (country_data.loc[:, ['CO2_emissions_per_capita', 'out_CO2_emissions_per_capita']].sort_values(
        'CO2_emissions_per_capita', ascending=False))

    # pct_female_employment
    country_data['out_pct_female_employment'] = 0

    for val in enumerate(country_data.loc[:, 'pct_female_employment']):
        if val[1] > femploy_limit_hi:
            country_data.loc[val[0], 'out_pct_female_employment'] = 1

    country_data['out_pct_female_employment'].abs().sum()
    check = (
        country_data.loc[:, ['pct_female_employment', 'out_pct_female_employment']].sort_values('pct_female_employment',
                                                                                                ascending=False))

    # pct_male_employment
    country_data['out_pct_male_employment'] = 0

    for val in enumerate(country_data.loc[:, 'pct_male_employment']):
        if val[1] > memploy_limit_hi:
            country_data.loc[val[0], 'out_pct_male_employment'] = 1

    country_data['out_pct_male_employment'].abs().sum()
    check = (country_data.loc[:, ['pct_male_employment', 'out_pct_male_employment']].sort_values('pct_male_employment',
                                                                                                 ascending=False))

    # pct_services_employment
    country_data['out_pct_services_employment'] = 0

    for val in enumerate(country_data.loc[:, 'pct_services_employment']):
        if val[1] < servemploy_lo:
            country_data.loc[val[0], 'out_pct_services_employment'] = 1

    country_data['out_pct_services_employment'].abs().sum()
    check = (country_data.loc[:, ['pct_services_employment', 'out_pct_services_employment']].sort_values(
        'pct_services_employment', ascending=False))

    # gdp_usd
    country_data['out_gdp_usd'] = 0

    for val in enumerate(country_data.loc[:, 'gdp_usd']):
        if val[1] > gdp_usd_hi:
            country_data.loc[val[0], 'out_gdp_usd'] = 1

    country_data['out_gdp_usd'].abs().sum()
    check = (country_data.loc[:, ['gdp_usd', 'out_gdp_usd']].sort_values('gdp_usd', ascending=False))

    # adult_literacy_pct
    # country_data['out_adult_literacy_pct'] = 0
    #
    # for val in enumerate(country_data.loc[ : , 'adult_literacy_pct']):
    #    if val[1] < adult_lit_lo:
    #        country_data.loc[val[0], 'out_adult_literacy_pct'] = 1
    #
    # country_data['out_adult_literacy_pct'].abs().sum() check = (country_data.loc[ : , ['adult_literacy_pct',
    # 'out_adult_literacy_pct']].sort_values('adult_literacy_pct', ascending = False))

    # avg_air_pollution
    country_data['out_avg_air_pollution'] = 0

    for val in enumerate(country_data.loc[:, 'avg_air_pollution']):
        if val[1] < airpoll_limit_lo:
            country_data.loc[val[0], 'out_avg_air_pollution'] = 1

    country_data['out_avg_air_pollution'].abs().sum()
    check = (country_data.loc[:, ['avg_air_pollution', 'out_avg_air_pollution']].sort_values('avg_air_pollution',
                                                                                             ascending=False))

    # tax_revenue_pct_gdp
    # country_data['out_tax_revenue_pct_gdp'] = 0
    #
    # for val in enumerate(country_data.loc[ : , 'tax_revenue_pct_gdp']):
    #    if val[1] > tax_rev_limit:
    #        country_data.loc[val[0], 'out_tax_revenue_pct_gdp'] = 1
    #
    # country_data['out_tax_revenue_pct_gdp'].abs().sum() check = (country_data.loc[ : , ['tax_revenue_pct_gdp',
    # 'out_tax_revenue_pct_gdp']].sort_values('tax_revenue_pct_gdp', ascending = False))

    no_eg = country_data[country_data['country_name'] != 'Equatorial Guinea']
    no_eg.reset_index(drop=True, inplace=True)
    # exports_pct_gdp
    # country_data[country_data['income_group'] == 'Low income']['exports_pct_gdp']
    """ flag: 30 is outlier threshold for low income country """
    country_data['out_exports_pct_gdp'] = 0
    for index, value in enumerate(country_data['exports_pct_gdp']):
        if value > exports_pct_gdp_limit and country_data.loc[index, 'income_group'] == 'Low income':
            country_data.loc[index, 'out_exports_pct_gdp'] = 1

    # histogram
    sns.distplot(country_data['exports_pct_gdp'])
    # # plt.show()

    # plot
    sns.pairplot(x_vars=['exports_pct_gdp'],
                 y_vars=['country_name'],
                 data=country_data,
                 hue='income_group',
                 size=5)
    plt.axvline(x=exports_pct_gdp_limit,
                label='Outlier Thresholds (low income countries)')
    plt.title('Export of Goods and Services by Country')
    plt.xlabel('Export of Goods and Services (% of GDP)')
    plt.ylabel('')
    # # plt.show()

    # no Equatorial Guinea
    sns.pairplot(x_vars=['exports_pct_gdp'],
                 y_vars=['country_name'],
                 data=no_eg,
                 hue='income_group',
                 size=5)
    plt.axvline(x=exports_pct_gdp_limit,
                label='Outlier Thresholds (low income countries)')
    plt.title('Export of Goods and Services by Country (Equatorial Guinea excluded)')
    plt.xlabel('Export of Goods and Services (% of GDP)')
    plt.ylabel('')
    # # plt.show()

    # fdi_pct_gdp
    # country_data[country_data['income_group'] == 'Low income']['fdi_pct_gdp']
    """flag: 4.5 is outlier threshold for low income country"""
    country_data['out_fdi_pct_gdp'] = 0
    for index, value in enumerate(country_data['fdi_pct_gdp']):
        if value > fdi_pct_gdp_limit and country_data.loc[index, 'income_group'] == 'Low income':
            country_data.loc[index, 'out_fdi_pct_gdp'] = 1

    # histogram
    sns.distplot(country_data['fdi_pct_gdp'])
    # # plt.show()

    # plot
    sns.pairplot(x_vars=['fdi_pct_gdp'],
                 y_vars=['country_name'],
                 data=country_data,
                 hue='income_group',
                 size=5)
    plt.axvline(x=fdi_pct_gdp_limit,
                label='Outlier Thresholds (low income countries)')
    plt.title('Foreign Direct Investment by Country')
    plt.xlabel('Foreign Derict Investment (% of GDP)')
    plt.ylabel('')
    # # plt.show()

    # internet_usage_pct
    # country_data[country_data['income_group'] == 'Lower middle income']['internet_usage_pct']
    """ flag: 27 is upper outlier threshold and 15 is lower outlier threshold for lower middle income country """
    country_data['out_internet_usage_pct'] = 0
    for index, value in enumerate(country_data['internet_usage_pct']):
        if value > internet_usage_pct_up and country_data.loc[index, 'income_group'] == 'Lower middle income':
            country_data.loc[index, 'out_internet_usage_pct'] = 1
        elif value < internet_usage_pct_low and country_data.loc[index, 'income_group'] == 'Lower middle income':
            country_data.loc[index, 'out_internet_usage_pct'] = 1

    # histogram
    sns.distplot(country_data['internet_usage_pct'])
    # # plt.show()

    # plot
    sns.pairplot(x_vars=['internet_usage_pct'],
                 y_vars=['country_name'],
                 data=country_data,
                 hue='income_group',
                 size=5)
    plt.axvline(x=internet_usage_pct_up,
                label='Upper Outlier Thresholds (Lower middle income countries)',
                color='orange')
    plt.axvline(x=internet_usage_pct_low,
                label='Lower Outlier Thresholds (Lower middle income countries)',
                color='orange')
    plt.title('Internet Usage by Country')
    plt.xlabel('Internet Usage')
    plt.ylabel('')
    # # plt.show()

    # gni_index
    # country_data[country_data['income_group'] == 'Low income']['gni_index']
    """ flag: 1200 is upper outlier threshold for low income country """
    country_data['out_gni_index'] = 0
    for index, value in enumerate(country_data['gni_index']):
        if value > gni_index_limit and country_data.loc[index, 'income_group'] == 'Low income':
            country_data.loc[index, 'out_gni_index'] = 1

    country_data['out_gni_index'].abs().sum()
    check = (country_data.loc[:, ['gni_index', 'out_gni_index']].sort_values('gni_index', ascending=False))

    # histogram
    sns.distplot(country_data['gni_index'])
    # # plt.show()

    # plot
    sns.pairplot(x_vars=['gni_index'],
                 y_vars=['country_name'],
                 data=country_data,
                 hue='income_group',
                 size=5)
    plt.axvline(x=gni_index_limit,
                label='Outlier Thresholds (low income countries)')

    plt.title('Gross National Income by Country')
    plt.xlabel('Gross National Income ($ per capita)')
    plt.ylabel('')
    # # plt.show()

    # no EG
    sns.pairplot(x_vars=['gni_index'],
                 y_vars=['country_name'],
                 data=no_eg,
                 hue='income_group',
                 size=5)
    plt.axvline(x=gni_index_limit,
                label='Outlier Thresholds (low income countries)')

    plt.title('Gross National Income by Country (Equatorial Guinea excluded)')
    plt.xlabel('Gross National Income ($ per capita)')
    plt.ylabel('')
    # # plt.show()
    ###############################################################################
    # Analyze Outliers
    ###############################################################################
    # take out removed columns
    # count outliers
    country_data['out_total'] = country_data[['out_avg_air_pollution',
                                              'out_gdp_usd',
                                              'out_pct_services_employment',
                                              'out_pct_male_employment',
                                              'out_pct_female_employment',
                                              'out_CO2_emissions_per_capita',
                                              'out_access_to_electricity_urban',
                                              'out_access_to_electricity_rural',
                                              'out_gni_index',
                                              'out_internet_usage_pct',
                                              'out_fdi_pct_gdp',
                                              'out_exports_pct_gdp']].sum(axis=1)

    # plot outliers
    sns.pairplot(x_vars=['out_total'],
                 y_vars=["country_name"],
                 data=country_data,
                 hue='income_group',
                 size=6,
                 plot_kws={"s": 100})
    plt.xticks([0, 1, 2, 3, 4])
    plt.xlabel('Total Outliers')
    plt.ylabel('')
    plt.title("Total Outliers by Country", fontsize=15)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'total outlier layout.png')
    # # plt.show()

    country_data['out_sum'] = (
            country_data['out_access_to_electricity_rural'] + country_data['out_access_to_electricity_urban'] +
            country_data['out_CO2_emissions_per_capita'] + country_data['out_pct_female_employment'] + country_data[
                'out_pct_male_employment'] + country_data['out_pct_services_employment'] + country_data[
                'out_exports_pct_gdp'] + country_data['out_fdi_pct_gdp'] + country_data['out_gni_index'] + country_data[
                'out_gdp_usd'] + country_data['out_internet_usage_pct'] + country_data['out_avg_air_pollution'])

    check = (country_data.loc[:, ['out_sum', 'out_access_to_electricity_rural', 'out_access_to_electricity_urban',
                                  'out_CO2_emissions_per_capita', 'out_pct_female_employment',
                                  'out_pct_male_employment',
                                  'out_pct_services_employment', 'out_exports_pct_gdp', 'out_fdi_pct_gdp',
                                  'out_gni_index',
                                  'out_gdp_usd', 'out_internet_usage_pct', 'out_adult_literacy_pct',
                                  'out_avg_air_pollution', 'out_tax_revenue_pct_gdp']].sort_values(['out_sum'],
                                                                                                   ascending=False))

    country_data['out_sum'] = (
            country_data['out_access_to_electricity_rural'] + country_data['out_access_to_electricity_urban'] +
            country_data['out_CO2_emissions_per_capita'] + country_data['out_pct_female_employment'] + country_data[
                'out_pct_male_employment'] + country_data['out_pct_services_employment'] + country_data[
                'out_exports_pct_gdp'] + country_data['out_fdi_pct_gdp'] + country_data['out_gni_index'] + country_data[
                'out_gdp_usd'] + country_data['out_internet_usage_pct'] + country_data['out_avg_air_pollution'])

    check = (country_data.loc[:, ['out_sum', 'out_access_to_electricity_rural', 'out_access_to_electricity_urban',
                                  'out_CO2_emissions_per_capita', 'out_pct_female_employment',
                                  'out_pct_male_employment',
                                  'out_pct_services_employment', 'out_exports_pct_gdp', 'out_fdi_pct_gdp',
                                  'out_gni_index',
                                  'out_gdp_usd', 'out_internet_usage_pct', 'out_avg_air_pollution']].sort_values(
        ['out_sum'], ascending=False))

    """
    correct mislabeling: Congo anf Congo Dem
    """
    country_data.loc[country_data.country_name == 'Congo, Dem. Rep.', 'income_group'] = 'Low income'
    country_data.loc[country_data.country_name == 'Congo, Rep.', 'income_group'] = 'Lower middle income'

    # low income Central Africa 1 (CA)
    low_income_ca = country_data[country_data.income_group == 'Low income']
    low_income_ca.reset_index(drop=True, inplace=True)

    # lower middle income CA
    lower_middle_income_ca = country_data[country_data.income_group == 'Lower middle income']
    lower_middle_income_ca.reset_index(drop=True, inplace=True)

    # upper middle income CA
    upper_middle_income_ca = country_data[country_data.income_group == 'Upper middle income']
    upper_middle_income_ca.reset_index(drop=True, inplace=True)

    # no Equatorial Guinea
    no_eg = country_data[country_data['country_name'] != 'Equatorial Guinea']
    no_eg.reset_index(drop=True, inplace=True)

    ###############################################################################
    # Correlation Matrix for all variables without flags
    ###############################################################################
    world_cor = world_data.loc[:, ['access_to_electricity_pop',
                                   'access_to_electricity_rural',
                                   'access_to_electricity_urban',
                                   'CO2_emissions_per_capita',
                                   'compulsory_edu_yrs',
                                   'pct_female_employment',
                                   'pct_male_employment',
                                   'pct_agriculture_employment',
                                   'pct_industry_employment',
                                   'pct_services_employment',
                                   'exports_pct_gdp',
                                   'fdi_pct_gdp',
                                   'gdp_usd',
                                   'gdp_growth_pct',
                                   'incidence_hiv',
                                   'internet_usage_pct',
                                   'unemployment_pct',
                                   'child_mortality_per_1k',
                                   'avg_air_pollution',
                                   'women_in_parliament',
                                   'urban_population_pct',
                                   'urban_population_growth_pct',
                                   'gni_index']].corr()
    world_lower_mid_cor = lower_middle_income_world.loc[:, ['access_to_electricity_pop',
                                                            'access_to_electricity_rural',
                                                            'access_to_electricity_urban',
                                                            'CO2_emissions_per_capita',
                                                            'compulsory_edu_yrs',
                                                            'pct_female_employment',
                                                            'pct_male_employment',
                                                            'pct_agriculture_employment',
                                                            'pct_industry_employment',
                                                            'pct_services_employment',
                                                            'exports_pct_gdp',
                                                            'fdi_pct_gdp',
                                                            'gdp_usd',
                                                            'gdp_growth_pct',
                                                            'incidence_hiv',
                                                            'internet_usage_pct',
                                                            'unemployment_pct',
                                                            'child_mortality_per_1k',
                                                            'avg_air_pollution',
                                                            'women_in_parliament',
                                                            'urban_population_pct',
                                                            'urban_population_growth_pct',
                                                            'gni_index']].corr()
    central_africa_corr = country_data.loc[:, ['access_to_electricity_pop',
                                               'access_to_electricity_rural',
                                               'access_to_electricity_urban',
                                               'CO2_emissions_per_capita',
                                               'compulsory_edu_yrs',
                                               'pct_female_employment',
                                               'pct_male_employment',
                                               'pct_agriculture_employment',
                                               'pct_industry_employment',
                                               'pct_services_employment',
                                               'exports_pct_gdp',
                                               'fdi_pct_gdp',
                                               'gdp_usd',
                                               'gdp_growth_pct',
                                               'incidence_hiv',
                                               'internet_usage_pct',
                                               'unemployment_pct',
                                               'child_mortality_per_1k',
                                               'avg_air_pollution',
                                               'women_in_parliament',
                                               'urban_population_pct',
                                               'urban_population_growth_pct',
                                               'gni_index']].corr()
    ca_lower_mid_cor = lower_middle_income_ca.loc[:, ['access_to_electricity_pop',
                                                      'access_to_electricity_rural',
                                                      'access_to_electricity_urban',
                                                      'CO2_emissions_per_capita',
                                                      'compulsory_edu_yrs',
                                                      'pct_female_employment',
                                                      'pct_male_employment',
                                                      'pct_agriculture_employment',
                                                      'pct_industry_employment',
                                                      'pct_services_employment',
                                                      'exports_pct_gdp',
                                                      'fdi_pct_gdp',
                                                      'gdp_usd',
                                                      'gdp_growth_pct',
                                                      'incidence_hiv',
                                                      'internet_usage_pct',
                                                      'unemployment_pct',
                                                      'child_mortality_per_1k',
                                                      'avg_air_pollution',
                                                      'women_in_parliament',
                                                      'urban_population_pct',
                                                      'urban_population_growth_pct',
                                                      'gni_index']].corr()

    fig, ax = plt.subplots(figsize=(25, 35))
    plt.subplot(2, 2, 1)
    # fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(world_cor,
                cmap='coolwarm',
                yticklabels=True,
                xticklabels=True,
                linewidths=1)
    plt.title('worldwide -- all')

    plt.subplot(2, 2, 2)
    # fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(world_lower_mid_cor,
                cmap='coolwarm',
                yticklabels=True,
                xticklabels=True,
                linewidths=1)
    plt.title('worldwide -- lower middle income')

    plt.subplot(2, 2, 3)
    # fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(central_africa_corr,
                cmap='coolwarm',
                yticklabels=True,
                xticklabels=True,
                linewidths=1)
    plt.xlabel('Central Africa 1 -- all')

    plt.subplot(2, 2, 4)
    # fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(ca_lower_mid_cor,
                cmap='coolwarm',
                yticklabels=True,
                xticklabels=True,
                linewidths=1)
    plt.xlabel('Central Africa 1 -- lower middle income')
    # # plt.show()

    ###############################################################################
    # Correlation Matrix for all variables without flags
    ##############################################################################
    # -------> remove flags for cleaner correlation matrix

    # low income group correlations
    low_income_ca_corr = low_income_ca.corr().round(2)
    print(low_income_ca_corr)

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(low_income_ca_corr, cmap='Blues', square=True,
                annot=False,
                linecolor='black',
                linewidths=0.5)

    # lower middle income group correlations
    lower_middle_income_corr = lower_middle_income_ca.corr().round(2)
    print(lower_middle_income_corr)

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(lower_middle_income_corr, cmap='Blues', square=True,
                annot=False,
                linecolor='black',
                linewidths=0.5)

    ###############################################################################
    # Plotting Correlations (Scatter)
    ###############################################################################

    """
    GNI vs CO2
    """
    sns.lmplot(x='gni_index',
               y='CO2_emissions_per_capita',
               data=country_data,
               hue='income_group')
    plt.xlabel('Gross National Income')
    plt.ylabel('CO2 Emissions (per capita)')
    plt.title('GNI vs CO2 Emissions')
    # # plt.show()

    # no EG
    sns.lmplot(x='gni_index',
               y='CO2_emissions_per_capita',
               data=no_eg,
               hue='income_group')
    plt.xlabel('Gross National Income')
    plt.ylabel('CO2 Emissions (per capita)')
    plt.title('GNI vs CO2 Emissions (Equatorial Guinea excluded)')
    # # plt.show()

    # just low income
    sns.lmplot(x='gni_index',
               y='CO2_emissions_per_capita',
               data=low_income_ca,
               hue='country_name')
    plt.xlabel('Gross National Income')
    plt.ylabel('CO2 Emissions (per capita)')
    plt.title('GNI vs CO2 Emissions for Low Income Group')
    # # plt.show()

    # just lower middle income
    sns.lmplot(x='gni_index',
               y='CO2_emissions_per_capita',
               data=lower_middle_income_ca,
               hue='country_name')
    plt.xlabel('Gross National Income')
    plt.ylabel('CO2 Emissions (per capita)')
    plt.title('GNI vs CO2 Emissions for Lower Middle Income Group')
    # # plt.show()

    """
    female vs male employment
    (Kenya)
    """
    sns.lmplot(x='pct_female_employment',
               y='pct_male_employment',
               data=country_data,
               hue='income_group')
    plt.xlabel('Female employment')
    plt.ylabel('Male employment')
    plt.title('Female vs Male Employment')
    # # plt.show()

    # no EG
    # sns.lmplot(x = 'pct_female_employment',
    #           y = 'pct_male_employment',
    #           data = no_eg,
    #           hue = 'income_group')
    # plt.xlabel('Female employment')
    # plt.ylabel('Male employment')
    # plt.title('Female vs Male Employment (Equatorial Guinea excluded)')
    # # # plt.show()

    """
    service vs agriculture
    """
    sns.lmplot(x='pct_agriculture_employment',
               y='pct_services_employment',
               data=country_data,
               hue='income_group')
    plt.xlabel('Agriculture Employment')
    plt.ylabel('Services employment')
    plt.title('Agriculture vs Services Employment')
    # # plt.show()

    # no EG
    sns.lmplot(x='pct_agriculture_employment',
               y='pct_services_employment',
               data=no_eg,
               hue='income_group')
    plt.xlabel('Agriculture Employment')
    plt.ylabel('Services employment')
    plt.title('Agriculture vs Services Employment (Equatorial Guinea excluded)')
    # # plt.show()

    """
    urban pop vs export gdp
    """
    sns.lmplot(x='urban_population_pct',
               y='exports_pct_gdp',
               data=country_data,
               hue='income_group')
    plt.xlabel('Urban Population (% of total population)')
    plt.ylabel('Export (% of GDP)')
    plt.title('Urban Population vs Export')
    # # plt.show()

    # no EG
    sns.lmplot(x='urban_population_pct',
               y='exports_pct_gdp',
               data=no_eg,
               hue='income_group')
    plt.xlabel('Urban Population (% of total population)')
    plt.ylabel('Export (% of GDP)')
    plt.title('Urban Population vs Export (Equatorial Guinea excluded)')
    # # plt.show()

    """
    HIV vs GNI
    """
    sns.lmplot(x='gni_index',
               y='incidence_hiv',
               data=country_data,
               hue='income_group')
    plt.xlabel('Gross National Income')
    plt.ylabel('Incidence of HIV')
    plt.title('GNI vs Incidence of HIV')
    # # plt.show()

    # no EG
    sns.lmplot(x='gni_index',
               y='incidence_hiv',
               data=no_eg,
               hue='income_group')
    plt.xlabel('Gross National Income')
    plt.ylabel('Incidence of HIV')
    plt.title('GNI vs Incidence of HIV (Equatorial Guinea excluded)')
    # # plt.show()

    """
    electricty rural vs GDP growth rate
    """
    sns.lmplot(x='access_to_electricity_rural',
               y='gdp_growth_pct',
               data=country_data,
               hue='income_group')
    plt.xlabel('Access to electricity, rural (% of rural population)')
    plt.ylabel('GDP growth (annual %)')
    plt.title('Access to Electricity, Rural vs GDP Growth Rate')
    # # plt.show()

    # no EG
    sns.lmplot(x='access_to_electricity_rural',
               y='gdp_growth_pct',
               data=no_eg,
               hue='income_group')
    plt.xlabel('Access to electricity, rural (% of rural population)')
    plt.ylabel('GDP growth (annual %)')
    plt.title('Access to Electricity, Rural vs GDP Growth Rate (Equatorial Guinea excluded)')
    # # plt.show()

    """
    electricty pop vs internet usage
    """
    sns.lmplot(x='access_to_electricity_pop',
               y='internet_usage_pct',
               data=country_data,
               hue='income_group')
    plt.xlabel('Access to electricity, population (% of population)')
    plt.ylabel('Individuals using the Internet (% of population)')
    plt.title('Access to Electricity, Population vs Individuals Using the Internet')
    # # plt.show()

    # no EG
    sns.lmplot(x='access_to_electricity_pop',
               y='internet_usage_pct',
               data=no_eg,
               hue='income_group')
    plt.xlabel('Access to electricity, population (% of population)')
    plt.ylabel('Individuals using the Internet (% of population)')
    plt.title('Access to Electricity, Population vs Individuals Using the Internet (Equatorial Guinea excluded)')
    # # plt.show()

    """
    fdi vs tax revenue
    """
    # sns.lmplot(x = 'fdi_pct_gdp',
    #           y = 'tax_revenue_pct_gdp',
    #           data = country_data,
    #           hue = 'income_group')
    # plt.xlabel('Access to electricity, population (% of population)')
    # plt.ylabel('Foreign direct investment (% of GDP)')
    # plt.title('Foreign Direct Investment vs Tax Revenue')
    # # # plt.show()
    #
    # no EG
    # sns.lmplot(x = 'fdi_pct_gdp',
    #           y = 'tax_revenue_pct_gdp',
    #           data = no_eg,
    #           hue = 'income_group')
    # plt.xlabel('Access to electricity, population (% of population)')
    # plt.ylabel('Foreign direct investment (% of GDP)')
    # plt.title('Foreign Direct Investment vs Tax revenue (Equatorial Guinea excluded)')
    # # # plt.show()

    ###############################################################################
    # Compare regions
    ###############################################################################
    sns.violinplot(x='income_group',
                   y='gni_index',
                   data=no_eg,
                   orient='v')

    # # plt.show()

    """
    scatter plot countries with GNI by income group
    """
    gni_x_list = ['access_to_electricity_pop',
                  'access_to_electricity_rural',
                  'access_to_electricity_urban',
                  'CO2_emissions_per_capita',
                  'compulsory_edu_yrs',
                  'pct_female_employment',
                  'pct_male_employment',
                  'pct_agriculture_employment',
                  'pct_industry_employment',
                  'pct_services_employment',
                  'exports_pct_gdp',
                  'fdi_pct_gdp',
                  'gdp_usd',
                  'gdp_growth_pct',
                  'incidence_hiv',
                  'internet_usage_pct',
                  'unemployment_pct',
                  'child_mortality_per_1k',
                  'avg_air_pollution',
                  'women_in_parliament',
                  'urban_population_pct',
                  'urban_population_growth_pct']

    for x in gni_x_list:
        sns.pairplot(x_vars=x,
                     y_vars=['gni_index'],
                     data=country_data,
                     hue='income_group',
                     size=5)
        sns.set(rc={'figure.figsize': (19.20, 10.80)})
        sns.set_style('white')
        plt.ylabel('GNI Index')
        txt = generate_title(str(x) + ' vs ' + 'gni_index')
        plt.title(txt)
        plt.savefig(pairplot_folder / f'{x} vs GNI.png')
        # # plt.show()

    """
    scatter plot x variables with country
    """
    x_list = ['access_to_electricity_pop',
              'access_to_electricity_rural',
              'access_to_electricity_urban',
              'CO2_emissions_per_capita',
              'compulsory_edu_yrs',
              'pct_female_employment',
              'pct_male_employment',
              'pct_agriculture_employment',
              'pct_industry_employment',
              'pct_services_employment',
              'exports_pct_gdp',
              'fdi_pct_gdp',
              'gdp_usd',
              'gdp_growth_pct',
              'incidence_hiv',
              'internet_usage_pct',
              'unemployment_pct',
              'child_mortality_per_1k',
              'avg_air_pollution',
              'women_in_parliament',
              'urban_population_pct',
              'urban_population_growth_pct',
              'gni_index']

    for x_var in x_list:
        sns.pairplot(x_vars=x_var,
                     y_vars=['country_name'],
                     data=country_data,
                     hue='income_group',
                     size=5)
        plt.ylabel('')
        txt = generate_title(str(x_var) + ' by ' + 'country_name')
        plt.title(txt)
        plt.tight_layout()
        plt.savefig(pairplot_folder / f'{x_var} by country.png')
        # # plt.show()

    """
    corr between unemployment and [pct_agriculture_employment', 'pct_industry_employment','pct_services_employment]
    """
    corr_list = ['pct_agriculture_employment',
                 'pct_industry_employment',
                 'pct_services_employment']

    for x_v in corr_list:
        sns.pairplot(x_vars=x_v,
                     y_vars=['unemployment_pct'],
                     data=country_data,
                     kind='reg',
                     size=5,
                     hue='income_group')
        plt.ylabel('Unemployment Rate')
        txt = generate_title(str(x_v) + ' vs ' + 'unemployment_pct')
        plt.title(txt)
        plt.savefig(pairplot_folder / f'{x_v} vs unemployment rate.png')
        plt.tight_layout()
        # # plt.show()

    """
    air pollution for lower middle income group
    """
    ### compulsory education year
    # worldwide
    sns.pairplot(x_vars=['compulsory_edu_yrs'],
                 y_vars=['avg_air_pollution'],
                 data=lower_middle_income_world,
                 size=5)
    plt.title('Education (year) vs Air Pollution. Worldwide Lower Middle Income Country')
    # # plt.show()

    # central Africa 1
    sns.pairplot(x_vars=['compulsory_edu_yrs'],
                 y_vars=['avg_air_pollution'],
                 data=lower_middle_income_ca,
                 size=5)
    plt.title('Education (year) vs Air Pollution. Central Africa 1 Lower Middle Income Country')
    # # plt.show()

    ### male empolyment
    sns.pairplot(x_vars=['pct_male_employment'],
                 y_vars=['avg_air_pollution'],
                 data=lower_middle_income_world,
                 size=5)
    plt.title('Male Employment Rate vs Air Pollution. Worldwide Lower Middle Income Country')
    # # plt.show()

    # central Africa 1
    sns.pairplot(x_vars=['pct_male_employment'],
                 y_vars=['avg_air_pollution'],
                 data=lower_middle_income_ca,
                 size=5)
    plt.title('Male Employment Rate vs Air Pollution. Central Africa 1 Lower Middle Income Country')
    # # plt.show()

    """
    women in parliament for lower middle income group
    """
    ### gdp growth rate
    # worldwide
    sns.pairplot(x_vars=['gdp_growth_pct'],
                 y_vars=['women_in_parliament'],
                 data=lower_middle_income_world,
                 size=5)
    plt.title('GDP Growth Rate vs Women in Parliament (%). Worldwide Lower Middle Income Country')
    # # plt.show()

    # central Africa 1
    sns.pairplot(x_vars=['gdp_growth_pct'],
                 y_vars=['women_in_parliament'],
                 data=lower_middle_income_ca,
                 size=5)
    plt.title('GDP Growth Rate vs Women in Parliament (%). Central Africa 1 Lower Middle Income Country')
    # # plt.show()

    ### unemployment rate
    # worldwide
    sns.pairplot(x_vars=['unemployment_pct'],
                 y_vars=['women_in_parliament'],
                 data=lower_middle_income_world,
                 size=5)
    plt.title('Unemployment Rate vs Women in Parliament (%). Worldwide Lower Middle Income Country')
    # # plt.show()

    # central Africa 1
    sns.pairplot(x_vars=['unemployment_pct'],
                 y_vars=['women_in_parliament'],
                 data=lower_middle_income_ca,
                 size=5)
    plt.title('Unemployment Rate vs Women in Parliament (%). Central Africa 1 Lower Middle Income Country')
    # # plt.show()

    """
    Congo Rep
    """
    low_no_congo = low_income_ca[low_income_ca['country_name'] != 'Congo, Rep.']
    congo = low_income_ca[low_income_ca['country_name'] == 'Congo, Rep.']

    # GNI
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.axvline(x=lower_middle_income_ca['gni_index'].median(),
                label='median gni for lower middle income country',
                color='orange')
    plt.scatter(x='gni_index',
                y='country_name',
                data=lower_middle_income_ca,
                color='orange',
                alpha=0.3,
                s=100)
    plt.scatter(x='gni_index',
                y='country_name',
                data=low_no_congo,
                color='blue',
                alpha=0.2,
                s=100)
    plt.scatter(x='gni_index',
                y='country_name',
                data=congo,
                color='blue',
                s=100)
    t = '''
    Median GNI of 
    Lower Middle Income countries'''
    plt.annotate(t,
                 xy=(1600, 'Comoros'),
                 xytext=(2000, 'Rwanda'),
                 arrowprops={'color': 'orange'})
    plt.annotate('Congo, Rep.',
                 xy=(2600, 'Congo, Rep.'))
    plt.title('Gross National Income by Country (Equatorial Guinea excluded)', fontsize=15)
    plt.xlabel('Gross National Income ($ per capita)')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(scatterplot_folder / 'GNI for congo.png')
    # # plt.show()

    # Foreign direct investment
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.axvline(x=lower_middle_income_ca['fdi_pct_gdp'].median(),
                label='median Foreign direct investment of lower middle income',
                color='orange')
    plt.scatter(x='fdi_pct_gdp',
                y='country_name',
                data=lower_middle_income_ca,
                color='orange',
                alpha=0.3,
                s=100)
    plt.scatter(x='fdi_pct_gdp',
                y='country_name',
                data=low_no_congo,
                color='blue',
                alpha=0.2,
                s=100)
    plt.scatter(x='fdi_pct_gdp',
                y='country_name',
                data=congo,
                color='blue',
                s=100)
    t = '''
    Median foreign direct investment of 
    Lower Middle Income coutries'''
    plt.annotate(t,
                 xy=(1.7, 'Nigeria'),
                 xytext=(5, 'Burundi'),
                 arrowprops={'color': 'orange'})
    plt.annotate('Congo, Rep.',
                 xy=(16, 'Uganda'))
    plt.title('Foreign direct investment by Country (Equatorial Guinea excluded)', fontsize=15)
    plt.xlabel('Foreign direct investment (% of GDP)')
    plt.ylabel('')
    plt.tight_layout
    plt.savefig(scatterplot_folder / 'Foreign direct investment for congo.png')
    # # plt.show()

    # Exports of goods and services
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.axvline(x=lower_middle_income_ca['exports_pct_gdp'].median(),
                label='median Exports of goods and services of lower middle income',
                color='orange')
    plt.scatter(x='exports_pct_gdp',
                y='country_name',
                data=lower_middle_income_ca,
                color='orange',
                alpha=0.3,
                s=100)
    plt.scatter(x='exports_pct_gdp',
                y='country_name',
                data=low_no_congo,
                color='blue',
                alpha=0.2,
                s=100)
    plt.scatter(x='exports_pct_gdp',
                y='country_name',
                data=congo,
                color='blue',
                s=100)
    t = '''
    Median exports of 
    Lower Middle Income coutries'''
    plt.annotate(t,
                 xy=(37, 'Nigeria'),
                 xytext=(40, 'Burundi'),
                 arrowprops={'color': 'orange'})
    plt.title('Exports of goods and services by Country (Equatorial Guinea excluded)', fontsize=15)
    plt.xlabel('Exports of Goods and Services (% of GDP)')
    plt.ylabel('')
    plt.tight_layout
    plt.savefig(scatterplot_folder / 'Exports of goods and services for congo.png')
    # # plt.show()

    """
    Equatorial Guinea
    """
    # public spending
    eg = country_data[country_data.country_name == 'Equatorial Guinea']

    fig, ax = plt.subplots(figsize=(8, 5))
    plt.scatter(x='compulsory_edu_yrs',
                y='incidence_hiv',
                data=no_eg,
                cmap='summer',
                alpha=0.3,
                s=100)
    plt.scatter(x='compulsory_edu_yrs',
                y='incidence_hiv',
                data=eg,
                cmap='summer',
                color='red',
                s=100)
    plt.ylabel('Incidence of HIV')
    plt.xlabel('Compulsory Education, Duration (year)')
    plt.title("Public Spending by Country", fontsize=20)
    plt.annotate('Equatorial Guinea',
                 xy=(6.2, 0.48))
    plt.savefig(scatterplot_folder / 'Public Spending for Equatorial Guinea.png')
    # # plt.show()

    # gni
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.scatter(x='gni_index',
                y='country_name',
                data=no_eg,
                cmap='summer',
                alpha=0.3,
                s=100)
    plt.scatter(x='gni_index',
                y='country_name',
                data=eg,
                cmap='summer',
                color='red',
                s=100)
    plt.ylabel('')
    plt.xlabel('Gross National Income ($ per capita)')
    plt.title("Gross National Income by Country", fontsize=20)
    plt.tight_layout()
    plt.savefig(scatterplot_folder / 'GNI for Equatorial Guinea.png')
    # # plt.show()

    ############################################################################
    # Interesting Correlations for Low Income Countries (Central Africa 1)
    ############################################################################

    # higher urban pop % = lesser access to electricity (rural)
    sns.pairplot(data=low_income_ca,
                 x_vars=['urban_population_pct'],
                 y_vars=['access_to_electricity_rural'],
                 size=5,
                 palette='plasma')
    texts = []
    for line in range(0, low_income_ca.shape[0]):
        texts.append(
            plt.text(low_income_ca.urban_population_pct[line], low_income_ca.access_to_electricity_rural[line],
                     low_income_ca.country_name[line], horizontalalignment='left',
                     size='medium', color='black', weight='semibold'))
    plt.title('Urban Population % vs. Rural Access to Electricity')
    plt.xlabel('Urban Population (% of total)')
    plt.ylabel('Access to Electricity, Rural (% of rural population)')
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'low - urban pop % vs. rural access to electricity.png')
    # # plt.show()

    # higher urban pop growth vs. lesser access to electricity (population)
    sns.pairplot(data=low_income_ca,
                 x_vars=['urban_population_growth_pct'],
                 y_vars=['access_to_electricity_pop'],
                 size=6,
                 palette='plasma')
    texts = []
    for line in range(0, low_income_ca.shape[0]):
        texts.append(plt.text(low_income_ca.urban_population_growth_pct[line],
                              low_income_ca.access_to_electricity_pop[line],
                              low_income_ca.country_name[line], horizontalalignment='left',
                              size='medium', color='black', weight='semibold'))
    plt.title('Urban Population Growth vs. Population Access to Electricity')
    plt.xlabel('Urban Population Growth (annual %)')
    plt.ylabel('Access to Electricity (% of population)')
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'low - urban pop growth vs. population access to electricity.png')
    # # plt.show()

    # higher air pollution = higher hiv incidence
    sns.pairplot(data=low_income_ca,
                 x_vars=['avg_air_pollution'],
                 y_vars=['incidence_hiv'],
                 size=5,
                 palette='plasma')
    plt.title('Air Pollution (mean) vs. HIV Incidence')
    plt.xlabel('Air Pollution, mean annual exposure (micrograms per cubic meter)')
    plt.ylabel('HIV incidence (% of uninfected population ages 15-49)')
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'low - avg air pollution vs. HIV incidence.png')
    # # plt.show()

    # higher air pollution % vs. lesser access to electricity (urban)
    sns.pairplot(data=low_income_ca,
                 x_vars=['avg_air_pollution'],
                 y_vars=['access_to_electricity_urban'],
                 size=5,
                 palette='plasma')
    plt.title('Air Pollution (mean) vs. Urban Access to Electricity')
    plt.xlabel('Air Pollution, mean annual exposure (micrograms per cubic meter)')
    plt.ylabel('Access to Electricity, urban (% of urban population)')
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'low - avg air pollution % vs. urban access to electricity.png')
    # # plt.show()

    ############################################################################
    # Interesting Correlations for Lower Middle Income Countries (Central Africa 1)
    ############################################################################

    # higher compulsory education years % = higher air pollution
    sns.pairplot(data=lower_middle_income_ca,
                 x_vars=['compulsory_edu_yrs'],
                 y_vars=['avg_air_pollution'],
                 size=5,
                 palette='plasma')
    plt.xlabel('Compulsory education, duration (years)')
    plt.ylabel('Air Pollution, mean annual exposure (micrograms per cubic meter)')
    plt.title('Compulsory Education vs Air Pollution')
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'lowmid - compulsory edu yrs % vs. air pollution.png')
    # # plt.show()

    # higher urban pop = lesser female employment
    sns.pairplot(data=lower_middle_income_ca,
                 x_vars=['urban_population_pct'],
                 y_vars=['pct_female_employment'],
                 size=5,
                 palette='plasma')
    plt.xlabel('Urban Population (% of total)')
    plt.ylabel('Female Employment (% of female population)')
    plt.tight_layout()
    plt.title('Urban Population vs Female Employment')
    plt.savefig(pairplot_folder / 'lowmid - Urban pop vs. female employment.png')
    # # plt.show()

    #  higher air pollution = lesser male employment
    sns.pairplot(data=lower_middle_income_ca,
                 x_vars=['avg_air_pollution'],
                 y_vars=['pct_male_employment'],
                 size=5,
                 palette='plasma')
    plt.xlabel('Air Pollution, mean annual exposure (micrograms per cubic meter)')
    plt.ylabel('Male Employment (% of male population)')
    plt.title('Air Pollution vs Male Employment')
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'lowmid - Air pollution vs male employment.png')
    # # plt.show()

    # higher urban pop = lower industry employment
    sns.pairplot(data=lower_middle_income_ca,
                 x_vars=['urban_population_pct'],
                 y_vars=['pct_industry_employment'],
                 size=5,
                 palette='plasma')
    plt.xlabel('Urban Population (% of total)')
    plt.ylabel('Employment in Industry (% of total employment)')
    plt.title('Employment in Industry vs Urban Population')
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'lowmid - Urban pop vs. industry employment.png')
    # # plt.show()

    """"
    GNI group by income group
    """
    low_median = low_income_world['gni_index'].median()
    lower_middle_median = lower_middle_income_world['gni_index'].median()
    upper_middle_median = upper_middle_income_world['gni_index'].median()
    clean_no_high = clean_data[clean_data['income_group'] != 'High income']
    no_us = clean_no_high[clean_no_high['Hult_Team_Regions'] != 'Central Africa 1']

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.swarmplot(x='income_group',
                  y='gni_index',
                  data=no_us,
                  hue='Hult_Team_Regions',
                  cmap='summer',
                  alpha=0.2,
                  size=15)
    sns.swarmplot(x='income_group',
                  y='gni_index',
                  data=country_data,
                  color='red',
                  size=15)

    plt.xlabel('Income Group')
    plt.ylabel('GNI (per capita)')
    plt.title('Gross National Income for Each Country by Income Group', fontsize=20)
    plt.savefig(swarmplot_folder / 'region by income group')
    # plt.show()

    """
    Lower middle income)  
    higher urban population (%) correlates with less industry employment
    """
    sns.pairplot(x_vars=['urban_population_pct'],
                 y_vars=['pct_industry_employment'],
                 data=lower_middle_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, lower_middle_income_ca.shape[0]):
        texts.append(plt.text(lower_middle_income_ca.urban_population_pct[line],
                              lower_middle_income_ca.pct_industry_employment[line],
                              lower_middle_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Urban Population vs Industry Employment - \nLower Middle Income Group', fontsize=16)
    plt.xlabel('Urban population (% of total)', fontsize=14)
    plt.ylabel('Employment in industry (% of total employment)', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'Urban Population vs Industry Employment (lower middle).png')
    # # plt.show()

    """
    Lower middle income
    Higher urban population (%) → Less female employment (%)
    """
    sns.pairplot(x_vars=['urban_population_pct'],
                 y_vars=['pct_female_employment'],
                 data=lower_middle_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, lower_middle_income_ca.shape[0]):
        texts.append(plt.text(lower_middle_income_ca.urban_population_pct[line],
                              lower_middle_income_ca.pct_female_employment[line],
                              lower_middle_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Urban Population vs Contributed Female Family Workers - \nLower Middle Income Group', fontsize=16)
    plt.xlabel('Urban population (% of total)', fontsize=14)
    plt.ylabel('Contributing family workers, female', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'Urban Population vs Female Family Workers (lower middle).png')
    # # plt.show()

    """
    low income
    Higher air pollution 
    → Higher HIV incidence
    GDP Growth (.79) 
    → Higher air pollution (.79)
    
    """
    plt.subplot(1, 2, 1)
    plt.scatter(x='gdp_growth_pct',
                y='avg_air_pollution',
                data=low_income_ca,
                s=200)
    plt.title('PM2.5 Air Pollution vs GDP Growth Rate', fontsize=20)
    plt.xlabel('GDP Growth Rate')
    plt.ylabel('PM2.5 Air Pollution')
    plt.tight_layout()

    plt.subplot(1, 2, 2)
    plt.scatter(x='incidence_hiv',
                y='avg_air_pollution',
                data=low_income_ca,
                s=200)
    plt.title('PM2.5 Air Pollution vs Incidence of HIV', fontsize=20)
    plt.xlabel('Incidence of HIV')
    plt.ylabel('PM2.5 Air Pollution')
    plt.tight_layout()

    plt.savefig(scatterplot_folder / 'Higher air pollution → Higher HIV incidence GDP Growth (.79) .png')
    # # plt.show()

    """
    low income
    GDP Growth (.79) 
    → Higher air pollution (.79)
    → Less access to electricity
    """
    plt.subplot(1, 2, 1)
    plt.scatter(x='gdp_growth_pct',
                y='avg_air_pollution',
                data=low_income_ca,
                s=200)
    plt.title('PM2.5 Air Pollution vs GDP Growth Rate', fontsize=20)
    plt.xlabel('GDP Growth Rate')
    plt.ylabel('PM2.5 Air Pollution')
    plt.tight_layout()

    plt.subplot(1, 2, 2)
    plt.scatter(x='access_to_electricity_pop',
                y='avg_air_pollution',
                data=low_income_ca,
                s=200)
    plt.title('PM2.5 Air Pollution vs Access to electricity', fontsize=20)
    plt.xlabel('Access to electricity (% of population)')
    plt.ylabel('PM2.5 Air Pollution')
    plt.tight_layout()

    plt.savefig(scatterplot_folder / 'Higher air pollution → Access to electricity GDP Growth (.79) .png')
    # # plt.show()

    """
    Low income countries
    Increased urban population → Less access to electricity for everyone
    """
    sns.pairplot(x_vars=['urban_population_growth_pct'],
                 y_vars=['access_to_electricity_pop'],
                 data=low_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, low_income_ca.shape[0]):
        texts.append(plt.text(low_income_ca.urban_population_growth_pct[line],
                              low_income_ca.access_to_electricity_pop[line],
                              low_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Urban Population Growth Ratevs Access to Electricity -\n Low Income Group', fontsize=16)
    plt.xlabel('Urban Population Growth (Annual %)', fontsize=14)
    plt.ylabel('Access to electricity (% of population)', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'Urban Population growth vs Access to Electricity (low).png')
    # plt.show()

    """
    HIV
    """

    # lower Middle income: internet usage
    sns.pairplot(x_vars=['incidence_hiv'],
                 y_vars=['internet_usage_pct'],
                 data=lower_middle_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, lower_middle_income_ca.shape[0]):
        texts.append(plt.text(lower_middle_income_ca.incidence_hiv[line],
                              lower_middle_income_ca.internet_usage_pct[line],
                              lower_middle_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Incidence of HIV vs Individuals using the Internet \n Lower Middle Income Group', fontsize=16)
    plt.xlabel('Incidence of HIV', fontsize=14)
    plt.ylabel('Individuals using the Internet (% of population)', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(pairplot_folder / 'Incidence of HIV vs Individuals using the Internet (lower mid).png')
    # plt.show()

    # low income: air pollution
    sns.pairplot(x_vars='incidence_hiv',
                 y_vars='avg_air_pollution',
                 data=low_income_ca,
                 kind='reg',
                 size=8)
    # for line in range(0, lower_middle_income_ca.shape[0]):
    #    texts.append(plt.text(lower_middle_income_ca.incidence_hiv[line],
    #                          lower_middle_income_ca.internet_usage_pct[line]+1,
    #                          lower_middle_income_ca.country_name[line],
    #                          horizontalalignment='left',
    #                          size='large',
    #                          color='black',
    #                          weight='semibold'))
    plt.title('PM2.5 Air Pollution vs Incidence of HIV', fontsize=20)
    plt.xlabel('Incidence of HIV (% of uninfected population ages 15-49)', fontsize=14)
    plt.ylabel('PM2.5 Air Pollution', fontsize=14)
    plt.tight_layout()
    plt.savefig(scatterplot_folder / 'Higher air pollution → Higher HIV incidence GDP Growth (.79) .png')
    # plt.show()

    # lower middle income: ccess to electricity
    sns.pairplot(x_vars=['incidence_hiv'],
                 y_vars=['access_to_electricity_pop'],
                 data=lower_middle_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, lower_middle_income_ca.shape[0]):
        texts.append(plt.text(lower_middle_income_ca.incidence_hiv[line],
                              lower_middle_income_ca.access_to_electricity_pop[line],
                              lower_middle_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Incidence of HIV vs Access to Electricity \n Lower Middle Income Group', fontsize=16)
    plt.xlabel('Incidence of HIV', fontsize=14)
    plt.ylabel('Access to electricity (% of population)', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(scatterplot_folder / 'Incidence of HIV vs Access to electricity (low).png')
    # plt.show()

    # lower middle income: Higher percentage of agriculture employment
    sns.pairplot(x_vars=['incidence_hiv'],
                 y_vars=['pct_agriculture_employment'],
                 data=lower_middle_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, lower_middle_income_ca.shape[0]):
        texts.append(plt.text(lower_middle_income_ca.incidence_hiv[line],
                              lower_middle_income_ca.pct_agriculture_employment[line],
                              lower_middle_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Incidence of HIV vs Employment in agriculture \n Lower Middle Income Group', fontsize=16)
    plt.xlabel('Incidence of HIV', fontsize=14)
    plt.ylabel('Employment in agriculture (% of total employment)', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(scatterplot_folder / 'Incidence of HIV vs Employment in agriculture (lower mid).png')
    # plt.show()

    # lower middle income: Higher percentage of service employment
    sns.pairplot(x_vars=['incidence_hiv'],
                 y_vars=['pct_services_employment'],
                 data=lower_middle_income_ca,
                 kind='reg',
                 size=8)
    texts = []
    for line in range(0, lower_middle_income_ca.shape[0]):
        texts.append(plt.text(lower_middle_income_ca.incidence_hiv[line],
                              lower_middle_income_ca.pct_services_employment[line],
                              lower_middle_income_ca.country_name[line],
                              horizontalalignment='left',
                              size='large',
                              color='black',
                              weight='semibold'))
    plt.title('Incidence of HIV vs Employment in services \n Lower Middle Income Group', fontsize=16)
    plt.xlabel('Incidence of HIV', fontsize=14)
    plt.ylabel('Employment in services (% of total employment)', fontsize=14)
    adjust_text(texts)
    plt.tight_layout()
    plt.savefig(scatterplot_folder / 'Incidence of HIV vs Employment in agriculture (lower mid).png')
    # plt.show()
