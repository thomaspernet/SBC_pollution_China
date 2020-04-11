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
# New Tables: Industry level

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
    
## Summary

### Size

| Industry                   | Size         |              |              |              |              |              |
|----------------------------|--------------|--------------|--------------|--------------|--------------|--------------|
|                            | Below Median | Below Median | Below Median | Above Median | Above Median | Above Median |
| TCZ * Period * Polluted    | -            |              | -            | -            |              | -            |
| Target * Period * Polluted |              | -***         | -***         |              | -*           | -            |

### Output

|                            | Below median |     |         |      |         |     | Above Median |     |         |      |         |      |
|----------------------------|--------------|-----|---------|------|---------|-----|--------------|-----|---------|------|---------|------|
|                            | Foreign      | SOE | Foreign | SOE  | Foreign | SOE | Foreign      | SOE | Foreign | SOE  | Foreign | SOE  |
| TCZ * Period * Polluted    | +            | -*  |         |      | +       | -   | -***         | -   |         |      | -***    | +    |
| Target * Period * Polluted |              |     | -***    | -*** | -***    | -*  |              |     | -       | -*** | -       | -*** |

### Capital

|                            | Below median |      |         |     |         |      | Above Median |     |         |      |         |      |
|----------------------------|--------------|------|---------|-----|---------|------|--------------|-----|---------|------|---------|------|
|                            | Foreign      | SOE  | Foreign | SOE | Foreign | SOE  | Foreign      | SOE | Foreign | SOE  | Foreign | SOE  |
| TCZ * Period * Polluted    | -            | -*** |         |     | +       | -*** | -***         | +   |         |      | -***    | **   |
| Target * Period * Polluted |              |      | -***    | -*  | -***    | -    |              |     | -       | -*** | -       | -*** |


### employment

|                            | Below median |      |         |     |         |     | Above Median |     |         |      |         |      |
|----------------------------|--------------|------|---------|-----|---------|-----|--------------|-----|---------|------|---------|------|
|                            | Foreign      | SOE  | Foreign | SOE | Foreign | SOE | Foreign      | SOE | Foreign | SOE  | Foreign | SOE  |
| TCZ * Period * Polluted    | -            | -*** |         |     | +       | -** | -*           | +*  |         |      | -       | +*** |
| Target * Period * Polluted |              |      | -***    | -   | -***    | -   |              |     | -       | -*** | -       | -*** |
<!-- #endregion -->

```sos kernel="SoS"
import pandas as pd
from Fast_connectCloud import connector
import numpy as np
```

```sos kernel="Python 3"
import sys
sys.path.insert(0,'..')
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

<!-- #region kernel="SoS" -->
Get the industries available in our dataset, so that we match the firm level table
<!-- #endregion -->

```sos kernel="SoS"
list_industry = df_final['industry'].to_list()
```

```sos kernel="R"
options(warn=-1)
library(tidyverse)
library(lfe)
library(lazyeval)
library('progress')

path = "../functions/SBC_pollution_R.R"
source(path)
path = "../functions/SBC_pollutiuon_golatex.R"
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
## Tableau 8 A and B 

Estimate the following models using different subsamples:

### Model A 

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { TCZ }_{i} \times \text { Polluting sectors }_{k} \right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { TCZ }_{i} \times \text { Polluting sectors }_{k} \times \text{ Share X}_i \right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
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

<!-- #region kernel="python3" -->
### Compute Herfhindal: proxy Size

$$
H=\sum_{i=1}^{N} s_{i}^{2}
$$

where $s_i$ is the market share of industry $i$ in a city, and $N$ is the number of firms. 

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city-industry: `market_share_cit`
- Step 2: compute the sum of squared market share by industry: `Herfindahl_it`
- Step 3: Compute the average across time: `Herfindahl_i`
- Step 4: Compute the deciles of step 3: `decile_herfhindal_i`
    - Low decile implies a low concentration within sectors
    - High decile implies a high concentration within sectors
<!-- #endregion -->

