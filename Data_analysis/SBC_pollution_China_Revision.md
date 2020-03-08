---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.3
  kernelspec:
    display_name: SoS
    language: sos
    name: sos
---

<!-- #region Collapsed="false" kernel="SoS" -->
# SBC_pollution_China Revision Paper

Here is the link with all the revisions:

- https://coda.io/d/SoftBudgetConstraint_dD-uOwatzMS/Revision_suYyi#_luGfQ

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

<!-- #region Collapsed="true" kernel="SoS" -->
# Revision

## Load the data


<!-- #endregion -->

```sos Collapsed="false" kernel="SoS"
import pandas as pd
from Fast_connectCloud import connector

gs = connector.open_connection(online_connection = False,
                              path_credential = '/Users/thomas/Google Drive/Projects/Data_science/Google_code_n_Oauth/Client_Oauth/Google_auth/')

service = gs.connect_remote('GCP')
```

<!-- #region kernel="SoS" Collapsed="true" -->
## Load SBC_pollution_China from Google Big Query

Feel free to add description about the dataset or any usefull information.
<!-- #endregion -->

```sos Collapsed="false" kernel="SoS"
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

<!-- #region kernel="SoS" Collapsed="true" -->
## Load Herfindahl_China_cic_city from Google Big Query

Feel free to add description about the dataset or any usefull information.
<!-- #endregion -->

```sos Collapsed="false" kernel="SoS"
query_herfindhal = (
          "SELECT * "
            "FROM China.Herfindahl_China_cic_city "

        )
df_herfhindal = gcp.upload_data_from_bigquery(query = query_herfindhal,
                                         location = 'US').rename(columns = {'cic':'industry',
                                'cityen_correct':'cityen'})
```

```sos Collapsed="false" kernel="R"
options(warn=-1)
library(tidyverse)
library(lfe)
library(lazyeval)
library('progress')
```

```sos Collapsed="false" kernel="R"
path = "functions/SBC_pollution_R.R"
source(path)
path = "functions/SBC_pollutiuon_golatex.R"
source(path)

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

<!-- #region Collapsed="false" kernel="SoS" -->
# Comment Empirical analysis:

First of all, notice again that there is no convincing evidence that SOEs shifts the burden of the environmental adaptation to private firms. In most of the cases, there are interaction terms with three or even form variables in the regression equation. My major concern is if the authors have also included all the sublevel interaction terms in the regression. For instance, in equation (1), there is an interaction term of four variables, TCZi, Polluting sectorsk, Period, Share SOEk. However, it seems in table 3 not all the corresponding triple interaction terms (such as $TCZi *Polluting sectorsk *Share SOEk$) are controlled. 

## Answers:

Compute the following equation to show the fixed effect tackle the "missing" coefficients

$$EQUATION$$

