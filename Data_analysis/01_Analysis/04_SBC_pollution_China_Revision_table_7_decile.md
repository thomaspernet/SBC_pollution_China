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
    - https://htmlpreview.github.io/?https://github.com/thomaspernet/SBC_pollution_China/blob/master/Data_analysis/Reports/SBC_pollution_China_Revision_table_7_decile.html

## Revision table 7 - Decile analysis

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

<!-- #region kernel="SoS" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
# Table 7: improvement Decile

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
  
## Objective

Find the elasticities of the private sectors when the share of SOE is either higher (threshold) or increasing (cummulative), characterized by industry; city, city-industry level)

Our hypothesis: 

- The elasticities should decrease when the share of [output, capital, employement] of the State in increasing 
    - We have two way to test it.
        1. Use the exact decile -> Take only the industries belonging to a given decile. Note that, low decile indicate a low output share of the SOE. Say differently, there are industries with a strong output done by the private. For instance, decile 1 indicates that we keep the first 10 percent of the indsutries with the lowest share of [output, capital, employement]
    - how to read table: Less observations -> larger coefficients in absolute values because the share is mostly done by the private. More observation implies larger operation by the SOE.
<!-- #endregion -->

<!-- #region kernel="SoS" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
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

<!-- #region kernel="R" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
# Foreign vs Public

1.  Pour montrer que le secteur privé doit compenser l'absence de réaction du secteur public, nous allons procéder de la manière suivante: 

Nous avons Identifié les secteurs où la part des entreprises publiques est inférieure à un seuil critique. Nous allons comparer la réponse du secteur privé dans ces secteurs. 

- Il s'agit du tableau 7, panel B: deux options (si possible les faire toutes les deux): 
  
    - on regarde les entreprises privées dans les villes-secteurs où la part étatique est plus faible, Elle devrait être plus vigoureuse. Deux estimations donc au lieu d'une seule. 
    - on change le seuil de dominance privé/public. Moins il y a de privé, plus la réaction de ce dernier doit être forte.
<!-- #endregion -->

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
## Level industry

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry, ownership: `Share_io`
- Step 2: Compute the deciles of step 1 by  ownership: `Share_io`

We only need when `ownership` is equal to `SOE`. First decile indicates a low share of SOE in these sectors. For instance, when the decile is 1, it means this is the bottom 10% of sectors with the lowest share of SOE. The larger the decile, the higher the state presences.

In a nutshell, we can run estimate in two ways:

- by decile 
- by cumulated decile
<!-- #endregion -->

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
### Code load data
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
```

```sos kernel="SoS"
%put df_final_i --to R
df_final_i = (df_final.merge(
    df_share.loc[lambda x: x['OWNERSHIP'].isin(['SOE'])][
        [
            'industry',
            'share_output_io',
            'rank_share_output_io',
            'rank_share_capital_io',
            'rank_share_employement_io'
             ]],
    how = 'left',
    indicator = True
)
)
```

```sos kernel="SoS"
#temp = (pd.concat([(df_final_i[['industry', 'rank_share_output_io']]
# .drop_duplicates()
# .sort_values(by = 'rank_share_output_io')
# .set_index('industry')
#),
#          pd.DataFrame((pd.qcut(
#    df_share.loc[lambda x: 
#      x['OWNERSHIP'].isin(['SOE'])]
#    .set_index('industry')['share_output_io'],
#    10,retbins = True, precision = 5 #,labels=True
#)
#)
#            ).T.drop(columns = ['Unnamed 0'])
#         ], axis = 1)
# .dropna(subset = ['rank_share_output_io'])
# .sort_values(by ='rank_share_output_io')
#        .rename(columns = {'rank_share_output_io':'rank',
#                           'share_output_io':'decile'})
#        .reset_index()
#)
#temp.loc[lambda x: x['rank'].isin([3])].head(2)
```

```sos kernel="SoS"
df_final_i.shape
```

```sos kernel="SoS"
(df_final_i
 .groupby([ 'rank_share_output_io', 'TCZ_c'])['rank_share_output_io']
 .count()
 .unstack(1))