```sos kernel="SoS"
query = """
WITH sum_cit AS (
  SELECT geocode4_corr, cic, sum(output) as sum_o_cit, year
  FROM China.asif_firm_china 
  WHERE year >= 2002 AND year <= 2007
  AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
  GROUP BY geocode4_corr, cic, year
) 
SELECT * 
FROM 
  (WITH sum_it AS (
    SELECT cic, SUM(sum_o_cit) as sum_o_it, year
    FROM sum_cit
    WHERE year >= 2002 AND year <= 2007
    GROUP BY year, cic
)
SELECT *
FROM
  (WITH ms_cit AS (
    SELECT  sum_cit.cic, sum_cit.geocode4_corr, sum_cit.year,
    sum_cit.sum_o_cit/NULLIF(sum_it.sum_o_it, 0) as market_share_cit
    FROM sum_cit
    LEFT JOIN sum_it
ON (
sum_cit.year = sum_it.year AND 
sum_cit.cic = sum_it.cic
)
)
SELECT *
FROM
  (WITH agg_1 AS (
SELECT cic, SUM(POW(market_share_cit, 2)) as Herfindahl_it,
year
FROM ms_cit
GROUP BY year, cic
ORDER BY year, cic 
)
SELECT *
FROM (
SELECT cic as industry,
AVG(Herfindahl_it) as Herfindahl_i
FROM agg_1
GROUP BY cic
ORDER BY cic
)

)))
"""
df_herfhindal = (gcp.upload_data_from_bigquery(query = query,
                                         location = 'US')
                 .loc[lambda x: x['industry'].isin(list_industry)]
                )
df_herfhindal.shape
```

<!-- #region kernel="SoS" -->
### Compute Ownership: proxy Foreign/SOE

$$\sum output_{io}/ \sum output_i$$

- with $i$ stands for industry
- $o$ stands for ownership (Foreign vs Domestic or SOE vs private)


<!-- #endregion -->

<!-- #region kernel="SoS" -->
#### Foreign vs domestic

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry, ownership (Foreign/Domestic): `Share_X_io`
- Step 2: Compute dummy when share Foreign above share domestic by industry
- Step 3: Compute decile by industry-ownership
    - Note,  high decile in Foreign means the industry has relatively high share of foreign output, but not in absolule value as in step 2. A decile 9 in foreign can be a decile 2 or 3 in Domestic
<!-- #endregion -->

```sos kernel="SoS"
query_share_foreign = """ 
WITH sum_io AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_io, 
    SUM(fa_net / 10000000) as fa_net_io, 
    SUM(employment / 100000) as employment_io,
    cic
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
    cic
) 
SELECT 
  * 
FROM 
  (
    WITH sum_i AS(
      SELECT 
        SUM(output_io) as output_i, 
        SUM(fa_net_io) as fa_net_i, 
        SUM(employment_io) as employment_i, 
        cic AS cic_b
      FROM 
        sum_io 
      GROUP BY 
        cic
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_io AS(
          SELECT 
            OWNERSHIP, 
            output_io / output_i AS share_output_io, 
            fa_net_io / fa_net_i AS share_fa_net_io, 
            employment_io / employment_i AS share_employement_io, 
            cic
          FROM 
            sum_io 
            LEFT JOIN sum_i ON sum_io.cic = sum_i.cic_b 
        ) 
        SELECT 
        cic as industry,
        OWNERSHIP,  
        share_output_io,
        share_fa_net_io,
        share_employement_io
        FROM share_io
        WHERE OWNERSHIP = 'FOREIGN'
        )
        )
"""
df_share_foreign = (gcp.upload_data_from_bigquery(query = query_share_foreign,
                                         location = 'US')
                    .loc[lambda x: x['industry'].isin(list_industry)]
                   )
df_share_foreign.shape
#df_share_foreign['rank_share_output_i'].value_counts().sort_index()
```

