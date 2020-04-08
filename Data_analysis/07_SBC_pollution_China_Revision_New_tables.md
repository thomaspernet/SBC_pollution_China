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
# New Tables

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

```sos kernel="python3"
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

<!-- #region kernel="R" -->
# Partie 3
<!-- #endregion -->

<!-- #region kernel="R" -->
## Tableau 4: Kuznet: benchmark 

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/06_new_tables/01_kuznet

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)

Note, we download the file `df_TCZ_list_china` from Google spreadsheet because SOS kernel has trouble loading the json file to connect to the remote.
<!-- #endregion -->

```sos kernel="python3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
import pandas as pd

gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])
```

<!-- #region kernel="R" -->
### Load chinese_city_characteristics from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="python3"
# Please go here https://docs.google.com/spreadsheets/d/1-x9DCX4cun6Ed9iH5MiI4g21fXm7seRHHz7WXGiVKVU
# To change the range

sheetid = "1-x9DCX4cun6Ed9iH5MiI4g21fXm7seRHHz7WXGiVKVU"
sheetname = "chinese_city_characteristics"

df_chinese_city_characteristics = (gdr.upload_data_from_spreadsheet(
    sheetID=sheetid, sheetName=sheetname, to_dataframe=True
).loc[
    lambda x: x["year"].isin(
        ["2001", "2002", "2003", "2004", "2005", "2006"])
][
    ["cityen", "geocode4_corr", "year", "gdp", "population"]
].rename(columns={'year': 'year_lagged'})
    .apply(pd.to_numeric, errors='ignore')
    .assign(year=lambda x:
            x['year_lagged'] + 1,
            gdp_cap=lambda x: x['gdp'] / x['population']
            )
).to_csv('df_chinese_city_characteristics.csv', index = False)
```

```sos kernel="R"
df_chinese_city_characteristics = read_csv('df_chinese_city_characteristics.csv') %>% 
select(-cityen) %>%
left_join(df_final, by = c('year', 'geocode4_corr')) %>%
mutate(
    ln_gdp_cap= log(gdp_cap),
    ln_gdp_cap_sqred = ln_gdp_cap * ln_gdp_cap,
    ln_pop = log(population)
)
```

```sos kernel="R"
### Low FE
t0 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period *polluted_thre * out_share_SOE
          + ln_gdp_cap
          + ln_gdp_cap_sqred
          + ln_pop
          + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
           + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
          + ln_gdp_cap
           + ln_gdp_cap_sqred
           + ln_pop
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour'#,
        #'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_1.txt")
except:
    pass
try:
    os.remove("table_1.tex")
except:
    pass
```

```sos kernel="R"
test <- list(t0, t1, t2)
turning = c()
turning_dol = c()
for (c in test){
   turning <- append(turning, round(exp(abs(c$beta[5] / (2 * c$beta[6]))), 0))
    turning_dol <- append(turning_dol, round(exp(abs(c$beta[5] / (2 * c$beta[6])))/8.07,0))
}

fe1 <- list(
    c('turning point RMB', turning),
    c('turning point Dollar', turning_dol),
    c("City fixed effects", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes"),
    c("Yes fixed effects","Yes", "Yes", "Yes", "No")
)

table_1 <- go_latex(
    test,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Kuznet Curve hypothesis",
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_1.txt"
)
```

```sos kernel="python3"
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
            table_nte =tb)

#try:
#    os.remove("df_TCZ_list_china.csv")
#except:
#    pass
```

<!-- #region kernel="python3" -->
# Partie 6
<!-- #endregion -->

<!-- #region kernel="python3" -->
## Tableau 8: 

Estimate the following models using different subsamples:

1. 

$$
Log SO2 emission $_{i k t}=\alpha\left(\text { Period } \times \text { TCZ }_{i} \times \text { Polluting sectors }_{k}\right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

2.

$$
Log SO2 emission $_{i k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k}\right)+\nu_{i k}+\lambda_{i t}+\phi_{k t}+\epsilon_{i k t}
$$

* Big
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
### Load data Herfhindal -Industry

