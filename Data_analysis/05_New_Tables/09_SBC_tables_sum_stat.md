---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.4.0+dev
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region kernel="SoS" -->
# Table 1 and 2
<!-- #endregion -->

```python kernel="Python 3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
import pandas as pd
import numpy as np

gs = connector.open_connection(online_connection = False,
                              path_credential = 
                               '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/'
                              )
service_gd = gs.connect_remote(engine = 'GS')
gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])
service = gs.connect_remote('GCP')
from GoogleDrivePy.google_platform import connect_cloud_platform
project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service['GoogleCloudP'])   
```

<!-- #region kernel="Python 3" -->
# Load data
<!-- #endregion -->

<!-- #region kernel="Python 3" -->
## parameters
<!-- #endregion -->

```python kernel="Python 3"
aggregation_param = 'geocode4_corr'
decile = 6
```

<!-- #region kernel="Python 3" -->
## Load cityname_and_code from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```python kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA
### To change the range

sheetid = '1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA'
sheetname = 'final'

df_cityname_and_code = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_cityname_and_code.head()
```

<!-- #region kernel="Python 3" -->
## Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```python kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range

sheetid = '15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q'
sheetname = 'TCZ'

df_TCZ_list_china = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_TCZ_list_china.head()
```

<!-- #region kernel="SoS" -->
## Load yearbook9813 from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset

We need this table for the table 0 -> Need year 2001
<!-- #endregion -->

```python kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range


sheetid = '1NpfDQ6dz7knjZDPSjRz2QanVf7td3ujSQn7hD7Gxkow'
sheetname = 'yearbook'

yearbook9813 = (gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True).loc[lambda x: x['year'].isin(['2003','2004',
                                                       '2005', '2006',
                                                       '2007', '2008',
                                                       '2009', '2010'])]
                .drop(columns = ['代码',
                  '简称', 
                  "[Envirct06:工业二氧化硫去除量][单位:吨]",
                 '[Envirct08:工业烟尘去除量][单位:吨]',
                 '[Envirct09:工业烟尘排放量][单位:吨]']
               )
                .rename(columns = {'[Envirct07:工业二氧化硫排放量][单位:吨]':
                                   'tso2'})
                .assign(tso2 = lambda x: pd.to_numeric(x['tso2'],
                                                         errors = 'coerce'
                                                         )
                                                         )
               )
```

## Load chinese_city_characteristics from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset

```python
df_chinese_city_characteristics = pd.read_csv('../df_chinese_city_characteristics.csv')
```

```python
df_chinese_city_characteristics.head()
```

<!-- #region -->
## Load provinces_location from Google Spreadsheet


Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```python

### Please go here https://docs.google.com/spreadsheets/d/1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g
### To change the range

sheetid = '1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g'
sheetname = 'provinces_location.csv'

df_provinces_location = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_provinces_location.head()
```

<!-- #region kernel="Python 3" -->
## Paper dataset
<!-- #endregion -->

```python kernel="Python 3"
query = (
          "SELECT * "
            "FROM China.SBC_pollution_China "

        )

df_final = gcp.upload_data_from_bigquery(query = query, location = 'US')
```

```python kernel="Python 3"
list_agg = df_final[aggregation_param].to_list()
```

<!-- #region kernel="Python 3" -->
## Pollution China 1998-2005
<!-- #endregion -->

```python kernel="Python 3"
query = ("""SELECT SUM( tso2) sum_so2, year, citycode as geocode4_corr
FROM China.pollution_city_cic4_china
GROUP BY year, citycode
"""
        )
df_pol = (gcp.upload_data_from_bigquery(query = query, location = 'US')
          .loc[lambda x: ~x['geocode4_corr'].isna()]
      .assign(geocode4_corr = lambda x: 
              x['geocode4_corr'].astype(int).astype('str')
             )
         )
          
```

```python kernel="Python 3"
### Zhaoruili data
sheetid = '1kSyGnkWOwoGVe1PgsQUGoWYO3DB8p9fgVh_VE6ilBt8'
sheetname = 'SO2_emission'

df_TCZ_SO2_Zhaoruili= gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True).apply(lambda x: pd.to_numeric(x, errors ='ignore'))
```

<!-- #region kernel="Python 3" -->
## Compute Herfhindal: proxy Size

$$
H=\sum_{i=1}^{N} s_{i}^{2}
$$

where $s_i$ is the market share of industry[city] $i$ in a city [industry], and $N$ is the number of firms. 

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city-industry: `market_share_cit`
- Step 2: compute the sum of squared market share by industry[city]: `Herfindahl_agg_t`
- Step 3: Compute the average across time: `Herfindahl_agg`
- Step 4: Compute the deciles of step 3: `decile_herfhindal_agg`
    - Low decile implies a low concentration within sectors
    - High decile implies a high concentration within sectors
<!-- #endregion -->

```python kernel="Python 3"
query = """
WITH sum_cit AS (
  SELECT geocode4_corr, cic as industry, sum(output) as sum_o_cit, year
  FROM China.asif_firm_china 
  WHERE year >= 2002 AND year <= 2007
  AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
  GROUP BY geocode4_corr, cic, year
) 
SELECT * 
FROM 
  (WITH sum_agg_t AS (
    SELECT {0}, SUM(sum_o_cit) as sum_o_agg_t, year
    FROM sum_cit
    WHERE year >= 2002 AND year <= 2007
    GROUP BY year, {0}
)
SELECT *
FROM
  (WITH ms_cit AS (
    SELECT  sum_cit.industry, sum_cit.geocode4_corr, sum_cit.year,
    sum_cit.sum_o_cit/NULLIF(sum_agg_t.sum_o_agg_t, 0) as market_share_cit
    FROM sum_cit
    LEFT JOIN sum_agg_t
ON (
sum_cit.year = sum_agg_t.year AND 
sum_cit.{0} = sum_agg_t.{0}
)
)
SELECT *
FROM
  (WITH agg_1 AS (
SELECT {0}, SUM(POW(market_share_cit, 2)) as Herfindahl_agg_t,
year
FROM ms_cit
GROUP BY year, {0}
ORDER BY year, {0} 
)
SELECT *
FROM (
SELECT {0},
AVG(Herfindahl_agg_t) as Herfindahl_agg
FROM agg_1
GROUP BY {0}
ORDER BY {0}
)

)))
"""
df_herfhindal = (gcp.upload_data_from_bigquery(
    query = query.format(aggregation_param),
                                         location = 'US')
                 .loc[lambda x: x[aggregation_param].isin(list_agg)]
                )
