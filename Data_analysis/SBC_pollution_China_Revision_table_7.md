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
# SBC_pollution_China Revision Paper

Here is the link with all the revisions:

- https://coda.io/d/SoftBudgetConstraint_dD-uOwatzMS/Revision_suYyi#_luGfQ

- Notebook also available here in html format:
    - https://htmlpreview.github.io/?https://github.com/thomaspernet/SBC_pollution_China/blob/master/Data_analysis/SBC_pollution_China_Revision.html

## Revision table 

| Comments_by | URL      | People          | Comments                                                                                                                                                                                                                                                 |
|-------------|----------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Author 1    | Revision | Thomas,Mathilde | Je réfléchis à ce que nous pourrions faire ici, c'est en effet un point intéressant.                                                                                                                                                                     |
| Author 1    | Revision | Thomas          | Pouvez vous me rassurer sur ce point? Tos les termes d'interaction sont ils dans l'équation? Je me souviens que nous en avions parlé en effet. J'espère qu'il n'y a pas d'erreurs et que nous pouvons justifier. C'est discutable. Mais on peut essayer. |
| Author 1    | Revision | Mathilde        | Je ré-écrirai.                                                                                                                                                                                                                                           |
| Author 1    | Revision |                 | Avons nous ces informations? Si non peut on les trouver?                                                                                                                                                                                                 |
| Author 1    | Revision |                 | TCZ et Target sont indépendants n'est ce pas?                                                                                                                                                                                                            |
| Author 1    | Revision |                 |                                                                                                                                                                                                                                                          |
| Author 1    | Revision |                 | Il faut reformuler ici.                                                                                                                                                                                                                                  |
| Author 2    | Revision | Thomas          | Avons nous des entreprises étrangères dans l'échantillon?                                                                                                                                                                                                |
| Author 2    | Revision | Thomas          | Oui je suppose, pouvez vous regarder?                                                                                                                                                                                                                    |
| Author 2    | Revision | Thomas          | Pouvez vous faire ce test?                                                                                                                                                                                                                               |
| Author 2    | Revision | Thomas          | Pouvez vous corriger ce point?                                                                                                                                                                                                                           |
| Author 2    | Revision | Mathilde        | Très bon commentaire, je m'en occupe.                                                                                                                                                                                                                    |

## Proposal 

The proposal is available [here](https://drive.google.com/open?id=1tmSFvdUMXcL3vMKBSNYmf5xe6OEmYNnD)

### Equation to estimate

$$
\begin{aligned} \text { SO2 emission }_{i k t}=& \alpha T C Z_{i} \times \text { Polluted sectors }_{k} \times \text { post } \\ &+\beta T C Z_{i} \times \text { Polluted sectors }_{k} \times \text { post } \times \text { Share Foreign }_{k} \\ & +\theta {X}_{i k t}+\nu_{c i}+\lambda_{t i} +\phi_{t c} +\epsilon_{ikt} \end{aligned}
$$

city-industry; time-industry and time-city
<!-- #endregion -->

<!-- #region kernel="SoS" -->
# Table 7: improvement

Instead of reconstructed all the data, we compute the:

- share [output, capital, employment] by city, industry, ownership
- share  [output, capital, employment] by city, industry
- Average share  [output, capital, employment]  by city, ownership

from the table `asif_firm_china` -> the one used in the paper

and select the pairs city-industry dominated by the SOE.

* Sum up table 7 
  * Need to compute the [output, capital, employment] at the:
    * city,
    * industry
    * industry, city
  * Estimate table 7 with three ascending threshold (less and less private in panel B)
  * The coefficient should be larger in absolute value for more restrictive threshold
<!-- #endregion -->

<!-- #region kernel="SoS" -->
## Load the data
<!-- #endregion -->

```sos kernel="SoS"
import pandas as pd
from Fast_connectCloud import connector
import numpy as np

gs = connector.open_connection(online_connection = False,
                              path_credential = '/Users/thomas/Google Drive/Projects/Data_science/Google_code_n_Oauth/Client_Oauth/Google_auth/')
service = gs.connect_remote('GCP')
```

```sos kernel="python3"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
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

<!-- #region kernel="R" -->
# Foreign vs Public

1.  Pour montrer que le secteur privé doit compenser l'absence de réaction du secteur public, nous allons procéder de la manière suivante: 

Nous avons Identifié les secteurs où la part des entreprises publiques est inférieure à un seuil critique. Nous allons comparer la réponse du secteur privé dans ces secteurs. 

- Il s'agit du tableau 7, panel B: deux options (si possible les faire toutes les deux): 
  
    - on regarde les entreprises privées dans les villes-secteurs où la part étatique est plus faible, Elle devrait être plus vigoureuse. Deux estimations donc au lieu d'une seule. 
    - on change le seuil de dominance privé/public. Moins il y a de privé, plus la réaction de ce dernier doit être forte.
<!-- #endregion -->

<!-- #region kernel="R" -->
## Replicate table 7
<!-- #endregion -->

<!-- #region kernel="R" -->
### SOE

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 10_reproduce_Table_7_SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1rIRHIeIJVtA6V4cH_WcjgWRWI1ZIIn3i)
<!-- #endregion -->

```sos kernel="R"
t1<-SOE_dominate(df_final, 'out_share_SOE', TRUE, 'cityen', print_ = FALSE)
t2<-SOE_dominate(df_final, 'cap_share_SOE', TRUE, 'cityen', print_ = FALSE)
t3<-SOE_dominate(df_final, 'lab_share_SOE', TRUE, 'cityen', print_ = FALSE)

fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes")
             )
