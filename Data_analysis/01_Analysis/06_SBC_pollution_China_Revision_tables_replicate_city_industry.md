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
# Tables city Industry level

All images are in this [folder](https://drive.google.com/open?id=1QDxWkftCPejrqJ7pH7j7vUhA3bHp4NqH)

## tables objective

* table 3: Baseline Regression
    * Replicate table 3 paper with FE at 3 more columns with city/industry/year 
* table 3 APPENDIX
    * Replicate table 3 with threshold
      * .6-.9 knowing.7 is the baseline 
* table 5:
    * Soft budget constraint as reflected in the SOEs' reaction to the SPZs' and coastal area's policies in China
      * Replicate table 5 paper with FE at 3 more columns with city/industry/year 
* table 6
    * Robustness check: Environmental policy,Wealth and Population pressure
      * Replicate table 6 paper with FE at 3 more columns with city/industry/year 
* table 7
    * Robustness check: Foreign share
      * Replicate table 3 using foreign share instead of SOE share and add 3 more columns with city/industry/year 
* table 7 bis:
    * Robustness check: Foreign share & SOE share
      * Replicate table 3 using foreign share and share soe and add 3 more columns with city/industry/year 
* table 8:
    * Robustness check: Competition effect
      * Add hefhindal index at the citry industry for control
* table 9: 
    * Firm size
      * Compute decile Herfhindal by city industry
      * Replicate table 3 by subsampling decile 1 , then decile 1 + 2 and so on
        * Show no endogeneity of large firm on the policy



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

<!-- #region kernel="SoS" -->
## Add city-industry variable 
<!-- #endregion -->

```sos kernel="SoS"
query = """
WITH sum_cio AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' WHEN ownership = 'SOE' 
    THEN 'SOE' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_io, 
    SUM(fa_net / 10000000) as fa_net_io, 
    SUM(employment / 100000) as employment_io,
    cic, geocode4_corr 
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
    cic,
    geocode4_corr
  ORDER BY geocode4_corr, cic, OWNERSHIP
) 
SELECT 
  * 
FROM 
  (
    WITH sum_ci AS(
      SELECT 
        SUM(output_io) as output_i, 
        SUM(fa_net_io) as fa_net_i, 
        SUM(employment_io) as employment_i, 
        cic AS cic_b,
        geocode4_corr as geocode4_corr_b
      FROM 
        sum_cio 
      GROUP BY 
        geocode4_corr, cic
    )
SELECT 
      * 
    FROM 
      (
        WITH share_cio AS(
          SELECT 
          geocode4_corr,
          cic as industry,
            OWNERSHIP, 
            output_io / output_i AS out_share_SOE, 
            fa_net_io / fa_net_i AS cap_share_SOE, 
            employment_io / employment_i AS lab_share_SOE, 
             
            
          FROM 
            sum_cio 
            LEFT JOIN 
            sum_ci ON sum_cio.geocode4_corr = sum_ci.geocode4_corr_b AND
            sum_cio.cic = sum_ci.cic_b 
        )
SELECT * FROM share_cio 
WHERE OWNERSHIP = 'SOE'
ORDER BY geocode4_corr, industry, OWNERSHIP
)
)
"""
df_share = gcp.upload_data_from_bigquery(query = query,
                                         location = 'US')
```

```sos kernel="SoS"
%put df_final_ci --to R
df_final_ci = (df_final.drop(columns = ['out_share_SOE','cap_share_SOE',
                                        'lab_share_SOE'])
              .merge(
    df_share,
    how = 'left',
    on = ['geocode4_corr', 'industry']
)
              .assign(
                  out_share_SOE = lambda x: x['out_share_SOE'].fillna(0),
    cap_share_SOE = lambda x: x['cap_share_SOE'].fillna(0),
    lab_share_SOE = lambda x: x['lab_share_SOE'].fillna(0)
)
             )
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

df_final <- df_final_ci %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below')
  )
head(df_final)
```

<!-- #region kernel="SoS" -->
## Table 03: All variables: Our new baseline

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/01_baseline_revision

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1i31VAW3PQE_s4EsRHWK21cos2lDPeFAY)
<!-- #endregion -->

<!-- #region kernel="R" -->
### Codes
<!-- #endregion -->

```sos kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
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
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Year fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Baseline regression',
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
            remove_control = False,
    constraint = True,
    city_industry = False, 
    new_row = decile,
    table_nte =tb,
           test_city_industry = True)
```

