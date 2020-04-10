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
# New Tables: city level

* Faire les tableaux suivants:
  * Tableau 4: Kuznet: benchmark → Revision
      * Trouver un tableau avec les déciles pour montrer:
        * turning point croissant pour des villes avec une dominance étatique de plus en plus large
      * Regarder si gdp/cap prix constant
      * Indiquer les turning points dans les tableaux
* Partie 6:
  * Tableau 8: 
    * estimer 2 modèles sur des échantillons differents
      * modèle 1 →  TCZ * Polluted * Period
      * modèle 2 → Target * polluted*Period  
    * Echantillonnage → prendre soit industry soit city industry
      * Big
        * Via Herfhindal 
          * benchmark →Revision
      * Foreign 
        * via output/capital/employment 
      * SOEs
        * via output/capital/employment 
      * SPZ
      * Coastal
    * Chaque tableau avec Panel A pour supérieur threshold, Panel B pour inférieur threshold
  * Tableau 9:
    * Enlever SPZ & Coastal
    * estimer 2 modèles sur des échantillons differents
      * modèle 1 →  TCZ * Polluted * Period
      * modèle 2 → Target * polluted*Period  
    * Idem tableau 8
<!-- #endregion -->

```sos kernel="SoS"
import pandas as pd
from Fast_connectCloud import connector
import numpy as np
```

```sos kernel="Python 3"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos kernel="SoS"
gs = connector.open_connection(online_connection = False,
                              path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth')

service = gs.connect_remote('GCP')
```

```sos kernel="SoS"
%put df_final --to R

from GoogleDrivePy.google_platform import connect_cloud_platform
project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service['GoogleCloudP'])    
query = (
          "SELECT * "
            "FROM China.SBC_pollution_China "

        )

df_final = gcp.upload_data_from_bigquery(query = query, location = 'US')
df_final.head()
```

```sos kernel="R"
options(warn=-1)
library(tidyverse)
library(lfe)
library(lazyeval)
library('progress')

path = "functions/SBC_pollution_R.R"
source(path)
path = "functions/SBC_pollutiuon_golatex.R"
source(path)
```

```sos kernel="R"
df_final <- df_final %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
head(df_final)
```

<!-- #region kernel="python3" -->
# Partie 6
<!-- #endregion -->

<!-- #region kernel="python3" -->
## Tableau 9 A and B 

Estimate the following models using different subsamples:

### Model A 

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k} \right)+ Kuznet +\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k} \times \text{ Share X}_i \right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

* Size
    * Via Herfhindal 
        * benchmark →Revision
* Foreign 
    * via output/capital/employment 
* SOEs
    * via output/capital/employment 
* SPZ
* Coastal
<!-- #endregion -->

<!-- #region kernel="python3" -->
## Load Data
<!-- #endregion -->

<!-- #region kernel="R" -->
### Load chinese_city_characteristics from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="Python 3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
import pandas as pd
import numpy as np

gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])
```

```sos kernel="Python 3"
# Please go here https://docs.google.com/spreadsheets/d/1-x9DCX4cun6Ed9iH5MiI4g21fXm7seRHHz7WXGiVKVU
# To change the range

#sheetid = "1-x9DCX4cun6Ed9iH5MiI4g21fXm7seRHHz7WXGiVKVU"
#sheetname = "chinese_city_characteristics"

#df_chinese_city_characteristics = (gdr.upload_data_from_spreadsheet(
#    sheetID=sheetid, sheetName=sheetname, to_dataframe=True
#).loc[
#    lambda x: x["year"].isin(
#        ["2001", "2002", "2003", "2004", "2005", "2006"])
#][
#    ["cityen", "geocode4_corr", "year", "gdp", "population"]
#].rename(columns={'year': 'year_lagged'})
# .apply(pd.to_numeric, errors='ignore')
# .assign(year=lambda x:
#            x['year_lagged'] + 1,
#            gdp_cap=lambda x: x['gdp'] / x['population'],
#            ln_gdp_cap= lambda x:np.log(x['gdp_cap']),
#            ln_gdp_cap_sqred = lambda x: x['ln_gdp_cap'] * x['ln_gdp_cap'],
#            ln_pop = lambda x: np.log(x['population'])
#            )
#  .drop(columns= 'cityen')
#                                   .to_csv(
#    'df_chinese_city_characteristics.csv', index = False)
#                                  )
```

```sos kernel="SoS"
df_chinese_city_characteristics = df_final.merge(
    pd.read_csv('df_chinese_city_characteristics.csv'),
    on = ['year','geocode4_corr']
)
df_chinese_city_characteristics.shape
```

<!-- #region kernel="SoS" -->
### Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range

#sheetid = '15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q'
#sheetname = 'All_cities'

#df_TCZ_list_china = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
#sheetName = sheetname,
#	 to_dataframe = True)
#df_TCZ_list_china.to_csv('df_TCZ_list_china.csv', index = False)
```