```

```sos kernel="SoS"
df_final_i.groupby([ 'rank_share_output_io',
                    'polluted_thre'])['rank_share_output_io'].count().unstack(1)
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

<!-- #region kernel="python3" toc-hr-collapsed=true kernel="SoS" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
### Output

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 010_output_industry_thresh_
    - 011_output_industry_cum
    
**Threshold**

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1g7zQH-RkmQeY6tM5KzIU6tEdWhumsNEl)

**Cumulative**

![](https://drive.google.com/uc?export=view&id=1wkvLZRe8ftyqXBtY3I5iM4RFKD4Ki7al)

<!-- #endregion -->

<!-- #region kernel="R" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
#### Code
<!-- #endregion -->

<!-- #region kernel="R" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
##### Private - Output - threshold
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_output_io == i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles output',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
##### Private - Output - cumulative
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_output_io <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Cumulative Deciles output',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
### Capital

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 020_capital_industry_thresh
    - 021_capital_industry_cum
    
**Threshold**

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1SpsDjKPnS9guANOUMAdHEaZr2KxFJejg)

**Cumulative**

![](https://drive.google.com/uc?export=view&id=1E-A5gREVvfHxj5dKQ6Sc39zymoh8Vayc)
<!-- #endregion -->

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
#### Code
<!-- #endregion -->

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
##### Private - capital - threshold
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_capital_io == i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles capital',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
##### Private - capital - cumulative
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_capital_io <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Cumulative Deciles output',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
### Employement

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 030_employement_industry_thresh
    - 031_employement_industry_thresh
    
**Threshold**

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1uJz3NDW3hlPMscdvBAF5HPjDyqZ664HG)

**Cumulative**

