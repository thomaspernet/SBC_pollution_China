---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.4.2
  kernelspec:
    display_name: SoS
    language: sos
    name: sos
---

<!-- #region kernel="SoS" -->
# Final tables: TFP
    
## Instruction Notebook

The notebook allows the user to construct to different level of aggregation:

- `industry`
- `geocode4_corr` -> city

By default, the `aggregation_param` parameter is set to `industry`. To switch to city, change for `geocode4_corr`. Then launch the notebook for new results

In the paper, we define a threshold to distinguish cities or industries. Choose among this set of threshold:

- 5
- 6
- 7
- 8
- mean

By default, the `threshold_full` parameter is set to `6`. To switch to another threshold, change the threshold `threshold_full`. Then launch the notebook for new results

## TFP

$$ TFP _{i k t}=\alpha\left(\text { Period } \times \text { Target }{i} \times \text { Polluting sectors }{k} \right)+\nu{i}+\lambda_{t}+\phi_{k}+\epsilon_{i k t} $$

$$ TFP _{i k t}=\alpha\left(\text { Period } \times \text { Target }{i} \times \text { Polluting sectors }{k} \right)+\nu_{ct}+\lambda_{kt}+\phi_{ck}+\epsilon_{i k t} $$



<!-- #endregion -->

```sos kernel="SoS"
import pandas as pd
from Fast_connectCloud import connector
import numpy as np
```

```sos kernel="Python 3"
import sys, os, shutil
sys.path.insert(0,'..')
```

```sos kernel="Python 3"
import functions.latex_beautify as lb

%load_ext autoreload
%autoreload 2
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

```sos kernel="SoS"
from GoogleDrivePy.google_platform import connect_cloud_platform
project = 'valid-pagoda-132423'

gs = connector.open_connection(online_connection = False,
                              path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth')

service = gs.connect_remote('GCP')

gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service['GoogleCloudP']) 
```

<!-- #region kernel="SoS" -->
# Load Data

## Paper dataset

<!-- #endregion -->

```sos kernel="SoS"
%put df_final --to R
#query = (
#          "SELECT * "
#            "FROM China.TFP_SBC_firm "

#        )

#df_final = gcp.upload_data_from_bigquery(query = query, location = 'US')
#df_final.head()
df_final = pd.read_csv('../01_TFP_SBC_firm.gz')
```

```sos kernel="SoS"
aggregation_param = 'geocode4_corr'
list_agg = df_final[aggregation_param].to_list()

threshold_full = 6
```

```sos kernel="R"
%put aggregation_param --to R
%put threshold_full --to R
```

<!-- #region kernel="R" -->
## Compute Herfhindal: proxy Size

$$
H=\sum_{i=1}^{N} s_{i}^{2}
$$

where $s_i$ is the market share of industry[city] $i$ in a city [industry], and $N$ is the number of firms. 

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by city-industry: `market_share_cit`
- Step 2: compute the sum of squared market share by industry[city]: `Herfindahl_agg_t`
- Step 3: Compute the average across time: `Herfindahl_agg`
- Step 4: Compute the deciles of step 3: `decile_herfhindal_agg`
    - Low decile implies a low concentration within sectors
    - High decile implies a high concentration within sectors
<!-- #endregion -->

```sos kernel="SoS"
query = """
WITH sum_cit AS (
  SELECT geocode4_corr, cic as industry, sum(output) as sum_o_cit, year
  FROM China.asif_firm_china 
  WHERE year >= 2002 AND year <= 2007
  AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
  GROUP BY geocode4_corr, cic, year
) 
SELECT * 
FROM 
  (WITH sum_agg_t AS (
    SELECT {0}, SUM(sum_o_cit) as sum_o_agg_t, year
    FROM sum_cit
    WHERE year >= 2002 AND year <= 2007
    GROUP BY year, {0}
)
SELECT *
FROM
  (WITH ms_cit AS (
    SELECT  sum_cit.industry, sum_cit.geocode4_corr, sum_cit.year,
    sum_cit.sum_o_cit/NULLIF(sum_agg_t.sum_o_agg_t, 0) as market_share_cit
    FROM sum_cit
    LEFT JOIN sum_agg_t
ON (
sum_cit.year = sum_agg_t.year AND 
sum_cit.{0} = sum_agg_t.{0}
)
)
SELECT *
FROM
  (WITH agg_1 AS (
SELECT {0}, SUM(POW(market_share_cit, 2)) as Herfindahl_agg_t,
year
FROM ms_cit
GROUP BY year, {0}
ORDER BY year, {0} 
)
SELECT *
FROM (
SELECT {0},
AVG(Herfindahl_agg_t) as Herfindahl_agg
FROM agg_1
GROUP BY {0}
ORDER BY {0}
)

)))
"""
df_herfhindal = (gcp.upload_data_from_bigquery(
    query = query.format(aggregation_param),
                                         location = 'US')
                 .loc[lambda x: x[aggregation_param].isin(list_agg)]
                )