```sos kernel="SoS"
#df_share_foreign_ = (df_share_foreign
# .set_index(['industry', 'OWNERSHIP'])
# .drop(columns = ['rank_share_output_i',
#                  'rank_share_capital_i',
#                  'rank_share_employement_i'])
# .unstack(-1)
# .fillna(0)
# .assign(
# output = lambda x: np.where(
#     x.iloc[:,1] > x.iloc[:,0],
#     'Above', 'Below'
# ),
#     capital = lambda x: np.where(
#     x.iloc[:,3] > x.iloc[:,0],
#     'Above', 'Below'
# ),
#     employment = lambda x: np.where(
#     x.iloc[:,5] > x.iloc[:,0],
#     'Above', 'Below'
# )
# )
# .iloc[:, -3:]
# .droplevel(level = 1, axis = 1)
# .reset_index()
#)
#for i in ['output','capital', 'employment']:
#    print(df_share_foreign_[i].value_counts().sort_index())
```

```sos kernel="SoS"
#df_share_foreign =  (df_share_foreign
# .set_index(['industry','OWNERSHIP'])
# .drop(columns = ['share_output_io',
#                  'share_fa_net_io',
#                  'share_employement_io'])
# .xs('FOREIGN', level='OWNERSHIP', axis=0)
# .reset_index()
# .merge(df_share_foreign_)
#)
```

<!-- #region kernel="SoS" -->
#### SOE

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry, ownership (SOE/Private): `Share_X_io`
- Step 2: Compute dummy when share SOE above share Private by industry
- Step 3: Compute decile by industry-ownership
    - Note,  high decile in SOE means the industry has relatively high share of SOE output, but not in absolule value as in step 2. A decile 9 in SOE can be a decile 2 or 3 in Private
<!-- #endregion -->

```sos kernel="SoS"
query_share_soe = """ 
WITH sum_io AS (
  SELECT 
    case WHEN ownership = 'SOE' THEN 'SOE' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_io, 
    SUM(fa_net / 10000000) as fa_net_io, 
    SUM(employment / 100000) as employment_io,
    cic
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
    cic
) 
SELECT 
  * 
FROM 
  (
    WITH sum_i AS(
      SELECT 
        SUM(output_io) as output_i, 
        SUM(fa_net_io) as fa_net_i, 
        SUM(employment_io) as employment_i, 
        cic AS cic_b
      FROM 
        sum_io 
      GROUP BY 
        cic
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_io AS(
          SELECT 
            OWNERSHIP, 
            output_io / output_i AS share_output_io, 
            fa_net_io / fa_net_i AS share_fa_net_io, 
            employment_io / employment_i AS share_employement_io, 
            cic
          FROM 
            sum_io 
            LEFT JOIN sum_i ON sum_io.cic = sum_i.cic_b 
        ) 
        SELECT 
        * 
        FROM(
        SELECT 
        cic as industry,
        OWNERSHIP,  
          share_output_io,
          share_fa_net_io,
          share_employement_io
        FROM share_io
        WHERE OWNERSHIP = 'SOE'
        )
        )
        )
"""
df_share_soe = (gcp.upload_data_from_bigquery(query = query_share_soe,
                                         location = 'US')
                .loc[lambda x: x['industry'].isin(list_industry)]
                   )
df_share_soe.shape
#df_share_soe['rank_share_output_i'].value_counts().sort_index()
```

```sos kernel="SoS"
#df_share_soe_ = (df_share_soe
# .set_index(['industry', 'OWNERSHIP'])
# .drop(columns = ['rank_share_output_i',
#                  'rank_share_capital_i',
#                  'rank_share_employement_i'])
# .unstack(-1)
# .fillna(0)
# .assign(
# output = lambda x: np.where(
#     x.iloc[:,1] > x.iloc[:,0],
#     'Above', 'Below'
# ),
#     capital = lambda x: np.where(
#     x.iloc[:,3] > x.iloc[:,0],
#     'Above', 'Below'
# ),
#     employment = lambda x: np.where(
#     x.iloc[:,5] > x.iloc[:,0],
#     'Above', 'Below'
# )
# )
# .iloc[:, -3:]
# .droplevel(level = 1, axis = 1)
# .reset_index()
#)

#for i in ['output','capital', 'employment']:
#    print(df_share_soe_[i].value_counts().sort_index())
```