![](https://drive.google.com/uc?export=view&id=1d_C-H8LkIrcL_cXdlLC3j1OLgefE4NfB)
<!-- #endregion -->

<!-- #region kernel="python3" -->
#### Code
<!-- #endregion -->

<!-- #region kernel="python3" -->
##### Private - employment - threshold
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_employement_io == i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles Employment',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
##### Private - employment - cumulative
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_employement_io <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Cumulative Deciles employment',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
## Level City

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry, ownership: `Share_io`
- Step 2: Compute the deciles of step 1 by  ownership: `Share_io`

We only need when `ownership` is equal to `SOE`. First decile indicates a low share of SOE in these sectors. For instance, when the decile is 1, it means this is the bottom 10% of sectors with the lowest share of SOE. The larger the decile, the higher the state presences.

In a nutshell, we can run estimate in two ways:

- by decile 
- by cumulated decile
<!-- #endregion -->

<!-- #region kernel="python3" toc-hr-collapsed=true kernel="SoS" -->
### Code load data
<!-- #endregion -->

```sos kernel="SoS"
query_share = """ WITH sum_co AS (
  SELECT 
    case WHEN ownership = 'Foreign' THEN 'FOREIGN' WHEN ownership = 'SOE' 
    THEN 'SOE' ELSE 'DOMESTIC' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_co, 
    SUM(fa_net / 10000000) as fa_net_co, 
    SUM(employment / 100000) as employment_co,
    geocode4_corr 
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
        geocode4_corr,
        OWNERSHIP,  
        NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_output_co) 
          as rank_share_output_co,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_fa_net_co) 
          as rank_share_capital_co,
          NTILE(10)  OVER (PARTITION BY OWNERSHIP ORDER BY share_employement_co) 
          as rank_share_employement_co,
        share_output_co
        FROM share_co
 
        )
        )
        
"""
df_share = gcp.upload_data_from_bigquery(query = query_share,
                                         location = 'US')
```

```sos kernel="SoS"
%put df_final_c --to R
df_final_c = (df_final.merge(
    df_share.loc[lambda x: x['OWNERSHIP'].isin(['SOE'])][
        [
            'geocode4_corr',
            'share_output_co',
            'rank_share_output_co',
            'rank_share_capital_co',
            'rank_share_employement_co'
             ]],
    how = 'left',
    indicator = True
)
)
```

```sos kernel="SoS"
df_final_c.shape
```

```sos kernel="R"
df_final <- df_final_c %>% 
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

<!-- #region kernel="python3" toc-hr-collapsed=true kernel="SoS" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
### Output

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 040_output_city_thresh
    - 041_output_city_cum
    
**Threshold**

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1B7yGNh6iXDAh5Otf2yd3XprDkh-OSEUp)

**Cumulative**

![](https://drive.google.com/uc?export=view&id=17u9cRVeTZIm_xo1XhZacgvqx2lwNQAH_)
<!-- #endregion -->

<!-- #region kernel="R" toc-hr-collapsed=true kernel="SoS" -->
#### Code
<!-- #endregion -->

<!-- #region kernel="R" -->
##### Private - Output - threshold
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_output_co == i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles output',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
##### Private - Output - cumulative
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_output_co <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Cumulative Deciles output',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
### Capital

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 050_capital_city_thresh
    - 051_city_industry_cum
    
**Threshold**

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1nW2NqDZ_KGWTSJGDgDoct53UauplCh2G)

**Cumulative**

![](https://drive.google.com/uc?export=view&id=1f-GnYoE7i5E0kOCVVP70DrCzYpd_VC9Y)
<!-- #endregion -->

<!-- #region kernel="python3" -->
#### Code
<!-- #endregion -->

<!-- #region kernel="python3" -->
##### Private - capital - threshold
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_capital_co == i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles capital',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
##### Private - capital - cumulative
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_capital_co <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Cumulative Deciles capital',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
### Employement

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 060_employement_city_thresh
    - 061_employement_city_thresh
    
**Threshold**

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1pUCoFUZAQ71i2PpOP4xLcXgk9ZhAMSVS)

**Cumulative**

![](https://drive.google.com/uc?export=view&id=1psm8mYl-wSc-T42CfLELmR5dzyRLOz6U)
<!-- #endregion -->

<!-- #region kernel="python3" -->
#### Code
<!-- #endregion -->

<!-- #region kernel="python3" toc-hr-collapsed=true toc-nb-collapsed=true kernel="SoS" -->
##### Private - employement - threshold
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_employement_co == i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Deciles Employment',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```

<!-- #region kernel="python3" -->
##### Private - employement - Cumulatice
<!-- #endregion -->

```sos kernel="R"
i <- 1
l = list()
while(i < 10) {
    t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final %>% filter(rank_share_employement_co <= i),
             exactDOF=TRUE)
    
    l[[i]] <- t1
    i <- i + 1
}
```

```sos kernel="python3"
import os
decile=['& decile .1','decile .2', ' decile .3', 'decile .4',
        'decile .5','decile .6', ' decile .7', 'decile .8',
        'decile .9']
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
              "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes", "Yes", 'Yes',
              "Yes", "Yes")
             )
table_1 <- go_latex(l,
    dep_var = "Dependent variable: \\text { SO2 emission }_{i k t}",
    title='Cumulative Deciles employment',
    addFE=fe1,
    save=TRUE,
                    note = FALSE,
    name="table_2.txt"
)
```

```sos kernel="python3"
tb = """\\footnotesize{
A decile indicates the rank share of [output, capital, employement] of the SOEs \\
More specifically, the low deciles means a low presence of SOEs firms in the industries. \\
Deciles close to one, however, implies a stronger share of [output, capital, employement] in the \\
industries belong to those deciles.
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\%
}
"""
lb.beautify(table_number = 2,
    constraint = False,
    city_industry = False, 
    new_row = decile,
    table_nte =tb)
```