```

<!-- #region kernel="SoS" -->
### Load chinese_city_characteristics from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos kernel="Python 3"
#from Fast_connectCloud import connector
#from GoogleDrivePy.google_drive import connect_drive
#import pandas as pd
#import numpy as np

#gs = connector.open_connection(online_connection = False, 
#	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

#service_gd = gs.connect_remote(engine = 'GS')

#gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])
```

```sos kernel="SoS"
%put df_herfhindal_final --to R
df_herfhindal_final = (df_final.merge(df_herfhindal,
                                     on=[aggregation_param],
                                     how='left',
                                     indicator=True
                                     )
                       .assign(
                       decile_herfhindal = lambda x:
                           pd.qcut(x['Herfindahl_agg'],10, labels=False),
                       mean_herfhindal= 
                           lambda x: np.where(
                               x["Herfindahl_agg"] > 
                               x["Herfindahl_agg"].drop_duplicates().mean(),
                               1,0
                           ),
                       third_herfhindal= 
                           lambda x: np.where(
                               x["Herfindahl_agg"] >
                               (x["Herfindahl_agg"]
                                .drop_duplicates()
                                .quantile([.75])
                                .values[0]),
                               1,0
                           ),
                     threshold_herfhindal= 
                           lambda x: np.where(
                               x["decile_herfhindal"] > threshold_full,
                               1,0
                           )
                           
                       )
                      )
```

```sos kernel="SoS"
%put df_chinese_city_characteristics --to R
df_chinese_city_characteristics = (df_final.merge(
    pd.read_csv('../df_chinese_city_characteristics.csv'),
    on = ['year','geocode4_corr']
).assign(
    threshold_tcz= 
                           lambda x: np.where(
                               x["gdp_cap"] > 18661,
                               1,0
                           ),
    threshold_concentrated= 
                           lambda x: np.where(
                               x["gdp_cap"] > 31244,
                               1,0
                           ),
    threshold_soe_output= 
                           lambda x: np.where(
                               x["gdp_cap"] > 17864,
                               1,0
                           ),
    threshold_soe_capital= 
                           lambda x: np.where(
                               x["gdp_cap"] > 18809,
                               1,0
                           ),
    threshold_soe_employment= 
                           lambda x: np.where(
                               x["gdp_cap"] > 22467,
                               1,0
                           ),
    #threshold_full= 
    #                       lambda x: np.where(
    #                           x["gdp_cap"] > 41247,
    #                           1,0
    #                       )
)
                                  )
df_chinese_city_characteristics.shape
```

```sos kernel="SoS"
(df_chinese_city_characteristics
 .groupby(['OWNERSHIP','threshold_concentrated'
          ])['threshold_concentrated'].count())
```

```sos kernel="R"
df_final <- df_final %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

```sos kernel="R"
df_herfhindal_final <- df_herfhindal_final %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