~CF this [paper](https://drive.google.com/file/d/1-SXSlRoS_2ZW7CK6XMhcXpJDPxAEF1xG/view)~ -> no need anymore

<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

<!-- #region Collapsed="true" kernel="python3" -->
## 01: All variables: Our new baseline

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 01_baseline_revision

In Google Drive:

![](https://drive.google.com/uc?export=view&id=14x1fwM2cYZBSwyt2XQmb5t3VzCExUtRH)
<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="true" -->
### Codes
<!-- #endregion -->

```sos Collapsed="false" kernel="R"
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
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_1.txt"
)
```

```sos Collapsed="false" kernel="python3"
import os
try:
    os.remove("table_1.tex")
except:
    pass
lb.beautify(table_number = 1, constraint = False)
```

<!-- #region Collapsed="false" kernel="python3" -->
## Foreign firms

 In particular, my main concern is that the author could explore the heterogeneity of response within the private sector and not only between the private and the state-owned sectors. Indeed, foreign firms may react differently to environmental constraints. They may be less sensitive to environmental regulations because they have cleaner technologies (see for instance: Dean et al., 2009, "Are Foreign Investors Attracted to Weak Environmental Regulations? Evidence from China", Journal of Development Economics). Another possibility is that foreign firms could negotiate with local authorities to obtain preferential treatment concerning the enforcement of environmental regulation (Wang et al., 2003, quoted in the paper)
<!-- #endregion -->

```sos Collapsed="false" kernel="R"
options(warn=-1)
library(tidyverse)
library(lfe)
library(lazyeval)
library('progress')
```

```sos Collapsed="false" kernel="SoS"
%put df_final --to R

from GoogleDrivePy.google_platform import connect_cloud_platform
project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service['GoogleCloudP'])    

query = (
    "SELECT * FROM China.SBC_pollution_China_foreign "
)

df_final = gcp.upload_data_from_bigquery(query=query, location="US").rename(columns = {
    'out_share_soe1':'out_share_SOE',
    'cap_share_soe1':'cap_share_SOE',
    'lab_share_soe1':'lab_share_SOE',
})
df_final.head()
```

```sos Collapsed="false" kernel="R"
path = "functions/SBC_pollution_R.R"
source(path)
path = "functions/SBC_pollutiuon_golatex.R"
source(path)

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

<!-- #region kernel="R" Collapsed="false" -->
## 02 Foreign-SOE

In this table, foreign and SOE share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 02_foreign_SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1KttrgK0dzsnh4-9bInpyvtKgTOyXewPo)
<!-- #endregion -->

<!-- #region kernel="R" Collapsed="false" -->
### Code
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos kernel="R" Collapsed="false"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
             + TCZ_c * Period * polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
             + TCZ_c * Period * polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
            cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
             + TCZ_c * Period * polluted_thre * lab_share_SOE	
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry   | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
             + TCZ_c * Period * polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
             + TCZ_c * Period * polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)
t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
             + TCZ_c * Period * polluted_thre * lab_share_SOE	
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2,
    t3,
    t4,
    t5,
    t6
),
    title='Baseline results revision: Foreign-SOE',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos Collapsed="false" kernel="python3"
try:
    os.remove('table_2.tex')
except:
    pass
lb.beautify(table_number = 2, constraint = False)
```

<!-- #region kernel="python3" Collapsed="false" -->
## 03: Foreign

In this table, only foreign share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 03_foreign

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1LMR9Os_Koz9FtdXMZLTb6lLC_Loj9c5z)
<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="false" -->
### Code
<!-- #endregion -->

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              cityen +  year + industry  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              cityen +  year + industry  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2,
    t3,
    t4,
    t5,
    t6
),
    title='Baseline results revision: Foreign',
    addFE=fe1,
    save=TRUE,
    name="table_3.txt"
)
```

```sos Collapsed="false" kernel="python3"
try:
    os.remove('table_3.tex')
except:
    pass
lb.beautify(table_number = 3, constraint = False)
```

<!-- #region Collapsed="false" kernel="python3" -->
## Herfindalh

It might be the case that large firms can influence local authorities concerning the effective enforcement of environmental regulation. If possible, I suggest to identify in each city 

- (i) and for each industry (k), an index of industrial concentration (or the share of large firms in the industry). 
    - Then, a solution would be to estimate the model on a sub-sample of city-industry characterized by a low industrial concentration. 
    - A comparison of the results between the total sample and the subsample would allow checking the magnitude of the endogeneity bias. 

* https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_Index

We can use the herfindhal index at the industry level, so that we are consistent with our strategy -> the interaction term is at the industry level and not city-industry level. 

In the first part, we compute the Herfindhal at the industry level -> average by industry. In the second part, we use the city industry, therefore, we estimate one more coefficient with the pair fixed effect

<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="false" -->
## Concentration at the industry level
<!-- #endregion -->

```sos kernel="SoS" Collapsed="false"
import numpy as np
```

```sos kernel="SoS" Collapsed="false"
df_herfhindal_ind = (df_herfhindal
                     .groupby('industry')['Herfindahl']
                     .mean()
                     .reset_index())
```

```sos kernel="SoS" Collapsed="false"
df_herfhindal_final = df_final.merge(df_herfhindal_ind,
                                     on=['industry'],
                                     how='left',
                                     indicator=True

                                     )
df_herfhindal_final['df_herfhindal_final'] = df_herfhindal_final['Herfindahl'].fillna(
    0)
```

```sos kernel="SoS" Collapsed="false"
df_herfhindal_final['Herfindahl'].quantile([.1,
                                            .15,
                                            .25,
                                            .5,
                                            .70,
                                            .75,
                                            .80,
                                            .85,
                                            .95])
