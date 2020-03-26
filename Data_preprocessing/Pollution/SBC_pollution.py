import pandas as pd
import numpy as np


def bounce_back(df_original):
    """Remove the firms coming back and forth in the original ASIF dataset
    Args:
        df_original: A dataframe containing the query from Bigquery with firm
        level data

    Returns:
        A list with the firms to keep from the original dataset

    """
    balanced_ckt = (df_original
                    .groupby([
                        'newID',
                        'year'
                    ]
                    )['newID']
                    .nunique()
                    .unstack(1, fill_value=0)
                    .stack()
                    .groupby('newID')
                    .apply(lambda x: x / x.shift(1))
                    .rename('count')
                    .reset_index()
                    .groupby(['newID', 'count'])
                    .count()
                    .loc[(slice(None), np.inf), :]
                    .loc[lambda x:x['year'] == 1]
                    .reset_index()['newID']
                    .to_list()
                    )

    return balanced_ckt


def prepare_ASIF(df_original, industry_agg):
    """Prepare the original ASIF dataset

    The function proceed as follow:

    - Keep year from 2002 to 2007
    - rename the original columns
    - create period, industry (to have a consistent industry variable) and
    convert the string some variables
    Args:
        df_original: A dataframe containing the query from Bigquery with firm
        level data
        industry_agg: (String) Explicit how to aggregate the data:
            - indu_2
            - cic


    Returns:
        A dataframe from ASIF during year 2002 to 2007

    """

    years = ['2002', '2003', '2004', '2005', '2006', '2007']
    df_asif_preprocessing = (df_original
                             .loc[lambda x:x['year'].isin(years)]
                             .rename(
                                 columns={"cityen_correct": "cityen",
                                          "citycn_correct": "citycn",
                                          "output": "output_fcit",
                                          "input": "input_fcit",
                                          "fa_net": "capital_fcit",
                                          "employment": "labour_fcit"}
                             )
                             .assign(
                                 Province_en=lambda x:
                                 x["Province_en"].str.strip(),
                                 Period=lambda x: np.where(x["year"] > 2005,
                                                           "After", "Before"),
                                 industry=lambda x: x[industry_agg].astype(
                                     'str'),
                                 geocode4_corr=lambda x:
                                 x['geocode4_corr'].astype('str'),
                             )
                             )

    return df_asif_preprocessing


def keep_cities(df_China_cities_target_so2, df_asif_preprocessing):
    """remove cities with a null SO2 mandates or those who are not in the
    dataset 6 concecutive years

    The function proceed as follow:

    - Keep year from 2002 to 2007
    - rename the original columns
    - create period, industry (to have a consistent industry variable) and
    convert the string some variables
    Args:
        df_original: A dataframe containing the query from Bigquery with firm
        level data
        industry_agg: (String) Explicit how to aggregate the data:
            - indu_2
            - cic

    Returns:
        A list with cities to remove

    """

    # keep variables we need in city SO2
    df_China_cities_target_so2_drop = df_China_cities_target_so2.drop(
        columns=[
            "prov2013",
            "citycn",
            "ttoutput",
            "SO2_05_city_reconstructed",
            "SO2_obj_2010",
            "SO2_perc_reduction_c",
        ]
    )

# Remove 0 mandate
    zero_mandate = (df_China_cities_target_so2
                    .apply(pd.to_numeric, errors='ignore')
                    .loc[lambda x: x['tso2_mandate_c'].isin([0])]
                    .set_index('cityen')
                    .index.to_list()
                    )

# Keep cities in dataset all years
    city_to_exclude = (df_asif_preprocessing[['cityen', 'year']]
                       .drop_duplicates()
                       .groupby('cityen')
                       .count()
                       .loc[lambda x: x['year'] != 6]
                       .index
                       .to_list()
                       )
# Add to the city list those who have 0 mandate
    city_to_exclude.extend(zero_mandate)

    return city_to_exclude, df_China_cities_target_so2_drop


