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
    name: python3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region -->
# asif_firm_china data preprocessing

This notebook has been generated on 2019-08-06 08:40 

The objective of this notebook is to prepare ASIF dataset. There are issues with year 2008 & 2009. We will cover it into more details in the section *Data prep*. 

DEPRECATED: (Are you reading for the pain to translate STATA do file to Python? Yes.. Let's do it.)

We changed the stata file to csv. We did it toi translate the STATA 13 unicode to modern chinese.



We follow this [do file](https://feb.kuleuven.be/public/u0044468//CHINA/appendix/Match%20Firms%20Over%20Time.do)

The paper related to the data construction is [Challenges of working with the Chinese NBS firm-level data](https://docs.google.com/file/d/16agSbxO7cYuEn1v2bvw16ZRAx9gg7-Zm/edit)

The Raw data has been processed following this Notebook, [Asif_raw_to_csv_preprocessing](https://nbviewer.jupyter.org/github/thomaspernet/DataLab-JupyterNotebooks/blob/master/Notebook_dataprocessing/Asif_raw_to_csv_preprocessing.ipynb)

Variables names 1998-2009 available [here](https://docs.google.com/spreadsheets/d/1gfdmBKzZ1h93atSMFcj_6YgLxC7xX62BCxOngJwf7qE/edit#gid=1504397597) 

## Global steps 

The global steps to construct the dataset are the following:



## Data source 

The data source to construct the dataset are the following:
<!-- #endregion -->


 ### Big Query Dataset 
 
 ### Google Cloud Storage Dataset 
 
 - asif_year_2008 
 - asif_year_ 
 ### Google Spreadsheet Dataset 
 
 - [cityname_and_code](https://docs.google.com/spreadsheets/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA) 
 - [provinces_location](https://docs.google.com/spreadsheets/1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g)


## Destination

The new dataset is available from XXX

- GS: None
- GCS: asif_firm_china.gz
- BG: asif_firm_china


# Load Dataset


```python jupyter={"outputs_hidden": true}
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
from GoogleDrivePy.google_platform import connect_cloud_platform
import pandas as pd 
import numpy as np
import pandas_profiling
import tqdm
```

```python jupyter={"outputs_hidden": true}
gs = connector.open_connection(online_connection = False, 
	path_credential = '/Users/Thomas/Google Drive/Projects/Data_science/Google_code_n_Oauth/Client_Oauth/Google_auth/')

service_gd = gs.connect_remote(engine = 'GS')
service_gcp = gs.connect_remote(engine = 'GCP')

gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])

project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project,
											 service_account = service_gcp['GoogleCloudP'])
```


## Load asif_firm_china from Google Cloud Storage

Feel free to add description about the dataset or any usefull information.



```python jupyter={"outputs_hidden": true}

#df_load_data = pd.DataFrame()
#for dataset in [
#    'asif_year_1998.gz', 'asif_year_1999.gz',
#    'asif_year_2000.gz', 'asif_year_2001.gz',
#    'asif_year_2002.gz', 'asif_year_2003.gz',
#    'asif_year_2004.gz', 'asif_year_2005.gz',
#    'asif_year_2006.gz', 'asif_year_2007.gz',
   # 'asif_year_2008.gz', 'asif_year_2009.gz'
#]:
#    gcp.download_blob(bucket_name = 'chinese_data',
#                  destination_blob_name = 'Panel_china/Asif_panel_china/Raw_',
#                  source_file_name = dataset)
#                  
#    df_temp = pd.read_csv(dataset,
#                          compression='gzip',
#                          header=0,
#                          sep=',',
#                          quotechar='"',
#                          error_bad_lines=False)
#    df_load_data = df_load_data.append(df_temp)
#df_load_data.head()

```


## Load cityname_and_code from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset



```python jupyter={"outputs_hidden": true}

### Please go here https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA
### To change the range

sheetid = '1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA'
sheetname = 'final'

df_cityname_and_code = gdr.upload_data_from_spreadsheet(sheetID = sheetid, sheetName = sheetname,
	 to_dataframe = True)
df_cityname_and_code.head()

```


## Load provinces_location from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset



```python jupyter={"outputs_hidden": true}

### Please go here https://docs.google.com/spreadsheets/d/1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g
### To change the range

sheetid = '1pNMYAannF0g47Vrecu9tzrQ83XaaYmnXJeSuIFwr26g'
sheetname = 'provinces_location.csv'

df_provinces_location = gdr.upload_data_from_spreadsheet(sheetID = sheetid, sheetName = sheetname,
	 to_dataframe = True)
df_provinces_location.head()

```

## Load CIC_industry_name from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset

```python jupyter={"outputs_hidden": true}
### Please go here https://docs.google.com/spreadsheets/d/1j6WnAV3AcUQ4yFw8BibzJ5yrzR6nXnOMelnNHPDZBQU
### To change the range

sheetid = '1j6WnAV3AcUQ4yFw8BibzJ5yrzR6nXnOMelnNHPDZBQU'
sheetname = 'industry_name'

df_CIC_industry_name = gdr.upload_data_from_spreadsheet(sheetID = sheetid, sheetName = sheetname,
	 to_dataframe = True)
df_CIC_industry_name.head()
```

# Workflow

In this section, we will construct the dataset, and document each step of the workflow.

Please use the following format for the documentation:

- `##` Step 1: XXX
- `###` (optional) Underlying process description
- `##` Step 2: YYY
- `###` (optional) Underlying process description

Note: **You need to rename the last dataframe `df_final`**

<!-- #region -->
## Step 1: Prepare data 1998-2007

For year 2008, we have ion hand two differents datasets. None of them look alike. We use the second one because it has all the observations BUT not the firm's ID. The first one missing 70% of the data

Variables kept: 

|  Brands          | 2008       | 2009               |
| ---------------- | ---------- | ------------------ |
| bdat             | B131/开业(成立)时间--年       | 开业(成立)时间--年        |
| cic              | B07  / 行业代码      | 行业代码               |
| dq               | B05 /新行政代码 (6 digits)       |                    |
| e_HMT            | E06        | -                  |
| e_collective     | E03        | -                  |
| e_foreign        | E02        | -                  |
| e_individual     | E05        | -                  |
| e_legal_person   | E04        | -                  |
| e_state          | E01        | -                  |
| employment       | B2001  /全部从业人员年平均人数    | 全部从业人员年平均人数        |
| export           | V12  /出口交货值      | 出口交货值              |
| fa_net           |     固定资产合计       |                    |
| fa_original      |            |                    |
| a_dep            |            |                    |
| c_dep            |            |                    |
| id               | B00        | 法人代码               |
| input            |            |                    |
| legal_person     | B03        |                    |
| name             |    法人单位        |                    |
| new_product      |            |                    |
| output           | V08 /工业总产值（当年价格       | 工业总产值(当年价格)        |
| phone            | B062 /电话号码      | 电话号码               |
| product1_        |   主营产品1         |                    |
| profit           | OS25  /营业利润     | 营业利润               |
| revenue          | OS03   /主营业务收入    | 主营业务收入             |
| street           | B053    /街道办事处   | 街道办事处              |
| town             | B051   /乡（镇）    | 乡（镇）               |
| type             | B10   /登记注册类型     | 登记注册类型             |
| va               | V08 - OS06 | 工业总产值(当年价格) - 营业费用 |
| village          | B052  /街（村）、门牌号     | 街（村）、门牌号           |
| wage             | OS35       |                    |
| zip              | B040  /邮政编码     | 邮政编码               |


**Issues**

- step 10: match by firm ID
    - deal with duplicates of IDs (there are a few firms that have same IDs)
    
    
We can import all the variables since all the files in Storage have each column respectively. Even thought, they don't have value
<!-- #endregion -->

```python jupyter={"outputs_hidden": true}
import tqdm
df_ASIF = pd.DataFrame()

dic_year = {}

dtypes = {
    'id':'str',
    'year':'str',
    'bdat':'str',
    'citycode':'str',
    'type':'str',
    'cic':'str',
    'zip':'str', 
    'phone':'str',
    'town':'str',
    'product1_':'str',
    'legal_person':'str',
    'output':np.int32,
    'export':np.int32, 
    'revenue':np.float32,
    'profit':np.int32,                
    'employment':np.int32, 
    'e_HMT':np.float32,
    'e_collective':np.float32,
    'e_foreign':np.float32,
    'e_individual':np.float32,
    'e_legal_person':np.float32,
    'e_state':np.float32,
    'wage':np.float32,
    'input':np.float32,
    'va':np.float32
    
}

for year in tqdm.tqdm(range(1998, 2008, 1)):
    #print(year)
    var = "df_{0}".format(year)    
    df_ = pd.read_csv(
        'asif_year_{0}.gz'.format(year),
        dtype = dtypes,
        compression='gzip',
        header=0,
        sep=',',
        quotechar='"',
        error_bad_lines=False
        )
    dic_year.update({var : df_})
    df_ASIF = df_ASIF.append(df_, sort=False)
```

```python jupyter={"outputs_hidden": true}
dic_ = {
    'year': ["1998",
             "1999",
             "2000",
             "2001",
             "2002",
             "2003",
             "2004",
             "2005",
             "2006",
             "2007"
             ],
    'count_brand':
        [165118,
         162033,
         162883,
         169030,
         181557,
         196222,
         279092,
         271835,
         301961,
         336768
         ],

    'output_brand':
    [
        6.77,
        7.27,
        8.57,
        9.41,
        11.08,
        14.23,
        20.16,
        25.16,
        31.66,
        40.52
    ],
    'va_brand':
    [
        1.94,
        2.16,
        2.54,
        2.79,
        3.30,
        4.20,
        6.62,
        7.22,
        9.11,
        11.70
    ],
    'employment_brand':
    [
        56.44,
        58.05,
        53.68,
        52.97,
        55.21,
        57.49,
        66.27,
        68.96,
        73.58,
        78.75

    ]
}
brand = pd.DataFrame(dic_).set_index('year')
count = df_ASIF.groupby('year')['id'].count().rename('count')
output = (df_ASIF.groupby('year')['output'].sum()/ 1000000000).round(1)
va = (df_ASIF.groupby('year')['va'].sum()/ 1000000000).round(1)
emp = (df_ASIF.groupby('year')['employment'].sum()/ 1000000).round(2)

asif = pd.concat(
    [brand, count, output, va, emp],
    axis=1).reindex(
    columns=['count_brand', 'count',
             'output_brand', 'output',
             'va_brand', 'va',
             'employment_brand', 'employment'])
asif
```

```python jupyter={"outputs_hidden": true}
df_ASIF.groupby(['year']).size().plot(kind='bar')
```

This is an ID test to make sure this ID has always 11 obs through the notebook

```python jupyter={"outputs_hidden": true}
df_ASIF.loc[lambda x:x['id'].isin(['209752211'])][
    ['year', 'id', 'name', 'citycode', 'output', 'phone']
].sort_values(by = ['id','year', 'name'])
```

## Create matching variables

1. match by the names of legal person representatives

Stata codes 

```
replace legal_person`i'="." if legal_person`i'==""
gen code1=legal_person`i'+substr(dq`i',1,4) 
```

2. match by phone number + city code

Stata codes 

```
replace phone`i'="." if phone`i'==""
gen code2=substr(dq`i',1,4)+substr(cic`i',1,3)+phone`i'
```

3. match by code = founding year + geographic code + industry code + name of town + name of main product

Stata codes 

```
replace town`i'="." if town`i'==""
replace product1_`i'="." if product1_`i'==""
gen code3=bdat`i'+substr(dq`i',1,6)+substr(cic`i',1,4)+town`i'+product1_`i'
```


# Add city and industry

We add city and industry now so that we get a consistent city code

```python jupyter={"outputs_hidden": true}
def multiple_city(df, cityvar = 'citycode'):
    temp_multi = (df
                  .groupby(['id'])[cityvar]
                  .nunique()
                  .sort_values()
                  .reset_index()
                  .rename(columns = {'citycode': 'count'})    
             )
    
    return temp_multi
```

```python jupyter={"outputs_hidden": true}
temp_multi = multiple_city(df = df_ASIF)
temp_multi.groupby('count')['id'].count()
```

In the following ID, the firm in 2004 went top  Huzhou, but the firm's name is Shanghai

```python jupyter={"outputs_hidden": true}
df_ASIF[df_ASIF['id'] == '147133481'][['year', 'id',
                                       'name', 'citycode',
                                       'output', 'phone']]
```

We extract the city name from the company's name, when possible 

```python jupyter={"outputs_hidden": true}
raw_list = df_cityname_and_code['citycn'].tolist()
df_ASIF['city_prod'] = df_ASIF['name'].str.extract(r"(?=(" + '|'.join(raw_list) +
                                             r"))")
missing_cities_before = df_ASIF['city_prod'].isnull().sum()
print('Sum missing cities {}'.format(missing_cities_before))
```

Now the firm's is in Shanghai, not Hezhou

```python jupyter={"outputs_hidden": true}
df_ASIF[df_ASIF['id'] == '147133481'][['year', 'id',
                                       'name', 'citycode',
                                       'city_prod',
                                       'output',
                                       'phone']]
```

```python jupyter={"outputs_hidden": true}
df_ASIF[df_ASIF['id'] == '114591099'][['year', 'id',
                                       'name', 'citycode',
                                       'city_prod',
                                       'output',
                                       'phone']]
```

```python jupyter={"outputs_hidden": true}
df_ASIF.loc[lambda x:x['id'].isin(['209752211'])][
    ['year', 'id', 'name', 'citycode', 'output', 'phone']
].sort_values(by = ['id','year', 'name'])
```

Test -> merge `df_cityname_and_code` with `city_prod`  and `citycn` to get the `geocode4_corr` 

```python jupyter={"outputs_hidden": true}
#test_m = df_ASIF.merge(
#    df_cityname_and_code[['citycn',
#                          'geocode4_corr'
#                         ]
#                        ].drop_duplicates(
#        subset = 'citycn'
#    ),
#    left_on= 'city_prod',
#    right_on = 'citycn',
#    how = 'left',
#indicator = True)
#test_m.shape
#test_m.groupby(['_merge'])['_merge'].count()
#test_m = test_m.drop(columns = ['_merge', 'citycn'])
```

<!-- #region toc-hr-collapsed=false -->
## Add city

1. Merge `citycode` with `df_cityname_and_code`
2. Merge `Province_cn` with `prov2013`


Warning, since we don't match the `citycn`, we need to drop the duplicates `citycn`. It's to avoid this:

```
5001	5001	重庆市	Chongqing	重庆	Chongqing	重庆市	Chongqing
5001	5001	重庆	Chongqing	重庆	Chongqing	重庆市	Chongqing
5002	5001	重庆市	Chongqing	重庆	Chongqing	重庆市	Chongqing
```
To add rows if many city name
<!-- #endregion -->

```python jupyter={"outputs_hidden": true}
df_ASIF.shape
```

```python jupyter={"outputs_hidden": true}
df_cityname_and_code_ = df_cityname_and_code.drop(columns = 
                                                  ['citycn',
                                                   'cityen']).drop_duplicates()
df_cityname_and_code_.loc[lambda x : x['geocode4_corr'].isin(['5001'])]
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city = df_ASIF.merge(df_cityname_and_code_,
               left_on = 'citycode',
               right_on = 'extra_coda',
               how = 'inner')
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city.loc[lambda x:x['id'].isin(['209752211'])][
    ['year', 'id', 'name', 'extra_coda','citycode', 'output', 'phone',
    'geocode4_corr']
].sort_values(by = ['id','year', 'name'])
```

```python jupyter={"outputs_hidden": true}
### 101326 observation unmatched
df_ASIF.shape[0] - df_ASIF_city.shape[0]
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city[df_ASIF_city['id'] == '147133481'][[
    'year', 'id', 'name', 'citycode','geocode4_corr',
    'city_prod',
    'output', 'phone']]
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city.loc[lambda x: 
                 (~x['city_prod'].isin([np.nan]))
                 &
                 (x['city_prod'] != x['citycn_correct'])
                ][[
    'year', 'id', 'name', 'citycode','geocode4_corr',
    'city_prod', 
    'output', 'phone']]
```

There are 8925 firms with different name and city, but only 37 have differents `citycode`

```python jupyter={"outputs_hidden": true}
temp_check = df_ASIF_city.loc[lambda x: 
                 (~x['city_prod'].isin([np.nan]))
                 &
                 (x['city_prod'] != x['citycn_correct'])
                ]#['id'].nunique()
(temp_check
 .groupby('id')['geocode4_corr']
 .nunique()
 .sort_values(ascending = False)
 .reset_index()
 .groupby('geocode4_corr').count()
)
```

We drop these 37 firms

```python jupyter={"outputs_hidden": true}
toremove = (temp_check
 .groupby('id')['geocode4_corr']
 .nunique()
 .sort_values(ascending = False)
 .loc[lambda x: x ==2]
 .index
)
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_ = df_ASIF_city.loc[lambda x: ~x['id'].isin(toremove)]
df_ASIF_city_.shape
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_.loc[lambda x:x['id'].isin(['209752211'])][
    ['year', 'id', 'name', 'citycode', 'output', 'phone']
].sort_values(by = ['id','year', 'name'])
```

Remember, for the city, we need to exclude:

- [Spreadsheet](https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA/edit#gid=304413184)
- `extra_coda`, `citycn`&`cityen`: Not unique name ie: (巴彦淖尔; 巴彦淖尔盟)


```python jupyter={"outputs_hidden": true}
for city in ['geocode4_corr','citycn_correct',
             'cityen_correct']:
    print('The variable {0} has {1} unique values'.format(city,
                                                          df_ASIF_city_[city].nunique()
                                                         ))
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_ = df_ASIF_city_.drop(columns = [
                                            'city_prod',
                                           'extra_coda'])
```

## Provinces

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov = df_ASIF_city.merge(df_provinces_location,
               left_on = 'Province_cn',
               right_on = 'prov2013',
               how = 'inner')
df_ASIF_city_prov = df_ASIF_city_prov.drop(columns =
                                           ['prov2013', 'Provinces'])
df_ASIF_city_prov.shape
```

Some city like 

1507	1507	呼伦贝尔	Hulunbeier	呼伦贝尔	Hulunbeier	内蒙古自治区	Inner Mongolia Autonomous Region
1507	1507	呼伦贝尔盟	Hulun Buir League	呼伦贝尔	Hulunbeier	内蒙古自治区	Inner Mongolia Autonomous Region

have the same codes but two city names, we need to drop the duplocates to remove the duplicates from the merge

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_ = df_ASIF_city_prov.drop_duplicates()
df_ASIF_city_prov.shape
```

Double check multiple cities

```python jupyter={"outputs_hidden": true}
temp_multi = multiple_city(df = df_ASIF_city_prov_,
                          cityvar = 'geocode4_corr')
temp_multi.groupby('geocode4_corr')['id'].count()
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_[df_ASIF_city_prov_['id'] == '245487275'][
    ['year', 'id', 'name','citycode' , 'geocode4_corr', 'output', 'phone']
]
```

Remove the 3 firms with 3 locations

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov.shape
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_ = df_ASIF_city_prov.merge(
    temp_multi.rename(columns = {'geocode4_corr': 'count'})
).loc[lambda x :x['count'] == 1]
df_ASIF_city_prov_.shape
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_['id'].nunique()
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_['year'].unique()
```

```python jupyter={"outputs_hidden": true}
pd.concat([
    df_ASIF.groupby('year')['id'].count(),
    df_ASIF_city_prov_.groupby('year')['id'].count()
], axis = 1).plot(kind='bar')
```

### New matching var

```python jupyter={"outputs_hidden": true}
#df_ASIF['legal_person'] = df_ASIF['legal_person'].str.strip()
```

<!-- #region toc-hr-collapsed=true toc-nb-collapsed=true -->
# ARCHIVE - Some issue with the data

- Need to correct chinese name:
 
 Cell below show same character but different spelling
 
 - ID: HB9432022	
    - name: 衡水市潴泷万向有限公司
- ID: HB9432225	
    - name: 衡水市潴龙万向有限公司


below, there are two differents firms, but in 2005, the ID is switched
<!-- #endregion -->

```python Collapsed="false"
#df_ASIF_city_prov_[(df_ASIF_city_prov_['id'] == 'HB9432225') |
#         (df_ASIF_city_prov_['id'] == 'HB9432022')
#        ][
#    ['year', 'id', 'name', 'citycode', 'output', 'phone']
#].sort_values(by = ['id','year', 'name'])
```

<!-- #region Collapsed="false" -->
Add name in pinyin, more reliable
<!-- #endregion -->

```python Collapsed="false"
#import pinyin
```

```python Collapsed="false"
#df_ASIF_city_prov_['namepinyin'] = df_ASIF_city_prov_['name'].apply(lambda x: pinyin.get(x,
#                                                      format="numerical")
#                                )
```

<!-- #region Collapsed="false" -->
Number of unique id -> 588,011
<!-- #endregion -->

```python Collapsed="false"
#df_ASIF_city_prov_['id'].nunique()
```

<!-- #region Collapsed="false" -->
Number of unique name -> 718,077. Multi name firms
<!-- #endregion -->

```python Collapsed="false"
#df_ASIF_city_prov_['namepinyin'].nunique()
```

## Archive

```python Collapsed="false"
#idphone = (df_ASIF_city_prov_[['id','phone', 'namepinyin', 'geocode4_corr']]
#             .drop_duplicates(#subset=['phone'],
#                              #keep=False
#                             )
#             .rename(columns = {'phone':'dup_phone'})
#            )
#idphone.isna().sum()
```

```python Collapsed="false"
#idphone.head()
```

## Get max rows ID

<!-- #region Collapsed="false" -->
count the number of name rows by id name, and the maximum count will be the ID
<!-- #endregion -->

```python Collapsed="false"
#idnamecity = (df_ASIF_city_prov_[['id', 'namepinyin', 'geocode4_corr']]
#              .groupby(['id', 'namepinyin', 'geocode4_corr'])
#              .size()
#              .reset_index(name='counts')
              #.sort_values(by = ['namepinyin', 'counts'])
#          )
#idnamecity['max'] = idnamecity.groupby(['namepinyin'])['counts'].transform('max') 
#idnamecity = idnamecity[idnamecity['counts'] == idnamecity['max']]
#idnamecity.head()
```

```python Collapsed="false"
#idnamecity[(idnamecity['id'] == 'HB9432225') |
#         (idnamecity['id'] == 'HB9432022')
#        ]
#衡水市潴泷万向有限公司
#河北程杰汽车转向机械制造有限公司
```

```python Collapsed="false"
#namephone = (df_ASIF_city_prov_[['phone', 'namepinyin', 'geocode4_corr']]
#             .drop_duplicates(#subset=['phone'],
#                              #keep=False
#                             )
#             .rename(columns = {'phone':'dup_phone'})
#            )
#namephone.isna().sum()
```

```python Collapsed="false"
#namephone.shape
```

```python Collapsed="false"
#test = idnamecity.merge(namephone, 
#                on = ['namepinyin', 'geocode4_corr'],
#                how = 'inner').drop(columns  = 'max')
#test.shape
```

```python Collapsed="false"
#test[(test['id'] == 'HB9432225') |
#         (test['id'] == 'HB9432022')
#        ]
```

<!-- #region Collapsed="false" -->
Number of firm by year
<!-- #endregion -->

```python Collapsed="false"
#(test[['id', 'counts']]
# .drop_duplicates()
# .groupby(['id'])['counts']
# .sum()
# .reset_index()
# .sort_values(by = 'counts')
# .groupby('counts')
# .count()
#)
```

```python Collapsed="false"
#df_ASIF_city_prov_.loc[lambda x:x['id'].isin(['169424423'])][
#    ['year', 'id', 'name', 'citycode', 'output', 'phone']
#].sort_values(by = ['id','year', 'name'])
```

## Archive

Now we keep the Firms with no ID and we find them back with Name and Phone

```python Collapsed="false"
#idNan = df_ASIF_city_prov_[df_ASIF_city_prov_['id'].isin([np.nan])][[
##                                                                    #'year',
#                                                                     'geocode4_corr',
#                                                                    'namepinyin',
#                                                                    'phone']]
```

```python Collapsed="false"
#idNan.isna().sum()
```

```python Collapsed="false"
#idNan['year'].unique()
```

<!-- #region Collapsed="false" -->
merge with name, city and phone
<!-- #endregion -->

```python Collapsed="false"
#year_0809 = test.merge(idNan,
#          left_on = ['namepinyin',
#                'geocode4_corr',
#                'dup_phone'],
#           right_on = ['namepinyin',
#                'geocode4_corr',
#                'phone'],
#           how = 'right',
#           indicator=True
#          )
```

```python Collapsed="false"
#year_0809.groupby('_merge')['_merge'].count()
```

```python Collapsed="false"
#year_0809.head()
```

<!-- #region Collapsed="false" -->
301719 firms matched.
<!-- #endregion -->

```python Collapsed="false"
#matched_0809 = year_0809[year_0809['_merge'] == 'both']
```

<!-- #region Collapsed="false" -->
Find the unmatched with name only
<!-- #endregion -->

```python Collapsed="false"
#unmatched_0809 = year_0809[year_0809['_merge'] == 'right_only'].drop(columns=[
#    '_merge', 'id', 'counts', 'namepinyin', 'dup_phone'
    
    #'dup_phone'
#])
```

```python Collapsed="false"
#test_1 = test.merge(unmatched_0809,
#          left_on=['dup_phone',
#                'geocode4_corr'],
#           right_on=['phone',
#                'geocode4_corr'],
#           how='right',
#           indicator=True
#          )#.groupby('_merge').count()

```

```python Collapsed="false"
#matched_0809_2 = test_1[test_1['_merge'] == 'both'].drop(columns = ['_merge', 'phone'])
```

```python Collapsed="false"
#matched_0809 = matched_0809.drop(columns = ['_merge', 'phone']).append(matched_0809_2)
```

```python Collapsed="false"
#matched_0809.shape
```

```python Collapsed="false"
#matched_0809.head()
```

```python Collapsed="false"
#test.head()
```

```python Collapsed="false"
#IDnew = test.append(matched_0809).drop_duplicates()
#IDnew.shape
```

```python Collapsed="false"
#temp = test == IDnew
#test.equals(IDnew)
```

## Unique ID

```python Collapsed="false"
#import random 
#import string
#def randomID():
#    random_ = ''.join([random.choice(string.ascii_letters+
#                                     string.digits) for n in range(30)])
#    return random_
```

```python Collapsed="false"
#newID = (test
#         .groupby('id')
#         .apply(lambda x: randomID())
#         .rename("newID")
#         .reset_index()
#         .merge(test, 
#                  on = 'id')
#         .rename(columns = {'dup_phone': 'phone'})
#        )
#newID.shape
```

```python Collapsed="false"
#newID.head()
```

```python Collapsed="false"
#df_ASIF_city_prov_.shape
```

```python Collapsed="false"
#newID[(newID['id'] == 'HB9432225') |
#         (newID['id'] == 'HB9432022')
#        ]
```

```python Collapsed="false"
#test = df_ASIF_city_prov_[(df_ASIF_city_prov_['id'] == 'HB9432225') |
#         (df_ASIF_city_prov_['id'] == 'HB9432022')
#        ][['year', 'id', 'name','output', 'phone', 'geocode4_corr',
# 'namepinyin']].sort_values(by = ['id','year', 'name'])
#test.head()
```

```python Collapsed="false"
#test_ = test.merge(newID, on = ['id', 'geocode4_corr', 'namepinyin', 'phone'],
#           how='left', indicator=True)

#unmatched = test_[test_['_merge'] == 'left_only'].drop(
#            columns=['_merge', 'newID',
#                     # 'counts'
#                     ]
#        )
#newID_ =  newID.loc[lambda x:x['id'].isin(unmatched['id'].to_list())]
```

```python Collapsed="false"
#unmatched
```

```python Collapsed="false"
#newID_
```

```python Collapsed="false"
#unmatched.merge(newID_, on = ['namepinyin', 'phone'], suffixes = ('_old', '_new'))
```

```python Collapsed="false"

```

### Merge 98-07

Need to make sure max year by ID is 10

```python Collapsed="false"
#df9807 = df_ASIF_city_prov_[~df_ASIF_city_prov_['year'].isin(['2008', '2009'])]
#df9807.shape
```

```python Collapsed="false"
def merge_(list_merge, df, newID, remove_=False):
    """
    List_merge: List of list containint the variables to
    merge with.
    Output is a dataframe with matched observation
    remove_: Avoid to have many firm's id for a single year
    """

    # Merge High level:

    unmatched = df
    newID_ = newID.loc[lambda x:x['id'].isin(unmatched['id'].to_list())]

    final_append = pd.DataFrame()
    size_ = df.shape[0]

    for m in list_merge:

        if unmatched.shape[0] == size_:

            merge = unmatched.merge(newID_,
                                    on=m,
                                    how='left',
                                    indicator=True
                                    )
        else:
            merge = unmatched.merge(newID_,
                                    on=m,
                                    how='inner',
                                    indicator=True,
                                    suffixes=('_old', '_new')
                                    )
        newID_ = newID_.loc[lambda x:x['id'].isin(unmatched['id'].to_list())]

        # Print
        print(merge.groupby('_merge')['_merge'].count())

        # select unmatched
        unmatched = merge[merge['_merge'] == 'left_only'].drop(
            columns=['_merge', 'newID',
                     # 'counts'
                     ]
        )

        # keep newmatch

        match_ = merge[merge['_merge'] == 'both'].drop(
            columns=['_merge',
                     # 'counts'
                     ]
        )

        final_append = final_append.append(match_, sort=False)

    # final_append = final_append.drop_duplicates()

    if remove_:

        size_ = (final_append
                 .drop_duplicates()
                 .groupby('newID')
                 .size()
                 .reset_index(name='size')
                 )

        final_append = final_append.merge(size_, on='newID')
        final_append = (final_append
                        .loc[lambda x: x['size'].isin([
                            1, 2, 3, 4, 5, 6, 7, 8, 9, 10
                        ])]
                        .drop(columns=[
                            'count',
                            'namepinyin',
                            'newID',
                            'counts',
                            'size'
                        ])
                        )

    return final_append
```

```python Collapsed="false"
#list_merge = [
#    [
#        'id', 'geocode4_corr', 'namepinyin', 'phone'
#    ],
    #[
    #    'namepinyin', 'phone'
        #'newID',
        #'id'
    #],

#]
```

```python Collapsed="false"
#df9807 = df_ASIF_city_prov_[~df_ASIF_city_prov_['year'].isin(['2008', '2009'])]
#print(df9807.shape)

#df_9807  = merge_(list_merge = list_merge,
#                  df = df9807,
#                  newID = newID,
#                  remove_ = True
#                 ) 
#df_9807.shape
```

```python Collapsed="false"
#df_9807.groupby('size')['size'].count()
```

```python Collapsed="false"
#list(df_9807)
```

### test

```python Collapsed="false"
#df_9807[(df_9807['id'] == '102933020') |
#         (df_9807['id'] == '102922655')
#        ][
#    ['year', 'id', 'newID','name', 'citycode', 'output', 'phone', 'id_old', 'id_new']
#].sort_values(by = ['newID','year', 'name'])
```

```python Collapsed="false"
#df_9807[(df_9807['newID'] == '5clFOkf2pmm8PZG9l5PvJt6Jd9vRgs')
#        ][
#    ['year', 'id', 'newID','name', 'citycode', 'output', 'phone', 'id_old', 'id_new']
#].sort_values(by = ['newID','year', 'name'])
```

```python Collapsed="false"
#(df_9807
# .drop_duplicates()
# .groupby('newID')
# .size()
# .sort_values()
# .reset_index(name = 'count')
# .groupby('count')['newID']
# .count()
#)
```

```python Collapsed="false"
#df_9807.loc[lambda x:x['newID'].isin(['9ZX1vcDNgeSNbacGnBoE3Y2CviHAxa'])][
#    ['year', 'id', 'newID','name', 'citycode', 'output', 'phone', 'id_old', 'id_new']
#].sort_values(by = ['newID','year', 'name'])
```

```python Collapsed="false"
#df_ASIF_city_prov_[(df_ASIF_city_prov_['id'] == '120967734') |
#         (df_ASIF_city_prov_['id'] == '120966897')
#        ][['year', 'id', 'name','output', 'phone', 'geocode4_corr',
# 'namepinyin']].sort_values(by = ['id','year', 'name'])
```

### Merge 2008: DEPRECATED

```python Collapsed="false"
#list_merge = [
#    [
#        'newID',
#        'namepinyin',
#        'geocode4_corr',
#        'phone'],
#    [
#        'newID',
#        'phone',
#        'geocode4_corr'],
#    [
#        'newID',
#        'namepinyin'],
#]
```

```python Collapsed="false"
#df08 = df_ASIF_city_prov_[df_ASIF_city_prov_['year'].isin(['2008'])]
#print(df08.shape)

#df_2008  = merge_(list_merge = list_merge,
#                  df = df08,
#                 remove_ = True) 
#df_2008.shape
```

### Merge 2009: DEPRECATED

```python Collapsed="false"
#list_merge = [
#    [
#        'newID',
#        'id',
#        'namepinyin',
#        'geocode4_corr',
#        'phone'
#    ],
#    [
#        'newID',
#        'namepinyin',
#        'geocode4_corr',
#        'phone'],
#    [
#        'newID',
#        'phone',
#        'geocode4_corr'],
#    [
#        'newID',
#        'namepinyin'],
#]
```

```python Collapsed="false"
#df09 = df_ASIF_city_prov_[df_ASIF_city_prov_['year'].isin(['2009'])]
#print(df09.shape)

#df_2009  = merge_(list_merge = list_merge,
#                  df = df09,
#                 remove_ = True ) 
#df_2009.shape
```

## append All and check if correct : DEPRECATED

```python Collapsed="false"
#df_appended = df_9807.append([df_2008, df_2009])
```

```python Collapsed="false"
#(df_appended
# .drop_duplicates()
# .groupby('newID')
# .size()
# .sort_values()
# .reset_index(name = 'count')
# .groupby('count')['newID']
# .count()
#)
```

```python Collapsed="false"
#df_appended.shape
```

```python Collapsed="false"
#pd.concat([
#    df_ASIF.groupby('year')['id'].count(),
#    df_appended.groupby('year')['newID'].count()
#], axis = 1).plot(kind='bar')
```

<!-- #region toc-hr-collapsed=true -->
## Archive
<!-- #endregion -->

```python Collapsed="false"
#df_ASIF_city_prov_[
#        (df_ASIF_city_prov_['id'] == '713996768') 
#    ][['year', 'id', 'name', 'geocode4_corr', 'output', 'phone']
#     ].sort_values(by=['id', 'year', 'name'])
```

```python Collapsed="false"
#idphone[idphone['id']=='713996768']
```

```python Collapsed="false"
#idphone.shape
```

```python Collapsed="false"
#namephone = (df_ASIF_city_prov_[['name','phone', 'geocode4_corr']]
#             .drop_duplicates()
#             .rename(columns = {'phone':'dup_phone'})
#             .dropna()
#            )
#namephone.head()
```

```python Collapsed="false"
### All name with the phone nimber
```

```python Collapsed="false"
#temp = idphone.dropna()
#temp.shape
```

```python Collapsed="false"
#idnamephone = temp.merge(namephone,
#          on = ['dup_phone','geocode4_corr'],
#          how = 'inner').drop_duplicates()
```

```python Collapsed="false"
#idnamephone[(idnamephone['id'] == 'HB9432225') |
#         (idnamephone['id'] == 'HB9432022')
#        ].sort_values(by = 'id')
```

```python Collapsed="false"
#df_ASIF_city_prov_[
#        (df_ASIF_city_prov_['id'] == '156226807') |
#        (df_ASIF_city_prov_['id'] == '704886356') |
##        (df_ASIF_city_prov_['id'] == '713996768') 
#    ][['year', 'id', 'name', 'geocode4_corr', 'output', 'phone']
#     ].sort_values(by=['id', 'year', 'name'])
```

```python Collapsed="false"
#idnamephone[(idnamephone['id'] == '156226807') |
#            (idnamephone['id'] == '704886356') |
#            (idnamephone['id'] == '713996768')
#        ].sort_values(by = 'id')
```

```python Collapsed="false"
#idnamephone[(idnamephone['id'] == 'HB9432225') |
#         (idnamephone['id'] == 'HB9432022')
#        ].sort_values(by = 'id')
```

<!-- #region Collapsed="false" -->
Unique list of ID and city
<!-- #endregion -->

```python Collapsed="false"
#idcity = (df_ASIF_city_prov_[['id','geocode4_corr']]
##             .drop_duplicates()
#            .dropna()
#            )
```

```python Collapsed="false"
#idcity.groupby('id')['geocode4_corr'].count().nunique()
```

<!-- #region Collapsed="false" -->
We create a unique random ID
<!-- #endregion -->

```python Collapsed="false"
#import random 
#import string
#def randomID():
##    random_ = ''.join([random.choice(string.ascii_letters+
#                                    string.digits) for n in range(30)])
#    return random_
```

```python Collapsed="false"
#randomID()
```

```python Collapsed="false"
#df_subsample = (df_ASIF_city_prov_[['id', 'name', 'geocode4_corr']]
#                .drop_duplicates()
#                .dropna()
#               )

#df_subsample.head()
```

```python Collapsed="false"
#df_subsample.shape
```

<!-- #region Collapsed="false" -->
Number of ID with different names
<!-- #endregion -->

```python Collapsed="false"
#df_subsample.groupby('id')['name'].count().reset_index().groupby(by = "name").count()
#(df_subsample[['id', 'name']]
# .drop_duplicates()
## .groupby('id')['name']
# .count()
# .rename('count_ID')
# .reset_index()
# .groupby('count_ID')
# .count()
#)
```

```python Collapsed="false"
#(df_subsample[['id', 'geocode4_corr']]
# .drop_duplicates()
# .groupby('id')['geocode4_corr']
# .count()
# .rename('count_ID')
# .reset_index()
# .groupby('count_ID')
# .count()
#)
```

<!-- #region Collapsed="false" -->
Drop firms with differents cities
<!-- #endregion -->

```python Collapsed="false"
#multple_cities = (
#    df_subsample[['id', 'geocode4_corr']]
# .drop_duplicates()
# .groupby('id')['geocode4_corr']
# .count()
# .rename('count_ID')
# .reset_index()   
# .query('count_ID>1') 
# .drop(columns = 'count_ID')   
#)
#multple_cities.head()
```

```python Collapsed="false"
#776931 - 860
```

```python Collapsed="false"
#df_subsample = df_subsample[~df_subsample['id'].isin(multple_cities['id'])]
#f_subsample.head()
```

<!-- #region Collapsed="false" -->
Merge ID with phone number
<!-- #endregion -->

```python Collapsed="false"
#df_subsample_ph = df_subsample.merge(idphone,
#                   on = ['id', 'geocode4_corr'], 
#                   how =  'left',
#                   indicator=True
#                  )
```

```python Collapsed="false"
#df_subsample_ph.shape
```

```python Collapsed="false"
#df_subsample_ph.groupby('_merge')['_merge'].count()
```

```python Collapsed="false"
#df_subsample_ph = df_subsample_ph.drop(columns = '_merge')
#df_subsample_ph[df_subsample_ph['id']=='713996768']
```

<!-- #region Collapsed="false" -->
Merge name city code and phone
<!-- #endregion -->

```python Collapsed="false"
#df_subsample_ph_name = df_subsample_ph.merge(namephone,
#                      on = ['name', 'geocode4_corr', 'dup_phone'],
#                      how = 'inner',
                      #indicator=True
#                     )
```

```python Collapsed="false"
#df_subsample_ph_name.groupby('_merge')['_merge'].count()
```

```python Collapsed="false"
#df_subsample_ph_name[ 
#    (df_subsample_ph_name['id'] == 'HB9432225') |
#    (df_subsample_ph_name['id'] == 'HB9432022')
#        ].sort_values(by = 'id')
```

```python Collapsed="false"
#newID = (df_subsample
#         .groupby('id')
#         .apply(lambda x: randomID())
#         .rename("newID")
#         .reset_index()
#         .merge(df_subsample, 
#                  on = 'id')
         #.merge(idnamephone,
         #  on = ['geocode4_corr', 'name'])
         #.rename(columns = {'dup_phone': 'phone'})
         #.merge(idcity, 
         #       on = ['id']
         #      )
#        )
```

```python Collapsed="false"
#newID.head()
```

### Test

```python Collapsed="false"
#newID[(newID['id'] == 'HB9432225') |
#         (newID['id'] == 'HB9432022')
#        ]
```

<!-- #region Collapsed="false" -->
Merge with name to get a combinaison of ID. For instance, if 1 company name has 2 ID, we had both ID combination

Ex:
10 A
11 A

```
New frame
10 A 10
10 A 11
11 A 10
11 A 11
```

If we duplicates and keep first, we can assign a single new ID
<!-- #endregion -->

```python Collapsed="false"
#df_newID = (newID
#        .merge(
#            newID,
#            on = ['name', #'phone',
#                  'geocode4_corr'],
#            suffixes = ['_old', '_new'])
#        .drop(columns= ['id_new'])
#        .drop_duplicates(
#            subset=['newID_old', 'name'],
#            keep='first', 
#            inplace=False)
#        .drop(columns= 'newID_old')   
#)
```

```python Collapsed="false"
#df_newID.head()
```

### Some test

Three differences cases:

- Wrong ID
- Multiple city

```python Collapsed="false"
#df_newID[(df_newID['id_old'] == 'HB9432225') |
##         (df_newID['id_old'] == 'HB9432022')
       # ]
```

```python Collapsed="false"
#df_newID[(df_newID['id_old'] == '62900210X')
#        ]
```

```python Collapsed="false"
##df_ASIF_city_prov_[
#        (df_ASIF_city_prov_['phone'] == '5710786')
#    ][['year', 'id', 'name', 'geocode4_corr', 'output', 'phone']
#     ].sort_values(by=['id', 'year', 'name'])
```

```python Collapsed="false"
#df_newID[(df_newID['id_old'] == '156226807') |
#         (df_newID['id_old'] == '704886356') |
#         (df_newID['id_old'] == '713996768')
#        ]
```

<!-- #region Collapsed="false" -->
back to our example, when we will merge on one of the three variables above, we end up with the same `ID`
<!-- #endregion -->

```python Collapsed="false"
##df_ASIF_city_prov_[(df_ASIF_city_prov_['id'] == 'HB9432225') |
#        (df_ASIF_city_prov_['id'] == 'HB9432022')
#        ][
#    ['year', 'id', 'name', 'geocode4_corr', 'output', 'phone']
#].sort_values(by = ['id','year', 'name'])
```

<!-- #region Collapsed="false" -->
Need to add citycode
<!-- #endregion -->

<!-- #region Collapsed="false" -->
Count the number of unqiue firms
<!-- #endregion -->

```python Collapsed="false"
#df_newID['newID_new'].nunique()
```

<!-- #region Collapsed="false" -->
Count the number of firms with many names and many ID
<!-- #endregion -->

```python Collapsed="false"
#(df_newID
# .groupby('newID_new')['id_old']
# .count()
# .rename('count_ID')
# .reset_index()
# .groupby('count_ID')
# .count()
#)
```

```python Collapsed="false"
#(df_newID
# .groupby('newID_new')['name']
# .count()
# .rename('count_ID')
# .reset_index()
# .groupby('count_ID')
# .count()
#)
```

<!-- #region toc-hr-collapsed=true -->
## Add new ID

We can add the new ID by merging on `id_old`. The new consistent ID becomes `newID_new`

Note that, for year 2008, we can only merge with `name` since `id` is missing.

Year 2009, has also many missing values

### Workflow

1) Merge using `id`, `name` and `phone`
- keep `right_only`

2) Merge using `name` and `phone`
- Keep `right_only` and delete when `phone == nan`

3) Merge using `phone` and `city_code`
- Delete left over

We take id `HB9432022` and  `HB9432225` as example 
<!-- #endregion -->

```python Collapsed="false"
#df_newID[(df_newID['id_old'] == 'HB9432022') |
#         (df_newID['id_old'] == 'HB9432225')
#        ]
```

### Test

Some firms have the same phone numbers but not the same city

```python Collapsed="false"
#df_ASIF_city_prov_[
#        (df_ASIF_city_prov_['id'] == '62900210X')
#    ][['year', 'id', 'name', 'geocode4_corr', 'output', 'phone']
#     ].sort_values(by=['id', 'year', 'name'])
```

```python Collapsed="false"
#df_newID[(df_newID['id_old'] == '62900210X')
#        ]
```

```python Collapsed="false"
#df_ASIF_city_prov_[
#        (df_ASIF_city_prov_['phone'] == '5710786')
#    ][['year', 'id', 'name', 'geocode4_corr', 'output', 'phone']
#     ].sort_values(by=['id', 'year', 'name'])
```

<!-- #region Collapsed="false" -->
Year 2004 hasn't been matched but the IDs in 2005 have been found
<!-- #endregion -->

```python Collapsed="false"
#df_wave2['example_id']
```

```python Collapsed="false"
#df_wave2['after_id']
```

<!-- #region toc-hr-collapsed=false -->
## Archive: Match 2008/2009

- Create a dataframe with 2008 and unmatched firms in 2009
- Match with name only
<!-- #endregion -->

```python Collapsed="false"
#unmatch_2009 = (df_ASIF_new[
#    df_ASIF_new['_merge'] == 'right_only']
#    .drop(columns = ['id_old',
#                     'newID_new',
##                     '_merge'
#                    ]
#                     )
#)
#df_200809 = (df_ASIF[df_ASIF['year'] == '2008']
#           .append(unmatch_2009, sort=False)
#           .merge(df_newID,
##                 on = 'name',
#                 how = 'left',
#                 indicator=True
#                 )
#           .drop(columns= 'id')
#          )
#df_200809.shape
```

```python Collapsed="false"
#df_200809.head(3)
```

```python Collapsed="false"
#df_200809.groupby(['year', '_merge'])['_merge'].count()
```

<!-- #region Collapsed="false" -->
Keep match only and append to `df_ASIF_new``
<!-- #endregion -->

```python Collapsed="false"
#df_200809_both = df_200809[df_200809['_merge'] == 'both']
#df_ASIF_new = df_ASIF_new.append(df_200809_both, sort = False)
```

```python Collapsed="false"
#df_ASIF_new.head(3)
```

```python Collapsed="false"
#list(df_ASIF_new)
```

```python Collapsed="false"
#df_ASIF_new['id_old'].isna().sum()
```

```python Collapsed="false"
#df_ASIF_new['newID_new'].isna().sum()
```

```python Collapsed="false"
#df_ASIF_new = df_ASIF_new.dropna(subset = ['id_old'])
```

<!-- #region Collapsed="false" -->
Compare before/after matching
<!-- #endregion -->

```python Collapsed="false"
#pd.concat([
#    df_ASIF.groupby('year')['id'].count(),
#    df_ASIF_new.groupby('year')['newID_new'].count()
#], axis = 1).plot(kind='bar')
```

<!-- #region toc-hr-collapsed=true toc-nb-collapsed=true -->
# Industry name

- Create 2 digits industry
- Merge industry name

We include only manuyfacturing sectors: 

|  CIC | Industry_Name                                                                      | Short                            |
| ---- | ---------------------------------------------------------------------------------- | -------------------------------- |
| 13   | Processing of Food from Agricultural Products                                      | Processing foods                 |
| 14   | Foods                                                                              | Foods                            |
| 15   | Beverages                                                                          | Beverages                        |
| 16   | Tobacco                                                                            | Tobacco                          |
| 17   | Textile                                                                            | Textile                          |
| 18   | Textile Wearing Apparel, Footwear, and Caps                                        | Textile wearing                  |
| 19   | Leather, Fur, Feather and Related Products                                         | Leather and others               |
| 20   | Processing of Timber, Manufacture of Wood,Bamboo, Rattan, Palm, and Straw Products | Processing of Timber             |
| 21   | Furniture                                                                          | Furniture                        |
| 22   | Paper and Paper Products                                                           | Paper                            |
| 23   | Printing, Reproduction of Recording Media                                          | Printing                         |
| 24   | Articles For Culture, Education and Sport Activity                                 |  article                         |
| 25   | Processing of Petroleum, Coking, Processing of Nuclear Fuel                        | Processing of Petroleum          |
| 26   | Raw Chemical Materials and Chemical Products                                       | Raw Chemical Materials           |
| 27   | Medicines                                                                          | Medicines                        |
| 28   | Chemical Fibers                                                                    | Chemical Fibers                  |
| 29   | Rubber                                                                             | Rubber                           |
| 30   | Plastics                                                                           | Plastics                         |
| 31   | Non-metallic Mineral Products                                                      | Non-metallic Products            |
| 32   | Smelting and Pressing of Ferrous Metals                                            | Smelting ferrous Metals          |
| 33   | Smelting and Pressing of Non-ferrous Metals                                        | Smelting Non-ferrous Metals      |
| 34   | Metal Products                                                                     | Metals                           |
| 35   | General Purpose Machinery                                                          | Machinery                        |
| 36   | Special Purpose Machinery                                                          | Special Purpose Machinery        |
| 37   | Transport Equipment                                                                | Transport Equipment              |
| 39   | Electrical Machinery and Equipment                                                 | Electrical Machine               |
| 40   | Communication Equipment, Computers and Other Electronic Equipment                  | Communication Equipment          |
| 41   | Measuring Instruments and Machinery for Cultural Activity and Office Work          | Cultural measurement instruments |
| 42   | Artwork and Other Manufacturing                                                    | Artwork                          |
<!-- #endregion -->

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_['indu_2'] = df_ASIF_city_prov_['cic'].str.slice(stop=2)
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_.shape
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_indu2 = df_ASIF_city_prov_.merge(df_CIC_industry_name,
                       left_on = "indu_2",
                       right_on = "CIC", 
                       how = 'inner')
```

```python jupyter={"outputs_hidden": true}
df_ASIF_city_prov_indu2.shape
```

Plot the difference before joining `CIC` and after.

- raw -> Raw data
- city_merge -> raw data after merged with cities
- indu_merge -> city_merge after merged with industry


```python jupyter={"outputs_hidden": true}
pd.concat([
    df_ASIF.groupby(['year']).size().rename('raw'),
    df_ASIF_city_prov_.groupby('year')['id'].count().rename('city_merge'),
    df_ASIF_city_prov_indu2.groupby('year')['id'].count().rename('indu_merge')
], axis = 1).plot(kind='bar')
```

## Sort variables

```python jupyter={"outputs_hidden": true}
to_sort = [
    #"newID",
    "id",
    "year",
    "bdat",
    "name",
    #'namepinyin',
    "legal_person",
    #"citycode",
    #'extra_coda',
    "geocode4_corr",
    "citycn_correct",
    "cityen_correct",
    "Province_cn",
    "Province_en",
    #"prov2013",
    #"Provinces",
    "Lower_location",
    "Larger_location",
    "Coastal",
    #'town',
    #'village',
    #'street',
    #'phone',
    #'zip',
    #'product1_',
    "cic",
    "indu_2",
    "CIC",
    "Industry_Name",
    "Short",
    "type",
    "employment",
    "output",
    "revenue",
    "profit",
    "wage",
    "input",
    "va",
    #'new_product',
    "export",
    "fa_original",
    "fa_net",
    "a_dep",
    "c_dep",
    'e_state',
    'e_collective',
    'e_legal_person',
    'e_individual',
    'e_HMT',
    'e_foreign'
]
df_toclean = df_ASIF_city_prov_indu2[to_sort]
```

```python jupyter={"outputs_hidden": true}
df_toclean.shape
```

```python jupyter={"outputs_hidden": true}
df_toclean.isna().sum()
```

2001-2004 does not have value added value. Let's replace them

```python jupyter={"outputs_hidden": true}
df_toclean.groupby("year")['va'].sum()
```

```python jupyter={"outputs_hidden": true}
df_tocleanva =  df_toclean.assign(va = lambda x: np.where(
    np.logical_or(x['year'] == '2001',
                  x['year'] == '2004'),
    x['output'] - x['input'],
    x['va'])
                                 )
```

```python jupyter={"outputs_hidden": true}
df_tocleanva.isna().sum()
```

```python jupyter={"outputs_hidden": true}
df_tocleanva.groupby("year")['va'].sum()
```

<!-- #region toc-hr-collapsed=true toc-nb-collapsed=true -->
# Clean the dataset

- According to the profiling, there is issue with the data:

- `a_dep` has negative values
- `bdat` has year with one digit only
- `c_dep` has negative values
- Remove `CIC`: same value as `indu_2`
- `cic` has `nan`
- `export` has negative values
- `fa_net` has negative values
- `input` has negative values
- `ownership` has missing values

Most of the variables are highly skew

We will proceed as follow:

- clean birthdate
- Clean negative values
- Remove `nan` & `CIC
- Clean `ownership`
<!-- #endregion -->

### Clean birthdate

For each `bdat` with digit number inferior to 4, then convert to `nan`

```python jupyter={"outputs_hidden": true}
count_ = pd.Series(df_tocleanva['bdat'].str.len(), name = 'count_')
df_clean = pd.concat([df_tocleanva, count_], axis = 1)
```

```python jupyter={"outputs_hidden": true}
df_clean.groupby('count_')['count_'].count()
```

```python jupyter={"outputs_hidden": true}
df_clean = df_clean[df_clean['count_'].isin([4])]
df_clean.shape
```

```python jupyter={"outputs_hidden": true}
#df_final.loc[df_final['count_'] <4] = np.nan
```

```python jupyter={"outputs_hidden": true}
#df_final['bdat'].str.len().nunique()
```

```python jupyter={"outputs_hidden": true}
#df_final = df_final[~df_final['bdat'].isin([0])]
```

```python jupyter={"outputs_hidden": true}
#df_final['bdat'].isna().sum()
```

```python jupyter={"outputs_hidden": true}
df_clean['year'].unique()
```

### Clean negative values

Since the variables with negative values are not very compelling, we exclude them 

```python jupyter={"outputs_hidden": true}
df_clean.describe().style.format('{0:,.0f}')
```

```python jupyter={"outputs_hidden": true}
df_clean_ = df_clean.copy() 

list_zeroes = ['revenue', 'wage', 'input', 'va',
               'fa_original', 'fa_net',
               'export',
               'a_dep', 'c_dep',
               'e_state',
               'e_collective',
               'e_legal_person',
               'e_individual',
               'e_HMT',
               'e_foreign', 'output', 'employment']

for var in list_zeroes:
    print("Var {0} has {1} values below 1".format(var,
                                                   df_clean_.loc[lambda x : x[var] <= 0][var].count(
                                                   )
                                                   )
          )
    if var in ['e_state',
               'e_collective',
               'e_legal_person',
               'e_individual',
               'e_HMT',
               'e_foreign',
               'export',
               'a_dep', 
               'c_dep',
              ]:
        df_clean_ = df_clean_.loc[lambda x: x[var] >= 0]
        
    else:
        df_clean_ = df_clean_.loc[lambda x: x[var] > 0]
df_clean_.shape

```

```python jupyter={"outputs_hidden": true}
df_clean_.describe().style.format('{0:,.0f}')
```

### CIC

Just remove `CIC`


```python jupyter={"outputs_hidden": true}
df_clean_ = df_clean_[~df_clean_['cic'].isin([np.nan])]
```

```python jupyter={"outputs_hidden": true}
df_clean_['cic'].isna().sum()
```

```python jupyter={"outputs_hidden": true}
df_clean_ = df_clean_.drop(columns = ['CIC', 'count_'])
```

```python jupyter={"outputs_hidden": true}
df_clean_.shape
```

### Clean ownership

```python Collapsed="false"
#df_final = df_final[df_final['ownership'].isin(['Private',
#                                     'Collective',
#                                     'Foreign',
#                                     'HTM',
#                                     'SOE'])
#        ]
```

```python Collapsed="false"
#df_final = df_final[
#    df_final["year"].isin(
#        [
#            "1998",
#            "1999",
#            "2000",
#            "2001",
#            "2002",
#            "2003",
#            "2004",
#            "2005",
#            "2006",
#            "2007",
           #"2008",
           #"2009",
#        ]
#    )
#]
```

```python Collapsed="false"
#df_final = df_final.dropna(subset = ['bdat'])
#df_final['bdat'].unique()
```

```python Collapsed="false"
#df_final.isna().sum()
```

```python Collapsed="false"
#df_final['year'].sort_values().unique()
```

<!-- #region toc-hr-collapsed=true toc-nb-collapsed=true -->
# Firms share
Variables name:

https://docs.google.com/spreadsheets/d/1gfdmBKzZ1h93atSMFcj_6YgLxC7xX62BCxOngJwf7qE/edit#gid=1504397597

 use "type" variable, classify ownership into four types:
- 1=state, 
- 2=collective, 
- 3=private, 
- 4=foreign, 
- 5=Hong Kong, Macau and Taiwan (4 and 5 can be combined into a single "foreign" category
  
In a nutshell, for the type of firm it is:
- 110 141 143 151=1 
- 120 130 142 149=2 
- 171 172 173 174 190=3 
- 210 220 230 240=4 
- 310 320 330 340=5

```
label def	type	110	"110 SOE"	
label def	type	120	"120 collective-owned"	,add
label def	type	130	"130 equity JV"	,add
label def	type	141	"141 state coop"	,add
label def	type	142	"142 collective coop"	,add
label def	type	143	"143 state&collective coop"	,add
label def	type	149	"149 other coop"	,add
label def	type	151	"151 SO Ltd liability Co."	,add
label def	type	159	"159 other Ltd liability Co."	,add
label def	type	160	"160 Share-holding Co. Ltd"	,add
label def	type	171	"171 private funded"	,add
label def	type	172	"172 private partnership"	,add
label def	type	173	"173 private Ltd liability"	,add
label def	type	174	"174 private Share-holding Co. Ltd"	,add
label def	type	190	"190 other domestic"	,add
label def	type	210	"210 HMT equity JV"	,add
label def	type	220	"220 HMT coop"	,add
label def	type	230	"230 HMT wholly owned"	,add
label def	type	240	"240 HMT Share-holding Co. Ltd"	,add
label def	type	310	"310 foreign equity JV"	,add
label def	type	320	"320 foreign coop"	,add
label def	type	330	"330 foreign wholly owned"	,add
label def	type	340	"340 foreign Share-holding Co. Ltd"	,add
```

The key is "159" and "160", which are joint stock and stock shareholding. We identify these firms' ownership using the information of other variables about firm equity structure.

To include them in either group, firm with the largest equity share.

We can't do it in 2008/2009, no equity.

*** use "type" variable, classify ownership into four types: 
 
``` 
for any HMT collective foreign state individual legal_person: replace e_X=0 if e_X<0
egen e_total=rsum(e_*)
replace e_state = e_state + e_legal_person
for any state collective individual \ num 1/3: replace ownership=Y if (e_X>=e_state&e_X>=e_collective&e_X>=e_individual)&(ownership==159|ownership==160)
tab ownership
```
<!-- #endregion -->

```python jupyter={"outputs_hidden": true}
def recode_type(df, recode_type_digit, recode_type_type):
    """
  Recode type:
    - 110 141 143 151=1 (State)
    - 120 130 142 149=2 (Collective)
    - 171 172 173 174 190=3 (Private)
    - 210 220 230 240=4 (Foreign)
    - 310 320 330 340=5 (HTM)
    
    Exclude year 2008/2009
  """
    list_drop = [
        'e_state', 'e_collective', 'e_legal_person', 'e_individual', 'e_HMT',
        'e_foreign'
    ]

    #for name in list_convert:
    #    df[name] = df[name].apply(pd.to_numeric, errors='ignore')

    #df['year'] = df['year'].astype('int')
    #df['bdat'] = df['bdat'].apply(
    #    pd.to_numeric, errors='coerce').fillna(
    #        0, downcast='infer')
    
    df_exclude0809 = df[~df['year'].isin(['2008', '2009'])]

    #dic_q = {'type': recode_type_digit}
    df_exclude0809['type_'] = df_exclude0809['type'] 
    df_asif_recoded = df_exclude0809.replace(recode_type_digit)

    #dic_q_ = {'type': recode_type_type}

    temp = df_asif_recoded[(df_asif_recoded['type'] == '159') |
                           (df_asif_recoded['type'] == '160')]

    first_owner = temp.columns.get_loc("e_state")

    last_owner = temp.columns.get_loc("e_foreign")
    temp = temp.iloc[:, np.r_[first_owner:last_owner]].stack().reset_index()

    temp.columns = ['index', 'type', 'capital']
    # temp.tail()
    temp = temp.set_index('index')
    idx = temp.groupby(temp.index)['capital'].transform(max) == temp['capital']
    temp = temp[idx]
    temp = temp[temp['capital'] != 0]
    temp = temp.replace(recode_type_type)

    df_recode = df_asif_recoded.copy()

    # return df_recode
    # The line below is useful if we wnat to slice some ownerships
    #df_recode['type'].loc[temp.index] = temp['type']
    df_recode = df_recode[~df_recode['type'].isin(['159', '160', '0'])]
    df_recode = df_recode.drop(columns=list_drop).rename(columns = {'type_': 
                                                                    'ownership'})
    df_recode['SOE'] = np.where(
        df_recode['ownership'] == 'SOE',
        'SOE', 'PRIVATE'
    )
    #df_recode = df_recode.iloc[:,np.r_[0,6, 11:17]]

    return df_recode
```

```python jupyter={"outputs_hidden": true}
recode_type_digit = {

    'type_': {
        '110': 'SOE',
        '141': 'SOE',
        '143': 'SOE',
        '151': 'SOE',
        '120': 'Collective',
        '130': 'Collective',
        '142': 'Collective',
        '149': 'Collective',
        '171': 'Private',
        '172': 'Private',
        '173': 'Private',
        '174': 'Private',
        '190': 'Private',
        '210': 'Foreign',
        '220': 'Foreign',
        '230': 'Foreign',
        '240': 'Foreign',
        '310': 'HTM',
        '320': 'HTM',
        '330': 'HTM',
        '340': 'HTM'
    }
}

recode_type_ = {
    'type_': {
        'e_collective': 'Collective',
        'e_state': 'SOE',
        'e_individual': 'Private',
        'e_legal_person': 'Private',
        'e_HMT': 'HTM',
        'e_foreign': 'Foreign'
    }
}
```

## Ownership 2002-2007

We compare with the raw data


### Raw Data

```python jupyter={"outputs_hidden": true}
raw_data = df_ASIF.copy()
df_ASIF_raw_data = recode_type(
    raw_data,
    recode_type_digit=recode_type_digit,
    recode_type_type=recode_type_)
```

```python jupyter={"outputs_hidden": true}
#raw_data = raw_data.replace(recode_type_digit)[[
#    'year', 'id','citycode',
#    'output', 'type','e_state', 'e_collective', 'e_legal_person', 'e_individual', 'e_HMT',
#        'e_foreign']]
#raw_data['SOE'] =np.where(
#        raw_data['type'] == 'SOE',
#        'SOE', 'PRIVATE'
#    )
df_ASIF_raw_data.loc[lambda x :x['year'] == '2005'].describe().style.format('{0:,.0f}')
```

```python jupyter={"outputs_hidden": true}
(df_ASIF_raw_data
 .groupby([ 'year', 'SOE'])['output']
 .mean()
 .unstack(-1)
 .plot()
)
```

### Clean Data

```python jupyter={"outputs_hidden": true}
df_ASIF_1 =  recode_type(
    df_clean_,
    recode_type_digit=recode_type_digit,
    recode_type_type=recode_type_)
```

Plot the difference before creating `ownership` and after. The blue bars are new dataframe (ie with ownership)

```python jupyter={"outputs_hidden": true}
pd.concat([
    df_ASIF.groupby(['year']).size().rename('raw'),
    df_ASIF_city_prov_.groupby('year')['id'].count().rename('city_merge'),
    df_ASIF_city_prov_indu2.groupby('year')['id'].count().rename('indu_merge'),
    df_ASIF_1.groupby('year')['id'].count().rename('ownership')
], axis = 1).plot(kind='line')
```

```python jupyter={"outputs_hidden": true}
(df_ASIF_1
 .groupby([ 'year', 'SOE'])['SOE']
 .count()
 .unstack()
 .plot(kind='bar',stacked=True)
)
```

```python jupyter={"outputs_hidden": true}
(df_ASIF_1
 .groupby([ 'year', 'ownership'])['type']
 .count()
 .unstack()
 .plot(kind='bar',stacked=True)
)
```

```python jupyter={"outputs_hidden": true}
(df_ASIF_1
 .groupby([ 'year'])['output']
 .describe()
 .style
 .format('{0:,.0f}')
 #.unstack(-1)
)
```

```python jupyter={"outputs_hidden": true}
pd.concat([
    (df_ASIF_raw_data
    .groupby(['year'])['output']
    .mean()
    .rename('mean_raw')
    )
    ,
    (df_ASIF_1
     .groupby(['year'])['output']
     .mean()
     .rename('mean_clean')
     )
], axis=1
).plot()
```

Mean

```python jupyter={"outputs_hidden": true}
pd.concat([
    (df_ASIF_raw_data
    .groupby(['year', 'SOE'])['output']
    .mean()
    .unstack(-1)
    .rename(columns={'PRIVATE': 'PRIVATE_Raw',
                     'SOE': "SOE_Raw"})
    )
    ,
    (df_ASIF_1
     .groupby(['year', 'SOE'])['output']
     .mean()
     .unstack(-1)
     .rename(columns={'PRIVATE': 'PRIVATE_Clean',
                     'SOE': "SOE_Clean"})
     )
], axis=1
).reindex(columns = ['SOE_Raw', 
                     'SOE_Clean',
                     'PRIVATE_Raw',
                     'PRIVATE_Clean']).plot(title = 'mean')
```

Median

```python jupyter={"outputs_hidden": true}
pd.concat([
    (df_ASIF_raw_data
    .groupby(['year', 'SOE'])['output']
    .median()
    .unstack(-1)
    .rename(columns={'PRIVATE': 'PRIVATE_Raw',
                     'SOE': "SOE_Raw"})
    )
    ,
    (df_ASIF_1
     .groupby(['year', 'SOE'])['output']
     .median()
     .unstack(-1)
     .rename(columns={'PRIVATE': 'PRIVATE_Clean',
                     'SOE': "SOE_Clean"})
     )
], axis=1
).reindex(columns = ['SOE_Raw', 
                     'SOE_Clean',
                     'PRIVATE_Raw',
                     'PRIVATE_Clean']).plot(title = 'median')
```

### Sanitary check 

``` 
- 110 141 143 151=1 (State)
- 120 130 142 149=2 (Collective)
- 171 172 173 174 190=3 (Private)
- 210 220 230 240=4 (Foreign)
- 310 320 330 340=5 (HTM)
```

Any issue in the data for type 110? 

```python jupyter={"outputs_hidden": true}
temp = (raw_data
 .loc[lambda x:
      #(x['year'].isin(['2007']))
     #& 
     (x['type'].isin(['110','141','143','151']))]
 .groupby(['type','year'])['output']
 .describe()
 .unstack(0)
 #.style
 #.format('{0:,.0f}')
 )
temp[['count', 'mean']].style.format('{0:,.0f}')
```

```python jupyter={"outputs_hidden": true}
to_slice = ['count', 'mean', 'std', '25%', '50%', '75%', 'max']

for x in to_slice:
    temp[x].plot(title = x).legend(loc='center left',
                                   bbox_to_anchor=(1.25, 0.5), ncol=1)
```

```python jupyter={"outputs_hidden": true}
(df_ASIF_raw_data
 .loc[lambda x:x['year'].isin(['2007'])]
 .groupby(['SOE', 'year'])['output']
 .describe()
 .style
 .format('{0:,.0f}')
 )
```

```python jupyter={"outputs_hidden": true}
(df_ASIF_1
 .loc[lambda x:x['year'].isin(['2007'])]
 .groupby(['SOE', 'year'])['output']
 .describe()
 .style
 .format('{0:,.0f}')
 )
```

```python jupyter={"outputs_hidden": true}
df_ASIF_1.groupby('SOE')['output'].describe().style.format('{0:,.0f}')
```

```python jupyter={"outputs_hidden": true}
df_ASIF_1.groupby(['year','SOE'])['output'].mean().unstack(-1).style.format('{0:,.0f}')
```

```python jupyter={"outputs_hidden": true}
import seaborn as sns
import matplotlib.pyplot as plt
```

```python jupyter={"outputs_hidden": true}
sns.distplot(df_ASIF_1.loc[lambda x:x['SOE'].isin(['SOE'])]['output'],
            #rug=True,
             hist=False)
sns.distplot(df_ASIF_1.loc[lambda x:x['SOE'].isin(['PRIVATE'])]['output'],
            #rug=True,
             hist=False)
```

```python jupyter={"outputs_hidden": true}
df_ASIF_1.shape
```

```python jupyter={"outputs_hidden": true}
total_id_year = (df_ASIF_1
 .groupby(['id'])['id']
 .count()
 .reset_index(name = 'count')
 .groupby('count')
 .count()
 .assign(total_obs = lambda x:
        x.index.get_level_values(0) * x['id'])
)
total_id_year['id'].plot.bar(title = 'count by # of year')
```

```python jupyter={"outputs_hidden": true}
total_id_year['total_obs'].sum() == df_ASIF_1.shape[0]
```

```python jupyter={"outputs_hidden": true}
df_ASIF_1.describe().style.format('{0:,.0f}')
```

### Ownership 2008/2009

```python Collapsed="false"
#df_include0809 = df_appended[df_appended["year"].isin(["2008", "2009"])]
### need to exclude e_*

#list_remove = [
#    "e_state",
#   "e_collective",
#    "e_legal_person",
#    "e_individual",
#    "e_HMT",
#    "e_foreign",
#]

#df_include0809 = df_include0809.drop(columns = list_remove)
```

```python Collapsed="false"
#dic_q = {'type': recode_type_digit}
#df_0809_ = df_include0809.replace(dic_q)
#df_0809_ = df_0809_[~df_0809_['type'].isin(['159', '160', '0'])]
```

```python Collapsed="false"
#df_0809_['type'].unique()
```

<!-- #region Collapsed="false" -->
Append with `df_ASIF_1` 
<!-- #endregion -->

```python Collapsed="false"
#df_ASIF_1 = df_ASIF_1.append(df_0809_,
#                             sort=False)
```

# Profiling

In order to get a quick summary statistic of the data, we generate an HTML file with the profiling of the dataset we've just created. 

The profiling will be available at this URL after you commit a push to GitHub. 

**You need to rename the final dataframe `df_final` in the previous section to generate the profiling.**

```python Collapsed="false"
#### make sure the final dataframe is stored as df_final
#profile = pandas_profiling.ProfileReport(df_ASIF_1, check_recoded = False)
#name_html = "Dataset_profiling/asif_firm_china.html"
#profile.to_file(output_file=name_html)
```

# Upload to cloud

The dataset is ready to be shared with your colleagues. 



<!-- #region -->


### Move to GCS and BigQuery

We move the dataset to the following:

- **bucket**: *chinese_data*

- **Destination_blob**: *Panel_china/Asif_panel_china/Processed_*
- **name**:  *asif_firm_china.gz*
- **Dataset**: *China*

- **table**: *asif_firm_china*

### GCS

We first need to save *asif_firm_china* with `.gz` extension locally then we can move it
to GCS

<!-- #endregion -->

```python jupyter={"outputs_hidden": true}
bucket_name = 'chinese_data'
destination_blob_name = 'Panel_china/Asif_panel_china/Processed_/asif_firm_china9807Clean.gz'

gcp.delete_blob(bucket_name = bucket_name,
                destination_blob_name= destination_blob_name)
gcp.delete_table(dataset_name = 'China', name_table = 'asif_firm_china9807Clean')
```

```python jupyter={"outputs_hidden": true}

### First save locally
df_ASIF_1.to_csv(
	'asif_firm_china9807Clean.gz',
	sep=',',
	header=True,
	index=False,
	chunksize=100000,
	compression='gzip',
	encoding='utf-8')

### Then upload to GCS
bucket_name = 'chinese_data'
destination_blob_name = 'Panel_china/Asif_panel_china/Processed_'
source_file_name = 'asif_firm_china9807Clean.gz'
gcp.upload_blob(bucket_name, destination_blob_name, source_file_name)

```

```python jupyter={"outputs_hidden": true}
SQL_schema = [
    ['newID', 'STRING'],
    ['id','STRING'],
    ['year','STRING'],
    ['bdat','STRING'],
    ['name','STRING'],
    ['namepinyin','STRING'],
    ['legal_person','STRING'],
    ['geocode4_corr','STRING'],
    ['citycn_correct','STRING'],
    ['cityen_correct','STRING'],
    ['Province_cn','STRING'],
    ['Province_en','STRING'],
    ['prov2013','STRING'],
    ['Provinces','STRING'],
    ['Lower_location','STRING'],
    ['Larger_location','STRING'],
    ['Coastal','STRING'],
    ['cic','STRING'],
    ['indu_2','STRING'],
    ['Industry_Name','STRING'],
    ['Short','STRING'],
    ['ownership','STRING'],
    ['employment','FLOAT'],
    ['output','FLOAT'],
    ['revenue','FLOAT'],
    ['profit','FLOAT'],
    ['wage','FLOAT'],
    ['input','FLOAT'],
    ['export','FLOAT'],
    ['va','FLOAT'],
    ['fa_original','FLOAT'],
    ['fa_net','FLOAT'],
    ['a_dep','FLOAT'],
    ['c_dep','FLOAT']
]

gcp.move_to_bq_autodetect(
    dataset_name="China",
    name_table="asif_firm_china9807Clean",
    bucket_gcs="chinese_data/Panel_china/Asif_panel_china/Processed_/asif_firm_china9807Clean.gz",
    #sql_schema=SQL_schema,
)

```

# Remove local file

```python jupyter={"outputs_hidden": true}
import glob
import os
```

```python jupyter={"outputs_hidden": true}
list_gz = glob.glob('asif_year_*.gz')
```

```python jupyter={"outputs_hidden": true}
[os.remove(item) for item in list_gz]
```

```python jupyter={"outputs_hidden": true}
os.remove('asif_firm_china9807Clean.csv')
os.remove('asif_firm_china9807Clean.gz')
```