```sos kernel="R"
#df_chinese_city_characteristics = read_csv('df_chinese_city_characteristics.csv') %>% 
#select(-cityen) %>%
#left_join(df_final, by = c('year', 'geocode4_corr')) %>%
#mutate(
#    ln_gdp_cap= log(gdp_cap),
#    ln_gdp_cap_sqred = ln_gdp_cap * ln_gdp_cap,
#    ln_pop = log(population)
#)
```

<!-- #region kernel="python3" -->
### Compute Herfhindal: proxy Size

$$
H=\sum_{i=1}^{N} s_{i}^{2}
$$

where $s_i$ is the market share of city $i$ in the industry, and $N$ is the number of firms. 

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city-industry: `market_share_cit`
- Step 2: compute the sum of squared market share by city: `Herfindahl_ct`
- Step 3: Compute the average across time: `Herfindahl_c`
- Step 4: Compute the deciles of step 3: `decile_herfhindal_c`
    - Low decile implies a low concentration within sectors
    - High decile implies a high concentration within sectors
<!-- #endregion -->

```sos kernel="SoS"
query = """
WITH sum_cit AS (
  SELECT geocode4_corr, cic, sum(output) as sum_o_cit, year
  FROM China.asif_firm_china 
  WHERE year >= 2002 AND year <= 2007
  GROUP BY geocode4_corr, cic, year
) 
SELECT * 
FROM 
  (WITH sum_ct AS (
    SELECT geocode4_corr, SUM(sum_o_cit) as sum_o_ct, year
    FROM sum_cit
    WHERE year >= 2002 AND year <= 2007
    GROUP BY year, geocode4_corr
)
SELECT *
FROM
  (WITH ms_cit AS (
    SELECT  sum_cit.cic, sum_cit.geocode4_corr, sum_cit.year,
    sum_cit.sum_o_cit/NULLIF(sum_ct.sum_o_ct, 0) as market_share_cit
    FROM sum_cit
    LEFT JOIN sum_ct
ON (
sum_cit.year = sum_ct.year AND 
sum_cit.geocode4_corr = sum_ct.geocode4_corr
)
)
SELECT *
FROM
  (WITH agg_1 AS (
SELECT geocode4_corr, SUM(POW(market_share_cit, 2)) as Herfindahl_ct,
year
FROM ms_cit
GROUP BY year, geocode4_corr
ORDER BY year, geocode4_corr 
)
SELECT *
FROM (
WITH avg_H_c AS (
SELECT geocode4_corr, AVG(Herfindahl_ct) as Herfindahl_c
FROM agg_1
GROUP BY geocode4_corr
)
SELECT geocode4_corr, Herfindahl_c ,
NTILE(10)  OVER (ORDER BY Herfindahl_c) as
decile_herfhindal_c
FROM avg_H_c
ORDER BY decile_herfhindal_c
))))
"""
df_herfhindal = gcp.upload_data_from_bigquery(query = query,
                                         location = 'US')
df_herfhindal['decile_herfhindal_c'].value_counts().sort_index()
```

<!-- #region kernel="SoS" -->
### Compute Ownership: proxy Foreign/SOE

$$\sum output_{co}/ \sum output_c$$

- with $c$ stands for city
- $o$ stands for ownership (Foreign vs Domestic or SOE vs private)


<!-- #endregion -->