```sos kernel="R"
df_chinese_city_characteristics <- df_chinese_city_characteristics %>% 
    mutate_if(is.character, as.factor) %>%
    mutate_at(vars(starts_with("FE")), as.factor) %>%
    mutate(
         Period = relevel(Period, ref='Before'),
         TCZ_c = relevel(TCZ_c, ref='No_TCZ'),
         polluted_thre = relevel(polluted_thre, ref='Below'),
  )
```

<!-- #region kernel="SoS" -->
# Table TFP

$$
TFP _{fi k t}=\alpha\left(\text { Period } \times \text { Target }_{i} \times \text { Polluting sectors }_{k} \right)+\nu_{i}+\lambda_{t}+\phi_{k}+\epsilon_{i k t}
$$

1. Full sample
2. SOE dominated
3. TCZ vs No TCZ
4. Coastal vs No Coastal
3. Kuznet threshold
    - TCZ: 18661
    - Concentrated: 31244
    - SOE output: 17864
    - SOE Capital: 18809
    - SPE employment: 22467
    
<!-- #endregion -->

<!-- #region kernel="R" -->
## TCZ and concentration

Ouput: 

- Overleaf
    - Temp_tables/Tables_paper/02_paper_version_2/07_DC_TFP_Coastal
    - Temp_tables/Tables_paper/02_paper_version_2/08_DC_TFP_TCZ
    - Temp_tables/Tables_paper/02_paper_version_2/09_DC_TFP_Concentrated
    - Temp_tables/Tables_paper/02_paper_version_2/10_DC_TFP_kuznet