```sos kernel="SoS"
#df_share_soe = (df_share_soe
# .set_index(['industry','OWNERSHIP'])
# .drop(columns = ['share_output_io',
#                  'share_fa_net_io',
#                  'share_employement_io'])
# .xs('SOE', level='OWNERSHIP', axis=0)
# .reset_index()
# .merge(df_share_soe_)
 #.loc[lambda x: x.index.get_level_values('OWNERSHIP').isin(['FOREIGN'])]
#)
#df_share_soe.head()
```

<!-- #region kernel="SoS" -->
### Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="python3"
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
df_TCZ_list_china = read_csv('../df_TCZ_list_china.csv') %>% 
select(-c(TCZ, Province)) %>% 
left_join(df_final)
```

<!-- #region kernel="SoS" -->
### Add to table
<!-- #endregion -->

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = (df_final.merge(df_herfhindal,
                                     on=['industry'],
                                     how='left',
                                     indicator=True
                                     )
                       .assign(
                       decile_herfhindal_i = lambda x:
                           pd.qcut(x['Herfindahl_i'],10, labels=False)
                       )
                      )
```

```sos kernel="SoS"
print('Median: {}'.format(df_herfhindal_final['Herfindahl_i'].median()))
print(pd.qcut(df_herfhindal_final['Herfindahl_i'],
        10).drop_duplicates().sort_values().reset_index(drop = True))

df_herfhindal_final['decile_herfhindal_i'].value_counts().sort_index()
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
df_share_soe.columns
```

```sos kernel="SoS"
%put df_final_SOE --to R
df_final_SOE = (df_final.merge(
    df_share_soe,
    on = ['industry'],
    how = 'left',
    indicator = True
)
                .assign(
                       output = lambda x:
                           pd.qcut(x['share_output_io'],10, labels=False),
                       capital = lambda x:
                           pd.qcut(x['share_fa_net_io'],10, labels=False),
                       employment = lambda x:
                           pd.qcut(x['share_employement_io'],10, labels=False),
                       )

)
for i in ['output', 'capital', 'employment']:
    if i == 'output':
        v = 'share_output_io'
    elif i =='capital':
        v = 'share_fa_net_io'
    else:
        v = 'share_employement_io'
    print('Median: {}'.format(df_final_SOE[v].median()))
    print(pd.qcut(df_final_SOE[v],
        10).drop_duplicates().sort_values().reset_index(drop = True))

    print(df_final_SOE[i].value_counts().sort_index())
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
df_final_FOREIGN = (df_final.merge(
    df_share_foreign,
    on = ['industry'],
    how = 'left',
    indicator = True
)
                .assign(
                       output = lambda x:
                           pd.qcut(x['share_output_io'],10, labels=False),
                       capital = lambda x:
                           pd.qcut(x['share_fa_net_io'],10, labels=False),
                       employment = lambda x:
                           pd.qcut(x['share_employement_io'],10, labels=False),
                       )

)
for i in ['output', 'capital', 'employment']:
    if i == 'output':
        v = 'share_output_io'
    elif i =='capital':
        v = 'share_fa_net_io'
    else:
        v = 'share_employement_io'
    print('Median: {}'.format(df_final_FOREIGN[v].median()))
    print(pd.qcut(df_final_FOREIGN[v],
        10).drop_duplicates().sort_values().reset_index(drop = True))

    print(df_final_FOREIGN[i].value_counts().sort_index())
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

<!-- #region kernel="R" -->
### Decile
<!-- #endregion -->

<!-- #region kernel="python3" -->
#### Size
<!-- #endregion -->

```sos kernel="R"
change_target <- function(table){
    check_target <- grep("PeriodAfter:polluted_threAbove:target_c$", rownames(table$coef))
    
    if (length(check_target) !=0) {
    rownames(table$coefficients)[check_target] <- 'target_c:PeriodAfter:polluted_threAbove'
    rownames(table$beta)[check_target] <- 'target_c:PeriodAfter:polluted_threAbove'
}
    return (table)
}
```

```sos kernel="R"
cat <- 'Size'
df_to_filter <- df_herfhindal_r

### inferior median
t1 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(decile_herfhindal_i <= 5),
             exactDOF=TRUE)
t1 <-change_target(t1)
t2 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(decile_herfhindal_i <= 5),
             exactDOF=TRUE)
t2 <-change_target(t2)

