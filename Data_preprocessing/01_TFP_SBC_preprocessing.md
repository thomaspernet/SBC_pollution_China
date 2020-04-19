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
    display_name: Python 3
    language: python
    name: python3
---

# 01_TFP_SBC data preprocessing

This notebook has been generated on 2020-04-18 07:59 

The objective of this notebook is to compute TFP using OP or LP algorithm using ASIF panel data

## Global steps 

The global steps to construct the dataset are the following:

* Steps:
  * Import data 2001-2007
  * Select cities and industries from the paper's table
  * Exclude outliers
  * Remove firm with different:
    *  ownership, cities and industries over time
  * Compute TFP using 2 ways:
    * full samples
    * Split by ownership

## Data source 

The data source to construct the dataset are the following:



### Big Query Dataset 
 
 - [SBC_pollution_China](https://console.cloud.google.com/bigquery?project=valid-pagoda-132423&p=valid-pagoda-132423&d=China&t=SBC_pollution_China&page=table) 
 - [asif_firm_china](https://console.cloud.google.com/bigquery?project=valid-pagoda-132423&p=valid-pagoda-132423&d=China&t=asif_firm_china&page=table) 
### Google Cloud Storage Dataset 
 
### Google Spreadsheet Dataset 



## Destination

The new dataset is available from XXX

- GS: None
- GCS: 01_TFP_SBC.gz
- BG: 01_TFP_SBC


# Load Dataset


```python
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
from GoogleDrivePy.google_platform import connect_cloud_platform
from app_creation import studio
import pandas as pd 
import numpy as np
import pandas_profiling
from pathlib import Path
import os, re,  requests, json 

from dask.distributed import Client
#from dask import dataframe as dd 
client = Client()  # set up local cluster on your laptop
client
```

```python
gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')
service_gcp = gs.connect_remote(engine = 'GCP')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])

project = 'SBC_pollution_China'
gcp = connect_cloud_platform.connect_console(project = project,
											 service_account = service_gcp['GoogleCloudP'])
```


## Load SBC_pollution_China from Google Big Query

Feel free to add description about the dataset or any usefull information.

    

```python

query = (
          "SELECT * "
            "FROM China.SBC_pollution_China "

        )

df_SBC_pollution_China = gcp.upload_data_from_bigquery(query = query,
                                                       location = 'US',
                                                      to_dask = True)
df_SBC_pollution_China
    
```


```python
#df_SBC_pollution_China = dd.from_pandas(df_SBC_pollution_China, npartitions=3)
```

## Load asif_firm_china from Google Big Query

Feel free to add description about the dataset or any usefull information.

    

```python
%%time
query = """
WITH sum_id AS (
  SELECT 
    id, 
    case WHEN ownership = 'SOE' THEN 'SOE' ELSE 'PRIVATE' END AS OWNERSHIP, 
    year, 
    geocode4_corr, 
    cic as industry, 
    SUM(output / 10000000) as output_agg_o, 
    SUM(fa_net / 10000000) as fa_net_agg_o, 
    SUM(employment / 100000) as employment_agg_o, 
    SUM(input / 10000000) as input_agg_o, 
  FROM 
    China.asif_firm_china 
  WHERE 
    year >= 2002 
    AND year <= 2007 
    AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
    AND input > 0 
  GROUP BY 
    id, 
    OWNERSHIP, 
    year, 
    geocode4_corr, 
    cic, 
    OWNERSHIP
) 
SELECT 
  sum_id.id, 
  OWNERSHIP, 
  year, 
  geocode4_corr, 
  industry, 
  output_agg_o, 
  fa_net_agg_o, 
  employment_agg_o, 
  input_agg_o, 
  occurence 
FROM 
  sum_id 
  LEFT JOIN (
    SELECT 
      id, 
      COUNT(id) as occurence 
    FROM 
      sum_id 
    GROUP BY 
      id
  ) as occ on sum_id.id = occ.id 
ORDER BY 
  occurence, 
  id, 
  year

"""

df_asif_firm_china = gcp.upload_data_from_bigquery(query = query,
                                                   location = 'US',
                                                  to_dask =True)
df_asif_firm_china.head()
    
```

```python
df_asif_firm_china = dd.from_pandas(df_asif_firm_china, npartitions=3)
df_asif_firm_china
```

<!-- #region -->
# Workflow

In this section, we will construct the dataset, and document each step of the workflow.

Please use the following format for the documentation:

- Step 1: Select cities and industries from the paper's table
    - (optional) Underlying process description
- Step 2: Exclude outliers
    - (optional) Underlying process description
- Step 3: Remove firm with different:
    - (optional) ownership, cities and industries over time
- Step 4: Compute TFP
    - Done with R in EC2
- Step 5: AddT TFP to dataset
    - Subset city characteristics
        - Coastal
        - TCZ
        - Target
    - Subset industry characteristic
        - Polluted


Note: **You need to rename the last dataframe `df_final`**
<!-- #endregion -->

## Step 1 to 3

```python
cities = df_SBC_pollution_China['geocode4_corr'].unique().compute()
industries = df_SBC_pollution_China['industry'].unique().compute()

print("""
total cities : {}\n
total industries: {}
""".format(len(cities), len(industries)))
```

```python
(df_asif_firm_china.loc[
                      (df_asif_firm_china['geocode4_corr'].isin(cities))&
                      (df_asif_firm_china['industry'].isin(industries))
                      ]
 .groupby(["OWNERSHIP",'occurence'])['occurence']
 .count()
 .compute()
 .unstack(0)
 .plot
 .bar()
)
```

Outliers by `ONWERSHIP`

```python
outliers = (df_asif_firm_china.loc[
                      (df_asif_firm_china['geocode4_corr'].isin(cities))&
                      (df_asif_firm_china['industry'].isin(industries))
                      ]
 .groupby(["OWNERSHIP"])['output_agg_o']
 .apply(lambda x:x.quantile([.05,.25, .5, .75, .85, .9, .95]), meta=object)
 .compute()
 .unstack(0)
 .loc[[0.05, 0.95]]
)
```

```python
(df_asif_firm_china.loc[
                      (df_asif_firm_china['geocode4_corr'].isin(cities))&
                      (df_asif_firm_china['industry'].isin(industries))
                      ]
 .groupby('OWNERSHIP')['output_agg_o']
 .apply(lambda x: x.describe(), meta=object)
).compute()
```

```python
outliers#['SOE'].loc[0.05]
```

```python
%%time
df_final = (
    (df_asif_firm_china.loc[
        (df_asif_firm_china['geocode4_corr'].isin(cities))&
        (df_asif_firm_china['industry'].isin(industries)) &
        (df_asif_firm_china['OWNERSHIP'].isin(['SOE'])) &
        (df_asif_firm_china['output_agg_o']> outliers['SOE'].loc[0.05]) &
        (df_asif_firm_china['output_agg_o']< outliers['SOE'].loc[0.95])
                      ]
     .append(
        (
        df_asif_firm_china.loc[
        (df_asif_firm_china['geocode4_corr'].isin(cities))&
        (df_asif_firm_china['industry'].isin(industries)) &
        (df_asif_firm_china['OWNERSHIP'].isin(['PRIVATE'])) &
        (df_asif_firm_china['output_agg_o']> outliers['PRIVATE'].loc[0.05]) &
        (df_asif_firm_china['output_agg_o']< outliers['PRIVATE'].loc[0.95])
     ]
        )
        )
    )
    .assign(
        switch_ownership = lambda x:
        x.groupby(['id'])['OWNERSHIP'].transform('nunique', meta=object),
        switch_cities = lambda x:
        x.groupby('id')['geocode4_corr'].transform('nunique', meta=object),
        switch_industry = lambda x:
        x.groupby('id')['industry'].transform('nunique', meta=object)
    )
    #### Test if nan in the previous computation, if yes, and occurence is 1, 
    #### then 1
    .assign(
    switch_ownership = lambda x: 
        x['switch_ownership'].where(
            ~x['switch_ownership'].isin([np.nan])& 
            ~x['occurence'].isin([1]),
            1
        ),
    switch_cities = lambda x: 
        x['switch_cities'].where(
            ~x['switch_cities'].isin([np.nan])& 
            ~x['occurence'].isin([1]),
            1
        ),
    switch_industry = lambda x: 
        x['switch_industry'].where(
            ~x['switch_industry'].isin([np.nan])& 
            ~x['occurence'].isin([1]),
            1
        ),
    )
    #### Create nan for switch
    .assign(
    switch_ownership = lambda x: 
        x['switch_ownership'].where(
            x['switch_ownership'].isin([1]),
            np.nan
        ),
    switch_cities = lambda x: 
        x['switch_cities'].where(
            x['switch_cities'].isin([1]),
            np.nan
        ),
    switch_industry = lambda x: 
        x['switch_industry'].where(
            x['switch_industry'].isin([1]),
            np.nan
        ),
    )
    .dropna()
    .reindex(columns = ['id',
                        'occurence',
                        'OWNERSHIP',
                        'year',
                        'geocode4_corr', 
                        'industry',
                        'output_agg_o',
                        'fa_net_agg_o',
                        'employment_agg_o',
                        'input_agg_o'])
).compute()

```

```python
df_final.columns
```

```python
df_final.shape
```

```python
(df_final.loc[lambda x: 
              x['OWNERSHIP'].isin(['SOE'])]
 .groupby(['year', 'occurence'])['output_agg_o']
 .describe()
 .sort_index(level = 0, ascending = False)
)               
```

```python
### First save locally
df_final.to_csv(
	'01_TFP_SBC.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')
```

## Step 4: TFP computation

There is an issue with the latest version of R and Mac. It makes it impossible to install library not available in Conda. So, we computed the TFP using an EC2 instance. 

Here are the related source files:

- [Program](https://github.com/thomaspernet/SBC_pollution_China/blob/master/Data_preprocessing/program_tfp/tfp.R)
- [Models](https://console.cloud.google.com/storage/browser/chinese_data/Panel_china/Asif_panel_china/TFP_computation)
- [Data](https://storage.cloud.google.com/chinese_data/Panel_china/Asif_panel_china/TFP_computation/TFP_computed_ASIF_china_final.csv)

Note, in R, need to concert `NaN` to `None`. BigQuery does not support `NaN`

```
(df.where(pd.notnull(df), None)
 .to_csv("program_tfp/TFP_computed_ASIF_china_final.csv", index = False))
```

Three models:

**Full sample**

![](https://drive.google.com/uc?export=view&id=1m9XCI9oXDbSZnKZfhj1rRbBNRyfmYfmF)

**SOE sample**

![](https://drive.google.com/uc?export=view&id=1CUepeIMZINDoN63MX8LVORIZiNd5Sop6)

**Private sample**

![](https://drive.google.com/uc?export=view&id=10-QRGYUNOttZxtUucXfMttADOTay15Gt)



```python
query = (
          "SELECT * "
            "FROM China.TFP_ASIF_china "

        )

TFP_ASIF_china = gcp.upload_data_from_bigquery(query = query,
                                                       location = 'US',
                                                      to_dask = True)
TFP_ASIF_china
```

```python
TFP_ASIF_china[['tfp_OP', 'tfp_OWNERSHIP']].corr().compute()
```

```python
(TFP_ASIF_china
.groupby(['year','OWNERSHIP'])['tfp_OP']
.mean() 
.compute() 
.unstack(-1) 
.plot
.bar()
)
```

## Step 5

```python
TFP_ASIF_china.compute().shape
```

```python
import dask.array as da
```

```python
SBC_TFP_ASIF_china = (TFP_ASIF_china
.merge(
    (df_SBC_pollution_China[[
        'industry',
        'polluted_thre'
    ]]
     .drop_duplicates(subset = 'industry')
    ), on =  ['industry'])
.merge(
    (df_SBC_pollution_China[[
    'geocode4_corr',
    'cityen',    
    'Coastal',
    'TCZ_c',
    'target_c'
    ]]
 .drop_duplicates(subset = 'geocode4_corr')
), on = ['geocode4_corr']
)
                      .drop(columns = 
                           ['output_agg_o',
       'fa_net_agg_o', 'employment_agg_o', 'input_agg_o',
                           'tfp_OP_soe', 'tfp_OP_pri', 'id_1',
                           'switch_ownership',
                            'switch_cities', 'switch_industry'])
.assign(
    #Period=lambda x: da.where(
    #x["year"] > 2005, "Before", "After"),
        year=lambda x: x['year'].astype('str'),
        industry=lambda x: x['industry'].astype('str')
    )
).compute().assign(
    Period=lambda x: np.where(
    x["year"].isin(['2006', '2007']), "After", "Before")
)
```

```python
df_final = SBC_TFP_ASIF_china.copy()
df_final["FE_c_i"] = pd.factorize(df_final["cityen"] +
                                      df_final['industry'])[0]

df_final["FE_t_i"] = pd.factorize(df_final["year"] +
                                      df_final['industry'])[0]

df_final["FE_t_c"] = pd.factorize(df_final["year"] + df_final["cityen"])[0]

df_final["FE_c_i_o"] = pd.factorize(df_final["cityen"] + df_final["industry"] +
                                        df_final["OWNERSHIP"])[0]
df_final["FE_t_o"] = pd.factorize(
        df_final["year"] + df_final["OWNERSHIP"])[0]
```

```python
df_final.head()
```

```python

```

# Profiling

In order to get a quick summary statistic of the data, we generate an HTML file with the profiling of the dataset we've just created. 

The profiling will be available at this URL after you commit a push to GitHub. 

**You need to rename the final dataframe `df_final` in the previous section to generate the profiling.**

```python
#### make sure the final dataframe is stored as df_final
### Overide the default value: 
#https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_default.yaml

profile = pandas_profiling.ProfileReport(df_final,
                                        check_correlation_pearson = False)
name_html = "NAME.html"
profile.to_file(output_file=name_html)
```

# Upload to cloud

The dataset is ready to be shared with your colleagues. 



<!-- #region -->


### Move to GCS and BigQuery

We move the dataset to the following:

- **bucket**: *NEED TO DEFINE*

- **Destination_blob**: *XXXXX/Processed_*
- **name**:  *01_TFP_SBC.gz*
- **Dataset**: *China*

- **table**: *01_TFP_SBC*

### GCS

We first need to save *01_TFP_SBC* with `.gz` extension locally then we can move it
to GCS

<!-- #endregion -->

```python

### First save locally
df_final.to_csv(
	'01_TFP_SBC_firm.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')

### Then upload to GCS
bucket_name = 'chinese_data'
destination_blob_name = 'paper_project/Processed_'
source_file_name = '01_TFP_SBC_firm.gz'
gcp.upload_blob(bucket_name, destination_blob_name, source_file_name)

```

```python
### Move to bigquery
bucket_gcs ='chinese_data/paper_project/Processed/01_TFP_SBC_firm.gz'
gcp.move_to_bq_autodetect(dataset_name= 'China',
							 name_table= 'TFP_SBC_firm',
							 bucket_gcs=bucket_gcs)

```

# Generate Studio

To generate a notebook ready to use in the studio, please fill in the variables below:

- 'project_name' : Name of the repository
- 'input_datasets' : name of the table
- 'sheetnames' : Name of the sheet, if table saved in Google Spreadsheet
- 'bigquery_dataset' : Dataset name
- 'destination_engine' : 'GCP' or 'GS,
- 'path_destination_studio' : path to `Notebooks_Ready_to_use_studio`
- 'project' : 'valid-pagoda-132423',
- 'username' : "thomas",
- 'pathtoken' : Path to GCP token,
- 'connector' : 'GBQ', ## change to GS if spreadsheet
- 'labels' : Add any labels to the variables,
- 'date_var' : Date variable

```python
labels = []
date_var = ''
```

```python
regex = r"(.*)/(.*)"
path = os.getcwd()
parent_path = Path(path).parent
test_str = str(parent_path)
matches = re.search(regex, test_str)
github_repo = matches.group(2)

path_credential = '/Users/Thomas/Google Drive/Projects/Data_science/Google_code_n_Oauth/Client_Oauth/Google_auth/'

dic_ = {
    
          'project_name' : github_repo,
          'input_datasets' : 'TFP_SBC_firm',
          'sheetnames' : '',
          'bigquery_dataset' : 'China',
          'destination_engine' : 'GCP',
          'path_destination_studio' : os.path.join(test_str,
                                       'Notebooks_Ready_to_use_studio'),
          'project' : 'valid-pagoda-132423',
          'username' : "thomas",
          'pathtoken' : path_credential,
          'connector' : 'GBQ', ## change to GS if spreadsheet
          'labels' : labels,
          'date_var' : date_var
}
create_studio = studio.connector_notebook(dic_)
create_studio.generate_notebook_studio()
```

# Add data to catalogue

Now that the dataset is ready, you need to add the underlying information to the data catalogue. The data catalogue is stored in [Coda](https://coda.io/d/MasterFile-Database_dvfMWDBnHh8/MetaDatabase_suYFO#_ludIZ), more precisely, in the table named `DataSource`. 

The cells below helps you to push the information directly to the table using Coda API.

The columns are as follow:

- `Storage`: Define the location of the table
    - GBQ, GS, MongoDB
- `Theme`: Define a theme attached to the table
    - Accountancy, Complexity, Correspondance, Customer_prediction, Distance, Environment, Finance, Macro, Production, Productivity, Survey, Trade
- `Database`: Name of the dataset. Use only for GBQ or MongoDB (collection)
    - Business, China, Steamforged, Trade
- `Path`:A URL with the path of the location of the dataset
- `Filename`: Name of the table
- `Description`: Description of the table. Be very specific. 
- `Source_data`: A list of the data sources used to construct the table.
- `Link_methodology`: URL linked to the notebook
- `Dataset_documentation`: Github repository attached to the table
- `Status`: Status of the table. 
    - `Closed` if the table won't be altered in the future
    - `Active` if the table will be altered in the future
- `Profiling`: Specify if the user created a Pandas profiling
    - `True` if the profiling has been created
    - `False` otherwise
- `Profiling_URL`: Profiling URL (link to Github). Always located in `Data_catalogue/table_profiling`
- `JupyterStudio`: Specify if the user created a notebook to open the studio
    - `True` if the notebook has been created
    - `False` otherwise
- `JupyterStudio_launcher`: Notebook URL (link to Github). Always located in `Notebooks_Ready_to_use_studio`
- `Nb_projects`: Number of projects using this dataset. A Coda formula. Do not update this row
- `Created on`: Date of creation. A Coda formula. Do not update this row

Remember to commit in GitHub to activate the URL link for the profiling and Studio

```python
Storage = 'GBQ'
Theme = 'Trade' 
Database = 'China'
Description = "The table is related to the paper about FTP and SBC"
Filename = 'TFP_SBC_firm'
Status = 'Active'
```

```python
Source_data = ['SBC_pollution_China', 'asif_firm_china', 'TFP_ASIF_china']
```

The next cell pushes the information to [Coda](https://coda.io/d/MasterFile-Database_dvfMWDBnHh8/Test-API_suDBp#API_tuDK4)

```python
regex = r"(.*)/(.*)"
path = os.getcwd()
parent_path = Path(path).parent
test_str = str(parent_path)
matches = re.search(regex, test_str)
github_repo = matches.group(2)

Profiling = True
if Profiling:
    Profiling_URL = 'http://htmlpreview.github.io/?https://github.com/' \
    'thomaspernet/{}/blob/master/Data_catalogue/table_profiling/{}.html'.format(github_repo,
                                                                               Filename)
else:
    Profiling_URL = ''
JupyterStudio = False
if JupyterStudio:
    JupyterStudio_URL = '"https://mybinder.org/v2/gh/thomaspernet/{0}/' \
    'master?filepath=Notebooks_Ready_to_use_studio%2F{1}_studio.ipynb'.format(github_repo, Filename)
else:
    JupyterStudio_URL = ''
### BigQuery only 
path_url = 'https://console.cloud.google.com/bigquery?project=valid-pagoda-132423' \
'&p=valid-pagoda-132423&d=China&t={}&page=table'.format(Filename)

Link_methodology = 'https://nbviewer.jupyter.org/github/thomaspernet/' \
    '{0}/blob/master/Data_preprocessing/' \
    '{1}.ipynb'.format(github_repo,
    Filename)

Dataset_documentation = 'https://github.com/thomaspernet/{}'.format(github_repo)

to_add = {
    'Storage': Storage,
    'Theme': Theme,
    'Database': Database,
    'Path_url': path_url,
    'Filename': Filename,
    'Description': Description,
    'Source_data': Source_data,
    'Link_methodology': Link_methodology,
    'Dataset_documentation': Dataset_documentation,
    'Status': Status,
    'Profiling_URL': Profiling_URL,
    'JupyterStudio_launcher': JupyterStudio_URL

}
cols= []
for key, value in to_add.items():
    coda = {
    'column': key,
    'value':value
    }
    cols.append(coda)
    
###load token coda
with open('token_coda.json') as json_file:
    data = json.load(json_file)
    
token = data[0]['token'] 
headers = {'Authorization': 'Bearer {}'.format(token)}
uri = f'https://coda.io/apis/v1beta1/docs/vfMWDBnHh8/tables/grid-HgpAnIEhpP/rows'
payload = {
  'rows': [
    {
      'cells': cols,
    },
  ],
}
req = requests.post(uri, headers=headers, json=payload)
req.raise_for_status() # Throw if there was an error.
res = req.json()
```

```python

```