table_1 <- go_latex(list(
    t1,
    t2,
    t3
),
    title='SOE dominating sectors',
    addFE=fe1,
    save=TRUE,
    name="table_1.txt"
)
```

```sos kernel="python3"
import os
try:
    os.remove("table_1.tex")
except:
    pass
lb.beautify(table_number = 1, constraint = False, city_industry = False)
```

<!-- #region kernel="R" -->
### Private

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 10_reproduce_Table_7_SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1-exJrPengwvGeUbTky7NtOeLeedZaHey)
<!-- #endregion -->

```sos kernel="R"
t1<-SOE_dominate(df_final, 'out_share_SOE', FALSE, 'cityen', print_ = FALSE)
t2<-SOE_dominate(df_final, 'cap_share_SOE', FALSE, 'cityen', print_ = FALSE)
t3<-SOE_dominate(df_final, 'lab_share_SOE', FALSE, 'cityen', print_ = FALSE)

fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes")
             )
table_1 <- go_latex(list(
    t1,
    t2,
    t3
),
    title='Private dominating sectors',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos kernel="R"
import os
try:
    os.remove("table_2.tex")
except:
    pass
lb.beautify(table_number = 2, constraint = False, city_industry = False)
```

<!-- #region kernel="R" -->
## Level City-industry

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city, industry, ownership
- Step 2: Compute the average of step 1 by city, industry
- Step 3: if Step 1 > step 2, then Above

Three threshold:

- mean
- median
- decile .3
- decile .7
<!-- #endregion -->

<!-- #region kernel="R" -->
### code Load data
<!-- #endregion -->

```sos kernel="SoS"
query_share = """ WITH sum_cio AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' WHEN ownership = 'SOE' THEN 'SOE' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_cio, 
    SUM(fa_net / 10000000) as fa_net_cio, 
    SUM(employment / 100000) as employment_cio, 
    geocode4_corr, 
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
    geocode4_corr, 
    OWNERSHIP, 
    cic
) 
SELECT 
  * 
FROM 
  (
    WITH sum_ci AS(
      SELECT 
        SUM(output_cio) as output_ci, 
        SUM(fa_net_cio) as fa_net_ci, 
        SUM(employment_cio) as employment_ci, 
        geocode4_corr AS geocode4_corr_b, 
        cic AS cic_b 
      FROM 
        sum_cio 
      GROUP BY 
        geocode4_corr, 
        cic
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_cio AS(
          SELECT 
            OWNERSHIP, 
            output_cio / output_ci AS share_output_cio, 
            fa_net_cio / fa_net_ci AS share_fa_net_cio, 
            employment_cio / employment_ci AS share_employement_cio, 
            geocode4_corr, 
            cic 
          FROM 
            sum_cio 
            LEFT JOIN sum_ci ON sum_cio.geocode4_corr = sum_ci.geocode4_corr_b 
            AND sum_cio.cic = sum_ci.cic_b
        ) 
        SELECT 
          * 
        FROM 
          (
            WITH share_io AS (
              SELECT 
                AVG(share_output_cio) AS share_output_ci_mean, 
                AVG(share_fa_net_cio) AS share_fa_net_ci_mean, 
                AVG(share_employement_cio) AS share_employement_ci_mean, 
                cic AS cic_b, 
                OWNERSHIP AS OWNERSHIP_b 
              FROM 
                share_cio 
              GROUP BY 
                cic, 
                OWNERSHIP
            ) 
            SELECT 
              * 
            FROM 
              (
                WITH percentile AS (
                  SELECT 
                    cic, 
                    OWNERSHIP, 
                    
                    ANY_VALUE(share_output_ci_03) AS share_output_ci_03,
                    ANY_VALUE(share_output_ci_median) AS share_output_ci_median, 
                    ANY_VALUE(share_output_ci_07) AS share_output_ci_07, 
                    
                    ANY_VALUE(share_fa_net_ci_03) AS share_fa_net_ci_03,
                    ANY_VALUE(share_fa_net_ci_median) AS share_fa_net_ci_median, 
                    ANY_VALUE(share_fa_net_ci_07) AS share_fa_net_ci_07, 
                    
                    ANY_VALUE(share_employement_ci_03) AS share_employement_ci_03,
                    ANY_VALUE(share_employement_ci_median) AS share_employement_ci_median, 
                    ANY_VALUE(share_employement_ci_07) AS share_employement_ci_07 
                  FROM 
                    (
                      SELECT 
                        cic, 
                        OWNERSHIP, 
                        
                        PERCENTILE_CONT(share_output_cio, 0.3) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_output_ci_03,
                        PERCENTILE_CONT(share_output_cio, 0.5) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_output_ci_median, 
                        PERCENTILE_CONT(share_output_cio, 0.7) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_output_ci_07, 
                        
                        PERCENTILE_CONT(share_fa_net_cio, 0.3) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_fa_net_ci_03,
                        PERCENTILE_CONT(share_fa_net_cio, 0.5) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_fa_net_ci_median, 
                        PERCENTILE_CONT(share_fa_net_cio, 0.7) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_fa_net_ci_07, 
                        
                        PERCENTILE_CONT(share_employement_cio, 0.3) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_employement_ci_03,
                        PERCENTILE_CONT(share_employement_cio, 0.5) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_employement_ci_median, 
                        PERCENTILE_CONT(share_employement_cio, 0.7) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_employement_ci_07 
                      FROM 
                        share_cio
                    ) 
                  GROUP BY 
                    cic, 
                    OWNERSHIP
                ) 
                SELECT 
                  * 
                FROM 
                  (
                    WITH avg_pct AS(
                      SELECT 
                        cic_b, 
                        OWNERSHIP_b, 
                        share_output_ci_mean, 
                        share_fa_net_ci_mean, 
                        share_employement_ci_mean, 
                        share_output_ci_median, 
                        share_output_ci_03, 
                        share_output_ci_07, 
                        share_fa_net_ci_median, 
                        share_fa_net_ci_03, 
                        share_fa_net_ci_07, 
                        share_employement_ci_median, 
                        share_employement_ci_03, 
                        share_employement_ci_07 
                      FROM 
                        percentile 
                        LEFT JOIN share_io ON percentile.cic = share_io.cic_b 
                        AND percentile.OWNERSHIP = share_io.OWNERSHIP_b
                    ) 
                    SELECT 
                      geocode4_corr, 
                      cic AS industry, 
                      OWNERSHIP, 
                      share_output_ci_mean,
                      CASE WHEN share_output_cio > share_output_ci_mean THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_mean, 
                      CASE WHEN share_output_cio > share_output_ci_median THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_median, 
                      CASE WHEN share_output_cio > share_output_ci_03 THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_03,
                      CASE WHEN share_output_cio > share_output_ci_07 THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_07, 
                      
                      
                      share_fa_net_ci_mean, 
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_mean THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_mean, 
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_median THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_median, 
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_03 THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_03,
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_07 THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_07, 
                      
                      share_employement_ci_mean, 
                      CASE WHEN share_employement_cio > share_employement_ci_mean THEN 
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_mean, 
                      CASE WHEN share_employement_cio > share_employement_ci_median THEN
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_median, 
                      CASE WHEN share_employement_cio > share_employement_ci_03 THEN 
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_03,
                      CASE WHEN share_employement_cio > share_employement_ci_07 THEN 
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_07, 
                    FROM 
                      share_cio 
                      LEFT JOIN avg_pct ON share_cio.cic = avg_pct.cic_b 
                      AND share_cio.OWNERSHIP = avg_pct.OWNERSHIP_b 
                    ORDER BY 
                      OWNERSHIP, 
                      cic, 
                      geocode4_corr
                  )
              )
          )
      )
  )

"""
df_share = gcp.upload_data_from_bigquery(query = query_share,
                                         location = 'US')
```

```sos kernel="SoS"
%put df_final --to R
df_final = (df_final.merge(
    df_share.loc[lambda x: x['OWNERSHIP'].isin(['SOE'])][
        ['geocode4_corr',
               'industry',
 'output_dominated_mean',
 'output_dominated_median',
              'output_dominated_03',
 'output_dominated_07',
 'capital_dominated_mean',
 'capital_dominated_median',
              'capital_dominated_03',
 'capital_dominated_07',
 'employement_dominated_mean',
 'employement_dominated_median',
              'employement_dominated_03',
 'employement_dominated_07'
             ]],
    how = 'left',
    indicator = True
).assign(
    output_dominated_mean = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['output_dominated_mean']
    ),
    capital_dominated_mean = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['capital_dominated_mean']
    )
    ,
    employement_dominated_mean = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['employement_dominated_mean']
    ),
    output_dominated_median = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['output_dominated_median']
    ),
    capital_dominated_median = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['capital_dominated_median']
    )
    ,
    employement_dominated_median = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['employement_dominated_median']
    ),
     output_dominated_03 = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['output_dominated_03']
    ),
    capital_dominated_03 = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['capital_dominated_03']
    )
    ,
    employement_dominated_03 = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['employement_dominated_03']
    ),
    output_dominated_07 = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['output_dominated_07']
    ),
    capital_dominated_07 = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['capital_dominated_07']
    )
    ,
    employement_dominated_07 = lambda x: np.where(
        x['_merge'] == 'left_only',
        'BELOW',
        x['employement_dominated_07']
    )
)
)
```

```sos kernel="SoS"
df_final.shape
```

```sos kernel="SoS"
df_final.groupby([
                  'output_dominated_mean'])['output_dominated_mean'].count()