t3 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(decile_herfhindal_i <= 5),
             exactDOF=TRUE)
t3 <-change_target(t3)

### superior median
t4 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(decile_herfhindal_i > 5),
             exactDOF=TRUE)
t4 <-change_target(t4)

t5 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(decile_herfhindal_i > 5),
             exactDOF=TRUE)
t5 <-change_target(t5)

t6 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(decile_herfhindal_i > 5),
             exactDOF=TRUE)
t6 <-change_target(t6)

tables <- list(t1, t2, t3,t4, t5, t6)

fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
            )


table_1 <- go_latex(tables,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median Herfhindal - ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_1.txt"
                            )
```

```sos kernel="Python 3"
import os
decile=['& below median (inc.)', 'below median (inc.)', 'below median (inc.)',
        'above median (exc.)', 'above median (exc.)', 'above median (exc.)']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 1,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

<!-- #region kernel="python3" -->
#### Foreign

<!-- #endregion -->

```sos kernel="R"
cat <- 'Foreign'
df_to_filter <- df_final_FOREIGN

fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

### Remove text, tex and pdf files
toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)

for (var in list('output', 'capital', 'employment')){
    
    ### inferior median
    t1 <- felm(formula=log(tso2_cit) ~ 
               TCZ_c * Period * polluted_thre 
               + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= 5),
             exactDOF=TRUE)
    t1 <-change_target(t1)
    t2 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
               + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= 5),
             exactDOF=TRUE)
    t2 <-change_target(t2)
    t3 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= 5),
             exactDOF=TRUE)
    t3 <-change_target(t3)

    ### superior median
    t4 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) > 5),
             exactDOF=TRUE)
    t4 <-change_target(t4)
    t5 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) > 5),
             exactDOF=TRUE)
    t5 <-change_target(t5)

    t6 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) > 5),
             exactDOF=TRUE)
    t6 <-change_target(t6)
    
    if (var == 'output'){
        tables_o <- list(t1, t2, t3,t4, t5, t6)
        table_1 <- go_latex(tables_o,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median ", var, "- ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_1.txt"
                           )
    }else if ( var == 'capital'){
        tables_c <- list(t1, t2, t3,t4, t5, t6)
        table_1 <- go_latex(tables_c,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median ", var, "- ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_2.txt"
                            )
    }else{
        tables_e <- list(t1, t2, t3,t4, t5, t6)
        table_1 <- go_latex(tables_e,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median ", var, "- ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_3.txt"
                            )
    }
}
```

```sos kernel="Python 3"
import os
decile=['& below median (inc.)', 'below median (inc.)', 'below median (inc.)',
        'above median (exc.)', 'above median (exc.)', 'above median (exc.)']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 1,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

```sos kernel="Python 3"
lb.beautify(table_number = 2,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True,
            resolution = 200)
```

```sos kernel="Python 3"
lb.beautify(table_number = 3,
            remove_control= True,
            constraint = False,
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
cat <- 'SOE'
df_to_filter <- df_final_SOE

fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

### Remove text, tex and pdf files
toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)

for (var in list('output', 'capital', 'employment')){
    
    ### inferior median
    t1 <- felm(formula=log(tso2_cit) ~ 
               TCZ_c * Period * polluted_thre 
               + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= 5),
             exactDOF=TRUE)
    t1 <-change_target(t1)
    t2 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
               + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= 5),
             exactDOF=TRUE)
    t2 <-change_target(t2)
    t3 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= 5),
             exactDOF=TRUE)
    t3 <-change_target(t3)

    ### superior median
    t4 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) > 5),
             exactDOF=TRUE)
    t4 <-change_target(t4)
    t5 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) > 5),
             exactDOF=TRUE)
    t5 <-change_target(t5)

    t6 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(get(var) > 5),
             exactDOF=TRUE)
    t6 <-change_target(t6)
    
    if (var == 'output'){
        tables_o <- list(t1, t2, t3,t4, t5, t6)
        table_1 <- go_latex(tables_o,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median ", var, "- ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_1.txt"
                           )
    }else if ( var == 'capital'){
        tables_c <- list(t1, t2, t3,t4, t5, t6)
        table_1 <- go_latex(tables_c,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median ", var, "- ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_2.txt"
                            )
    }else{
        tables_e <- list(t1, t2, t3,t4, t5, t6)
        table_1 <- go_latex(tables_e,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Median ", var, "- ", cat),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_3.txt"
                            )
    }
}
```

```sos kernel="Python 3"
import os
decile=['& below median (inc.)', 'below median (inc.)', 'below median (inc.)',
        'above median (exc.)', 'above median (exc.)', 'above median (exc.)']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 1,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