```

```python kernel="Python 3"
df_herfhindal_final = (df_final.merge(df_herfhindal,
                                     on=[aggregation_param],
                                     how='left',
                                     indicator=True
                                     )
                       .assign(
                       decile_herfhindal = lambda x:
                           pd.qcut(x['Herfindahl_agg'],10, labels=False),
                       mean_herfhindal= 
                           lambda x: np.where(
                               x["Herfindahl_agg"] > 
                               x["Herfindahl_agg"].drop_duplicates().mean(),
                               1,0
                           ),
                       third_herfhindal= 
                           lambda x: np.where(
                               x["Herfindahl_agg"] >
                               (x["Herfindahl_agg"]
                                .drop_duplicates()
                                .quantile([.75])
                                .values[0]),
                               1,0
                           ),
                    concentrated_city = lambda x:np.where(
                    x['decile_herfhindal'] > decile,
                           'Concentrated city',"No Concentrated city"
                    )
                       )[['geocode4_corr',
                                           'concentrated_city']].drop_duplicates(
    subset = 'geocode4_corr')
                .assign(geocode4_corr = lambda x: 
                        x['geocode4_corr'].astype('str'))
                      )
```

<!-- #region kernel="Python 3" -->
## SOE vs Private

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry[city], ownership (SOE/PRIVATE): `Share_X_agg_o`
- ~Step 2: Compute dummy when share SOE above share domestic by industry[city]~
- Step 3: Compute decile by industry[city]-ownership
    - Note,  high decile in SOE means the industry[city] has relatively high share of SOE output, but not in absolule value as in step 2. A decile 9 in SOE can be a decile 2 or 3 in Domestic
<!-- #endregion -->

```python kernel="Python 3"
query_share_ = """ 
WITH sum_agg_o AS (
  SELECT 
    case WHEN ownership = '{2}' THEN '{2}' ELSE '{3}' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_agg_o, 
    SUM(fa_net / 10000000) as fa_net_agg_o, 
    SUM(employment / 100000) as employment_agg_o,
    {1} as {0}
  FROM 
    China.asif_firm_china 
  WHERE 
    year >= 2002 
    AND year <= 2007 
    AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
  GROUP BY 
    OWNERSHIP, 
    {0}
) 
SELECT 
  * 
FROM 
  (
    WITH sum_agg AS(
      SELECT 
        SUM(output_agg_o) as output_agg, 
        SUM(fa_net_agg_o) as fa_net_agg, 
        SUM(employment_agg_o) as employment_agg, 
        {0} AS {0}_b
      FROM 
        sum_agg_o 
      GROUP BY 
        {0}
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_agg_o AS(
          SELECT 
            OWNERSHIP, 
            output_agg_o / output_agg AS share_output_agg_o, 
            fa_net_agg_o / fa_net_agg AS share_fa_net_agg_o, 
            employment_agg_o / employment_agg AS share_employement_agg_o, 
            {0}
          FROM 
            sum_agg_o 
            LEFT JOIN sum_agg ON sum_agg_o.{0} = sum_agg.{0}_b 
        ) 
        SELECT 
        {0},
        OWNERSHIP,  
        share_output_agg_o,
        share_fa_net_agg_o,
        share_employement_agg_o
        FROM share_agg_o
        WHERE OWNERSHIP = '{2}'
        )
        )
"""
OWNERSHIP = 'SOE'
counterpart = 'PRIVATE'

df_share_soe= query_share_.format(aggregation_param,
                                             aggregation_param,
                                             OWNERSHIP,
                                            counterpart)
    
df_share_soe = (gcp.upload_data_from_bigquery(query = df_share_soe,
                                         location = 'US')
                    .loc[lambda x: x[aggregation_param].isin(list_agg)]
                   )
df_share_soe.shape 
```

<!-- #region kernel="Python 3" -->
# Table 1

Ouput: 

- Overleaf
    - Temp_tables/Tables_paper/02_paper_version_2/11_table_stat
- Google Drive
    - [11_table_stat](https://drive.google.com/open?id=1Xejq3Jem9sD34yif7s_8Co-4bAP4wWe9)
![](https://drive.google.com/uc?export=view&id=1Xejq3Jem9sD34yif7s_8Co-4bAP4wWe9)


<!-- #endregion -->

```python kernel="Python 3"
#### If industry, we need to use out_share_SOE, cap_share_SOE,lab_share_SOE
##### Output share already computed in the paper's table for industry but not
##### for city, in the later case, we use the data from ASIF
decile =6

if aggregation_param== 'industry':
    out = "out_share_SOE"
    cap = "cap_share_SOE"
    emp = "lab_share_SOE"
else:
    out = "share_output_agg_o"
    cap = "share_fa_net_agg_o"
    emp = "share_employement_agg_o"
    
df_final_SOE = (df_final.merge(
    df_share_soe,
    on = [aggregation_param],
    how = 'left',
    indicator = True
)
                .assign(
                       output = lambda x:
                           pd.qcut(x[out],10, labels=False),
                       capital = lambda x:
                           pd.qcut(x[cap],10, labels=False),
                       employment = lambda x:
                           pd.qcut(x[emp],10, labels=False),
                       mean_output = lambda x:np.where(
                    x[out] > x[out].drop_duplicates().mean(),
                           1,0
                       ),
                    mean_capital = lambda x:np.where(
                    x[cap] > x[cap].drop_duplicates().mean(),
                           1,0
                       ),
                    mean_employment = lambda x:np.where(
                    x[emp] > x[emp].drop_duplicates().mean(),
                           1,0
                       ),
                    soe_city = lambda x:np.where(
                    x['output'] > decile,
                           'SOE dominated',"No SOE dominated"
                       )
                    
                    )
                .drop(columns = '_merge')[['geocode4_corr',
                                           'output',
                                           'TCZ_c',
                                          'soe_city',
                                          'target_c']].drop_duplicates(
    subset = 'geocode4_corr')
            .assign(geocode4_corr = lambda x: 
                        x['geocode4_corr'].astype('str'))
                

)
df_final_SOE['soe_city'].value_counts()
```

```python kernel="Python 3"
df_final_SOE_table2 = (df_final.merge(
    df_share_soe,
    on = [aggregation_param],
    how = 'left',
    indicator = True
)
                .assign(
                       output = lambda x:
                           pd.qcut(x[out],10, labels=False),
                       capital = lambda x:
                           pd.qcut(x[cap],10, labels=False),
                       employment = lambda x:
                           pd.qcut(x[emp],10, labels=False),
                       mean_output = lambda x:np.where(
                    x[out] > x[out].drop_duplicates().mean(),
                           1,0
                       ),
                    mean_capital = lambda x:np.where(
                    x[cap] > x[cap].drop_duplicates().mean(),
                           1,0
                       ),
                    mean_employment = lambda x:np.where(
                    x[emp] > x[emp].drop_duplicates().mean(),
                           1,0
                       ),
                    soe_city = lambda x:np.where(
                    x['output'] > decile,
                           'SOE dominated',"No SOE dominated"
                    )
                )[['geocode4_corr',
                   'soe_city',
                   'Lower_location',
                   'Larger_location',
                   'TCZ_c',
                   'Coastal',
     'share_output_agg_o',
     'share_fa_net_agg_o',
     'share_employement_agg_o',
                  'target_c']]
                       .drop_duplicates(subset = 'geocode4_corr')
                       .assign(geocode4_corr = lambda x: 
                        x['geocode4_corr'].astype('str'))
                      )