def metafunctionTFP(df_original,
                    SBC_pollution_China,
                    df_TCZ_list_china,
                    df_TFP_asif_china,
                    df_China_cities_target_so2,
                    df_CIC_4_digit_average_SO2,
                    # order_columns,
                    industry_agg='cic',
                    agg_t_c_i_o=False,
                    panel=False,
                    bounce=False):
    """Prepare data for paper on SBC/TFP and pollution in China

    The program works as follow:

    - Step 1: If `bounce` is true, then the program exclude firms bouncing back
    on and on in the dataset
    - Step 2: Keep a set of year and create the period dummy variable. The dummy
     takes the value of `After` all year after 2005.
    - Step 3: Remove all cities not available every years
    - Step 8: Merge TCZ, TFP and polluted industry
    - Step 9 (optional): If the user choose to get a symmetric dataset, then
    the program excludes industries which are not available in both period
    - Step 10: Remove outliers : when SO2 emissions are below 500 and above
    2276992 (about .5 and .95 of the distribution)
    - Step 11: Create 3 bunches of fixed effect:  city-industry; time-industry
    and time-city

    Args:
        df_original: A dataframe containing the query from Bigquery with firm
        level data
        Query available here:
        df_TCZ_list_china: A dataframe containing the list of TCZ
        df_TFP_asif_china: A dataframe containing the TFP
        df_CIC_4_digit_average_SO2: A dataframe containing the polluted sectors
        order_columns: (list) A list to explicit how to rearrange the columns
        industry_agg: (String) Explicit how to aggregate the data:
            - indu_2
            - cic
        agg_t_c_i_o: Aggregate the dataframe at the year, city, industry and
        ownership level: Boolean By default, False
        symetric: (Boolean): If true, keep only industries available during
        both period
        (ie 10 and 11th FYP)
        bounce: (Boolean): If true,Remove firms who enter and leave the market
         many times

    Returns:
        A dataframe with the TFP  at the firm-city-industry-year
         level along with TCZ city, polluted sectors and sectors

    """

    # Remove firms enter and leaving the market many times
    if bounce == True:
        balanced_ckt = bounce_back(df_original)

        df_original = df_original.loc[lambda x:
                                      x['newID'].isin(balanced_ckt)]

    df_asif_preprocessing = prepare_ASIF(df_original, 'cic')

    city_to_exclude, df_China_cities_target_so2_drop = keep_cities(
        df_China_cities_target_so2,
        df_asif_preprocessing)

    df_asif_preprocessing_ = df_asif_preprocessing.loc[lambda x:
                                                       ~x['cityen'].isin(
                                                           city_to_exclude)]

    m_mandate = (df_China_cities_target_so2['tso2_mandate_c']
                 .astype('float')
                 .mean())

    df_temp = (df_asif_preprocessing_
               # .merge(
               #   (df_TFP_asif_china
               #      .assign(
               #        industry=lambda x: x['cic'].astype('str')))
               #   .drop(columns=['cic']))
               .merge(df_TCZ_list_china.drop(columns=['City', 'Province']))
               .merge(
                   (df_CIC_4_digit_average_SO2
                    .assign(industry=lambda x: x['cic'].astype('str'),
                            )
                       .drop(columns=['cic'])))
               .merge(
                   df_China_cities_target_so2_drop,
                   on="cityen",
                   how="inner",
               )
               .assign(Period=lambda x: np.where(x["year"] > 2005,
                                                 "After", "Before"),
                       TCZ=lambda x: np.where(x["TCZ"] == '1',
                                              "TCZ", "No_TCZ"),
                       year=lambda x: x['year'].astype('str'),
                       tso2_mandate_c=lambda x:
                       x['tso2_mandate_c'].astype('float'),
                       effort_c=lambda x: np.where(x['tso2_mandate_c'] > m_mandate,
                                                   'Above', 'Below'),
                       )
               .rename(columns={
                   "output": "output_fcit",
                   "TCZ": "TCZ_c",
                   "tso2_mandate_c": "target_c",
                   # "tfp": "tfp_fcit",
                   # "tfp_def": "tfp_def_fcit",
               })
               # .reindex(columns=order_columns)
               )

    # Aggregate city year indusrty ownership
    if agg_t_c_i_o:
        df_temp = (
            df_temp.drop(columns=['bdat', 'target_c'])
            .groupby([
                'year',
                'Period',
                'cityen',
                'industry',
                'SOE',
                'TCZ_c',
                'polluted_thre'
            ])
            .mean()
            .reset_index()
        )

    # Merge with orginal base paper: Keep same year, city, induystry as
    # In the paper's dataset
    df_temp = df_temp.merge(SBC_pollution_China[['year',
                                                 'cityen',
                                                 'industry']].assign(
        year=lambda x: x['year'].astype('str'),
        #geocode4_corr=lambda x: x['geocode4_corr'].astype('int'),
        industry=lambda x: x['industry'].astype('str')
    ).drop_duplicates())

    # Compute fixed effect

    df_final = df_temp.copy()

    df_final["FE_c_i"] = pd.factorize(df_final["cityen"] +
                                      df_final['industry'])[0]

    df_final["FE_t_i"] = pd.factorize(df_final["year"] +
                                      df_final['industry'])[0]

    df_final["FE_t_c"] = pd.factorize(df_final["year"] + df_final["cityen"])[0]

    df_final["FE_c_i_o"] = pd.factorize(df_final["cityen"] + df_final["industry"] +
                                        df_final["SOE"])[0]

    df_final["FE_t_o"] = pd.factorize(
        df_final["year"] + df_final["SOE"])[0]

    if panel:
        df_final = (df_final
                    .groupby(['year', 'cityen', 'industry', 'SOE'])['cityen']
                    .count()
                    .unstack(0)
                    .dropna(axis=0)
                    .reset_index('SOE')
                    .groupby(level=[0, 1])['SOE']
                    .count()
                    .loc[lambda x: x == 2]
                    .reset_index()
                    .rename(columns={'SOE': 'count'})
                    ).merge(df_final)

    return df_final