<!-- #region kernel="SoS" -->
#### Foreign vs domestic

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city, ownership (Foreign/Domestic): `Share_X_co`
- Step 2: Compute dummy when share Foreign above share domestic by city
- Step 3: Compute decile by city-ownership
    - Note,  high decile in Foreign means the city has relatively high share of foreign output, but not in absolule value as in step 2. A decile 9 in foreign can be a decile 2 or 3 in Domestic

<!-- #endregion -->

```sos kernel="SoS"
query_share_foreign = """ 
WITH sum_co AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_co, 
    SUM(fa_net / 10000000) as fa_net_co, 
    SUM(employment / 100000) as employment_co,
    geocode4_corr
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
    geocode4_corr
) 
SELECT 
  * 
FROM 
  (
    WITH sum_c AS(
      SELECT 
        SUM(output_co) as output_c, 
        SUM(fa_net_co) as fa_net_c, 
        SUM(employment_co) as employment_c, 
        geocode4_corr AS geocode4_corr_b
      FROM 
        sum_co 
      GROUP BY 
        geocode4_corr
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_co AS(
          SELECT 
            OWNERSHIP, 
            output_co / output_c AS share_output_co, 
            fa_net_co / fa_net_c AS share_fa_net_co, 
            employment_co / employment_c AS share_employement_co, 
            geocode4_corr
          FROM 
            sum_co 
            LEFT JOIN sum_c ON sum_co.geocode4_corr = sum_c.geocode4_corr_b 
        ) 
        SELECT 
        * 
        FROM(
        WITH decile_c AS (
        SELECT 
        geocode4_corr,
        OWNERSHIP,  
        NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_output_co) 
          as rank_share_output_c,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_fa_net_co) 
          as rank_share_capital_c,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_employement_co) 
          as rank_share_employement_c,
          share_output_co,
          share_fa_net_co,
          share_employement_co
        FROM share_co
        )
        SELECT * 
        FROM decile_c 
        /*WHERE OWNERSHIP = 'FOREIGN'*/
        )
        )
        )
"""
df_share_foreign = gcp.upload_data_from_bigquery(query = query_share_foreign,
                                         location = 'US')
df_share_foreign['rank_share_output_c'].value_counts().sort_index()
```

```sos kernel="SoS"
df_share_foreign_ = (df_share_foreign
 .set_index(['geocode4_corr', 'OWNERSHIP'])
 .drop(columns = ['rank_share_output_c',
                  'rank_share_capital_c',
                  'rank_share_employement_c'])
 .unstack(-1)
 .fillna(0)
 .assign(
 output = lambda x: np.where(
     x.iloc[:,1] > x.iloc[:,0],
     'Above', 'Below'
 ),
     capital = lambda x: np.where(
     x.iloc[:,3] > x.iloc[:,0],
     'Above', 'Below'
 ),
     employment = lambda x: np.where(
     x.iloc[:,5] > x.iloc[:,0],
     'Above', 'Below'
 )
 )
 .iloc[:, -3:]
 .droplevel(level = 1, axis = 1)
 .reset_index()
)
for i in ['output','capital', 'employment']:
    print(df_share_foreign_[i].value_counts().sort_index())
```

```sos kernel="SoS"
df_share_foreign =  (df_share_foreign
 .set_index(['geocode4_corr','OWNERSHIP'])
 .drop(columns = ['share_output_co',
                  'share_fa_net_co',
                  'share_employement_co'])
 .xs('FOREIGN', level='OWNERSHIP', axis=0)
 .reset_index()
 .merge(df_share_foreign_)
)
```

<!-- #region kernel="SoS" -->
#### SOE

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city, ownership (SOE/Private): `Share_X_co`
- Step 2: Compute dummy when share SOE above share Private by city
- Step 3: Compute decile by city-ownership
    - Note,  high decile in SOE means the city has relatively high share of SOE output, but not in absolule value as in step 2. A decile 9 in SOE can be a decile 2 or 3 in Private
<!-- #endregion -->

