---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.3
  kernel_info:
    name: sos
  kernelspec:
    display_name: SoS
    language: sos
    name: sos
---

<!-- #region Collapsed="false" kernel="SoS" toc-hr-collapsed=false -->
# SBC_pollution_china data preprocessing: Foreign

This notebook has been generated on 2019-10-05 07:45 

The objective of this notebook is to YYY

## Proposal 

The proposal is available [here](https://drive.google.com/open?id=1tmSFvdUMXcL3vMKBSNYmf5xe6OEmYNnD)

### Equation to estimate

$$
\begin{aligned} \text { SO2 emission }_{i k t}=& \alpha T C Z_{i} \times \text { Polluted sectors }_{k} \times \text { post } \\ &+\beta T C Z_{i} \times \text { Polluted sectors }_{k} \times \text { post } \times \text { Share Foreign }_{k} \\ & +\theta {X}_{i k t}+\nu_{c i}+\lambda_{t i} +\phi_{t c} \end{aligned}
$$

city-industry; time-industry and time-city

## Global steps 

The global steps to construct the dataset are the following:


- From BigQuery
    - Select year 1998-2007 ASIF
    
- Set parameters:
    - Choice of aggregation
    - Keep used variables in SO2 dataset
    - Exclude cities not operation 7 years in a row
    
## Data source 

The data source to construct the dataset are the following:
<!-- #endregion -->

<!-- #region Collapsed="false" kernel="SoS" -->

### Big Query Dataset 
 
 - asif_firm_china 
 - China_city_pollution_98_2007 
 
### Google Cloud Storage Dataset 
 
### Google Spreadsheet Dataset 
 
 - [TCZ_list_china](https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q) 
 - [cityname_and_code](https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA) 
 - [provinces_location](https://docs.google.com/spreadsheets/d/1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g)
<!-- #endregion -->

<!-- #region Collapsed="false" kernel="SoS" -->
## Destination

The new dataset is available from XXX

- GS: None
- GCS: SBC_pollution_china.gz
- BG: SBC_pollution_china
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
from GoogleDrivePy.google_platform import connect_cloud_platform
import pandas as pd 
import numpy as np
import pandas_profiling
import Pollution.SBC_pollution as sbc
from pathlib import Path
import os, re,  requests, json
```

```sos Collapsed="false" kernel="python3"
gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/Thomas/Google Drive/Projects/Data_science/Google_code_n_Oauth/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')
service_gcp = gs.connect_remote(engine = 'GCP')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])

project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project,
											 service_account = service_gcp['GoogleCloudP'])
```

<!-- #region Collapsed="false" kernel="python3" -->
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
- Aggregate by CIC 2 digits
- Keep year 2002-2008
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
#
query = (
    "SELECT case \
    WHEN ownership = 'Foreign' THEN 'FOREIGN' \
    WHEN ownership = 'SOE' THEN 'SOE' \
    ELSE 'DOMESTIC' END AS FOREIGN, \
    SUM(output/10000000) as output, \
    SUM(fa_net/10000000) as fa_net, \
    SUM(employment/100000) as employment, \
    newID,Province_en, cityen_correct, geocode4_corr, \
    Lower_location, Larger_location, Coastal, \
    year, cic,indu_2, Short \
    FROM China.asif_firm_china \
    WHERE year >= 2001 AND year < 2008 AND output > 0 AND fa_net > 0 \
    AND employment > 0 \
    GROUP BY newID,Province_en, cityen_correct, geocode4_corr, \
    Lower_location, Larger_location, Coastal, \
    year, FOREIGN, cic,indu_2, Short "
)

df_asif_firm_china = gcp.upload_data_from_bigquery(query=query, location="US")
df_asif_firm_china.head()
```

<!-- #region Collapsed="false" kernel="python3" -->
## Load China_city_pollution_98_2007 from Google Big Query

Feel free to add description about the dataset or any usefull information.

<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
query = (
    "SELECT year,cityen, indus_code, ind2, SUM(tso2) as tso2, SUM(tCOD) as tCOD, \
    SUM(twaste_water) as twaste_water "
    "FROM China.China_city_pollution_98_2007 "
    "WHERE year > 2001 AND year <= 2007 "
    "GROUP BY year, cityen,indus_code, ind2"
    

)