def metafunction(df_original,
                 df_TCZ_list_china,
                 df_China_city_pollution_98_2007,
                 df_China_cities_target_so2,
                 order_columns,
                 industry_agg='indu_2',
                 symetric=True,
                 bounce=False,
                 soe=False):
    """Prepare data for paper on SBC and pollution in China

    The program works as follow:

    - Step 1: If `bounce` is true, then the program exclude firms bouncing back
    on and on in the dataset
    - Step 2: Keep a set of year and create the period dummy variable. The dummy
     takes the value of `After` all year after 2005.
    - Step 3: Remove all cities not available every years
    - Step 4: Prepare the SOE industries. More precisely, the program computes
    the numbers of SOE firms for each year during 2002-2005 by industry
    (either HS2 or CIC), and get the average output;capital and labour at the
     same level. Then, the share by industry is computed.
    - Step 5: Define the polluted sectors in three difference ways. First,
    the program computes the average SO2 emission by industries for the year
    2002. Then, polluted sectors are defined whether the average is above the
    national average, the third decile or 68070.
    - Step 6: Remove the city-industry with null value for SO2 emission
    - Step 7: Aggregate the control variable at the city-industry-year level
    - Step 8: Merge TCZ, Share SOE, pollution, pollution by industry
    - Step 9 (optional): If the user choose to get a symmetric dataset, then
    the program excludes industries which are not available in both period
    - Step 10: Remove outliers : when SO2 emissions are below 500 and above
    2276992 (about .5 and .95 of the distribution)
    - Step 11: Create 3 bunches of fixed effect:  city-industry; time-industry
    and time-city

    Args:
        df_original: A dataframe containing the query from Bigquery with firm
        level data
        Query available here:
        df_TCZ_list_china: A dataframe containing the list of TCZ
        df_China_city_pollution_98_2007: A dataframe containing the SO2 emission
        level
        years: (List) years to keep from the df_original data
        order_columns: (list) A list to explicit how to rearrange the columns
        industry_agg: (String) Explicit how to aggregate the data:
            - indu_2
            - cic
        symetric: (Boolean): If true, keep only industries available during
        both period
        (ie 10 and 11th FYP)
        bounce: (Boolean): If true,Remove firms who enter and leave the market
         many times

    Returns:
        A dataframe with the SO2 emission aggregated at the city-industry-year
         level along with TCZ city,
        polluted sectors and sectors with the share of SOE defined with the
         count, output, capital or labor

    """

    # Remove firms enter and leaving the market many times
    # Remove firms enter and leaving the market many times
    if bounce == True:
        balanced_ckt = bounce_back(df_original)

        df_original = df_original.loc[lambda x:
                                      x['newID'].isin(balanced_ckt)]

    # Keep defined year, rename columns and create period variable
    df_asif_preprocessing = prepare_ASIF(df_original, industry_agg)
    # keep variables we need in city SO2
    df_China_cities_target_so2_drop = df_China_cities_target_so2.drop(
        columns=[
            "prov2013",
            "citycn",
            "ttoutput",
            "SO2_05_city_reconstructed",
            "SO2_obj_2010",
            "SO2_perc_reduction_c",
        ]
    )

    # Remove 0 mandate
    city_to_exclude = keep_cities(df_China_cities_target_so2,
                                  df_asif_preprocessing)

    df_asif_preprocessing_ = df_asif_preprocessing.loc[lambda x:
                                                       ~x['cityen'].isin(
                                                           city_to_exclude)]
    # Compute nb of SOE by industry-year and get mean share
    # Compute output of SOE by industry-year and get mean share
    if soe:
        share_SOE = (df_asif_preprocessing_
                     .loc[lambda x:x['year'].isin(['2002', '2003', '2004',
                      '2005'])]
                     .groupby(['year',
                               'industry',
                               'SOE'
                               ]
                              )
                     .agg(  # newID=('newID', 'count'),
                         output_fcit=('output_fcit', 'sum'),
                         capital_fcit=('capital_fcit', 'sum'),
                         labour_fcit=('labour_fcit', 'sum')
                     )
                     .unstack(fill_value=0)
                     .assign(  # count_=lambda x: x.iloc[:, 0] + x.iloc[:, 1],
                         total_o=lambda x: x.iloc[:, 0] + x.iloc[:, 1],
                         total_k=lambda x: x.iloc[:, 2] + x.iloc[:, 3],
                         total_l=lambda x: x.iloc[:, 4] + x.iloc[:, 5],
                         #count_SOE=lambda x: x.iloc[:, 1] / x.iloc[:, -4],
                         out_share_SOE=lambda x: x.iloc[:, 1] / x['total_o'],
                         cap_share_SOE=lambda x: x.iloc[:, 3] / x['total_k'],
                         lab_share_SOE=lambda x: x.iloc[:, 5] / x['total_l'],
                         #count_private=lambda x: 1 - x.iloc[:, -4],
                     )
                     .groupby(level=1)
                     .agg(  # count_SOE=('count_SOE', 'mean'),
                         out_share_SOE=('out_share_SOE', 'mean'),
                         cap_share_SOE=('cap_share_SOE', 'mean'),
                         lab_share_SOE=('lab_share_SOE', 'mean'),
                         #     #count_private=('count_private', 'mean')
                     )
                     .reset_index()
                     )
    # Share foreign/SOE
    else:
        share_for = (df_asif_preprocessing_
                     .loc[lambda x:x['year'].isin(['2002', '2003', '2004',
                      '2005'])]
                     .groupby(['year',
                               'industry',
                               'FOREIGN'
                               ]
                              )
                     .agg(
                         output_fcit=('output_fcit', 'sum'),
                         capital_fcit=('capital_fcit', 'sum'),
                         labour_fcit=('labour_fcit', 'sum')
                     )
                     .unstack(fill_value=0)
                     .assign(
                         total_o=lambda x: x.iloc[:, 0] +
                         x.iloc[:, 1] + x.iloc[:, 2],
                         total_k=lambda x: x.iloc[:, 3] +
                         x.iloc[:, 4] + x.iloc[:, 5],
                         total_l=lambda x: x.iloc[:, 6] +
                         x.iloc[:, 7] + x.iloc[:, 8],
                         out_share_for=lambda x: x.iloc[:, 1] / x['total_o'],
                         out_share_soe1=lambda x: x.iloc[:, 2] / x['total_o'],
                         cap_share_for=lambda x: x.iloc[:, 4] / x['total_k'],
                         cap_share_soe1=lambda x: x.iloc[:, 5] / x['total_k'],
                         lab_share_for=lambda x: x.iloc[:, 7] / x['total_l'],
                         lab_share_soe1=lambda x: x.iloc[:, 8] / x['total_l']
                     )
                     .groupby(level=1)
                     .agg(
                         out_share_for=('out_share_for', 'mean'),
                         out_share_soe1=('out_share_soe1', 'mean'),
                         cap_share_for=('cap_share_for', 'mean'),
                         cap_share_soe1=('cap_share_soe1', 'mean'),
                         lab_share_for=('lab_share_for', 'mean'),
                         lab_share_soe1=('lab_share_soe1', 'mean')
                     )
                     .reset_index()
                     )
    # Compute pollution

    if industry_agg == 'cic':
        col_rename = 'indus_code'
    else:
        col_rename = 'ind2'

    # Polluted sectors
    pollution_ind = (df_China_city_pollution_98_2007
                     .loc[lambda x: ~x['tso2'].isin([0])]
                     .loc[lambda x: x['year'].isin(['2002'])]
                     .rename(columns={col_rename: industry_agg})
                     .groupby(industry_agg)[['tso2', 'toutput']]
                     .mean()
                     .reset_index()
                     .assign(
                         polluted_di=lambda x: np.where(
                             x["tso2"] > x["tso2"].quantile(
                                 [0.75]).loc[(0.75)],
                             "Above",
                             "Below",
                         ),
                         polluted_mi=lambda x: np.where(
                             x["tso2"] > x["tso2"].mean(),
                             "Above",
                             "Below",
                         ),
                         polluted_thre=lambda x: np.where(
                             #x["tso2"] > 68173.11,
                             x["tso2"] > 68070.78,
                             "Above",
                             "Below",
                         ),
                         pollution_intensity_i=lambda x: x['tso2'] / \
                         x['toutput']
                     )
                     .assign(industry=lambda x: x[industry_agg].astype('str'))
                     .rename(columns={
                         'tso2': 'tso2_i'
                     })
                     )

    # Input/output indutry -> try sector

    va_sector = (df_asif_preprocessing_
                 .loc[lambda x: x['year'].isin(['2002'])]
                 # .rename(columns={col_rename: industry_agg})
                 .groupby('industry')[['output_fcit', 'input_fcit']]
                 .sum()
                 .assign(va_i=lambda x: x['output_fcit'] - x['input_fcit'])
                 .rename(columns={'output_fcit': 'output_i',
                                  'input_fcit': 'input_i'})
                 .reset_index()
                 )

    pollution = (df_China_city_pollution_98_2007
                 .loc[lambda x: ~x['tso2'].isin([0])]
                 .rename(columns={col_rename: industry_agg})
                 .rename(columns={
                     industry_agg: 'industry',
                     'tso2': 'tso2_cit',
                     'tCOD': 'tCOD_cit',
                     'twaste_water': 'twaste_water_cit',
                     # 'toutput' : 'toutput_cit'
                 }
                 )
                 .assign(industry=lambda x: x['industry'].astype('str')
                         )
                 )

    # Aggregate controle variable
    df_perc = (df_asif_preprocessing_
               .groupby(['year',
                         'Period',
                         'Province_en',
                         'Lower_location',
                         'Larger_location',
                         'Coastal',
                         'cityen',
                         'geocode4_corr',
                         'industry',
                         'Short',
                         ]
                        )['output_fcit', 'capital_fcit', 'labour_fcit']
               .sum()
               .reset_index()
               )

    ###
    m_mandate = (df_China_cities_target_so2['tso2_mandate_c']
                 .astype('float')
                 .mean())

    # Merge data
    df_temp = (
        df_perc
        .merge(
            df_TCZ_list_china[["geocode4_corr", "TCZ"]],
            on="geocode4_corr",
            how="inner",
        )
        .merge(pollution, on=[
            'year',
            'cityen',
            'industry'
        ],
            how='inner')
        .merge(pollution_ind, on=[
            'industry'
        ],
            how='inner')
        .merge(
            df_China_cities_target_so2_drop,
            on="cityen",
            how="inner",
        )
        #.merge(
        #    va_sector,
        #    on='industry',
        #    how='left'
        #)
        .assign(Period=lambda x: np.where(x["year"] > 2005,
                                          "After", "Before"),
                TCZ=lambda x: np.where(x["TCZ"] == '1',
                                       "TCZ", "No_TCZ"),
                year=lambda x: x['year'].astype('str'),
                tso2_mandate_c=lambda x: x['tso2_mandate_c'].astype('float'),
                effort_c=lambda x: np.where(x['tso2_mandate_c'] > m_mandate,
                                            'Above', 'Below'),
                )
        .rename(columns={
            "output": "output_fcit",
            "TCZ": "TCZ_c",
            "tso2_mandate_c": "target_c",
        })

    )

    if soe:
        df_temp = df_temp.merge(
            share_SOE,
            on="industry",
            how="inner",
        )
    else:
        df_temp = df_temp.merge(
            share_for,
            on="industry",
            how="inner",
        )

    # Remove industry not in both year

    if symetric:
        both_period = (
            df_temp
            .groupby(['industry', 'Period'])['Period']
            .nunique().groupby(level=0)
            .sum()
            .loc[lambda x:x == 2]
            .index
        )

        df_temp = df_temp.loc[lambda x:x['industry'].isin(both_period)]

    # Remove outliers

    df_temp = df_temp.loc[lambda x:(x['tso2_cit'] > 500)
                          &
                          (x['tso2_cit'] < 2276992)
                          ].reindex(columns=order_columns)

    # Compute fixed effect

    df_final = df_temp.copy()

    df_final["FE_c_i"] = pd.factorize(df_final["cityen"] +
                                      df_final['industry'])[0]

    df_final["FE_t_i"] = pd.factorize(df_final["year"] +
                                      df_final['industry'])[0]

    df_final["FE_t_c"] = pd.factorize(df_final["year"] + df_final["cityen"])[0]

    return df_final, va_sector