df_final.groupby([
                  'output_dominated_median'])['output_dominated_median'].count()
df_final.groupby([
                  'output_dominated_03'])['output_dominated_03'].count()
df_final.groupby([
                  'output_dominated_07'])['output_dominated_07'].count()
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
### City-industry

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 010_SOE_city_industry
    - 011_PRIVATE_city_industry
    
#### SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1jJ5WR3ka22qL9Rsfhg3Rwdg6M4QY1QdW)

#### Private

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1pwjPnAlCIqlh0ixodV-VNldVtKxYx412)
<!-- #endregion -->

<!-- #region kernel="R" -->
### Code
<!-- #endregion -->

<!-- #region kernel="R" -->
#### SOE
<!-- #endregion -->

```sos kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_mean == 'ABOVE'),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_median == 'ABOVE'),
             exactDOF=TRUE)
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_03 == 'ABOVE'),
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_07 == 'ABOVE'),
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_mean == 'ABOVE'),
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_median == 'ABOVE'),
             exactDOF=TRUE)
t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_03 == 'ABOVE'),
             exactDOF=TRUE)
t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_07 == 'ABOVE'),
             exactDOF=TRUE)
t9 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_mean == 'ABOVE'),
             exactDOF=TRUE)
t10 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_median == 'ABOVE'),
             exactDOF=TRUE)
t11 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_03 == 'ABOVE'),
             exactDOF=TRUE)
t12 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_07 == 'ABOVE'),
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile= ['& mean', 'median','decile .3', 'decile .7',
        'mean', 'median','decile .3', 'decile .7',
        'mean', 'median','decile .3', 'decile .7']
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
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes'),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes'),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes')
             )
table_1 <- go_latex(list(
    t1,
    t2,
    t3, 
    t4,
    t5,
    t6,
    t7, 
    t8,
    t9,
    t10,
    t11, 
    t12
),
    title='SOE dominating sectors',
    addFE=fe1,
    save=TRUE,
    name="table_1.txt"
)
```