- Average Herfhindal by Industry
- Compute the decile
<!-- #endregion -->

```sos kernel="SoS"
query = """
WITH data AS (
  SELECT 
    id, 
    geocode4_corr, 
    cic, 
    output, 
    year 
  FROM 
    China.asif_firm_china 
  WHERE 
    year >= 2002 
    AND year <= 2007
) 
SELECT 
  * 
FROM 
  (
    WITH sum_out AS (
      SELECT 
        geocode4_corr, 
        cic, 
        SUM(output) as sum_output, 
        year 
      FROM 
        China.asif_firm_china 
      WHERE 
        year >= 2002 
        AND year <= 2007
      GROUP BY 
        year, 
        geocode4_corr, 
        cic
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH agg AS (
          SELECT 
            data.id, 
            data.cic, 
            data.geocode4_corr, 
            data.year, 
            data.output / NULLIF(sum_out.sum_output, 0) as market_share 
          FROM 
            data 
            LEFT JOIN sum_out ON (
              data.year = sum_out.year 
              AND data.cic = sum_out.cic 
              AND data.geocode4_corr = sum_out.geocode4_corr
            )
        ) 
        SELECT 
          * 
        FROM 
          (
            WITH agg_1 AS (
              SELECT 
                cic, 
                geocode4_corr, 
                SUM(
                  POW(market_share, 2)
                ) as Herfindahl, 
                year 
              FROM 
                agg 
              GROUP BY 
                year, 
                cic, 
                geocode4_corr 
              ORDER BY 
                year, 
                geocode4_corr, 
                cic
            ) 
            SELECT 
              * 
            FROM 
              (
                WITH avg_H AS (
                  SELECT 
                    cic, 
                    AVG(Herfindahl) as Herfindahl 
                  FROM 
                    agg_1 
                  WHERE Herfindahl IS NOT NULL
                  GROUP BY 
                    cic
                ) 
                SELECT 
                  cic as industry, 
                  Herfindahl, 
                  NTILE(10) OVER (
                    ORDER BY 
                      Herfindahl
                  ) as decile_herfhindal 
                FROM 
                  avg_H
              )
          )
      )
  )
"""
df_herfhindal = gcp.upload_data_from_bigquery(query = query,
                                         location = 'US')
df_herfhindal['decile_herfhindal'].value_counts()
```

<!-- #region kernel="SoS" -->
### Level industry

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry, ownership: `Share_io`
- Step 2: Compute the deciles of step 1 by  ownership: `Share_io`

We only need when `ownership` is equal to `SOE`. First decile indicates a low share of SOE in these sectors. For instance, when the decile is 1, it means this is the bottom 10% of sectors with the lowest share of SOE. The larger the decile, the higher the state presences.

In a nutshell, we can run estimate in two ways:

- by decile 
- by cumulated decile
<!-- #endregion -->

```sos kernel="SoS"
query_share = """ WITH sum_io AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' WHEN ownership = 'SOE' 
    THEN 'SOE' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_io, 
    SUM(fa_net / 10000000) as fa_net_io, 
    SUM(employment / 100000) as employment_io,
    cic 
  FROM 
    China.asif_firm_china 
  WHERE 
    year >= 2002 
    AND year < 2006 
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
        NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_output_io) 
          as rank_share_output_io,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_fa_net_io) 
          as rank_share_capital_io,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_employement_io) 
          as rank_share_employement_io,
        share_output_io
        FROM share_io
 
        )
        )
        
"""
df_share = gcp.upload_data_from_bigquery(query = query_share,
                                         location = 'US')
df_share.head()
```

<!-- #region kernel="SoS" -->
### Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="python3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range

sheetid = '15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q'
sheetname = 'All_cities'

df_TCZ_list_china = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_TCZ_list_china.to_csv('df_TCZ_list_china.csv', index = False)
```

```sos kernel="R"
df_TCZ_list_china = read_csv('df_TCZ_list_china.csv') %>% 
select(-c(TCZ, Province)) %>% 
left_join(df_final)
```

<!-- #region kernel="SoS" -->
### Add to table
<!-- #endregion -->

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = df_final.merge(df_herfhindal,
                                     on=['industry'],
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
head(df_herfhindal_r)
```

