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
# Re-estimate table 3

* Table 3: estimate two models
  * Model 1: target x period x polluted 
  * Model 2: target x polluted x period x share 
    * output/capital/employment
* All sample
* Subsample
  * TCZ
  * SPZ
  * Coastal
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

<!-- #region kernel="Python 3" -->
# Load Data
<!-- #endregion -->

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
```

```sos kernel="R"
options(warn=-1)
shhh <- suppressPackageStartupMessages
shhh(library(tidyverse))
shhh(library(lfe))
shhh(library(lazyeval))
shhh(library('progress'))

path = "../functions/SBC_pollution_R.R"
source(path)
path = "../functions/SBC_pollutiuon_golatex.R"
source(path)
```

<!-- #region kernel="R" -->
### Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="R"
df_TCZ_list_china = read_csv('../df_TCZ_list_china.csv',
                            col_types = cols(
  Province = col_character(),
  City = col_character(),
  geocode4_corr = col_double(),
  TCZ = col_double(),
  SPZ = col_double()
)) %>% 
select(-c(TCZ, Province)) %>% 
left_join(df_final, by = 'geocode4_corr') %>%
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

<!-- #region kernel="R" -->
# Table 3

## Models to estimate 

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k} \right)+\nu_{it}+\lambda_{kt}+\phi_{ck}+\epsilon_{i k t}
$$

$$
Log SO2 emission _{i k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k} \times \text{Share X}_{i}\right)+\nu_{it}+\lambda_{kt}+\phi_{ck}+\epsilon_{i k t}
$$

- Estimate full sample
- Estimate subsample
    * TCZ
    * SPZ
    * Coastal
<!-- #endregion -->

```sos kernel="SoS"
list(df_final)
```

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

<!-- #region kernel="R" -->
## Full Sample 
<!-- #endregion -->

```sos kernel="R"
toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)

t1 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)
t1 <-change_target(t1)

t2 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre * out_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)
t2 <-change_target(t2)

t3 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre * cap_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)
t3 <-change_target(t3)

t4 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre * lab_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china,
             exactDOF=TRUE)
t4 <-change_target(t4)

tables <- list(t1, t2, t3,t4)

fe1 <-  list(c("City-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", "Yes")
             )


table_1 <- go_latex(tables,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title="Table 3- Replicate Target Full sample",
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name="table_1.txt"
                            )
```

```sos kernel="Python 3"
import os
decile=['& Full', 'Output', 'Capital',
        'Employment']

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

<!-- #region kernel="Python 3" -->
## SubSample 

- Three subsamples
    * TCZ
    * SPZ
    * Coastal

- 4 models
    * target x period x polluted
    * target x period x polluted x share Output
    * target x period x polluted x share Capital
    * target x period x polluted x share Employment
<!-- #endregion -->

```sos kernel="R"
fe1 <-  list(c("City-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("Industry-year fixed effects", "Yes", "Yes", "Yes", "Yes"),
             c("City-industry fixed effects", "Yes", "Yes", "Yes", "Yes")
             )

toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)
i = 1
for (c in list(1,2)){
    for (subsample in list("TCZ_c", "Coastal", "SPZ")){
        if (subsample == "TCZ_c"){
            if (c == 1){
                filter_ = 'TCZ'
                n = "Yes"
            }else{
                filter_ = 'No_TCZ'
                n = "No"
                }
        }else if (subsample == "Coastal"){
            if (c == 1){
                filter_ = TRUE
                n = "Yes"
            }else{
                filter_ = FALSE
                n = "No"
                }
        }else if (subsample == "SPZ"){
            if (c == 1){
                filter_ = 1
                n = "Yes"
            }else{
                filter_ = 0
                n = "No"
            }
        }
        
        t1 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre 
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(get(subsample) == filter_),
             exactDOF=TRUE)
        t1 <-change_target(t1)

        t2 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre * out_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(get(subsample) == filter_),
             exactDOF=TRUE)
        t2 <-change_target(t2)

        t3 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre * cap_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(get(subsample) == filter_),
             exactDOF=TRUE)
        t3 <-change_target(t3)

        t4 <- felm(formula=log(tso2_cit) ~ 
           target_c * Period * polluted_thre * lab_share_SOE
           + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_t_i + FE_c_i  | 0 |
             industry, data= df_TCZ_list_china %>% filter(get(subsample) == filter_),
             exactDOF=TRUE)
        t4 <-change_target(t4)

        tables <- list(t1, t2, t3,t4)

        name = paste0("table_", i, ".txt")
        table_1 <- go_latex(tables,
                dep_var = "Dependent variable \\text { SO2 emission }_{i k t}",
                title=paste0("Table 3- Replicate Target ", subsample, " ", n),
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name=name
                            )
        i = i+1
    }
}
```

```sos kernel="Python 3"
decile=['& Full', 'Output', 'Capital',
        'Employment']

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""
x = [a for a in os.listdir() if a.endswith(".txt")]
for i, val in enumerate(x):
    lb.beautify(table_number = i+1,
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

```sos kernel="SoS"
import os, time, shutil
from pathlib import Path

filename = '09_SBC_pollution_China_Revision_table_3'
source = filename + '.ipynb'
source_to_move = filename +'.html'
path = os.getcwd()
parent_path = str(Path(path).parent)
path_report = "{}/Reports".format(parent_path)
dest = os.path.join(path_report, filename)+'_.html'

os.system('jupyter nbconvert --no-input --to html {}'.format(source))

time.sleep(5)
shutil.move(source_to_move, dest)
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass
```
