---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.4.2
  kernel_info:
    name: sos
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region Collapsed="false" kernel="SoS" toc-hr-collapsed=false kernel="SoS" -->
# SBC_pollution_china data preprocessing

This notebook has been generated on 2019-10-05 07:45 

The objective of this notebook is to YYY

## Proposal 

The proposal is available [here](https://drive.google.com/open?id=1tmSFvdUMXcL3vMKBSNYmf5xe6OEmYNnD)

### Equation to estimate

$$
\begin{aligned} \text { SO2 emission }_{i k t}=& \alpha T C Z_{i} \times \text { Polluted sectors }_{k} \times \text { post } \\ & +\theta {X}_{i k t}+\nu_{c i}+\lambda_{t i} +\phi_{t c} \end{aligned}
$$

city-industry; time-industry and time-city

## Global steps 

The global steps to construct the dataset are the following:


- From BigQuery
    - Select year 1998-2007 ASIF
    
- Set parameters:
    - Choice of aggregation
    - Keep used variables in SO2 dataset
    
## Data source 

The data source to construct the dataset are the following:
<!-- #endregion -->

<!-- #region kernel="SoS" -->

### Big Query Dataset 
 
 - asif_firm_china 
 - China_city_pollution_98_2007 
 
### Google Cloud Storage Dataset 
 
### Google Spreadsheet Dataset 
 
 - [TCZ_list_china](https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q) 
 - [cityname_and_code](https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA) 
<!-- #endregion -->

<!-- #region kernel="SoS" -->
## Destination

The new dataset is available from XXX

- GS: None
- GCS: SBC_pollution_china.gz
- BG: SBC_pollution_china
<!-- #endregion -->

```python kernel="Python3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
from GoogleDrivePy.google_platform import connect_cloud_platform
import pandas as pd 
import numpy as np
#import pandas_profiling
import Pollution.SBC_pollution as sbc
```

```python kernel="Python3"
gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')
service_gcp = gs.connect_remote(engine = 'GCP')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])

project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project,
											 service_account = service_gcp['GoogleCloudP'])
```

<!-- #region kernel="python3" -->
## Load asif_firm_china from Google Big Query

Data studio for this dataset available [here](https://drive.google.com/open?id=1ppXfCw73EGVmUQdcM5MI_S9RbtjunhQ_)

Feel free to add description about the dataset or any usefull information.

### Format Data:

- Output: in trillions RMB
- Employement: in trillions RMB
- Fixed Asset: in millions of workers.

### Preprocess original data

- Rescale output; employment and capital
- Remove firms with zeroes values
- Keep year 2002-2007
<!-- #endregion -->

```python kernel="Python3"
query = (
    """SELECT case 
    WHEN ownership = 'SOE' THEN 'SOE' ELSE 'PRIVATE' END AS SOE, 
       SUM(output/10000000) as output_fcit, 
       SUM(fa_net/10000000) as capital_fcit, 
       SUM(employment/100000) as labour_fcit, 
       Province_en,
       cityen_correct as cityen,
       citycn_correct as citycn,
       geocode4_corr, 
       Lower_location,
       Larger_location,
       Coastal, 
       CAST(year AS STRING) as year,
       CAST(cic AS STRING) as industry,
       Short 
FROM China.asif_firm_china 
WHERE year >= 2002 AND year < 2008 AND output > 0 AND fa_net > 0 
    AND employment > 0 
GROUP BY Province_en, cityen,citycn, geocode4_corr, 
    Lower_location, Larger_location, Coastal, 
    year, SOE, cic,industry, Short """
)

df_asif_firm_china = gcp.upload_data_from_bigquery(query=query, location="US")
df_asif_firm_china.head()
```

<!-- #region kernel="python3" -->
## Load df_China_city_pollution_03_2007 from Google Big Query

Feel free to add description about the dataset or any usefull information.

<!-- #endregion -->

```python kernel="Python3"
query = (
    """SELECT 
    CAST(year AS STRING) as year,
    cityen,
    CAST(indus_code AS STRING) as industry,
    SUM(tso2) as tso2,
    SUM(ttoutput) as toutput
    FROM China.China_city_pollution_98_2007 
    WHERE year >= 2002 AND year <= 2007 
    GROUP BY year, cityen,industry"""
)

df_China_city_pollution_03_2007 = gcp.upload_data_from_bigquery(
    query=query, location='US')
df_China_city_pollution_03_2007.head()
```

<!-- #region kernel="python3" -->
## Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

We use the sheet `paper` because it's the geocode we originaly used. After the dataset has been created, we changed some geocode to match the correspondance table. In order to make the replication possible, we use the geocode from the paper https://drive.google.com/file/d/1-SXSlRoS_2ZW7CK6XMhcXpJDPxAEF1xG/view

Profiling will be available soon for this dataset
<!-- #endregion -->

```python kernel="Python3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range

sheetid = '15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q'
sheetname = 'paper'

df_TCZ_list_china = (gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
                     .assign(geocode4_corr=lambda x: 
                             x['geocode4_corr'].astype('int')
                    )
                    )
df_TCZ_list_china.head()
```

<!-- #region kernel="python3" -->
## Load China_cities_target_so2 from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```python kernel="Python3" jupyter={"outputs_hidden": true}
### Please go here https://docs.google.com/spreadsheets/d/1z3A_I8_StdyNL5O38s2l9hx6W3VR49CGVmaosypjFMA
### To change the range

sheetid = '1z3A_I8_StdyNL5O38s2l9hx6W3VR49CGVmaosypjFMA'
sheetname = 'China_cities_target_so2'

df_China_cities_target_so2 = (gdr.upload_data_from_spreadsheet(sheetID = 
                                                              sheetid,
sheetName = sheetname,
	 to_dataframe = True)
                              .drop(
        columns=[
            "prov2013",
            "citycn",
            "ttoutput",
            "SO2_05_city_reconstructed",
            "SO2_obj_2010",
            "SO2_perc_reduction_c",
            "in_10_000tonnes"
        ]
    )
                             )
df_China_cities_target_so2.head()
```

<!-- #region Collapsed="false" kernel="python3" toc-hr-collapsed=false kernel="SoS" -->
# Workflow

In this section, we will construct the dataset, and document each step of the workflow.

Please use the following format for the documentation:

- `##` Step 1: XXX
- `###` (optional) Underlying process description
- `##` Step 2: YYY
- `###` (optional) Underlying process description

Note: **You need to rename the last dataframe `df_final`**
<!-- #endregion -->

<!-- #region Collapsed="false" kernel="python3" toc-hr-collapsed=true kernel="SoS" -->
## Steps 

The program works as follow:

- Step 1: Compute share SOE by industry
- Step 2: Compute polluted sectors
- Step 3: Merge dataframe 
    - For TCZ, `left_join` -> Cities not matched become no tcz
<!-- #endregion -->

<!-- #region kernel="python3" -->
### 1. Prepapre  `df_asif_firm_china`

There is some preprocessing to perform on the original dataframe:
<!-- #endregion -->

```python kernel="Python3"
dic_ = {'var': [],
       'count':[],
       'values': []}
for v in df_asif_firm_china.select_dtypes(include='object').columns:
    cat = df_asif_firm_china[v].nunique()
    value_cat  = df_asif_firm_china[v].unique()
    dic_['var'].append(v)
    dic_['count'].append(cat)
    dic_['values'].append(value_cat)

(pd.DataFrame(dic_)
 .sort_values(by = ['count'])
 .set_index('var')
)
```

```python kernel="Python3"
share_SOE = (df_asif_firm_china
                     .groupby(['year',
                               'industry',
                               'SOE'
                               ]
                              )
                     .agg(
                         output_fcit=('output_fcit', 'sum'),
                         capital_fcit=('capital_fcit', 'sum'),
                         labour_fcit=('labour_fcit', 'sum')
                     )
                     .unstack(fill_value=0)
                     .assign( 
                         total_o=lambda x: x.iloc[:, 0] + x.iloc[:, 1],
                         total_k=lambda x: x.iloc[:, 2] + x.iloc[:, 3],
                         total_l=lambda x: x.iloc[:, 4] + x.iloc[:, 5],
                         out_share_SOE=lambda x: x.iloc[:, 1] / x['total_o'],
                         cap_share_SOE=lambda x: x.iloc[:, 3] / x['total_k'],
                         lab_share_SOE=lambda x: x.iloc[:, 5] / x['total_l'],
                     )
                     .groupby(level=1)
                     .agg( 
                         out_share_SOE=('out_share_SOE', 'mean'),
                         cap_share_SOE=('cap_share_SOE', 'mean'),
                         lab_share_SOE=('lab_share_SOE', 'mean'),
                     )
                     .reset_index()
                     )
share_SOE.head()
```

```python kernel="Python3"
# Polluted sectors
pollution_ind = (df_China_city_pollution_03_2007
                     .loc[lambda x: ~x['tso2'].isin([0])]
                     .loc[lambda x: x['year'].isin(['2002'])]
                     #.rename(columns={'indus_code': 'industry'})
                     .groupby('industry')[['tso2', 'toutput']]
                     .mean()
                     .reset_index()
                     .assign(
                         polluted_di=lambda x: np.where(
                             x["tso2"] > x["tso2"].quantile(
                                 [0.75]).loc[(0.75)],
                             "Above",
                             "Below",
                         ),
                         polluted_mi=lambda x: np.where(
                             x["tso2"] > x["tso2"].mean(),
                             "Above",
                             "Below",
                         ),
                         polluted_thre=lambda x: np.where(
                             x["tso2"] > 68070.78,
                             "Above",
                             "Below",
                         ),
                     )
                     .drop(columns = ['toutput'])
                     .rename(columns={
                         'tso2': 'tso2_i'
                     })
                     )
pollution_ind.head()
```

```python kernel="Python3"
df_China_city_pollution_03_2007.loc[lambda x: x['tso2']<=0].shape
```

```python kernel="Python3"
df_temp = (df_asif_firm_china
 .merge(df_China_city_pollution_03_2007)
 .merge(pollution_ind)
 .merge(df_China_cities_target_so2)
 .merge(df_TCZ_list_china, on = ['geocode4_corr'], how = 'left')
 .loc[lambda x: ~x['tso2'].isin([0])]
 .assign(
     TCZ = lambda x: x['TCZ'].fillna('0'),
     Period=lambda x: np.where(x["year"] > "2005","After", "Before"),
 )
           .rename(columns={
            "TCZ": "TCZ_c",
            "tso2_mandate_c": "target_c",
            'tso2': 'tso2_cit'
        })
.replace({'TCZ_c': {"1": 'TCZ', "0": 'No_TCZ'}})
)

# Compute fixed effect
df_final = df_temp.copy()

df_final["FE_c_i"] = pd.factorize(df_final["cityen"] +
                                      df_final['industry'])[0]

df_final["FE_t_i"] = pd.factorize(df_final["year"] +
                                      df_final['industry'])[0]

df_final["FE_t_c"] = pd.factorize(df_final["year"] + 
                                  df_final["cityen"])[0]
```

```python kernel="Python3"
df_final.groupby('year')['tso2'].sum()
```

```python kernel="Python3" jupyter={"outputs_hidden": true}
df_final.describe()
```

```python kernel="python3" jupyter={"outputs_hidden": true}
df_final.to_csv(
	'SBC_pollution_China.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')
```

<!-- #region kernel="python3" -->
# Profiling

In order to get a quick summary statistic of the data, we generate an HTML file with the profiling of the dataset we've just created. 

The profiling will be available at this URL after you commit a push to GitHub. 

**You need to rename the final dataframe `df_final` in the previous section to generate the profiling.**
<!-- #endregion -->

```python kernel="python3" jupyter={"outputs_hidden": true}
#### make sure the final dataframe is stored as df_final
### Overide the default value: 
#https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_default.yaml

profile = pandas_profiling.ProfileReport(df_final,
                                        check_correlation_pearson = False)
name_html = "Dataset_profiling/SBC_pollution_China.html"
profile.to_file(output_file=name_html)
```

<!-- #region kernel="python3" -->
# Upload to cloud

The dataset is ready to be shared with your colleagues. 
<!-- #endregion -->

<!-- #region kernel="python3" -->
### Move to GCS and BigQuery

We move the dataset to the following:

- **bucket**: *chinese_data*

- **Destination_blob**: *Environmental_Statistics_china/Processed_ES*
- **name**:  *SBC_pollution_China.gz*
- **Dataset**: *China*

- **table**: *SBC_pollution_China*

### GCS

We first need to save *SBC_pollution_China* with `.gz` extension locally then we can move it
to GCS
<!-- #endregion -->

<!-- #region kernel="python3" -->
## Delete previous dataset
<!-- #endregion -->

```python kernel="Python3" jupyter={"outputs_hidden": true}
bucket_name = 'chinese_data'
destination_blob_name = 'paper_project/SBC_pollution_China_not_constraint.gz'

#gcp.delete_blob(bucket_name = bucket_name,
#                destination_blob_name= destination_blob_name)
#gcp.delete_table(dataset_name = 'China', name_table = 'SBC_pollution_China')
```

```python kernel="Python3" jupyter={"outputs_hidden": true}
### First save locally
df_final.to_csv(
	'SBC_pollution_China_not_constraint.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')

### Then upload to GCS
bucket_name = 'chinese_data'
destination_blob_name = 'paper_project'
source_file_name = 'SBC_pollution_China_not_constraint.gz'
gcp.upload_blob(bucket_name, destination_blob_name, source_file_name)
```

```python kernel="Python3" jupyter={"outputs_hidden": true}
### Move to bigquery
bucket_gcs ='chinese_data/paper_project/SBC_pollution_China_not_constraint.gz'
gcp.move_to_bq_autodetect(dataset_name= 'China',
							 name_table= 'SBC_pollution_China_not_constraint',
							 bucket_gcs=bucket_gcs)
```