df_China_city_pollution_98_2007 = gcp.upload_data_from_bigquery(
    query=query, location='US')
df_China_city_pollution_98_2007.head()
```

<!-- #region Collapsed="false" kernel="python3" -->
## Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range

sheetid = '15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q'
sheetname = 'paper'

df_TCZ_list_china = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_TCZ_list_china.head()
```

<!-- #region Collapsed="false" kernel="python3" -->
## Load cityname_and_code from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
### Please go here https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA
### To change the range

sheetid = '1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA'
sheetname = 'final'

df_cityname_and_code = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_cityname_and_code.head()
```

<!-- #region Collapsed="false" kernel="python3" -->
## Load provinces_location from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
### Please go here https://docs.google.com/spreadsheets/d/1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g
### To change the range

sheetid = '1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g'
sheetname = 'provinces_location.csv'

df_provinces_location = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_provinces_location.head()
```

<!-- #region Collapsed="false" kernel="python3" -->
## Load China_cities_target_so2 from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
### Please go here https://docs.google.com/spreadsheets/d/1z3A_I8_StdyNL5O38s2l9hx6W3VR49CGVmaosypjFMA
### To change the range

sheetid = '1z3A_I8_StdyNL5O38s2l9hx6W3VR49CGVmaosypjFMA'
sheetname = 'China_cities_target_so2'

df_China_cities_target_so2 = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_China_cities_target_so2.head()
```

<!-- #region Collapsed="false" kernel="python3" toc-hr-collapsed=false -->
# Workflow

In this section, we will construct the dataset, and document each step of the workflow.

Please use the following format for the documentation:

- `##` Step 1: XXX
- `###` (optional) Underlying process description
- `##` Step 2: YYY
- `###` (optional) Underlying process description

Note: **You need to rename the last dataframe `df_final`**
<!-- #endregion -->

<!-- #region Collapsed="false" kernel="python3" toc-hr-collapsed=true -->
## Parameters

For each change we will modify the original dataset `df_asif_firm_china`

Parameteres contains 3 parts:

1. Choice of aggregation

We are left with two options to aggregate the data:

- Indu 2 digits or CIC
- `to_group`: Aggregate the data during the first part of the chain: from firm to industry
- `to_group_reshape`:  Group the data to create a squared dataframe. The dataset has all industries for each city. If the city does not produce anything, we fill by one. 

2. Format data

Change the format of the city variable in the TCZ data and keep the variables needed in the pollution data

3. Exclude city not operating during the 7 years of our analysis: Fill list excluded:

- 'Bayannaoer', 'Dingxi', 'Jiuquan', 'Lijiang', 'Lincang', 'Longnan',
- 'Luliang', 'Pingliang', 'Qingyang', 'Simao', 'Wulanchabu', 'Wuwei',
- 'Zhangye', 'Zhongwei'