<!-- #region kernel="python3" -->
## APPENDIX test different treshold

Replicate table three with the following threshold:


- decile 6
- decile 7: baseline
- decile 8
- decile 9

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/09_decile_6
    - Temp_tables_revision/04_city_industry/10_decile_7
    - Temp_tables_revision/04_city_industry/11_decile_8
    - Temp_tables_revision/04_city_industry/12_decile_9

In Google Drive:

**decile 6**

![](https://drive.google.com/uc?export=view&id=1LNlZoNXdn4SciBrvCVv9Ub_0pv0VQ4yq)

**decile 7: baseline**

![](https://drive.google.com/uc?export=view&id=1UN8VN-CSm3dAyxUsa9XudEKM5g2J9RRN)

**decile 8**

![](https://drive.google.com/uc?export=view&id=1RYnTCsAJKWCp0IrYkGxcJ2Ht0hRLv3-O)

**decile 9**

![](https://drive.google.com/uc?export=view&id=1L-tFzsEamVbzQA2Cj54iAr4iZmRY4FR_)
<!-- #endregion -->

```sos kernel="SoS"
%put df_final_1 --to R
df_final_1 = df_final_ci.copy()
df_final_1['decile_so2_i'] = pd.qcut(df_final_1['tso2_i'], 10, labels=False)

df_final_1 = df_final_1.assign(
    decile_so2_6 = lambda x: np.where(x['tso2_i'] < 59695.8,
                                     'Below', 'Above'),
    decile_so2_7 = lambda x: np.where(x['tso2_i'] < 68070.78,
                                     'Below', 'Above'),
    decile_so2_8 = lambda x: np.where(x['tso2_i'] < 77783.4,
                                     'Below', 'Above'),
    decile_so2_9 = lambda x: np.where(x['tso2_i'] < 437425.19,
                                     'Below', 'Above')
)
```

```sos kernel="R"
df_final_1 <- df_final_1 %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         effort_c = relevel(effort_c, ref='Below'),
         polluted_di = relevel(polluted_di, ref='Below'),
         polluted_mi = relevel(polluted_mi, ref='Below'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
        decile_so2_6 = relevel(decile_so2_6, ref='Below'),
        decile_so2_7 = relevel(decile_so2_7, ref='Below'),
        decile_so2_8 = relevel(decile_so2_8, ref='Below'),
        decile_so2_9 = relevel(decile_so2_9, ref='Below')
  )
head(df_final_1)
```

<!-- #region kernel="R" -->
### Decile 6
<!-- #endregion -->

```sos kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_6 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_6 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_6 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_6 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_6 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_6 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_9.txt")
except:
    pass
try:
    os.remove("table_9.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Year fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Decile 6',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_9.txt"
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

try:
    os.remove("table_9.tex")
except:
    pass


lb.beautify(table_number = 9,
            remove_control = False,
    constraint = True,
    city_industry = False, 
    new_row = decile,
    table_nte =tb,
test_city_industry = True)
```

<!-- #region kernel="python3" -->
### Decile 7: Baseline
<!-- #endregion -->

```sos kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_7 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_7 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_7 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_7 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_7 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_7 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_10.txt")
except:
    pass
try:
    os.remove("table_10.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Year fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Decile 7',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_10.txt"
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

try:
    os.remove("table_10.tex")
except:
    pass


lb.beautify(table_number = 10,
            remove_control = False,
    constraint = True,
    city_industry = False, 
    new_row = decile,
    table_nte =tb,
test_city_industry = True)
```

<!-- #region kernel="python3" -->
### Decile 8
<!-- #endregion -->

```sos kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_8 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_8 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_8 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_8 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_8 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_8 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_11.txt")
except:
    pass
try:
    os.remove("table_11.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Year fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Decile 8',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_11.txt"
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

try:
    os.remove("table_11.tex")
except:
    pass


lb.beautify(table_number = 11,
            remove_control = False,
    constraint = True,
    city_industry = False, 
    new_row = decile,
    table_nte =tb,
test_city_industry = True)
```

<!-- #region kernel="python3" -->
### Decile 9
<!-- #endregion -->

```sos kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_9 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_9 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_9 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_9 * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_9 * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *decile_so2_9 * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final_1,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_12.txt")
except:
    pass
try:
    os.remove("table_12.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Year fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Decile 9',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_12.txt"
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

try:
    os.remove("table_12.tex")
except:
    pass


lb.beautify(table_number = 12,
            remove_control = False,
    constraint = True,
    city_industry = False, 
    new_row = decile,
    table_nte =tb,
test_city_industry = True)
```

<!-- #region kernel="python3" -->
## Table 05: Robustness check: Soft budget constraint as re ected in the SOEs' reaction to the SPZs' and coastal area's policies in China

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/02_table_5_rob_1

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1mdxml_aPhGnujWrT7aX574lcV19tmtoh)

Note, we download the file `df_TCZ_list_china` from Google spreadsheet because SOS kernel has trouble loading the json file to connect to the remote.
<!-- #endregion -->

```sos kernel="python3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
import pandas as pd
```

```sos kernel="python3"
gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])
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
	 to_dataframe = True).to_csv('df_TCZ_list_china.csv', index = False)
```

<!-- #region kernel="python3" -->
### Codes
<!-- #endregion -->

```sos kernel="R"
df_TCZ_list_china = read_csv('df_TCZ_list_china.csv') %>% 
select(-c(TCZ, Province)) %>% 
left_join(df_final)
```

```sos kernel="R"
### Low FE
t0 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period *polluted_thre * out_share_SOE
          + SPZ * Period * polluted_thre * out_share_SOE
          + Coastal * Period * polluted_thre * out_share_SOE
          + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
           + SPZ * Period * polluted_thre * cap_share_SOE
           + Coastal * Period * polluted_thre * cap_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
           + SPZ * Period * polluted_thre * lab_share_SOE
           + Coastal * Period * polluted_thre * lab_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)
### High FE
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
           + SPZ * Period * polluted_thre * out_share_SOE
           + Coastal * Period * polluted_thre * out_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
            FE_t_c + FE_t_i + FE_c_i| 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
           + SPZ * Period * polluted_thre * cap_share_SOE
           + Coastal * Period * polluted_thre * cap_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
           + SPZ * Period * polluted_thre * lab_share_SOE
           + Coastal * Period * polluted_thre * lab_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
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
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Soft budget constraint as reflected in the SOE s reaction to the SPZ s and coastal area's policies in China ",
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
            table_nte =tb,
           test_city_industry = True)

try:
    os.remove("df_TCZ_list_china.csv")
except:
    pass
```

<!-- #region kernel="python3" -->
## Table 06: Robustness check: Environmental policy,Wealth and Population pressure 

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/03_table_6_rob_2

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1bFSPlreNmmdmHhNnbtAhckkir6MSatC-)

Note, we download the file `df_TCZ_list_china` from Google spreadsheet because SOS kernel has trouble loading the json file to connect to the remote.
<!-- #endregion -->

<!-- #region kernel="python3" -->
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

<!-- #region kernel="python3" -->
### Codes
<!-- #endregion -->

```sos kernel="R"
df_chinese_city_characteristics = read_csv('df_chinese_city_characteristics.csv') %>% 
select(-cityen) %>%
left_join(df_final, by = c('year', 'geocode4_corr'))
```

```sos kernel="R"
### Low FE
t0 <- felm(formula=log(tso2_cit) ~ 
           TCZ_c * Period *polluted_thre * out_share_SOE
          + polluted_thre * log(gdp_cap)
          + polluted_thre * log(population)
          + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
           + polluted_thre * log(gdp_cap)
           + polluted_thre * log(population)
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
           + polluted_thre * log(gdp_cap)
           + polluted_thre * log(population)
           + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)
### High FE
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
           + polluted_thre * log(gdp_cap)
           + polluted_thre * log(population)
           + output_fcit + capital_fcit + labour_fcit
                  |
            FE_t_c + FE_t_i + FE_c_i| 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
           + polluted_thre * log(gdp_cap)
           + polluted_thre * log(population)
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
           + polluted_thre * log(gdp_cap)
           + polluted_thre * log(population)
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_chinese_city_characteristics,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
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
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Environmental policy,Wealth and Population pressure ",
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
            table_nte =tb,
            test_city_industry = True
           )

try:
    os.remove("df_chinese_city_characteristics.csv")
except:
    pass
```

<!-- #region kernel="python3" -->
## Table 07: Robustness check: Foreign share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/04_table_7_rob_3

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1WbmKaM9OUu3U-TWCM01wVJLbZz2K0-U1)

<!-- #endregion -->

<!-- #region kernel="python3" -->
### Code load data
<!-- #endregion -->

```sos kernel="SoS"
query_share = """WITH sum_io AS (
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
  ORDER BY cic, OWNERSHIP
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
            cic as industry 
          FROM 
            sum_io 
            LEFT JOIN sum_i ON sum_io.cic = sum_i.cic_b
        )
SELECT * FROM share_io ORDER BY industry, OWNERSHIP
)
)"""
df_share = gcp.upload_data_from_bigquery(query = query_share,
                                         location = 'US')

df_share = (df_share
            .set_index(['industry','OWNERSHIP'])
            .unstack(level = 1)
            .droplevel(level = 1, axis = 1)
            .fillna(0)
           )

df_share.columns  = ['out_share_dom','out_share_for', 'out_share_SOE_',
                     'share_fa_net_io','cap_share_for', 'cap_share_SOE_' ,
                     'share_employement_io', 'lab_share_for','lab_share_SOE_' 
                    ]
df_share.head()
```

```sos kernel="SoS"
%put df_final_i --to R
df_final_i = (df_final_ci.merge(
    df_share.reset_index()[
        ['industry',
         'out_share_for', 'out_share_SOE_',
         'cap_share_for', 'cap_share_SOE_' ,
         'lab_share_for','lab_share_SOE_' 
        ]],
    how = 'left',
    indicator = True
)
             )
```

```sos kernel="R"
df_final <- df_final_i %>% 
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

```sos kernel="R"

t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
            cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_4.txt")
except:
    pass
try:
    os.remove("table_4.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Presence of Foreign firms",
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_4.txt"
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
lb.beautify(table_number = 4,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           test_city_industry = True)
```

<!-- #region kernel="python3" -->
## Table 07 BIS: Robustness check: Foreign share & SOE share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/04bis_table_7_rob_3

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1UmRn_aSnU8-8lZp4-8R0y1OYxpy-lI9X)
<!-- #endregion -->

<!-- #region kernel="python3" -->
### Code
<!-- #endregion -->

```sos kernel="R"

t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for
          + TCZ_c * Period * polluted_thre * out_share_SOE_
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
           +TCZ_c * Period * polluted_thre * cap_share_SOE_	
                  + output_fcit + capital_fcit + labour_fcit
                  |
            cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for
           + TCZ_c * Period * polluted_thre * lab_share_SOE_
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for
           +TCZ_c * Period * polluted_thre * out_share_SOE_
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for
           +TCZ_c * Period * polluted_thre * cap_share_SOE_
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for
           +TCZ_c * Period * polluted_thre * lab_share_SOE_
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_4.txt")
except:
    pass
try:
    os.remove("table_4.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Presence of Foreign firms",
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_4.txt"
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
try:
    os.remove("table_4.tex")
except:
    pass
lb.beautify(table_number = 4,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
test_city_industry = True
)
```

<!-- #region kernel="python3" -->
## Table 08: Robustness check: Competition effect

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/05_table_8_rob_4

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1eMdEZGXGOs2UQMXPVA3rcFsI-irV407l)
<!-- #endregion -->

<!-- #region kernel="python3" -->
### Code load data

We use all years so that we still have value for pair city-industry when year > 2005
<!-- #endregion -->

```sos kernel="SoS"
query = """WITH data AS (
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
                    geocode4_corr, 
                    AVG(Herfindahl) as Herfindahl 
                  FROM 
                    agg_1 
                  WHERE Herfindahl IS NOT NULL
                  GROUP BY 
                    cic, 
                    geocode4_corr
                ) 
                SELECT 
                  cic as industry, 
                  geocode4_corr, 
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
df_herfhindal.head()
```

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_ind = (df_herfhindal
                     .groupby('industry')['Herfindahl']
                     .mean()
                     .reset_index())
df_herfhindal_final = df_final_ci.merge(df_herfhindal_ind,
                                     on=['industry'],
                                     how='left',
                                     indicator=True
                                     )
```

```sos kernel="R"
df_final <- df_herfhindal_final %>% 
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

```sos kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile=['& Output','Capital', 'Labour',
        'Output','Capital', 'Labour'
       ]
try:
    os.remove("table_5.txt")
except:
    pass
try:
    os.remove("table_5.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0,
    t1,
    t2,
    t3,
    t4,
    t5
),
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title="Concentration of industry",
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_5.txt"
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
lb.beautify(table_number = 5,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
            test_city_industry = True
           )
```

<!-- #region kernel="python3" -->
## Table 9: Firm size

It might be the case that large firms can influence local authorities concerning the effective enforcement of environmental regulation. If possible, I suggest to identify

- in each city (i) and for each industry (k), an index of industrial concentration (or the share of large firms in the industry). 
    - Then, a solution would be to estimate the model on a sub-sample of city-industry characterized by a low industrial concentration. 
    - A comparison of the results between the total sample and the subsample would allow checking the magnitude of the endogeneity bias. 

* https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_Index

A low industrial concentration is indicated by low Herfhindal value. The Herfindahl Index (H) ranges from 1/N to one, where N is the number of firms in the market. Equivalently, if percents are used as whole numbers, as in 75 instead of 0.75, the index can range up to 1002, or 10,000.

- An H below 0.01 (or 100) indicates a highly competitive industry.
- An H below 0.15 (or 1,500) indicates an unconcentrated industry.
- An H between 0.15 to 0.25 (or 1,500 to 2,500) indicates moderate concentration.
- An H above 0.25 (above 2,500) indicates high concentration.

So the strategy here is to estimate the model on cumulative subsample by city-sector concentration. For instance, decile 1, indicates the bottom 10% sectors with the lowest concentration

### Table 09: Size effect: Cumulated decile

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - Temp_tables_revision/04_city_industry/06_table_9_size_output
    - Temp_tables_revision/04_city_industry/07_table_9_size_capital
    - Temp_tables_revision/04_city_industry/08_table_9_size_employement

In Google Drive:

**Output**
![](https://drive.google.com/uc?export=view&id=1rNUQoXMdXsrrbxE5pzoYV4UYIXlGfTQ8)

**Capital**
![](https://drive.google.com/uc?export=view&id=1kOBIcEFgKs3AM2wrgxi4suttTNSAq6El)


**Employement**
![](https://drive.google.com/uc?export=view&id=1K3wx1VUyF8T_FdywjFl3yVO9lfbcpFNC)
<!-- #endregion -->

<!-- #region kernel="python3" -->
### Load data
<!-- #endregion -->

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = df_final_ci.merge(df_herfhindal,
                                     on=['geocode4_corr','industry'],
                                     how='left',
                                     indicator=True
                                     )
```

```sos kernel="R"
df_final <- df_herfhindal_final %>% 
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
#### Output
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 11) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre *out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(decile_herfhindal <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 
       'decile .8','decile .9', ' Baseline']
try:
    os.remove("table_6.txt")
except:
    pass
try:
    os.remove("table_6.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes'),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes'),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes')
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles output',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_6.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank of the city-industry concentration (Herfhindal index) \\
More specifically, the low deciles means a low concentration by city-industry \\
Deciles close to one, however, implies a stronger concentration.
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 6,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           test_city_industry = True)
```

<!-- #region kernel="python3" -->
#### Capital
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 11) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre *cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(decile_herfhindal <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 
       'decile .8','decile .9', ' Baseline']
try:
    os.remove("table_7.txt")
except:
    pass
try:
    os.remove("table_7.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes'),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes'),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes')
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles Capital',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_7.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank of the city-industry concentration (Herfhindal index) \\
More specifically, the low deciles means a low concentration by city-industry \\
Deciles close to one, however, implies a stronger concentration.
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 7,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           test_city_industry = True)
```

<!-- #region kernel="python3" -->
#### Labour
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 11) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre *lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(decile_herfhindal <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 
       'decile .8','decile .9', ' Baseline']
try:
    os.remove("table_8.txt")
except:
    pass
try:
    os.remove("table_8.tex")
except:
    pass
```

```sos kernel="R"
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes'),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes'),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes', "Yes", "Yes", 'Yes', 'Yes')
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles Employement',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_8.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank of the city-industry concentration (Herfhindal index) \\
More specifically, the low deciles means a low concentration by city-industry \\
Deciles close to one, however, implies a stronger concentration.
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
lb.beautify(table_number = 8,
            remove_control= True,
            constraint = True,
            city_industry = False, 
            new_row = decile,
            table_nte =tb,
           test_city_industry = True)
```