<!-- #region kernel="R" -->
#### Private
<!-- #endregion -->

```sos kernel="R"
#### Output
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_mean == 'BELOW'),
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_median == 'BELOW'),
             exactDOF=TRUE)
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_03 == 'BELOW'),
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(output_dominated_07 == 'BELOW'),
             exactDOF=TRUE)

#### Capital
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_mean == 'BELOW'),
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_median == 'BELOW'),
             exactDOF=TRUE)
t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_03 == 'BELOW'),
             exactDOF=TRUE)
t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(capital_dominated_07 == 'BELOW'),
             exactDOF=TRUE)

#### Employement
t9 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_mean == 'BELOW'),
             exactDOF=TRUE)
t10 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_median == 'BELOW'),
             exactDOF=TRUE)
t11 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_03 == 'BELOW'),
             exactDOF=TRUE)
t12 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(employement_dominated_07 == 'BELOW'),
             exactDOF=TRUE)
```

```sos kernel="python3"
import os
decile= ['& mean', 'median','decile .3', 'decile .7',
        'mean', 'median','decile .3', 'decile .7',
        'mean', 'median','decile .3', 'decile .7']
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
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes'),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes'),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes')
             )
table_1 <- go_latex(list(
    t1,
    t2,
    t3, 
    t4,
    t5,
    t6,
    t7, 
    t8,
    t9,
    t10,
    t11, 
    t12
),
    title='Private dominating sectors',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos kernel="python3"
for i in range(1,3):
    lb.beautify(table_number = i,
    constraint = False,
    city_industry = False, 
    new_row = decile)
```

