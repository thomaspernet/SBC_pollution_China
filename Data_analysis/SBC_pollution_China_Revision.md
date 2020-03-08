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

<!-- #region Collapsed="false" kernel="SoS" -->
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

<!-- #region kernel="SoS" Collapsed="false" -->
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

<!-- #region kernel="SoS" Collapsed="false" -->
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
path = "SBC_pollution_R.R"
source(path)
path = "SBC_pollutiuon_golatex.R"
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
## Comment Empirical analysis:

First of all, notice again that there is no convincing evidence that SOEs shifts the burden of the environmental adaptation to private firms. In most of the cases, there are interaction terms with three or even form variables in the regression equation. My major concern is if the authors have also included all the sublevel interaction terms in the regression. For instance, in equation (1), there is an interaction term of four variables, TCZi, Polluting sectorsk, Period, Share SOEk. However, it seems in table 3 not all the corresponding triple interaction terms (such as TCZi *Polluting sectorsk *Share SOEk) are controlled. 

## Answers:

Compute the following equation to show the fixed effect tackle the "missing" coefficients

$$EQUATION$$

CF this [paper](https://drive.google.com/file/d/1-SXSlRoS_2ZW7CK6XMhcXpJDPxAEF1xG/view)

Output latex table available here

- https://www.overleaf.com/project/5deca0097e9f3a0001506527

<!-- #endregion -->

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes",
               "Yes"),
             c("Industry fixed effects", "Yes", "Yes"),
             c("Year fixed effects", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2
),
    title='Revision results',
    addFE=fe1,
    save=TRUE,
    name="table_1_revision.txt"
)
```

```sos Collapsed="false" kernel="python3"
import latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 1)
```

<!-- #region Collapsed="true" kernel="python3" -->
### Redo table 1
<!-- #endregion -->

```sos Collapsed="false" kernel="R"
t0_ <- felm(formula=log(tso2_cit) ~ TCZ_c * Period 
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
t1_ <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t0 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='count_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                   cluster= 'industry',
                   print=FALSE)
t1 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='out_share_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                  cluster= 'industry',
                   print=FALSE)
t2 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='cap_share_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                  cluster= 'industry',
                   print=FALSE)
t3 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='lab_share_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                  cluster= 'industry',
                   print=FALSE)
fe1 <- list(c("City-year fixed effects", "No", "No", "Yes","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "Yes", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "Yes", "Yes", "Yes","Yes")
             )

table_1 <- go_latex(list(
    t0_,
    t1_,
    t0,
    t1,
    t2,
    t3
),
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 2)
```

<!-- #region Collapsed="false" kernel="python3" -->
### Redo table 1: All variables
<!-- #endregion -->

```sos Collapsed="false" kernel="R"
t0 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * lab_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t3 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='out_share_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                  cluster= 'industry',
                   print=FALSE)

t4 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='cap_share_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                  cluster= 'industry',
                   print=FALSE)

t5 <- final_model(df=df_final,
                   target='TCZ_c',
                   SOE='lab_share_SOE',
                   pol='polluted_thre',
                   control=TRUE,
                  cluster= 'industry',
                   print=FALSE)
```

```sos Collapsed="false" kernel="R"
fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Industry fixed effects", "Yes", "Yes", "Yes", "No", "No", "No"),
             c("Yes fixed effects","Yes", "Yes", "Yes", "No", "No", "No"),
             c("City-year fixed effects", "No", "No", "Yes","Yes", "Yes","Yes"),
             c("Industry-year fixed effects", "No", "No", "Yes", "Yes", "Yes","Yes"),
             c("City-industry fixed effects", "No", "No", "Yes", "Yes", "Yes","Yes")
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
    name="table_3.txt"
)
```

```sos Collapsed="false" kernel="python3"
import latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 3)
```

<!-- #region Collapsed="true" kernel="python3" -->
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
path = "SBC_pollution_R.R"
source(path)
path = "SBC_pollutiuon_golatex.R"
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

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
t3 <-felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2,
    t3
),
    title='Revision results: Foreign',
    addFE=fe1,
    save=TRUE,
    name="table_1.txt"
)
```