The program allows the users to pass two parameters. The first parameter `bounce. The exclude firms that enter and leave the market mutliple time through the year. The second parameter, `symmetric` gives the possibility to keep only industries available during both period (10/11th FYP). 


## Steps 

The program works as follow:

- Step 1: If `bounce` is true, then the program exclude firms bouncing back on and on in the dataset
- Step 2: Keep a set of year and create the period dummy variable. The dummy takes the value of `After` all year after 2005. 
- Step 3: Remove all cities not available every years
- Step 4: Prepare the SOE industries. More precisely, the program computes the numbers of SOE firms for each year during 2002-2005 by industry (either HS2 or CIC), and get the average output;capital and labour at the same level. Then, the share by industry is computed.
- Step 5: Define the polluted sectors in three difference ways. First, the program computes the average SO2 emission by industries for the year 2002. Then, polluted sectors are defined whether the average is above the national average, the third decile or 68070.
- Step 6: Remove the city-industry with null value for SO2 emission
- Step 7: Aggregate the control variable at the city-industry-year level
- Step 8: Merge TCZ, Share SOE, pollution, pollution by industry
- Step 9 (optional): If the user choose to get a symmetric dataset, then the program excludes industries which are not available in both period
- Step 10: Remove outliers : when SO2 emissions are below 500 and above 2276992 (about .5 and .95 of the distribution)
- Step 11: Create 3 bunches of fixed effect:  city-industry; time-industry and time-city
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
# industry_agg = ['indu_2']
industry_agg = ["indu_2"]

years = ["2002", "2003", "2004", "2005", "2006", "2007"]


order_columns = [
    "year",
    "Period",
    "Province_en",
    "Lower_location",
    "Larger_location",
    "Coastal",
    "cityen",
    "geocode4_corr",
    "TCZ_c",
    "target_c",
    "effort_c",
    "industry",
    "ind2",
    "Short",
    "output_fcit",
    "capital_fcit",
    "labour_fcit",
    'out_share_for',
    'out_share_soe1',
    'cap_share_for',
    'cap_share_soe1',
    'lab_share_for',
    'lab_share_soe1',
    "tso2_cit",
    "tso2_i",
    "tCOD_cit",
    "twaste_water_cit",
    "polluted_di",
    "polluted_mi",
    "polluted_thre",
    "FE_c_i",
    "FE_t_i",
    "FE_t_c",
]
```

<!-- #region Collapsed="false" kernel="python3" -->
### 1. Prepapre  `df_asif_firm_china`

There is some preprocessing to perform on the original dataframe:
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
df_asif_firm_china.shape
```

<!-- #region Collapsed="false" kernel="python3" -->
### Run metafunction
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
import datetime
import Pollution.SBC_pollution as sbc
```

```sos Collapsed="false" kernel="python3"
%load_ext autoreload
%autoreload 2
```

<!-- #region Collapsed="false" kernel="python3" -->
Note we manually added the foreign share because we changed the TCZ list file, so the number of obs didn't match. Instead, we load the previous data for the paper, construct the share using the metafunction (move the return after the bounce, and then merge back to the original dataset used in the paper

```
df_final_ = df_final_.merge(
    share_for
    .assign(industry = lambda x: 
            x['industry'].astype('int')),
    on = 'industry')
```
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
%%time
df_final = sbc.metafunction(df_original=df_asif_firm_china,
                        df_TCZ_list_china=df_TCZ_list_china,
                        df_China_city_pollution_98_2007=df_China_city_pollution_98_2007,
                        df_China_cities_target_so2= df_China_cities_target_so2,
                        order_columns=order_columns,
                        industry_agg='cic',
                        symetric=True,
                        bounce=True,
                        soe = False)
```

```sos Collapsed="false" kernel="python3"
df_final.shape
```

```sos Collapsed="false" kernel="python3"
df_final['year'].unique()
```

```sos Collapsed="false" kernel="python3"
df_final['industry'].nunique()
```

```sos Collapsed="false" kernel="python3"
df_final['cityen'].nunique()
```

```sos Collapsed="false" kernel="python3"
df_final.describe()
```

```sos Collapsed="false" kernel="python3"
df_final.to_csv(
	'SBC_pollution_China_foreign.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')
```

<!-- #region Collapsed="false" kernel="python3" -->
# Profiling

In order to get a quick summary statistic of the data, we generate an HTML file with the profiling of the dataset we've just created. 

The profiling will be available at this URL after you commit a push to GitHub. 

**You need to rename the final dataframe `df_final` in the previous section to generate the profiling.**
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
#### make sure the final dataframe is stored as df_final
### Overide the default value: 
#https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_default.yaml

profile = pandas_profiling.ProfileReport(df_final,
                                        check_correlation_pearson = False)
name_html = "SBC_pollution_China.html"
profile.to_file(output_file=name_html)
```

<!-- #region Collapsed="false" kernel="python3" -->
# Upload to cloud

The dataset is ready to be shared with your colleagues. 
<!-- #endregion -->

<!-- #region Collapsed="false" kernel="python3" -->
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

<!-- #region Collapsed="false" kernel="python3" -->
## Delete previous dataset
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
bucket_name = 'chinese_data'
destination_blob_name = 'paper_project/SBC_pollution_China_foreign.gz'