<!-- #region kernel="python3" -->
## Level industry

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city, industry, ownership
- Step 2: Compute the average of step 1 by city, industry
- Step 3: if Step 1 > step 2, then Above

Three threshold:

- mean
- median
- decile .3
- decile .7
<!-- #endregion -->

<!-- #region kernel="python3" -->
### Code load data
<!-- #endregion -->

```sos kernel="python3"
query_share = """ WITH sum_cio AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' WHEN ownership = 'SOE' THEN 'SOE' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_cio, 
    SUM(fa_net / 10000000) as fa_net_cio, 
    SUM(employment / 100000) as employment_cio,
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
    WITH sum_ci AS(
      SELECT 
        SUM(output_cio) as output_ci, 
        SUM(fa_net_cio) as fa_net_ci, 
        SUM(employment_cio) as employment_ci, 
        cic AS cic_b 
      FROM 
        sum_cio 
      GROUP BY 
        cic
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_cio AS(
          SELECT 
            OWNERSHIP, 
            output_cio / output_ci AS share_output_cio, 
            fa_net_cio / fa_net_ci AS share_fa_net_cio, 
            employment_cio / employment_ci AS share_employement_cio, 
            geocode4_corr, 
            cic 
          FROM 
            sum_cio 
            LEFT JOIN sum_ci ON sum_cio.cic = sum_ci.cic_b
        ) 
        SELECT 
          * 
        FROM 
          (
            WITH share_io AS (
              SELECT 
                AVG(share_output_cio) AS share_output_ci_mean, 
                AVG(share_fa_net_cio) AS share_fa_net_ci_mean, 
                AVG(share_employement_cio) AS share_employement_ci_mean, 
                cic AS cic_b, 
                OWNERSHIP AS OWNERSHIP_b 
              FROM 
                share_cio 
              GROUP BY 
                cic, 
                OWNERSHIP
            ) 
            SELECT 
              * 
            FROM 
              (
                WITH percentile AS (
                  SELECT 
                    cic, 
                    OWNERSHIP, 
                    
                    ANY_VALUE(share_output_ci_03) AS share_output_ci_03,
                    ANY_VALUE(share_output_ci_median) AS share_output_ci_median, 
                    ANY_VALUE(share_output_ci_07) AS share_output_ci_07, 
                    
                    ANY_VALUE(share_fa_net_ci_03) AS share_fa_net_ci_03,
                    ANY_VALUE(share_fa_net_ci_median) AS share_fa_net_ci_median, 
                    ANY_VALUE(share_fa_net_ci_07) AS share_fa_net_ci_07, 
                    
                    ANY_VALUE(share_employement_ci_03) AS share_employement_ci_03,
                    ANY_VALUE(share_employement_ci_median) AS share_employement_ci_median, 
                    ANY_VALUE(share_employement_ci_07) AS share_employement_ci_07 
                  FROM 
                    (
                      SELECT 
                        cic, 
                        OWNERSHIP, 
                        
                        PERCENTILE_CONT(share_output_cio, 0.3) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_output_ci_03,
                        PERCENTILE_CONT(share_output_cio, 0.5) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_output_ci_median, 
                        PERCENTILE_CONT(share_output_cio, 0.7) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_output_ci_07, 
                        
                        PERCENTILE_CONT(share_fa_net_cio, 0.3) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_fa_net_ci_03,
                        PERCENTILE_CONT(share_fa_net_cio, 0.5) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_fa_net_ci_median, 
                        PERCENTILE_CONT(share_fa_net_cio, 0.7) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_fa_net_ci_07, 
                        
                        PERCENTILE_CONT(share_employement_cio, 0.3) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_employement_ci_03,
                        PERCENTILE_CONT(share_employement_cio, 0.5) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_employement_ci_median, 
                        PERCENTILE_CONT(share_employement_cio, 0.7) 
                        OVER(PARTITION BY cic, OWNERSHIP) AS share_employement_ci_07 
                      FROM 
                        share_cio
                    ) 
                  GROUP BY 
                    cic, 
                    OWNERSHIP
                ) 
                SELECT 
                  * 
                FROM 
                  (
                    WITH avg_pct AS(
                      SELECT 
                        cic_b, 
                        OWNERSHIP_b, 
                        share_output_ci_mean, 
                        share_fa_net_ci_mean, 
                        share_employement_ci_mean, 
                        share_output_ci_median, 
                        share_output_ci_03, 
                        share_output_ci_07, 
                        share_fa_net_ci_median, 
                        share_fa_net_ci_03, 
                        share_fa_net_ci_07, 
                        share_employement_ci_median, 
                        share_employement_ci_03, 
                        share_employement_ci_07 
                      FROM 
                        percentile 
                        LEFT JOIN share_io ON percentile.cic = share_io.cic_b 
                        AND percentile.OWNERSHIP = share_io.OWNERSHIP_b
                    ) 
                    SELECT 
                      geocode4_corr, 
                      cic AS industry, 
                      OWNERSHIP, 
                      share_output_ci_mean,
                      CASE WHEN share_output_cio > share_output_ci_mean THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_mean, 
                      CASE WHEN share_output_cio > share_output_ci_median THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_median, 
                      CASE WHEN share_output_cio > share_output_ci_03 THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_03,
                      CASE WHEN share_output_cio > share_output_ci_07 THEN 
                      'ABOVE' ELSE 'BELOW' END AS output_dominated_07, 
                      
                      
                      share_fa_net_ci_mean, 
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_mean THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_mean, 
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_median THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_median, 
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_03 THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_03,
                      CASE WHEN share_fa_net_cio > share_fa_net_ci_07 THEN 
                      'ABOVE' ELSE 'BELOW' END AS capital_dominated_07, 
                      
                      share_employement_ci_mean, 
                      CASE WHEN share_employement_cio > share_employement_ci_mean THEN 
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_mean, 
                      CASE WHEN share_employement_cio > share_employement_ci_median THEN
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_median, 
                      CASE WHEN share_employement_cio > share_employement_ci_03 THEN 
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_03,
                      CASE WHEN share_employement_cio > share_employement_ci_07 THEN 
                      'ABOVE' ELSE 'BELOW' END AS employement_dominated_07, 
                    FROM 
                      share_cio 
                      LEFT JOIN avg_pct ON share_cio.cic = avg_pct.cic_b 
                      AND share_cio.OWNERSHIP = avg_pct.OWNERSHIP_b 
                    ORDER BY 
                      OWNERSHIP, 
                      cic
                  )
              )
          )
      )
  )

"""
df_share = gcp.upload_data_from_bigquery(query = query_share,
                                         location = 'US')
```

<!-- #region kernel="python3" -->
### Industry

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 020_SOE_industry
    - 021_PRIVATE_industry

#### SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)

#### Private

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)
<!-- #endregion -->

<!-- #region kernel="python3" -->
## Level City-industry

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city, industry, ownership
- Step 2: Compute the average of step 1 by city, industry
- Step 3: if Step 1 > step 2, then Above

Three threshold:

- mean
- median
- decile .3
- decile .7
<!-- #endregion -->

<!-- #region kernel="python3" -->
### City

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 030_SOE_city
    - 031_PRIVATE_city

#### SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)

#### Private

In Google Drive:

![](https://drive.google.com/uc?export=view&id=)
<!-- #endregion -->
