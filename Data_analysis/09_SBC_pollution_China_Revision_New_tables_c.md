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
## Tableau 8 A and B 

Estimate the following models using different subsamples:

### Model A 

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { TCZ }_{i} \times \text { Polluting sectors }_{k} \right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { TCZ }_{i} \times \text { Polluting sectors }_{k} \times \text{ Share X}_i \right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

### Model B

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k}\right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
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
df_share_foreign = (df_share_foreign
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
    print(df_share_foreign[i].value_counts().sort_index())
```

<!-- #region kernel="SoS" -->
#### SOE

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city, ownership (SOE/Private): `Share_X_co`
- Step 2: Compute dummy when share SOE above share Private by city
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
df_share_soe = (df_share_soe
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
    print(df_share_soe[i].value_counts().sort_index())
```

<!-- #region kernel="SoS" -->
### Add to table
<!-- #endregion -->

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = df_final.merge(df_herfhindal,
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
df_final_SOE = (df_final.merge(
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
df_final_FOREIGN = (df_final.merge(
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
### Test Size
<!-- #endregion -->

```sos kernel="R"
#### Output
l <- list()
l1 <- list()
for (i in seq(3, 9)){
    
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c < i),
             exactDOF=TRUE)
    
    t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c < i),
             exactDOF=TRUE)
    
    l[[i - 2]] <- t1
    l1[[i-2]] <- t2
}

#### Capital
l2 <- list()
for (i in seq(3, 9)){
    
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c < i),
             exactDOF=TRUE)

    l2[[i - 2]] <- t1
}

#### Employment
l3 <- list()
for (i in seq(3, 9)){
    
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal_c < i),
             exactDOF=TRUE)
    
    l3[[i - 2]] <- t1
}

file.remove("table_1.txt")
file.remove("table_1.tex")
file.remove("table_2.txt")
file.remove("table_2.tex")
file.remove("table_3.txt")
file.remove("table_3.tex")
file.remove("table_4.txt")
file.remove("table_4.tex")

fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
             c("Year fixed effects","Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles output: Size',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_1.txt"
)

table_1 <- go_latex(l1,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles output: Size',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)

table_1 <- go_latex(l2,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles Capital: Size',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_3.txt"
)
table_1 <- go_latex(l3,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles Employement: Size',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_4.txt"
)
```

```sos kernel="Python 3"
import os
decile=['& decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 
       'decile .8','decile .9']

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

```sos kernel="Python 3"
lb.beautify(table_number = 4,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           jupyter_preview = True, 
           resolution = 200)
```

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

file.remove("table_5.txt")
file.remove("table_5.tex")
file.remove("table_6.txt")
file.remove("table_6.tex")
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
    name="table_5.txt"
)
table_1 <- go_latex(lb,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Panel B: SOE',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_6.txt"
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
lb.beautify(table_number = 5,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True, 
           resolution = 200)
```

```sos kernel="Python 3"
lb.beautify(table_number = 6,
            remove_control= True,
            constraint = False,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            jupyter_preview = True, 
            resolution = 200)
```