```sos kernel="SoS"
%put df_final_SOE --to R
df_final_SOE = (df_final.merge(
    df_share.loc[lambda x: x['OWNERSHIP'].isin(['SOE'])][
        [
            'industry',
            'rank_share_output_io',
            'rank_share_capital_io',
            'rank_share_employement_io'
             ]],
    how = 'left',
    indicator = True
)
)
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
    df_share.loc[lambda x: x['OWNERSHIP'].isin(['FOREIGN'])][
        [
            'industry',
            'rank_share_output_io',
            'rank_share_capital_io',
            'rank_share_employement_io'
             ]],
    how = 'left',
    indicator = True
)
)
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
### Table 8: Panel A

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/06_new_tables/02_table_8_panel_A

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)

<!-- #endregion -->

<!-- #region kernel="SoS" -->
#### Codes
<!-- #endregion -->

```sos kernel="R"
### Big
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal > 5),
             exactDOF=TRUE)
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal > 5),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal > 5),
             exactDOF=TRUE)

### Foreign
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_io > 5),
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_capital_io > 5),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_employement_io > 5),
             exactDOF=TRUE)
### SOE
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_io > 5),
             exactDOF=TRUE)
t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_capital_io > 5),
             exactDOF=TRUE)
t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_employement_io > 5),
             exactDOF=TRUE)
### SPZ
t9 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 1),
             exactDOF=TRUE)
t10 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 1),
             exactDOF=TRUE)
t11 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 1),
             exactDOF=TRUE)

### Coastal
t12 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == TRUE),
             exactDOF=TRUE)
t13 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == TRUE),
             exactDOF=TRUE)
t14 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == TRUE),
             exactDOF=TRUE)
```

```sos kernel="R"
test <- list(t0, t1, t2, t3,t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour',
        'Output','Capital', 'Labour',
        'Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_2.txt")
except:
    pass
try:
    os.remove("table_2.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes"),
    c("Yes fixed effects","Yes", "Yes", "Yes", "No")
)

table_1 <- go_latex(
    test,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Kuznet Curve hypothesis",
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
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
            table_nte =tb)
```

<!-- #region kernel="python3" -->
### Table 8: Panel B

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/06_new_tables/02_table_8_panel_B

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)
<!-- #endregion -->

```sos kernel="R"
### Big
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal < 5),
             exactDOF=TRUE)
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal < 5),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_herfhindal_r %>% filter(decile_herfhindal < 5),
             exactDOF=TRUE)

### Foreign
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_output_io < 5),
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_capital_io < 5),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_FOREIGN %>% filter(rank_share_employement_io < 5),
             exactDOF=TRUE)
### SOE
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_output_io < 5),
             exactDOF=TRUE)
t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_capital_io < 5),
             exactDOF=TRUE)
t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final_SOE %>% filter(rank_share_employement_io < 5),
             exactDOF=TRUE)
### SPZ
t9 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 0),
             exactDOF=TRUE)
t10 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 0),
             exactDOF=TRUE)
t11 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(SPZ == 0),
             exactDOF=TRUE)

### Coastal
t12 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == FALSE),
             exactDOF=TRUE)
t13 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == FALSE),
             exactDOF=TRUE)
t14 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(Coastal == FALSE),
             exactDOF=TRUE)
```

```sos kernel="R"
test <- list(t0, t1, t2, t3,t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour',
        'Output','Capital', 'Labour',
        'Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_3.txt")
except:
    pass
try:
    os.remove("table_3.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(
    c("City fixed effects", "Yes", "Yes", "Yes"),
    c("Industry fixed effects", "Yes", "Yes", "Yes"),
    c("Yes fixed effects","Yes", "Yes", "Yes", "Yes")
)

table_1 <- go_latex(
    test,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Kuznet Curve hypothesis",
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_3.txt"
)
```

```sos kernel="python3"
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
            table_nte =tb)
```