```sos kernel="Python 3"
import os
decile=['& below median (inc.)', 'below median (inc.)', 'below median (inc.)',
        'above median (exc.)', 'above median (exc.)', 'above median (exc.)']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 2,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

```sos kernel="Python 3"
import os
decile=['& below median (inc.)', 'below median (inc.)', 'below median (inc.)',
        'above median (exc.)', 'above median (exc.)', 'above median (exc.)']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 3,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

<!-- #region kernel="Python 3" -->
## SPZ/Coastal
<!-- #endregion -->

```sos kernel="R"
df_to_filter <- df_TCZ_list_china
### SPZ

### Remove text, tex and pdf files
toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)

fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

for (var in range(1,2)){
    
    if (var == 1){
        filter_spz = 1
        filter_coast = TRUE
        filter_tcz = 'TCZ'
        
    }else if ( var == 2){
        
        filter_spz = 0
        filter_coast = FALSE
        filter_tcz = 'No_TCZ'
    }


    t1 <- felm(formula=log(tso2_cit) ~ 
               TCZ_c * Period * polluted_thre 
               + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(SPZ == filter_spz),
             exactDOF=TRUE)
    t1 <-change_target(t1)
    t2 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
               + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(SPZ == filter_spz),
             exactDOF=TRUE)
    t2 <-change_target(t2)

    t3 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(SPZ == filter_spz),
             exactDOF=TRUE)
    t3 <-change_target(t3)

    ### Coastal
    t4 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(Coastal == filter_coast),
             exactDOF=TRUE)
    t4 <-change_target(t4)

    t5 <- felm(formula=log(tso2_cit) ~ 
           target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(Coastal == filter_coast),
             exactDOF=TRUE)
    t5 <-change_target(t5)

    t6 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period * polluted_thre 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_to_filter %>% filter(Coastal == filter_coast),
             exactDOF=TRUE)
    t6 <-change_target(t6)

    t7 <- felm(formula=log(tso2_cit) ~ 
           + target_c  * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final %>% filter(TCZ_c == filter_tcz),
             exactDOF=TRUE)
    t7 <-change_target(t7)
    
     if (var == 1){
        tables_1 <- list(t1, t2, t3,t4, t5, t6, t7)
        table_1 <- go_latex(tables_1,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title="SPZ/Coastal/TCZ True",
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_1.txt"
                            )
        
    }else if (var == 2){
        
        tables_2 <- list(t1, t2, t3,t4, t5, t6, t7)
        table_1 <- go_latex(tables_2,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title="SPZ/Coastal/TCZ False",
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_2.txt"
                            )
    }
    
}
```

```sos kernel="Python 3"
import os
decile=['& SPZ', 'SPZ', 'SPZ',
        'Coastal', 'Coastal', 'Coastal', 'TCZ']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 1,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

```sos kernel="Python 3"
import os
decile=['& SPZ', 'SPZ', 'SPZ',
        'Coastal', 'Coastal', 'Coastal']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 2,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True,
           resolution = 200)
```

<!-- #region kernel="Python 3" -->
# Create Report
<!-- #endregion -->

```sos kernel="Python 3"
import os, time, shutil
from pathlib import Path

filename = '08_SBC_pollution_China_Revision_New_tables_i'
source = filename + '.ipynb'
source_to_move = filename + '.html'
path = os.getcwd()
parent_path = str(Path(path).parent)
path_report = "{}/Reports".format(parent_path)
dest = os.path.join(path_report, filename)+'.html'

os.system('jupyter nbconvert --no-input --to html {}'.format(source))
shutil.move(source_to_move, dest)

time.sleep(5)
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass
```
