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
    display_name: SoS
    language: sos
    name: sos
---

<!-- #region kernel="SoS" -->
# TEST TFP

## Objective

* Prepare data for TFP model
  * Compute TFP using OP or LP algorithm using ASIF panel data
* Steps:
  * Import data 2001-2007
  * Select cities and industries from the paper's table
  * Exclude outliers
  * Remove firm with different:
    *  ownership, cities and industries over time
  * Compute TFP using 2 ways:
    * full samples
    * Split by ownership
<!-- #endregion -->

```sos kernel="SoS"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
from GoogleDrivePy.google_platform import connect_cloud_platform
import pandas as pd 
import numpy as np
import pandas_profiling
```

```sos kernel="SoS"
gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

#service_gd = gs.connect_remote(engine = 'GS')
service_gcp = gs.connect_remote(engine = 'GCP')

#gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])

project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project,
											 service_account = service_gcp['GoogleCloudP'])
```

```sos kernel="Python 3"
query = """
SELECT year, geocode4_corr, cic as industry,
SUM(output / 10000000) as output_agg_o, 
SUM(fa_net / 10000000) as fa_net_agg_o, 
SUM(employment / 100000) as employment_agg_o,
SUM(input / 10000000) as input_agg_o,
  FROM China.asif_firm_china 
  WHERE year >= 2002 AND year <= 2007
  AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
    AND input > 0 
  GROUP BY year, geocode4_corr, cic
"""

df_asif_firm_china = gcp.upload_data_from_bigquery(query = query, location = 'US')
df_asif_firm_china.head()
```

```sos kernel="Python 3"
df_asif_firm_china.to_csv('test.csv', index = False)
```

<!-- #region kernel="Python 3" -->
Issue with `prodest` librairie, so I moved to EC2 to compute it
<!-- #endregion -->

```sos kernel="SoS"
query = (
          "SELECT * "
            "FROM China.SBC_pollution_China "

        )

df_temp = gcp.upload_data_from_bigquery(query = query, location = 'US')
df_temp.head()
```

```sos kernel="SoS"
OWNERSHIP = 'Foreign'
aggregation_param = 'geocode4_corr'
list_agg = df_temp[aggregation_param].to_list()

threshold_full = 6
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
if aggregation_param == 'industry':
    if OWNERSHIP == 'Foreign':
        counterpart = 'DOMESTIC'
    else:
        counterpart = 'PRIVATE'
    query_share_foreign= query_share_.format(aggregation_param,
                                             'cic',
                                             OWNERSHIP,
                                            counterpart)
else:
    if OWNERSHIP == 'Foreign':
        counterpart = 'DOMESTIC'
    else:
        counterpart = 'PRIVATE'
    query_share_foreign = query_share_.format(aggregation_param,
                                              aggregation_param,
                                              OWNERSHIP,
                                             counterpart)
        
OWNERSHIP = 'SOE'
if aggregation_param == 'industry':
    if OWNERSHIP == 'Foreign':
        counterpart = 'DOMESTIC'
    else:
        counterpart = 'PRIVATE'
    df_share_soe= query_share_.format(aggregation_param,
                                             'cic',
                                             OWNERSHIP,
                                            counterpart)
else:
    if OWNERSHIP == 'Foreign':
        counterpart = 'DOMESTIC'
    else:
        counterpart = 'PRIVATE'
    df_share_soe = query_share_.format(aggregation_param,
                                              aggregation_param,
                                              OWNERSHIP,
                                             counterpart)
    
df_share_soe = (gcp.upload_data_from_bigquery(query = df_share_soe,
                                         location = 'US')
                    .loc[lambda x: x[aggregation_param].isin(list_agg)]
                   )
```

```sos kernel="SoS"
#%put df_final_SOE --to R
#### If industry, we need to use out_share_SOE, cap_share_SOE,lab_share_SOE
##### Output share already computed in the paper's table for industry but not
##### for city, in the later case, we use the data from ASIF
if aggregation_param== 'industry':
    out = "out_share_SOE"
    cap = "cap_share_SOE"
    emp = "lab_share_SOE"
else:
    out = "share_output_agg_o"
    cap = "share_fa_net_agg_o"
    emp = "share_employement_agg_o"
    
df_final_SOE = (df_temp.merge(
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
                       )
                    )
    #.merge(
    #                       pd.read_csv('../df_chinese_city_characteristics.csv'),
    #                   on = ['year', 'geocode4_corr'],
    #                   how = 'left'
                       )
```

```sos kernel="SoS"
%put df_final_tfp --to R
df_final_tfp = (pd.read_csv('TFP_computed_ASIF_china.csv')[
    ['year','geocode4_corr', 'industry','tfp_OP']
]
 #.rename(columns= {'cic': 'industry'})
 .merge(df_final_SOE.drop(columns = 
                     ['FE_c_i', 'FE_t_i', 'FE_t_c']), 
                     on = ['year', 'geocode4_corr', 'industry'])
 .assign(
        year=lambda x: x['year'].astype('str'),
        industry=lambda x: x['industry'].astype('str')
 )
 #.groupby(['Period','year','Coastal','TCZ_c',"cityen", 'geocode4_corr',
 #          'polluted_thre','industry'])[['tfp', 'target_c']]
 #               .mean()
 #               .reset_index()
)

df_final_tfp["FE_c_i"] = pd.factorize(df_final_tfp["cityen"] +
                                      df_final_tfp['industry'])[0]

df_final_tfp["FE_t_i"] = pd.factorize(df_final_tfp["year"] +
                                      df_final_tfp['industry'])[0]

df_final_tfp["FE_t_c"] = pd.factorize(df_final_tfp["year"] + 
                                      df_final_tfp["cityen"])[0]

df_final_tfp.shape
```

```sos kernel="R"
library(tidyverse)
library(lfe)

df_final <- df_final_tfp %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         #effort_c = relevel(effort_c, ref='Below'),
         #polluted_di = relevel(polluted_di, ref='Below'),
         #polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
head(df_final)
```

```sos kernel="R"
summary(felm(formula= tfp_OP ~ 
          target_c * Period * polluted_thre
        #+ SPZ  * polluted_thre * Period
        #+ Coastal * polluted_thre* Period 
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output <6)
             ,
             exactDOF=TRUE))
```

```sos kernel="R"
summary(felm(formula= scale(tfp_OP) ~ 
          target_c * polluted_thre * Period 
        #+ SPZ  * polluted_thre * Period
        #+ Coastal * polluted_thre* Period 
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(TCZ_c != 'TCZ')
             ,
             exactDOF=TRUE))
```