```sos kernel="SoS"
query_share_soe = """ 
WITH sum_co AS (
  SELECT 
    case WHEN ownership = 'SOE' THEN 'SOE' ELSE 'PRIVATE' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_co, 
    SUM(fa_net / 10000000) as fa_net_co, 
    SUM(employment / 100000) as employment_co,
    geocode4_corr
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
    geocode4_corr
) 
SELECT 
  * 
FROM 
  (
    WITH sum_c AS(
      SELECT 
        SUM(output_co) as output_c, 
        SUM(fa_net_co) as fa_net_c, 
        SUM(employment_co) as employment_c, 
        geocode4_corr AS geocode4_corr_b
      FROM 
        sum_co 
      GROUP BY 
        geocode4_corr
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_co AS(
          SELECT 
            OWNERSHIP, 
            output_co / output_c AS share_output_co, 
            fa_net_co / fa_net_c AS share_fa_net_co, 
            employment_co / employment_c AS share_employement_co, 
            geocode4_corr
          FROM 
            sum_co 
            LEFT JOIN sum_c ON sum_co.geocode4_corr = sum_c.geocode4_corr_b 
        ) 
        SELECT 
        * 
        FROM(
        WITH decile_c AS (
        SELECT 
        geocode4_corr,
        OWNERSHIP,  
        NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_output_co) 
          as rank_share_output_c,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_fa_net_co) 
          as rank_share_capital_c,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_employement_co) 
          as rank_share_employement_c,
          share_output_co,
          share_fa_net_co,
          share_employement_co
        FROM share_co
        )
        SELECT * 
        FROM decile_c 
        /*WHERE OWNERSHIP = 'FOREIGN'*/
        )
        )
        )
"""
df_share_soe = gcp.upload_data_from_bigquery(query = query_share_soe,
                                         location = 'US')
df_share_soe['rank_share_output_c'].value_counts().sort_index()
```

```sos kernel="SoS"
df_share_soe_ = (df_share_soe
 .set_index(['geocode4_corr', 'OWNERSHIP'])
 .drop(columns = ['rank_share_output_c',
                  'rank_share_capital_c',
                  'rank_share_employement_c'])
 .unstack(-1)
 .fillna(0)
 .assign(
 output = lambda x: np.where(
     x.iloc[:,1] > x.iloc[:,0],
     'Above', 'Below'
 ),
     capital = lambda x: np.where(
     x.iloc[:,3] > x.iloc[:,0],
     'Above', 'Below'
 ),
     employment = lambda x: np.where(
     x.iloc[:,5] > x.iloc[:,0],
     'Above', 'Below'
 )
 )
 .iloc[:, -3:]
 .droplevel(level = 1, axis = 1)
 .reset_index()
)

for i in ['output','capital', 'employment']:
    print(df_share_soe_[i].value_counts().sort_index())
```

```sos kernel="SoS"
df_share_soe = (df_share_soe
 .set_index(['geocode4_corr','OWNERSHIP'])
 .drop(columns = ['share_output_co',
                  'share_fa_net_co',
                  'share_employement_co'])
 .xs('SOE', level='OWNERSHIP', axis=0)
 .reset_index()
 .merge(df_share_soe_)
 #.loc[lambda x: x.index.get_level_values('OWNERSHIP').isin(['FOREIGN'])]
)
df_share_soe.head()
```

<!-- #region kernel="SoS" -->
### Add to table
<!-- #endregion -->

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = df_chinese_city_characteristics.merge(df_herfhindal,
                                     on=['geocode4_corr'],
                                     how='left',
                                     indicator=True
                                     )
```

```sos kernel="R"
df_herfhindal_r <- df_herfhindal_final %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

```sos kernel="SoS"
%put df_final_SOE --to R
df_final_SOE = (df_chinese_city_characteristics.merge(
    df_share_soe,
    how = 'left',
    indicator = True
)
                #.assign(
                #    rank_share_output_ci= lambda x: 
                #    x['rank_share_output_i'].fillna(0),
                #    rank_share_capital_ci= lambda x: 
                #    x['rank_share_output_i'].fillna(0),
                #    rank_share_employement_ci= lambda x: 
                #    x['rank_share_output_i'].fillna(0),
                #)
)
for i in ['output', 'capital', 'employment']:
    print(df_final_SOE[i].value_counts())
```