- Google Drive
    - [07_DC_TFP_Coastal](https://drive.google.com/open?id=14Vw0gcUKM9Si2M0vG_HJmY7EckA0ETKG)
![](https://drive.google.com/uc?export=view&id=14Vw0gcUKM9Si2M0vG_HJmY7EckA0ETKG)
    - [08_DC_TFP_TCZ](https://drive.google.com/open?id=1GjuPRyb66Bh_SOF7aZFKzdtpqrqJIPI3)
![](https://drive.google.com/uc?export=view&id=1GjuPRyb66Bh_SOF7aZFKzdtpqrqJIPI3)
    - [09_DC_TFP_Concentrated](https://drive.google.com/open?id=1BNZ4Zudj30k7Gtwt0DtZkkjpeo0H3ovh)
![](https://drive.google.com/uc?export=view&id=1BNZ4Zudj30k7Gtwt0DtZkkjpeo0H3ovh)
    - [10_DC_TFP_kuznet](https://drive.google.com/open?id=1gkbgj42_Qfk4c9rDXgyiOwFrUokcPrhr)
![](https://drive.google.com/uc?export=view&id=1gkbgj42_Qfk4c9rDXgyiOwFrUokcPrhr)
<!-- #endregion -->

```sos kernel="R"
var_ <- 'threshold_herfhindal'
df_to_filter <- df_final

i = 3
fe1 <- list(
    c("Firm", "Yes", "Yes", "Yes", "Yes"),
    c("City-industry", "No", "No", "Yes", "Yes", "Yes", "Yes"),
    c("City-time", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("time-industry", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

for ( var in c(#"Coastal", "TCZ_c", 
               var_)){
    
    if (var == "Coastal"){
        filters <- TRUE  
        title_name = "Reduction mandate and TFP: Coastal versus non-Coastal"
    }else if (var == "TCZ_c"){
        filters <- "TCZ"   
        title_name = "Reduction mandate and TFP: TCZ versus non-TCZ"
    }else if (var == var_) {
        filters <- 1
        df_to_filter <- df_herfhindal_final
        title_name = "Reduction mandate and TFP: industrial concentration"
    }
    
    t1 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) == filters & 
                     OWNERSHIP == 'SOE'
                 ),
                 exactDOF=TRUE)

    t2 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) != filters&
                     OWNERSHIP == 'SOE'
                 ),
                 exactDOF=TRUE)

    t3 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) == filters & 
                     OWNERSHIP != 'SOE'
                 ),
                 exactDOF=TRUE)

    t4 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) != filters & 
                     OWNERSHIP != 'SOE'
                 ),
                 exactDOF=TRUE)

    name = paste0("table_",i,".txt")
    title = title_name
    tables <- list(t1, t2, t3, t4)
    table_1 <- go_latex(tables,
                dep_var = "Dependent variable \\text { TFP }_{fikt}",
                title=title,
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name=name)
    i = i+1
    print(title)
}
```

```sos kernel="Python 3"
jupyter_preview = False

tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""

multicolumn = {
    'SOE': 2,
    'PRIVATE': 2,
}

new_row = [
    ['& Coastal', 'NO Coastal',
     'Coastal', 'NO Coastal'],
    ['& TCZ', 'NO TCZ',
     'TCZ', 'NO TCZ'],
    ['& Concentrated', 'NO Concentrated',
     'Concentrated', 'NO Concentrated']
]
x = [a for a in os.listdir() if a.endswith(".txt")]
for i, val in enumerate(x):
    lb.beautify(table_number = i+1,
            remove_control= False,
            constraint = True,
            city_industry = False, 
            new_row = new_row[i],
            multicolumn = multicolumn,
            table_nte =tb,
           jupyter_preview = jupyter_preview,
           resolution = 700)
    
if jupyter_preview == False:
    source_to_move = ['table_1.tex',
                      'table_2.tex',
                      'table_3.tex'
                     ]
    dest = [
        'Overleaf/07_DC_TFP_Coastal.tex',
        'Overleaf/08_DC_TFP_TCZ.tex', 
        'Overleaf/09_DC_TFP_Concentrated.tex'
           ]
    for i, v in enumerate(source_to_move):
        shutil.move(
            v,
            dest[i]
        )
```

<!-- #region kernel="Python 3" -->
## Kuznet

cf: https://github.com/thomaspernet/SBC_pollution_China/blob/master/Data_analysis/06_TFP/01_TFP_analysis.md#with-firms-fixed-effect

Too long to reestimate
- overleaf table: 

Google Drive

![Kuznet](https://drive.google.com/uc?export=view&id=108G-uRs074klH_bIG7EQ0_PfsAxHj45L)
<!-- #endregion -->

```sos kernel="R"
df_to_filter %>% group_by(OWNERSHIP, threshold_concentrated) %>%
tally()
```

```sos kernel="R"

summary(felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     threshold_concentrated == 1 & 
                     OWNERSHIP == 'SOE'
                 ),
                 exactDOF=TRUE)
       )
```

```sos kernel="R"
toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)

var_ <- 'threshold_herfhindal'
df_to_filter <- df_final

i = 1
fe1 <- list(
    c("Firm", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("City-industry-ownership", "Yes", "Yes", "No", "No", "No", "No"),
    c("time-ownership", "Yes", "Yes", "No", "No", "No", "No"),
    c("City-industry", "No", "No", "Yes", "Yes", "Yes", "Yes"),
    c("City-time", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("time-industry", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

for ( var in c(#"TCZ_c", 
               #var_,
               "threshold_tcz",
               "threshold_concentrated", # ok
               "threshold_soe_output",
               "threshold_soe_capital",
               "threshold_soe_employment")){
    
    if (var == "Coastal"){
        filters <- TRUE  
        title_name = "Coastal"
    }else if (var == "TCZ_c"){
        filters <- "TCZ"   
        title_name = "TCZ"
    }else if (var == var_) {
        filters <- 1
        df_to_filter <- df_herfhindal_final
        title_name = "Herfhindhal"
    }else if ( 
              var == "threshold_tcz"|
              var == "threshold_concentrated"|
              var ==  "threshold_soe_output"|
              var ==  "threshold_soe_capital"|
              var ==  "threshold_soe_employment"|
              var ==  "threshold_full"
    ){
        filters <- 1
        df_to_filter <- df_chinese_city_characteristics
        title_name <- str_extract(var, regex("[^_]+$"))
    }
    
    #t1 <- felm(formula= tfp_OP ~ 
    #       target_c  * Period * polluted_thre * OWNERSHIP|
    #          id + FE_c_i_o + FE_t_o  + FE_t_c    
    #          | 0 |
    #         industry, data= df_to_filter %>% filter(get(var) == filters
                                                    #&occurence != 1
    #                                                ),
    #        exactDOF=TRUE)
           
    #t2 <- felm(formula= tfp_OP ~ 
    #           target_c  * Period * polluted_thre * OWNERSHIP|
    #              id + FE_c_i_o + FE_t_o  + FE_t_c    
    #              | 0 |
    #             industry, data= df_to_filter %>% filter(get(var) != filters
    #                                                    #&occurence != 1
    #                                                    ),
    #             exactDOF=TRUE)

    t3 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) == filters & 
                     OWNERSHIP == 'SOE'
                 #&occurence != 1
                 ),
                 exactDOF=TRUE)

    t4 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) != filters&
                     OWNERSHIP == 'SOE'
                 #&occurence != 1
                 ),
                 exactDOF=TRUE)

    t5 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) == filters & 
                     OWNERSHIP != 'SOE'
                     #&occurence != 1
                 ),
                 exactDOF=TRUE)

    t6 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) != filters & 
                     OWNERSHIP != 'SOE'
                 #&occurence != 1
                 ),
                 exactDOF=TRUE)

    name = paste0("table_",i,".txt")
    title = paste0("TFP subsample - ", title_name)
    tables <- list(t3, t4, t5, t6)
    table_1 <- go_latex(tables,
                dep_var = "Dependent variable \\text { TFP }_{fi k t}",
                title=title,
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name=name)
    i = i+1
    print(title)
}
```

```sos kernel="Python 3"
tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""

multicolumn = {
    'Dummy': 2,
    'SOE': 2,
    'PRIVATE': 2,
}

new_row = [
    ['& Coastal', 'NO Coastal',
     'Coastal', 'NO Coastal',
     'Coastal', 'NO Coastal']
          ,
    ['& TCZ', 'NO TCZ',
     'TCZ', 'NO TCZ',
     'TCZ', 'NO TCZ'],
    ['& Concentrated', 'NO Concentrated',
     'Concentrated', 'NO Concentrated',
     'Concentrated', 'NO Concentrated'],
['& Right', 'Left',
     'Right', 'Left',
     'Right', 'Left'],
['& Right', 'Left',
     'Right', 'Left',
     'Right', 'Left'],
['& Right', 'Left',
     'Right', 'Left',
     'Right', 'Left'],
['& Right', 'Left',
     'Right', 'Left',
     'Right', 'Left'],
['& Right', 'Left',
     'Right', 'Left',
     'Right', 'Left']
          ]
           
x = [a for a in os.listdir() if a.endswith(".txt")]
for i, val in enumerate(x):
    lb.beautify(table_number = i+1,
            remove_control= False,
            constraint = True,
            city_industry = False, 
            new_row = new_row[i],
            multicolumn = multicolumn,
            table_nte =False,
            jupyter_preview = True,
            resolution = 150)
```

<!-- #region kernel="Python 3" -->
### hefhindal with decile

For the baseline, use decile 6
<!-- #endregion -->

```sos kernel="R"
var <- 'decile_herfhindal'
df_to_filter <- df_herfhindal_final
toremove <- dir(path=getwd(), pattern=".tex|.pdf|.txt")
file.remove(toremove)

i = 1
fe1 <- list(
    c("Firm", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("City-industry-ownership", "Yes", "Yes", "No", "No", "No", "No"),
    c("time-ownership", "Yes", "Yes", "No", "No", "No", "No"),
    c("City-industry", "No", "No", "Yes", "Yes", "Yes", "Yes"),
    c("City-time", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("time-industry", "No", "No", "Yes", "Yes", "Yes", "Yes")
             )

i= 1
for (decile in list(5, 6, 7, 8)){
    filters <- decile
    
    t1 <- felm(formula= tfp_OP ~ 
           target_c  * Period * polluted_thre * OWNERSHIP|
              id + FE_c_i_o + FE_t_o  + FE_t_c    
              | 0 |
             industry, data= df_to_filter %>% filter(get(var) <= filters
                                                    #&occurence != 1
                                                    ),
             exactDOF=TRUE)
           
    t2 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre * OWNERSHIP|
                  id + FE_c_i_o + FE_t_o  + FE_t_c     
                  | 0 |
                 industry, data= df_to_filter %>% filter(get(var) > filters
                                                        #&occurence != 1
                                                        ),
                 exactDOF=TRUE)

    t3 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) <= filters & 
                     OWNERSHIP == 'SOE'
                 #&occurence != 1
                 ),
                 exactDOF=TRUE)

    t4 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) > filters&
                     OWNERSHIP == 'SOE'
                 #&occurence != 1
                 ),
                 exactDOF=TRUE)

    t5 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) <= filters & 
                     OWNERSHIP != 'SOE'
                     #&occurence != 1
                 ),
                 exactDOF=TRUE)

    t6 <- felm(formula= tfp_OP ~ 
               target_c  * Period * polluted_thre |
                  id + FE_t_c + FE_t_i + FE_c_i
                  | 0 |
                 industry, data= df_to_filter %>% filter(
                     get(var) > filters & 
                     OWNERSHIP != 'SOE'
                 #&occurence != 1
                 ),
                 exactDOF=TRUE)

    name = paste0("table_",i,".txt")
    title = paste0("TFP subsample - ", title_name, " decile ", decile)
    tables <- list(t1, t2, t3, t4, t5, t6)
    table_1 <- go_latex(tables,
                dep_var = "Dependent variable \\text { TFP }_{fi k t}",
                title=title,
                addFE=fe1,
                save=TRUE,
                note = FALSE,
                name=name)
    i = i+1
    print(title)
    
}
```

```sos kernel="Python 3"
tb = """\\footnotesize{
Due to limited space, only the coefficients of interest are presented 
for the regressions with city,industry, year fixed effect (i.e. columns 1-3).
\sym{*} Significance at the 10\%, \sym{**} Significance at the 5\%, \sym{***} Significance at the 1\% \\
heteroscedasticity-robust standard errors in parentheses are clustered by city 
}
"""

multicolumn = {
    'Dummy': 2,
    'SOE': 2,
    'PRIVATE': 2,
}

new_row =['& NO Concentrated', 'Concentrated',
     'NO Concentrated', 'Concentrated',
     'NO Concentrated', 'Concentrated']
           
x = [a for a in os.listdir() if a.endswith(".txt")]
for i, val in enumerate(x):
    lb.beautify(table_number = i+1,
            remove_control= False,
            constraint = True,
            city_industry = False, 
            new_row = new_row,
            multicolumn = multicolumn,
            table_nte =False,
            jupyter_preview = True,
            resolution = 150)
```

<!-- #region kernel="Python 3" -->
# Create Report
<!-- #endregion -->

```sos kernel="Python 3"
import os, time, shutil
from pathlib import Path

export = 'pdf' #'html'

filename = '11_SBC_final_tfp'
source = filename + '.ipynb'
source_to_move = filename +'.{}'.format(export)
path = os.getcwd()
parent_path = str(Path(path).parent)
path_report = "{}/Reports".format(parent_path)
dest = os.path.join(path_report, filename)+'_{}_{}_.{}'.format(
    aggregation_param,
    threshold_full,
    export
)

os.system('jupyter nbconvert --no-input --to {} {}'.format(export, source))

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