df_final_SOE_table2.shape
```

<!-- #region kernel="Python 3" -->
### 1998-2000

- TCZ
- No TCZ
- SOE
- No SOE
- Full 
<!-- #endregion -->

```python kernel="Python 3"
dic_ = {
    '1998-2001': [],
    '2002-2005': [],
    '2006-2010': [],
    'Target':[]
}
```

```python kernel="Python 3"
t1 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['1998', '2000'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 0)
 .pct_change()
 .dropna()
)

dic_['1998-2001'].append(np.round(t1.loc['No_TCZ'].values[0][0], 2))
dic_['1998-2001'].append(np.round(t1.loc['TCZ'].values[0][0], 2))
```

```python kernel="Python 3"
t2 = (df_pol
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['sum_so2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['1998', '2001']))
     ]
  .groupby(['soe_city',"year"])['sum_so2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['1998-2001'].append(np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['1998-2001'].append(np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
t3 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['1998', '2000'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 1)
 .sum()
 .pct_change()
 .dropna()
)
dic_['1998-2001'].append(np.round(t3.loc[2000].values[0], 2))
```

<!-- #region kernel="Python 3" -->
### 2001-2005

- TCZ
- No TCZ
- SOE
- No SOE
- Full 
<!-- #endregion -->

```python kernel="Python 3"
t1 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['2001', '2005'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['2002-2005'].append(np.round(t1.loc['No_TCZ'].values[0][0], 2))
dic_['2002-2005'].append(np.round(t1.loc['TCZ'].values[0][0], 2))
```

```python kernel="Python 3"
t2 = (df_pol
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['sum_so2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['2001', '2005']))
     ]
  .groupby(['soe_city',"year"])['sum_so2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['2002-2005'].append(np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['2002-2005'].append(np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
t3 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['2001', '2005'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 1)
 .sum()
 .pct_change()
 .dropna()
)
dic_['2002-2005'].append(np.round(t3.loc[2005].values[0], 2))
```

<!-- #region kernel="Python 3" -->
### 2006-2010
<!-- #endregion -->

```python kernel="Python 3"
t1 = (df_cityname_and_code
 .drop(
    columns=['citycn',
             'cityen',
             'citycn_correct',
             'cityen_correct',
             'Province_cn',
             'Province_en'])
 .merge(yearbook9813.rename(columns = {'geocode4_corr' : 'extra_coda'}))
 .drop(columns = ['extra_coda'])
 .merge(df_TCZ_list_china[['geocode4_corr', 'TCZ']], how = "left")
 .merge(df_final_SOE, on = ['geocode4_corr'],how = 'left')
 .apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
 .assign(TCZ = lambda x: x['TCZ'].fillna(0))
 .replace({'TCZ': {0: 'No_TCZ', 1:'TCZ'}})
 .loc[lambda x: 
 (x['year'].isin(['2006', '2010']))]
  .groupby(['TCZ',"year"])['tso2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)

dic_['2006-2010'].append(np.round(t1.loc['No_TCZ'].values[0], 2))
dic_['2006-2010'].append(np.round(t1.loc['TCZ'].values[0], 2))
```

```python kernel="Python 3"
#### average target
t1 = (df_cityname_and_code
 .drop(
    columns=['citycn',
             'cityen',
             'citycn_correct',
             'cityen_correct',
             'Province_cn',
             'Province_en'])
 .merge(yearbook9813.rename(columns = {'geocode4_corr' : 'extra_coda'}))
 .drop(columns = ['extra_coda'])
 .merge(df_TCZ_list_china[['geocode4_corr', 'TCZ']], how = "left")
 .merge(df_final_SOE, on = ['geocode4_corr'],how = 'left')
 .apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
 .assign(TCZ = lambda x: x['TCZ'].fillna(0))
 .replace({'TCZ': {0: 'No_TCZ', 1:'TCZ'}})
 .loc[lambda x: 
 (x['year'].isin(['2006']))]
  .groupby(['TCZ',"year"])['target_c']
.mean()
     )
dic_['Target'].append(-np.round(t1.loc['No_TCZ'].values[0], 2))
dic_['Target'].append(-np.round(t1.loc['TCZ'].values[0], 2))
```

```python kernel="Python 3"
t2 = (yearbook9813
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['tso2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['2006', '2010']))
     ]
  .groupby(['soe_city',"year"])['tso2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)

dic_['2006-2010'].append(np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['2006-2010'].append(np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
### target
t2 = (yearbook9813
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['tso2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['2006']))
     ]
  .groupby(['soe_city',"year"])['target_c']
  .mean()
     )
dic_['Target'].append(-np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['Target'].append(-np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
t3 = (df_cityname_and_code
 .drop(
    columns=['citycn',
             'cityen',
             'citycn_correct',
             'cityen_correct',
             'Province_cn',
             'Province_en'])
 .merge(yearbook9813.rename(columns = {'geocode4_corr' : 'extra_coda'}))
 .drop(columns = ['extra_coda'])
 .merge(df_TCZ_list_china[['geocode4_corr', 'TCZ']], how = "left")
 .merge(df_final_SOE, on = ['geocode4_corr'],how = 'left')
 .apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
 .assign(TCZ = lambda x: x['TCZ'].fillna(0))
 .replace({'TCZ': {0: 'No_TCZ', 1:'TCZ'}})
 .loc[lambda x: 
 (x['year'].isin(['2006', '2010']))]
  .groupby(["year"])['tso2']
 .sum()
 #.groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['2006-2010'].append(np.round(t3.loc[2010], 2))
dic_['Target'].append(-.1)
```

```python kernel="Python 3"
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass

title = "SO2 reduction during the subsequent FYPs"
(pd.DataFrame(dic_, index= ['No TCZ','TCZ',
                           'No Dominated SOE^a',
                           ' Dominated SOE^a',
                           'Full Sample'])
 .rename_axis('Cities')
 .reset_index()
 .to_latex('table_1.tex',
           caption = title,
           index=False,
           label = "table_1",
           float_format="{:,.2%}".format)
)
```

```python kernel="Python 3"
import sys, os, shutil
sys.path.insert(0,'..')
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```python kernel="Python 3"
jupyter_preview = False
table_nte = """
Sources: Author's own computation  \n
The list of TCZ is provided by the State Council, 1998.
"Official Reply to the State Council Concerning Acid Rain Control Areas
and Sulfur Dioxide Pollution Control Areas".
The information about the SO2 level are collected using various edition
of the China Environment Statistics Yearbook.
We compute the reduction of SO2 emission using the same methodology
as Chen and al.(2018).  \n
$a$ (No) Dominated SOEs cities refer to cities where the 
(output, capital, employment) share of SOEs is (below) above a critical threshold,
for instance the 6th decile
"""
lb.beautify_table(table_nte = table_nte,
                  name = 'table_1',
                  jupyter_preview  = jupyter_preview,
                  resolution = 500)
if jupyter_preview == False:
    source_to_move = ['table_1.tex']
    dest = ['Overleaf_statistic/11_table_stat.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i])
```

<!-- #region kernel="Python 3" -->
# Table 2

Ouput: 

- Overleaf
    - Temp_tables/Tables_paper/02_paper_version_2/11_table_stat
- Google Drive
    - [11_table_stat](https://drive.google.com/open?id=1MdWuHFzX-Ow5M34T8GnGiKQvFpmXY9I7)
![](https://drive.google.com/uc?export=view&id=1MdWuHFzX-Ow5M34T8GnGiKQvFpmXY9I7)
<!-- #endregion -->

```python kernel="Python 3"
t0 = (df_final_SOE_table2[['share_output_agg_o', 'share_fa_net_agg_o',
       'share_employement_agg_o']]
      .mean()
      .reset_index()
      .set_index('index')
      .T
      .rename(index={0: 'Full sample'}))
```

```python kernel="Python 3"
t1 = df_final_SOE_table2.groupby('Lower_location')[['share_output_agg_o',
                                                    'share_fa_net_agg_o',
       'share_employement_agg_o']].mean()
```

```python kernel="Python 3"
t2 = df_final_SOE_table2.groupby('Larger_location')[['share_output_agg_o',
                                                     'share_fa_net_agg_o',
       'share_employement_agg_o']].mean()
```

```python kernel="Python 3"
t3 = df_final_SOE_table2.groupby('TCZ_c')[['share_output_agg_o',
                                           'share_fa_net_agg_o',
       'share_employement_agg_o']].mean().rename(index={'No_TCZ': 'No TCZ'})
```

```python kernel="Python 3"
t4 = (df_final_SOE_table2
 .merge(df_herfhindal_final)
 .groupby('concentrated_city')[['share_output_agg_o', 'share_fa_net_agg_o',
       'share_employement_agg_o']]
 .mean()
)
```

Add target

```python kernel="Python 3"
jupyter_preview = False
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass

title = "Summary statistics by city characteristics"
header = ["Output share SOE_i", "Capital share SOE_i","Employment share SOE_i"
          #, "Target_i"
         ]
#pd.concat([
#   pd.concat([t0, t1, t2, t3, t4], axis = 0),
#    pd.concat([t5, t6, t7, t8, t9], axis = 0)
#], axis = 1)
pd.concat([t0, t1, t2, t3, t4], axis = 0).to_latex(
    'table_1.tex',
    caption = title,
    index=True,
    label = "table_1",
    header = header,
    float_format="{:,.2%}".format)

table_nte = """
Sources: Author's own computation \n
The list of TCZ is provided by the State Council, 1998. \n
Output $\text { Share SOE }_{i}$ refers to the ratio of output
(respectively capital, employment) of SOEs over the total production
(capital, employment) in city $i$
      
"""
lb.beautify_table(table_nte = table_nte,
                  name = 'table_1',
                  jupyter_preview  = jupyter_preview,
                  resolution = 200)

if jupyter_preview == False:
    source_to_move = ['table_1.tex']
    dest = ['Overleaf_statistic/12_table_stat.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i])
```

Only for the text:

SOE share by:

- Hinterland
- SPZ/no SPZ


```python
pd.concat([(df_final_SOE_table2
 .merge(df_TCZ_list_china)
 .groupby('SPZ')[['share_output_agg_o', 'share_fa_net_agg_o',
       'share_employement_agg_o']]
 .mean().rename(index={'0': 'No SPZ', '1': 'SPZ'})
),
           (df_final_SOE_table2
 .assign(hinterland = lambda x: 
         np.where(
             x['Lower_location'].isin(['Coastal']),
             "No", "Yes")
        )
 .groupby('hinterland')[['share_output_agg_o', 'share_fa_net_agg_o',
       'share_employement_agg_o']]
 .mean().rename(index={'No': 'No hinterland',
                       'Yes': 'hinterland'})
)
          ], axis = 0).rename(columns = {
    'share_output_agg_o':'Output share SOE_i',
    'share_fa_net_agg_o':'Capital share SOE_i',
    'share_employement_agg_o':'Employment share SOE_i'
}) .style.format('{:,.2%}')

```

### Table 2 bis

Ouput: 

https://drive.google.com/open?id=1HlzY8F6gjfT03WecoIxBTAovvh4OFnBI

- Overleaf
    - Temp_tables/Tables_paper/02_paper_version_2/14_table_stat
- Google Drive
    - [14_table_stat](https://drive.google.com/open?id=1HlzY8F6gjfT03WecoIxBTAovvh4OFnBI)
![](https://drive.google.com/uc?export=view&id=1HlzY8F6gjfT03WecoIxBTAovvh4OFnBI)

```python
df_final_SOE_table2.loc[lambda x: x['geocode4_corr'].isin(['3101'])]
```

```python
t1 = (df_final_SOE_table2[['target_c']]
      .mean()
      .reset_index()
      .set_index('index')
      .T
      .rename(index={0: 'Full sample'}))
t2 = df_final_SOE_table2.groupby('Lower_location')[['target_c']].mean()
t3 = df_final_SOE_table2.groupby('Larger_location')[['target_c']].mean()
t4 = df_final_SOE_table2.groupby('TCZ_c')[['target_c']
                                         ].mean().rename(index={'No_TCZ':
                                                                'No TCZ'})
t5 = (df_final_SOE_table2
 .merge(df_herfhindal_final)
 .groupby('concentrated_city')[['target_c']]
 .mean()
)
t6 = df_final_SOE_table2.groupby('Coastal')[['target_c']
                                         ].mean().rename(index={False:
                                                                'No Coastal',
                                                               True: 'Coastal'})
```

```python
t7 = (df_final_SOE_table2.groupby(['soe_city'])[['target_c']]
 .mean()
      .T
 .rename(index={'target_c': 'Full sample'})
)
t8 = (df_final_SOE_table2.groupby(['soe_city','Lower_location'])[['target_c']]
 .mean()
 .unstack(0)
 .droplevel(0, axis =1)
)

t9 = (df_final_SOE_table2.groupby(['soe_city','Larger_location'])[['target_c']]
 .mean()
 .unstack(0)
 .droplevel(0, axis =1)
)

t10 = (df_final_SOE_table2.groupby(['soe_city','TCZ_c'])[['target_c']]
 .mean()
 .unstack(0)
 .droplevel(0, axis =1)
      .rename(index={'No_TCZ':'No TCZ'})
)
t11 = (df_final_SOE_table2
 .merge(df_herfhindal_final)
 .groupby(['soe_city','concentrated_city'])[['target_c']]
 .mean().unstack(0).droplevel(0, axis =1)
)
t12 = (df_final_SOE_table2
       .groupby(['soe_city','Coastal'])[['target_c']]
       .mean()
       .rename(index={False:'No Coastal',
                      True: 'Coastal'})
       .unstack(0)
       .droplevel(0, axis =1)
      )
```

```python
index = (pd.concat([t7, t8, t9, t10, t11, t12],axis = 0)
 .reset_index()
)['index'].to_list()
```

```python
# Unit 1.000 tonnes
(pd.concat([t1, t2, t3, t4, t5, t6],axis = 0)
 .rename(columns={'target_c': 'All cities'})
 .reset_index()
).merge(
    (pd.concat([t7, t8, t9, t10, t11, t12] ,axis = 0)
     .reset_index()
    ) 
).set_index('index')
```

```python
title = "Summary statistics of Target by city characteristics"
header = ["All Cities","No SOE dominated", "SOE dominated"]

(pd.concat([t1, t2, t3, t4, t5, t6],axis = 0)
 .rename(columns={'target_c': 'All cities'})
 .reset_index()
).merge(
    (pd.concat([t7, t8, t9, t10, t11, t12] ,axis = 0)
 .reset_index())
    ,on = ['index']).drop_duplicates(
    subset = 
    ['index']).set_index('index').reindex(index = 
                                          index).to_latex(
    'table_1.tex',
    caption = title,
    index=True,
    label = "table_1",
    header = header,
    #float_format="{:,.2}".format
)

table_nte = """
Sources: Author's own computation \n
The list of TCZ is provided by the State Council, 1998. \n
$a$ (No) Dominated SOEs cities refer to cities where the 
(output, capital, employment) share of SOEs is (below) above a critical threshold,
for instance the 6th decile
      
"""
lb.beautify_table(table_nte = table_nte,
                  name = 'table_1',
                  jupyter_preview  = jupyter_preview,
                  resolution = 200)

if jupyter_preview == False:
    source_to_move = ['table_1.tex']
    dest = ['Overleaf_statistic/15_table_stat.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i])
```

# Table 3

Ouput: 

- Overleaf
    - Temp_tables/Tables_paper/02_paper_version_2/13_table_stat
- Google Drive
    - [13_table_stat](https://drive.google.com/open?id=1ITXwbLX3XpgnZWGOgXPhnQj17680Cgey)
![](https://drive.google.com/uc?export=view&id=1ITXwbLX3XpgnZWGOgXPhnQj17680Cgey)

```python
df_herfhindal_final.dtypes
```

```python
df_table_3 = (
    df_final
    .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
    .merge(
        (df_chinese_city_characteristics
 .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
 .merge(df_TCZ_list_china, how = 'left')
 .merge(df_final_SOE_table2[['geocode4_corr', 'soe_city']])
 .merge(df_herfhindal_final)
 .assign(
     TCZ = lambda x: x['TCZ'].fillna(0),
     SPZ = lambda x: x['SPZ'].fillna('0'),
        )
)
    )
             )
df_table_3.shape
```

Panel A

```python
jupyter_preview = False
title = "Summary statistics by city characteristics"
#header = ["Output share SOE_i", "Capital share SOE_i","Employment share SOE_i", "Target_i"]

(df_table_3
 .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
 .groupby('TCZ_c')[['tso2_cit','so2_intensity','gdp_cap',
       'population']].mean().rename(index={'No_TCZ': 'No TCZ'}).T
 .rename_axis('')
 .reset_index()
 .to_latex(
    'table_1.tex',
    caption = title,
    index=False,
    label = "table_3",
    #header = header,
    float_format="{:,.0f}".format)
)

table_nte = """
Sources: Author's own computation \n
The list of TCZ is provided by the State Council, 1998. \n
Output $\text { Share SOE }_{i}$ refers to the ratio of output
(respectively capital, employment) of SOEs over the total production
(capital, employment) in city $i$
      
"""
lb.beautify_table(table_nte = False,
                  name = 'table_1',
                  jupyter_preview  = jupyter_preview,
                  resolution = 200)

if jupyter_preview == False:
    source_to_move = ['table_1.tex']
    dest = ['Overleaf_statistic/13_table_stat.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i])
```

```python

```

Only in text:

GDP per capita in:

- SOE/No SOE cities
- Concentrated/ No concentrated
- SPZ
- Coastal 
- TCZ

  & No TCZ & Concentrated & No Concentrated & SOE dominated & SOE No dominated & SOE dominated & SOE No dominated & SOE dominated & SOE No dominated\\

Count number of city above turning point RMB:

- TCZ: 28795
- No Concentrated: 45396
- SOE No dominated Output: 30264
- SOE No dominated Capital: 24867
- SOE No dominated employment: 35190 

```python
pd.concat([
    (df_table_3
 .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
 .groupby('TCZ_c')[['tso2_cit','so2_intensity','gdp_cap',
       'population']].mean().rename(index={'No_TCZ': 'No TCZ'}).T
 #.style.format('{:,.0f}')
),
    (df_table_3
 .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
 .groupby('SPZ')[['tso2_cit','so2_intensity','gdp_cap',
       'population']].mean().rename(index={'0': 'No SPZ', '1': 'SPZ'}).T
),
    (df_table_3
 .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
 .groupby('soe_city')[['tso2_cit','so2_intensity','gdp_cap',
       'population']].mean().T
),
    (df_table_3
 .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
 .groupby('Coastal')[['tso2_cit','so2_intensity','gdp_cap',
       'population']].mean().rename(index={False: 'No Coastal', 
                                          True: 'Coastal'}).T
),
    (df_table_3
 .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
 .groupby('concentrated_city')[['tso2_cit','so2_intensity','gdp_cap',
       'population']].mean().T
)
], axis = 1).style.format('{:,.0f}')
    
```

- TCZ: 28795
- No Concentrated: 45396
- SOE No dominated Output: 30264
- SOE No dominated Capital: 24867
- SOE No dominated employment: 35190 

```python
(df_table_3[['geocode4_corr', 'soe_city']]
 .drop_duplicates()['soe_city']
 .value_counts())
```

```python
dic_ = {
     'TCZ': 28795,
     'No Concentrated': 45396,
     'SOE No dominated Output': 30264,
     'SOE No dominated Capital': 24867,
     'SOE No dominated employment': 35190
}
```

```python
81 + 146
```

```python
35/146
```

```python
for key, value in dic_.items():
    results = (df_table_3
 .assign(count = lambda x: 
         np.where(
             x['gdp_cap'] > value,
             "Above", "Below")
        )
 .loc[lambda x: x['soe_city'].isin(['SOE dominated']) 
     & x['year'].isin(['2007'])]
 [['geocode4_corr', 'count']]
 .drop_duplicates()
 ['count'].value_counts()
 .reset_index()
 .assign( percentage = lambda x: np.round(x['count']/x['count'].sum(),2) * 100)
 #.style.format('{:,.0%}', subset = ['percentage'])
).T
    print("\n", key, "\n",results )
```

```python
#df_table_3['cityen'].drop_duplicates()
```

```python

```

```python
141 + 87
```

```python
95/ 147
```

```python
(df_table_3
 .loc[lambda x: x['year'].isin(['2007'])]
 [['TCZ_c','geocode4_corr', 'soe_city', 'gdp_cap']]
 .drop_duplicates()
 .groupby(['TCZ_c','soe_city'])['gdp_cap']
 .mean()
 .unstack(-1)
)
```

```python
(df_table_3
 .loc[lambda x: x['year'].isin(['2007'])]
 [['TCZ_c','geocode4_corr', 'soe_city', 'gdp_cap']]
 .drop_duplicates()
 .groupby(['TCZ_c','soe_city'])['gdp_cap']
 .count()
 .unstack(-1)
)
```

```python
for key, value in dic_.items():
    results = (df_table_3
 .assign(count = lambda x: 
         np.where(
             x['gdp_cap'] > value,
             "Above", "Below")
        )
 .loc[lambda x: ~ x['soe_city'].isin(['SOE dominated'])  & 
      x['year'].isin(['2007'])]
 [['geocode4_corr', 'count']]
 .drop_duplicates()
 ['count'].value_counts()
 .reset_index()
 .assign( percentage = lambda x: np.round(x['count']/x['count'].sum(),2) * 100).T
 #.style.format('{:,.0%}', subset = ['percentage'])
)
    print("\n",key, "\n",results )
```

SO2 emission by TCZ before and after the 11th FYP, full sample

By:

- TCZ/No TCZ
- SO3/ No SOE

```python
(df_final[['TCZ_c', 'Period', 'cityen', 'tso2_cit', 'year']]
 .assign(
          tso2_cit = lambda x: x['tso2_cit']/10000)
 .groupby(['TCZ_c', 'Period', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['TCZ_c', 'Period'], ascending=True)
      .unstack(-1)
      .assign(difference=lambda x: np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1])
              )
      .round(2)
)
```

TCZ

```python
t1 = (df_final
      .assign(
          tso2_cit = lambda x: x['tso2_cit'])
      .groupby(['TCZ_c', 'Period', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['TCZ_c', 'Period'], ascending=True)
      .unstack(-1)
      .assign(difference=lambda x: np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1])
              )
      .round(2)
      #.iloc[:, 2:]
      .stack()
      .unstack(0)
      .rename(index={'':'Full sample'})
      .rename_axis("Location")
      )
t1
```

SO2 emission by TCZ before and after the 11th FYP, by city location

```python
t2 = (df_final
      .assign(tso2_cit = lambda x: x['tso2_cit'])
      .groupby(['TCZ_c', 'Period', 'Lower_location', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1, 2])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['TCZ_c', 'Period'], ascending=True)
      .unstack(-2)
      .assign(difference=lambda x:  np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1])
              )
      .sort_values(by='Lower_location')
      .round(2)
      .iloc[:, 2:]
      .unstack(0)
      .droplevel(level=1, axis=1)
      .rename_axis("Location")
      )
t2
```

SO2 emission by TCZ before and after the 11th FYP, by coastal area

```python
t3 = (df_final
      .assign(tso2_cit = lambda x: x['tso2_cit'])
      .groupby(['TCZ_c', 'Period', 'Coastal', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1, 2])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['TCZ_c', 'Period'], ascending=True)
      .unstack(-2)
      .assign(difference=lambda x: np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1]))
      .sort_values(by='Coastal')
      .round(2)
      .iloc[:, 2:]
      .unstack(0)
      .droplevel(level=1, axis=1)
      .rename_axis("Location")
      .rename(index={True:'Coastal',
                    False: 'Non Coastal'}
             )
      )
t3
```

SOE

```python
t4 = (df_final
      .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
      .merge(df_final_SOE_table2[['geocode4_corr', 'soe_city']])
      .assign(
          tso2_cit = lambda x: x['tso2_cit'])
      .groupby(['soe_city', 'Period', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['soe_city', 'Period'], ascending=True)
      .unstack(-1)
      .assign(difference=lambda x: np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1])
              )
      .round(2)
      .iloc[:, 2:]
      .stack()
      .unstack(0)
      .rename(index={'':'Full sample'})
      .rename_axis("Location")
      )
t4
```

```python
t5 = (df_final
      .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
      .merge(df_final_SOE_table2[['geocode4_corr', 'soe_city']])
      .assign(tso2_cit = lambda x: x['tso2_cit'])
      .groupby(['soe_city', 'Period', 'Lower_location', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1, 2])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['soe_city', 'Period'], ascending=True)
      .unstack(-2)
      .assign(difference=lambda x:  np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1])
              )
      .sort_values(by='Lower_location')
      .round(2)
      .iloc[:, 2:]
      .unstack(0)
      .droplevel(level=1, axis=1)
      .rename_axis("Location")
      )
t5
```

```python
t6 = (df_final
      .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
      .merge(df_final_SOE_table2[['geocode4_corr', 'soe_city']])
      .assign(tso2_cit = lambda x: x['tso2_cit'])
      .groupby(['soe_city', 'Period', 'Coastal', 'cityen'])
      .agg(
          sum_tso2_c=('tso2_cit', np.sum),
      )
      .groupby(level=[0, 1, 2])
      .agg(
          avg_tso2=('sum_tso2_c', np.mean)
      )
      .sort_values(by=['soe_city', 'Period'], ascending=True)
      .unstack(-2)
      .assign(difference=lambda x: np.round(x.iloc[:, 0] - x.iloc[:, 1], 0),
              variance=lambda x: 1-(x.iloc[:, 0] / x.iloc[:, 1]))
      .sort_values(by='Coastal')
      .round(2)
      .iloc[:, 2:]
      .unstack(0)
      .droplevel(level=1, axis=1)
      .rename_axis("Location")
      .rename(index={True:'Coastal',
                    False: 'Non Coastal'}
             )
      )
t6
```

```python
t = ((pd.concat([
    pd.concat([t1, t2, t3]),
    pd.concat([t4, t5,t6])
], axis = 1)
)
 .to_latex(index=True,
              float_format='%.2f'
             )
)
t = t.replace('\_',' ')
t = t.replace('.00','')
t = t.replace('TCZ c','TCZ')
print(t)
```

# Update:

Yearly average difference


Panel A

```python
df_table_3 = (
    df_final
    .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
    .merge(
        (df_chinese_city_characteristics
 .assign(geocode4_corr = lambda x: x['geocode4_corr'].astype('str'))
 .merge(df_TCZ_list_china, how = 'left')
 .merge(df_final_SOE_table2[['geocode4_corr', 'soe_city']])
 #.merge(df_herfhindal_final)
 .assign(
     TCZ = lambda x: x['TCZ'].fillna('0'),
     SPZ = lambda x: x['SPZ'].fillna('0'),
        )
)
    )
    .assign(so2_intensity = lambda x: x['tso2_cit']/ x['population'])
             )
df_table_3.columns
```

```python
(df_table_3[['year', 'Period', 'TCZ', 'geocode4_corr','Lower_location', 
            'soe_city','gdp_cap', 'population']].drop_duplicates()
 .replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['TCZ', 'Period'])[['gdp_cap']]
 .mean()
 .sort_index(level = ['TCZ','Period'], ascending = [True, False])
 .stack()
 .unstack([0, 1])
 .assign(

         difference_no_tcz=lambda x: x.iloc[:, 1] - x.iloc[:, 0],
         difference_tcz=lambda x: x.iloc[:, 3] - x.iloc[:, 2],
             )
 .rename(index={'sum_so2': 'Full sample'})
 .round(0)
)
```

```python
tcz = pd.concat([(df_table_3[['year', 'Period', 'TCZ', 'geocode4_corr','Lower_location', 
            'soe_city','gdp_cap', 'population']].drop_duplicates()
 .replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['TCZ', 'Period'])[['gdp_cap']]
 .mean()
 .sort_index(level = ['TCZ','Period'], ascending = [True, False])
 .stack()
 .unstack([0, 1])
 #.assign(

         #difference_no_tcz=lambda x: x.iloc[:, 1] - x.iloc[:, 0],
         #difference_tcz=lambda x: x.iloc[:, 3] - x.iloc[:, 2],
 #            )
 .rename(index={'sum_so2': 'Full sample'})
 .round(0)
),
                 (df_table_3[['year', 'Period', 'TCZ', 'geocode4_corr','Lower_location', 
            'soe_city','gdp_cap', 'population']].drop_duplicates()
 .replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['TCZ', 'Period'])[['population']]
 .mean()
 .sort_index(level = ['TCZ','Period'], ascending = [True, False])
 .stack()
 .unstack([0, 1])
# .assign(
#
#         difference_no_tcz=lambda x: x.iloc[:, 1] - x.iloc[:, 0],
#         difference_tcz=lambda x: x.iloc[:, 3] - x.iloc[:, 2],
#             )
 .rename(index={'sum_so2': 'Full sample'})
 .round(0)
)
                 
                ], axis = 0)
tcz
```

```python
soe = pd.concat([(df_table_3[['year', 'Period', 'TCZ', 'geocode4_corr','Lower_location', 
            'soe_city','gdp_cap', 'population']].drop_duplicates()
 #.replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['soe_city', 'Period'])[['gdp_cap']]
 .mean()
 .sort_index(level = ['soe_city','Period'], ascending = [True, False])
 .stack()
 .unstack([0, 1])
 #.assign(
         #difference_no_soe=lambda x: x.iloc[:, 1] - x.iloc[:, 0],
         #difference_soe=lambda x: x.iloc[:, 3] - x.iloc[:, 2],
         #    )
 #.rename(index={'sum_so2': 'Full sample'})
 .round(0)
),
                 (df_table_3[['year', 'Period', 'TCZ', 'geocode4_corr','Lower_location', 
            'soe_city','gdp_cap', 'population']].drop_duplicates()
 #.replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['soe_city', 'Period'])[['population']]
 .mean()
 .sort_index(level = ['soe_city','Period'], ascending = [True, False])
 .stack()
 .unstack([0, 1])
 #.assign(

         #difference_no_soe=lambda x: x.iloc[:, 1] - x.iloc[:, 0],
         #difference_soe=lambda x: x.iloc[:, 3] - x.iloc[:, 2],
         #    )
 #.rename(index={'sum_so2': 'Full sample'})
 .round(0)
)
                 
                ], axis = 0)
soe
```

```python
pd.concat([tcz, soe], axis = 1)
```

```python
import sys, os, shutil
sys.path.insert(0,'..')
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2

jupyter_preview = False
title = "Summary statistics by city characteristics"

pd.concat([tcz, soe], axis = 1).to_latex(
    'table_1.tex',
    caption = title,
    index=True,
    label = "table_3",
    #header = header,
    float_format="{:,.0f}".format)

table_nte = """
Sources: Author's own computation \n
The list of TCZ is provided by the State Council, 1998. \n
Output $\text { Share SOE }_{i}$ refers to the ratio of output
(respectively capital, employment) of SOEs over the total production
(capital, employment) in city $i$
      
"""
lb.beautify_table(table_nte = False,
                  name = 'table_1',
                  jupyter_preview  = jupyter_preview,
                  resolution = 200)

if jupyter_preview == False:
    source_to_move = ['table_1.tex']
    dest = ['Overleaf_statistic/13_table_stat_panel_a.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i])
```

Panel B

```python
df_TCZ_list_china.head()
```

```python
(df_pol
 .loc[lambda x: x['year']
      .isin(['2002', '2003', '2004', '2005',
                                    '2006', '2007'])]
 .merge(df_cityname_and_code.merge(df_TCZ_list_china)[
     ['extra_coda','Province' , 'cityen', 'TCZ', 'SPZ']],
        left_on = ['geocode4_corr'],
        right_on = ['extra_coda'],
        how = 'inner', indicator = True)
)
```

```python
df_provinces_location.head()
```

```python
df_pol_tcz = (df_pol
 .loc[lambda x: x['year']
      .isin(['2002', '2003', '2004', '2005',
                                    '2006', '2007'])]
 #.merge(df_TCZ_list_china,on = ['geocode4_corr'], how = 'left')
 .merge(df_cityname_and_code.merge(df_TCZ_list_china)[
     ['extra_coda','Province' , 'cityen', 'TCZ', 'SPZ']],
        left_on = ['geocode4_corr'],
        right_on = ['extra_coda'],
        how = 'inner', indicator = True)
 .merge(df_final_SOE_table2[['geocode4_corr', 'soe_city']], how = 'left')
 .merge(df_provinces_location)
 .assign(
     soe_city = lambda x: x['soe_city'].fillna('No SOE dominated'),
     Period = lambda x: np.where(
         x['year'].isin(['2002', '2003', '2004', '2005']), 
         'Before', 'After'
     )
     )
 
 )


df_pol_tcz.groupby('year')['sum_so2'].sum()
```

```python
(df_pol_tcz
     .assign(sum_so2 = lambda x: x['sum_so2']/1000000000)
 .loc[lambda x: x['year'].isin(['2007'])]
 .groupby(['soe_city'])[['sum_so2']]
 .mean()
)
```

```python
(1-np.exp(.430*0.118874)) *100
```

```python

```

```python
1-np.exp(0.430*0.1239)
```

```python
(df_pol_tcz
     .assign(sum_so2 = lambda x: x['sum_so2']/1000000000)
 .replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['TCZ', 'Period'])[['sum_so2']]
 .sum()
 .stack()
 .unstack([0, 1])
 .assign(
         #variance_no_tcz=lambda x: 1-(x.iloc[:, 1] / x.iloc[:, 0]),
         #variance_tcz=lambda x: 1-(x.iloc[:, 3] / x.iloc[:, 2])
         difference_no_tcz=lambda x: x.iloc[:, 0] - x.iloc[:, 1],
         difference_tcz=lambda x: x.iloc[:, 2] - x.iloc[:, 3],
             )
 .rename(index={'sum_so2': 'Full sample'})
)
```

```python
tcz = pd.concat([
    ####TCZ
    (df_pol_tcz
     .assign(sum_so2 = lambda x: x['sum_so2']/1000000000)
 .replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['TCZ', 'Period'])[['sum_so2']]
 .sum()
 .stack()
 .unstack([0, 1])
 .assign(
         #variance_no_tcz=lambda x: 1-(x.iloc[:, 1] / x.iloc[:, 0]),
         #variance_tcz=lambda x: 1-(x.iloc[:, 3] / x.iloc[:, 2])
         difference_no_tcz=lambda x: x.iloc[:, 0] - x.iloc[:, 1],
         difference_tcz=lambda x: x.iloc[:, 2] - x.iloc[:, 3],
             )
 .rename(index={'sum_so2': 'Full sample'})
),
    (df_pol_tcz
     .assign(sum_so2 = lambda x: x['sum_so2']/1000000000)
 .replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['TCZ', 'Period', 'Lower_location'])[['sum_so2']]
 .sum()
 .stack()
 .unstack([0, 1])
 .assign(
         difference_no_tcz=lambda x: x.iloc[:, 0] - x.iloc[:, 1],
         difference_tcz=lambda x: x.iloc[:, 2] - x.iloc[:, 3],
             )
 .reset_index(level=1, drop=True)
)], axis= 0)
tcz
```

```python
(df_pol_tcz.assign(sum_so2 = lambda x: x['sum_so2']/ 10000)).groupby('year')['sum_so2'].sum()
```

```python
soe = pd.concat([
    (df_pol_tcz
     .assign(sum_so2 = lambda x: x['sum_so2']/1000000000)
 #.replace({'soe_city': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['soe_city', 'Period'])[['sum_so2']]
 .sum()
 .stack()
 .unstack([0, 1])
 .assign(
         difference_no_tcz=lambda x: x.iloc[:, 0] - x.iloc[:, 1],
         difference_tcz=lambda x: x.iloc[:, 2] - x.iloc[:, 3],
             )
 .rename(index={'sum_so2': 'Full sample'})
),
    (df_pol_tcz
     .assign(sum_so2 = lambda x: x['sum_so2']/1000000000)
 #.replace({'TCZ': {'0': 'No TCZ', '1':'TCZ'}})
 .loc[lambda x: x['year'].isin(['2004', '2005', '2006', '2007'])]
 .groupby(['soe_city', 'Period', 'Lower_location'])[['sum_so2']]
 .sum()
 .stack()
 .unstack([0, 1])
 .assign(
         difference_no_tcz=lambda x: x.iloc[:, 0] - x.iloc[:, 1],
         difference_tcz=lambda x: x.iloc[:, 2] - x.iloc[:, 3],
             )
 .reset_index(level=1, drop=True)
)], axis = 0)
```

```python
pd.concat([tcz, soe], axis = 1)
```

```python
import sys, os, shutil
sys.path.insert(0,'..')
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2

jupyter_preview = False
title = "Summary statistics by city characteristics"

pd.concat([tcz, soe], axis = 1).to_latex(
    'table_1.tex',
    caption = title,
    index=True,
    label = "table_3",
    #header = header,
    float_format="{:,.3f}".format)

table_nte = """
Sources: Author's own computation \n
The list of TCZ is provided by the State Council, 1998. \n
Output $\text { Share SOE }_{i}$ refers to the ratio of output
(respectively capital, employment) of SOEs over the total production
(capital, employment) in city $i$
      
"""
lb.beautify_table(table_nte = False,
                  name = 'table_1',
                  jupyter_preview  = jupyter_preview,
                  resolution = 200)

if jupyter_preview == False:
    source_to_move = ['table_1.tex']
    dest = ['Overleaf_statistic/13_table_stat_panel_b.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i])
```

<!-- #region kernel="Python 3" -->
# Create report
<!-- #endregion -->

```python kernel="Python 3"
import os, time, shutil
from pathlib import Path

export = 'pdf' #'html'

filename = '11_SBC_tables_sum_stat'
source = filename + '.ipynb'
source_to_move = filename +'.{}'.format(export)
path = os.getcwd()
parent_path = str(Path(path).parent)
path_report = "{}/Reports".format(parent_path)
dest = os.path.join(path_report, filename)+'_{}_.{}'.format(
    aggregation_param, export
)

os.system('jupyter nbconvert --no-input --to {} {}'.format(export, source))

time.sleep(5)
shutil.move(source_to_move, dest)
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass
```

```python
np.exp(0.413 * .118874) #- 
```

```python
np.exp(0.413 * .118874)
```