```sos kernel="R"
df_final_SOE <- df_final_SOE %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

```sos kernel="SoS"
%put df_final_FOREIGN --to R
df_final_FOREIGN = (df_chinese_city_characteristics.merge(
    df_share_foreign,
    how = 'left',
    on = ['geocode4_corr'],
    indicator = True
)
                #.assign(
                #    rank_share_output_ci= lambda x: 
                #    x['rank_share_output_i'].fillna(0),
                #    rank_share_capital_ci= lambda x: 
                #    x['rank_share_output_i'].fillna(0),
                #    rank_share_employement_ci= lambda x: 
                #    x['rank_share_output_i'].fillna(0),
                #)

)
for i in ['output', 'capital', 'employment']:
    print(df_final_FOREIGN[i].value_counts())
```

```sos kernel="R"
df_final_FOREIGN <- df_final_FOREIGN %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

<!-- #region kernel="SoS" -->
## Table 8 Model A: Panel A


<!-- #endregion -->

<!-- #region kernel="python3" -->
### Size
<!-- #endregion -->

```sos kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c <= 5),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c <= 5),
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c <=5),
             exactDOF=TRUE)


t4 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c > 5),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c > 5),
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c > 5),
             exactDOF=TRUE)


l <- list(t1, t2, t3,t4, t5, t6)
turning = c()
turning_dol = c()
for (c in l){
   turning <- append(turning,
                     round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))]))),
                           0))
   turning_dol <- append(turning_dol,
                        round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))])))/8.07,
                           0))
}

file.remove("table_1.txt")
file.remove("table_1.tex")

fe1 <- list(
    c('turning point RMB', turning),
    c('turning point Dollar', turning_dol),
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Kuznet - Size',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_1.txt"
)
```

```sos kernel="Python 3"
import os
#decile=['& inf decile .3', ' inf decile .3', ' inf decile .3',
#        'sup decile .7', ' sup decile .7', ' sup decile .7']
decile=['& inf decile included .5', ' inf decile included .5', ' inf decile included .5',
        'sup .5', ' sup .5', ' sup .5']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 1,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True,
            resolution = 200)
```

<!-- #region kernel="Python 3" -->
#### Foreign
<!-- #endregion -->

```sos kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_c <= 5),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_c <= 5),
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_c <= 5),
             exactDOF=TRUE)


t4 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_c > 5),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_c > 5),
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_c > 5),
             exactDOF=TRUE)


l <- list(t1, t2, t3,t4, t5, t6)
turning = c()
turning_dol = c()
for (c in l){
   turning <- append(turning,
                     round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))]))),
                           0))
   turning_dol <- append(turning_dol,
                        round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))])))/8.07,
                           0))
}

file.remove("table_2.txt")
file.remove("table_2.tex")

fe1 <- list(
    c('turning point RMB', turning),
    c('turning point Dollar', turning_dol),
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Kuznet - Foreign',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="Python 3"
import os
#decile=['& inf decile .3', ' inf decile .3', ' inf decile .3',
#        'sup decile .7', ' sup decile .7', ' sup decile .7']
decile=['& inf decile included .5', ' inf decile included .5', ' inf decile included .5',
        'sup .5', ' sup .5', ' sup .5']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 2,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True,
            resolution = 200)
```

<!-- #region kernel="Python 3" -->
#### SOE
<!-- #endregion -->

```sos kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_c <= 5),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_c <= 5),
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_c <= 5),
             exactDOF=TRUE)


t4 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_c > 5),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_c > 5),
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_c > 5),
             exactDOF=TRUE)


l <- list(t1, t2, t3,t4, t5, t6)
turning = c()
turning_dol = c()
for (c in l){
   turning <- append(turning,
                     round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))]))),
                           0))
   turning_dol <- append(turning_dol,
                        round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))])))/8.07,
                           0))
}

file.remove("table_3.txt")
file.remove("table_3.tex")

fe1 <- list(
    c('turning point RMB', turning),
    c('turning point Dollar', turning_dol),
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Kuznet - SOE',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_3.txt"
)
```

```sos kernel="Python 3"
import os
#decile=['& inf decile .3', ' inf decile .3', ' inf decile .3',
#        'sup decile .7', ' sup decile .7', ' sup decile .7']
decile=['& inf decile included .5', ' inf decile included .5', ' inf decile included .5',
        'sup .5', ' sup .5', ' sup .5']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 3,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True,
            resolution = 200)
```