```sos Collapsed="false" kernel="python3"
import latex_beautify as lb

%load_ext autoreload
%autoreload 2
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 1)
```

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
             + TCZ_c * Period * polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
             + TCZ_c * Period * polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
             + TCZ_c * Period * polluted_thre * lab_share_SOE	
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)
```

```sos Collapsed="false" kernel="R"
fe1 <- list(c("City-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1,
    t2,
    t3
),
    title='Revision results: Foreign - SOE',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 2)
```

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * out_share_for	
             + TCZ_c * Period * polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              cityen +  year + industry  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * cap_share_for	
             + TCZ_c * Period * polluted_thre * cap_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
              cityen +  year + industry | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period * polluted_thre * lab_share_for	
             + TCZ_c * Period * polluted_thre * lab_share_SOE	
                  + output_fcit + capital_fcit + labour_fcit
                  |
              cityen +  year + industry  | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

fe1 <- list(c("City fixed effects", "Yes", "Yes", "Yes"),
             c("Industry fixed effects", "Yes", "Yes", "Yes"),
             c("Yes fixed effects","Yes", "Yes", "Yes")
           )

table_1 <- go_latex(list(
    t1,
    t2,
    t3
),
    title='Revision results: Foreign - SOE',
    addFE=fe1,
    save=TRUE,
    name="table_2.txt"
)
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 2)
```

<!-- #region Collapsed="false" kernel="python3" -->
## Herfinhdla
<!-- #endregion -->

```sos Collapsed="false" kernel="SoS"

df_test = df_final.merge(df_herfhindal,
              on = ['geocode4_corr', 'industry'],
               how = 'left'
              )
df_test['Herfindahl'] = df_test['Herfindahl'].fillna(0)

```

```sos Collapsed="false" kernel="SoS"
df_test['Herfindahl'].describe()
```

```sos Collapsed="false" kernel="SoS"
import seaborn as sns
import matplotlib.pyplot as plt
sns.distplot(df_test['Herfindahl'])
```

```sos Collapsed="false" kernel="SoS"
df_test['Herfindahl'].quantile([.1, .5,.70, .75,.80, .85, .95])
```

```sos Collapsed="false" kernel="SoS"
%put df_test --to R
import numpy as np
df_test = df_test.assign(
concentrated_25 = lambda x: np.where(x['Herfindahl'] > 0.280070,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_50 = lambda x: np.where(x['Herfindahl'] > 0.503871,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_75 = lambda x: np.where(x['Herfindahl'] > 0.775389,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
concentrated_85 = lambda x: np.where(x['Herfindahl'] > .910054,
                                 "CONCENTRATED",
                                 'NOT_CONCENTRATED'),
)
```

```sos Collapsed="false" kernel="SoS"
df_test.groupby('concentrated_75')['concentrated_75'].count()
```

```sos Collapsed="false" kernel="SoS"
df_test.groupby('concentrated_85')['concentrated_85'].count()
```

```sos Collapsed="false" kernel="R"
path = "SBC_pollution_R.R"
source(path)
path = "SBC_pollutiuon_golatex.R"
source(path)

df_final <- df_test %>% 
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

```sos Collapsed="false" kernel="R"

```

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_25
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t4 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_85
                  + output_fcit + capital_fcit + labour_fcit
                  |
               FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

fe1 <- list(
             c("City-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1, t2, t3,t4
),
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_6.txt"
)
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 6)
```

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_25
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t2 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_50
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

t3 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * concentrated_75
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i | 0 |
             cityen, data= df_final,
             exactDOF=TRUE)

fe1 <- list(
             c("City-year fixed effects", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes")
             )

table_1 <- go_latex(list(
    t1, t2, t3
),
    title='Baseline results revision',
    addFE=fe1,
    save=TRUE,
    name="table_3.txt"
)
```

```sos Collapsed="false" kernel="python3"
lb.beautify(table_number = 3)
```

```sos Collapsed="false" kernel="R"
t1 <- felm(formula=log(tso2_cit) ~ TCZ_c * Period *polluted_thre * out_share_SOE
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i| 0 |
             cityen, data= df_final %>% filter(concentrated == 'CONCENTRATED'),
             exactDOF=TRUE)
summary(t1)
```