```

```sos kernel="SoS" Collapsed="false"
%put df_herfhindal_final --to R
df_herfhindal_final = df_herfhindal_final.assign(
concentrated_25 = lambda x: np.where(x['Herfindahl'] > 0.632807,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_50 = lambda x: np.where(x['Herfindahl'] > 0.728706,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_75 = lambda x: np.where(x['Herfindahl'] > 0.784489,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_85 = lambda x: np.where(x['Herfindahl'] > 0.819006,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
)
```

```sos kernel="SoS" Collapsed="false"
df_herfhindal_final.groupby('concentrated_75')['concentrated_75'].count()
```

```sos kernel="SoS" Collapsed="false"
df_herfhindal_final.groupby('concentrated_85')['concentrated_85'].count()
```

```sos kernel="R" Collapsed="false"
path = "functions/SBC_pollution_R.R"
source(path)
path = "functions/SBC_pollutiuon_golatex.R"
source(path)

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
         concentrated_25 = relevel(concentrated_25, ref='NOT_CONCENTRATED'),
         concentrated_50 = relevel(concentrated_50, ref='NOT_CONCENTRATED'),
         concentrated_75 = relevel(concentrated_75, ref='NOT_CONCENTRATED'),
         concentrated_85 = relevel(concentrated_85, ref='NOT_CONCENTRATED'),
  )
head(df_final)
```

<!-- #region kernel="R" Collapsed="false" -->
### 04: Sector Concentration

Interaction with a concentration dummy

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 04_concentrated_indu

In Google Drive:

![](https://drive.google.com/uc?export=view&id=11gh-qQ9lqaltNdXyhfQgYmdtpay677Ap)
<!-- #endregion -->

<!-- #region kernel="R" Collapsed="false" -->
#### Code
<!-- #endregion -->

```sos kernel="R" Collapsed="false"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(
             c("City-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1, t2, t3,t4, t5, t6, t7, t8
),
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_4.txt"
)
```

```sos kernel="python3" Collapsed="false"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos kernel="python3" Collapsed="false"
import os
try:
    os.remove("table_4.tex")
except:
    pass
lb.beautify(table_number = 4, constraint = False)
```

<!-- #region kernel="python3" Collapsed="false" -->
### 05: Sector Concentration and output share SOE

Interaction with a concentration dummy and include SOE output share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 05_concentrated_ind_SOE

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1I4jFvbnP8CvXbt020gpFWPH6si9pkpS3)
<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="false" -->
#### Code
<!-- #endregion -->

```sos kernel="R" Collapsed="false"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
           +TCZ_c * Period *polluted_thre * out_share_SOE
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(
             c("City-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1, t2, t3,t4, t5, t6, t7, t8
),
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_5.txt"
)
```

```sos kernel="python3" Collapsed="false"
import os
try:
    os.remove("table_5.tex")
except:
    pass
lb.beautify(table_number = 5, constraint = False)
```

<!-- #region kernel="python3" Collapsed="false" -->
### 06: Sector Concentration,continuous var and share SOE

Use Herfindhal value and interact it with different SOE share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 06_conc_ind_soe

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1I3cyQya2ctpWqxDrXkDUtpznZSaRaH7J)
<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="false" -->
#### Code
<!-- #endregion -->

```sos kernel="R" Collapsed="false"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2,
    t3,
    t4,
    t5,
    t6
),
    title='Baseline results revision: concentration',
    addFE=fe1,
    save=TRUE,
    name="table_6.txt"
)
```

```sos kernel="python3" Collapsed="false"
import os
try:
    os.remove("table_6.tex")
except:
    pass
lb.beautify(table_number = 6, constraint = False)
```

<!-- #region kernel="python3" Collapsed="false" -->
## Herfindhal city-industry

We replicate the above three tables but instead of using the herfindahl at the industry level, we use the industry-city. Since we now have a variation city-industry, we estimate a new coefficient -> `Period * polluted * concentration`
<!-- #endregion -->

```sos kernel="SoS" Collapsed="false"
import numpy as np
```

```sos Collapsed="false" kernel="SoS"
df_herfhindal_final = df_final.merge(df_herfhindal,
                                     on=['geocode4_corr', 'industry'],
                                     how='left',
                                     indicator=True

                                     )
df_herfhindal_final['df_herfhindal_final'] = df_herfhindal_final['Herfindahl'].fillna(
    0)
df_herfhindal_final['Herfindahl'].describe()
```

```sos Collapsed="false" kernel="SoS"
df_herfhindal_final['Herfindahl'].quantile([.1,
                                            .15,
                                            .25,
                                            .5,
                                            .70,
                                            .75,
                                            .80,
                                            .85,
                                            .95])
```

```sos Collapsed="false" kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = df_herfhindal_final.assign(
concentrated_25 = lambda x: np.where(x['Herfindahl'] > 0.287788,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_50 = lambda x: np.where(x['Herfindahl'] > 0.511218,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_75 = lambda x: np.where(x['Herfindahl'] > 0.779449,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_85 = lambda x: np.where(x['Herfindahl'] > 0.916762,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
)
```

```sos Collapsed="false" kernel="R"
path = "functions/SBC_pollution_R.R"
source(path)
path = "functions/SBC_pollutiuon_golatex.R"
source(path)

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
         concentrated_25 = relevel(concentrated_25, ref='NOT_CONCENTRATED'),
         concentrated_50 = relevel(concentrated_50, ref='NOT_CONCENTRATED'),
         concentrated_75 = relevel(concentrated_75, ref='NOT_CONCENTRATED'),
         concentrated_85 = relevel(concentrated_85, ref='NOT_CONCENTRATED'),
  )
head(df_final)
```

<!-- #region kernel="R" Collapsed="false" -->
### 07: Sector Concentration: city-industry

Interaction with a concentration dummy

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 07_concentration_city_ind

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1FkB09EXfUmsxOsHd8FfWN4rDoX8Gtq97)
<!-- #endregion -->

<!-- #region kernel="R" Collapsed="false" -->
#### Code
<!-- #endregion -->

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(
             c("City-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1, t2, t3,t4, t5, t6, t7, t8
),
    title='Baseline results revision: concentration city-industry',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos kernel="python3" Collapsed="false"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos Collapsed="false" kernel="python3"
import os
try:
    os.remove("table_2.tex")
except:
    pass
lb.beautify(table_number = 2, constraint = False, city_industry = True)
```

<!-- #region kernel="python3" Collapsed="false" -->
### 08: Sector Concentration and output share: city-industry

Interaction with a concentration dummy and include SOE output share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 08_concentrated_ind_SOE_city_ind

In Google Drive:

![](https://drive.google.com/uc?export=view&id=1_WqkGLG26pLXNNRPRRDRmQII4p7n0mIp)
<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="false" -->
#### Code
<!-- #endregion -->

```sos kernel="R" Collapsed="false"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
           +TCZ_c * Period *polluted_thre * out_share_SOE
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * concentrated_25
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t7 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t8 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(
             c("City-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "No", "No", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1, t2, t3,t4, t5, t6, t7, t8
),
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_3.txt"
)
```

```sos kernel="python3" Collapsed="false"
import os
try:
    os.remove("table_3.tex")
except:
    pass
lb.beautify(table_number = 3, constraint = False, city_industry = True)
```

<!-- #region kernel="python3" Collapsed="false" -->
### 09: Sector Concentration, continuous var and share SOE: city-industry

Use Herfindhal value and interact it with different SOE share

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527
    - 09_conc_ind_soe_city_ind

In Google Drive:

![](https://drive.google.com/uc?export=view&id=18qgSIo_0ZTeuXXDsf6MTnEDZjYJoD0ab)
<!-- #endregion -->

<!-- #region kernel="python3" Collapsed="false" -->
#### Code
<!-- #endregion -->

```sos kernel="R" Collapsed="false"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t5 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

t6 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * Herfindahl
           +TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              FE_t_c + FE_t_i + FE_c_i | 0 |
             industry, data= df_final,
             exactDOF=TRUE)

fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "No","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "No", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "No", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2,
    t3,
    t4,
    t5,
    t6
),
    title='Baseline results revision: concentration',
    addFE=fe1,
    save=TRUE,
    name="table_4.txt"
)
```

```sos kernel="python3" Collapsed="false"
import os
try:
    os.remove("table_4.tex")
except:
    pass
lb.beautify(table_number = 4, constraint = False, city_industry = True)
```