<!-- #region kernel="Python 3" -->
### SPZ/Coastal/TCZ
<!-- #endregion -->

```sos kernel="R"
%put df_chinese_city_characteristics --to R
df_TCZ_list_china = read_csv('df_TCZ_list_china.csv') %>% 
select(-c(TCZ, Province)) %>% 
left_join(df_chinese_city_characteristics) %>%
mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

```sos kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 1),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == TRUE),
             exactDOF=TRUE)
t3 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_TCZ_list_china %>% filter(TCZ_c == 'TCZ'),
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 0),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == FALSE),
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ 
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry  | 0 |
             industry, data= df_TCZ_list_china %>% filter(TCZ_c != 'TCZ'),
             exactDOF=TRUE)

l <- list(t1, t2, t3,t4, t5,t6)
turning = c()
turning_dol = c()
for (c in l){
   turning <- append(turning,
                     round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))]))),
                           0))
   turning_dol <- append(turning_dol,
                        round(exp(abs(coef(c)[grep("ln_gdp_cap$", names(coef(c)))] / 
                                   (2 * 
                                    coef(c)[grep("ln_gdp_cap_sqred$",
                                                  names(coef(c)))])))/8.07,
                           0))
}

file.remove("table_4.txt")
file.remove("table_4.tex")

fe1 <- list(
    c('turning point RMB', turning),
    c('turning point Dollar', turning_dol),
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Kuznet -SPZ/Coastal/TCZ',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_4.txt"
)
```

```sos kernel="Python 3"
import os
#decile=['& inf decile .3', ' inf decile .3', ' inf decile .3',
#        'sup decile .7', ' sup decile .7', ' sup decile .7']
decile=['& SPZ', ' Coastal', ' TCZ',
        'No SPZ', 'No Coastal', 'No TCZ']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 4,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True,
            resolution = 200)
```

```sos kernel="Python 3"
import os
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass
```

<!-- #region kernel="Python 3" -->
### Absolute
<!-- #endregion -->

<!-- #region kernel="python3" -->
#### Foreign: Not applicable

Not enough observation, or say differently, no sectors are dominated by Foreign firms solenly
<!-- #endregion -->

<!-- #region kernel="python3" -->
#### SOE

Reminder, in the table below, we include sectors solenly dominated by SOE -> Share output/cap/emp of SOE stricly superior with Private
<!-- #endregion -->

```sos kernel="R"
##### Panel A
## Output
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(output =='Above'),
             exactDOF=TRUE)
    
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(output =='Above'),
             exactDOF=TRUE)
## Capital
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(capital =='Above'),
             exactDOF=TRUE)
    
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(capital =='Above'),
             exactDOF=TRUE)

## Employment
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(employment =='Above'),
             exactDOF=TRUE)
    
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(employment =='Above'),
             exactDOF=TRUE)
la <- list(t1, t2, t3, t4, t5, t6)
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### 
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### 
##### Panel B
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(output =='Below'),
             exactDOF=TRUE)
    
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(output =='Below'),
             exactDOF=TRUE)
## Capital
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(capital =='Below'),
             exactDOF=TRUE)
    
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(capital =='Below'),
             exactDOF=TRUE)

## Employment
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(employment =='Below'),
             exactDOF=TRUE)
    
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(employment =='Below'),
             exactDOF=TRUE)
lb <- list(t1, t2, t3, t4, t5, t6)

file.remove("table_13.txt")
file.remove("table_13.tex")
file.remove("table_14.txt")
file.remove("table_14.tex")
fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
             c("Year fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(la,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Panel A: SOE',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_13.txt"
)
table_1 <- go_latex(lb,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Panel B: SOE',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_14.txt"
)
```

```sos kernel="Python 3"
import os
decile=['& Output','Output',
        'Capital', 'Capital',
       'Employment','Employment']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 13,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True, 
           resolution = 200)
```

```sos kernel="Python 3"
lb.beautify(table_number = 14,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True, 
            resolution = 200)
```