gcp.delete_blob(bucket_name = bucket_name,
                destination_blob_name= destination_blob_name)
gcp.delete_table(dataset_name = 'China', name_table = 'SBC_pollution_China_foreign')
```

```sos Collapsed="false" kernel="python3"
### First save locally
df_final.to_csv(
	'SBC_pollution_China_foreign.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')

### Then upload to GCS
bucket_name = 'chinese_data'
destination_blob_name = 'paper_project'
source_file_name = 'SBC_pollution_China_foreign.gz'
gcp.upload_blob(bucket_name, destination_blob_name, source_file_name)
```

```sos Collapsed="false" kernel="python3"
### Move to bigquery
bucket_gcs ='chinese_data/paper_project/SBC_pollution_China_foreign.gz'
gcp.move_to_bq_autodetect(dataset_name= 'China',
							 name_table= 'SBC_pollution_China_foreign',
							 bucket_gcs=bucket_gcs)
```

<!-- #region Collapsed="true" kernel="python3" -->
# Generate Studio

To generate a notebook ready to use in the studio, please fill in the variables below:

'project_name' : Name of the repository
'input_datasets' : name of the table
'sheetnames' : Name of the sheet, if table saved in Google Spreadsheet
'bigquery_dataset' : Dataset name
'destination_engine' : 'GCP' or 'GS,
'path_destination_studio' : path to `Notebooks_Ready_to_use_studio`
'project' : 'valid-pagoda-132423',
'username' : "thomas",
'pathtoken' : Path to GCP token,
'connector' : 'GBQ', ## change to GS if spreadsheet
'labels' : Add any labels to the variables,
'date_var' : Date variable
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
labels = []
date_var = 'year'
```

```sos Collapsed="false" kernel="python3"
regex = r"(.*)/(.*)"
path = os.getcwd()
parent_path = Path(path).parent
test_str = str(parent_path)
matches = re.search(regex, test_str)
github_repo = matches.group(2)

path_credential = '/Users/Thomas/Google Drive/Projects/Data_science/Google_code_n_Oauth/Client_Oauth/Google_auth/'

dic_ = {
    
          'project_name' : github_repo,
          'input_datasets' : 'SBC_pollution_China_foreign',
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

<!-- #region Collapsed="true" kernel="SoS" nteract={"transient": {"deleting": false}} -->
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
<!-- #endregion -->

```sos Collapsed="false" jupyter={"outputs_hidden": false, "source_hidden": false} kernel="python3" nteract={"transient": {"deleting": false}}
Storage = 'GBQ'
Theme = 'Trade' 
Database = 'China'
Description = "The table is related to the paper on soft budget contrain. The difference with the SBC china is the use of foreign share instead of SOE share"
Filename = 'SBC_pollution_China_FOREIGN_preprocessing'
Status = 'Active'
```

```sos Collapsed="false" jupyter={"outputs_hidden": false, "source_hidden": false} kernel="python3" nteract={"transient": {"deleting": false}}
Source_data = [
    "asif_firm_china",
    "China_city_pollution_98_2007",
    "TCZ_list_china",
    "cityname_and_code",
    'province_location',
    'China_cities_target_so2'
    ]
```

<!-- #region Collapsed="false" kernel="SoS" nteract={"transient": {"deleting": false}} -->
The next cell pushes the information to [Coda](https://coda.io/d/MasterFile-Database_dvfMWDBnHh8/Test-API_suDBp#API_tuDK4)
The next cell pushes the information to Coda
<!-- #endregion -->

```sos Collapsed="false" kernel="python3"
regex = r"(.*)/(.*)"
path = os.getcwd()
parent_path = Path(path).parent
test_str = str(parent_path)
matches = re.search(regex, test_str)
github_repo = matches.group(2)

Profiling = False
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
    
with open('token_coda.json') as json_file:
    data = json.load(json_file)
    
token = data[0]['token'] 
headers = {"Authorization": "Bearer " + token}
params = {
  'isOwner': True
}

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

```sos Collapsed="false" kernel="python3"

```
