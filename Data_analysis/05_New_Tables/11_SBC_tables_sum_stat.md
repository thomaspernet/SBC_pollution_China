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

<!-- #region kernel="SoS" -->
# Table 1 and 2
<!-- #endregion -->

```python kernel="Python 3"
from Fast_connectCloud import connector
from GoogleDrivePy.google_drive import connect_drive
import pandas as pd
import numpy as np

gs = connector.open_connection(online_connection = False,
                              path_credential = 
                               '/Users/thomas/Google Drive/Projects/Client_Oauth/Google_auth/'
                              )
service_gd = gs.connect_remote(engine = 'GS')
gdr = connect_drive.connect_drive(service_gd['GoogleDrive'])
service = gs.connect_remote('GCP')
from GoogleDrivePy.google_platform import connect_cloud_platform
project = 'valid-pagoda-132423'
gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service['GoogleCloudP'])   
```

<!-- #region kernel="Python 3" -->
# Load data
<!-- #endregion -->

<!-- #region kernel="Python 3" -->
## parameters
<!-- #endregion -->

```python kernel="Python 3"
aggregation_param = 'industry'
decile = 6
```

<!-- #region kernel="Python 3" -->
## Load cityname_and_code from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```python kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA
### To change the range

sheetid = '1fIziz-Xt99-Rj6NLm52-i6jScOLXgAY20KJi8k3DruA'
sheetname = 'final'

df_cityname_and_code = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_cityname_and_code.head()
```

<!-- #region kernel="Python 3" -->
## Load TCZ_list_china from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset
<!-- #endregion -->

```python kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range

sheetid = '15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q'
sheetname = 'TCZ'

df_TCZ_list_china = gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True)
df_TCZ_list_china.head()
```

<!-- #region kernel="SoS" -->
## Load yearbook9813 from Google Spreadsheet

Feel free to add description about the dataset or any usefull information.

Profiling will be available soon for this dataset

We need this table for the table 0 -> Need year 2001
<!-- #endregion -->

```python kernel="Python 3"
### Please go here https://docs.google.com/spreadsheets/d/15bMeS2cMfGfYJkjuY6wOMzcAUWZNRGpO03hZ8rpgv0Q
### To change the range


sheetid = '1NpfDQ6dz7knjZDPSjRz2QanVf7td3ujSQn7hD7Gxkow'
sheetname = 'yearbook'

yearbook9813 = (gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True).loc[lambda x: x['year'].isin(['2003','2004',
                                                       '2005', '2006',
                                                       '2007', '2008',
                                                       '2009', '2010'])]
                .drop(columns = ['代码',
                  '简称', 
                  "[Envirct06:工业二氧化硫去除量][单位:吨]",
                 '[Envirct08:工业烟尘去除量][单位:吨]',
                 '[Envirct09:工业烟尘排放量][单位:吨]']
               )
                .rename(columns = {'[Envirct07:工业二氧化硫排放量][单位:吨]':
                                   'tso2'})
                .assign(tso2 = lambda x: pd.to_numeric(x['tso2'],
                                                         errors = 'coerce'
                                                         )
                                                         )
               )
```

<!-- #region kernel="Python 3" -->
## Paper dataset
<!-- #endregion -->

```python kernel="Python 3"
query = (
          "SELECT * "
            "FROM China.SBC_pollution_China "

        )

df_final = gcp.upload_data_from_bigquery(query = query, location = 'US')
```

```python kernel="Python 3"
list_agg = df_final[aggregation_param].to_list()
```

<!-- #region kernel="Python 3" -->
## Pollution China 1998-2005
<!-- #endregion -->

```python kernel="Python 3"
query = ("""SELECT SUM( tso2) sum_so2, year, citycode as geocode4_corr
FROM China.pollution_city_cic4_china
GROUP BY year, citycode
"""
        )
df_pol = (gcp.upload_data_from_bigquery(query = query, location = 'US')
          .loc[lambda x: ~x['geocode4_corr'].isna()]
      .assign(geocode4_corr = lambda x: 
              x['geocode4_corr'].astype(int).astype('str')
             )
         )
          
```

```python kernel="Python 3"
### Zhaoruili data
sheetid = '1kSyGnkWOwoGVe1PgsQUGoWYO3DB8p9fgVh_VE6ilBt8'
sheetname = 'SO2_emission'

df_TCZ_SO2_Zhaoruili= gdr.upload_data_from_spreadsheet(sheetID = sheetid,
sheetName = sheetname,
	 to_dataframe = True).apply(lambda x: pd.to_numeric(x, errors ='ignore'))
```

<!-- #region kernel="Python 3" -->
## SOE vs Private

We proceed as follow:
- Step 1: Compute the share [output, capital, employment] by industry[city], ownership (SOE/PRIVATE): `Share_X_agg_o`
- ~Step 2: Compute dummy when share SOE above share domestic by industry[city]~
- Step 3: Compute decile by industry[city]-ownership
    - Note,  high decile in SOE means the industry[city] has relatively high share of SOE output, but not in absolule value as in step 2. A decile 9 in SOE can be a decile 2 or 3 in Domestic
<!-- #endregion -->

```python kernel="Python 3"
query_share_ = """ 
WITH sum_agg_o AS (
  SELECT 
    case WHEN ownership = '{2}' THEN '{2}' ELSE '{3}' END AS OWNERSHIP, 
    SUM(output / 10000000) as output_agg_o, 
    SUM(fa_net / 10000000) as fa_net_agg_o, 
    SUM(employment / 100000) as employment_agg_o,
    {1} as {0}
  FROM 
    China.asif_firm_china 
  WHERE 
    year >= 2002 
    AND year <= 2007 
    AND output > 0 
    AND fa_net > 0 
    AND employment > 0 
  GROUP BY 
    OWNERSHIP, 
    {0}
) 
SELECT 
  * 
FROM 
  (
    WITH sum_agg AS(
      SELECT 
        SUM(output_agg_o) as output_agg, 
        SUM(fa_net_agg_o) as fa_net_agg, 
        SUM(employment_agg_o) as employment_agg, 
        {0} AS {0}_b
      FROM 
        sum_agg_o 
      GROUP BY 
        {0}
    ) 
    SELECT 
      * 
    FROM 
      (
        WITH share_agg_o AS(
          SELECT 
            OWNERSHIP, 
            output_agg_o / output_agg AS share_output_agg_o, 
            fa_net_agg_o / fa_net_agg AS share_fa_net_agg_o, 
            employment_agg_o / employment_agg AS share_employement_agg_o, 
            {0}
          FROM 
            sum_agg_o 
            LEFT JOIN sum_agg ON sum_agg_o.{0} = sum_agg.{0}_b 
        ) 
        SELECT 
        {0},
        OWNERSHIP,  
        share_output_agg_o,
        share_fa_net_agg_o,
        share_employement_agg_o
        FROM share_agg_o
        WHERE OWNERSHIP = '{2}'
        )
        )
"""
OWNERSHIP = 'SOE'
counterpart = 'PRIVATE'

df_share_soe= query_share_.format(aggregation_param,
                                             'cic',
                                             OWNERSHIP,
                                            counterpart)
    
df_share_soe = (gcp.upload_data_from_bigquery(query = df_share_soe,
                                         location = 'US')
                    .loc[lambda x: x[aggregation_param].isin(list_agg)]
                   )
#df_share_soe.shape 
```

<!-- #region kernel="Python 3" -->

<!-- #endregion -->

<!-- #region kernel="Python 3" -->
# Table 1
<!-- #endregion -->

```python kernel="Python 3"
#### If industry, we need to use out_share_SOE, cap_share_SOE,lab_share_SOE
##### Output share already computed in the paper's table for industry but not
##### for city, in the later case, we use the data from ASIF
decile =6

if aggregation_param== 'industry':
    out = "out_share_SOE"
    cap = "cap_share_SOE"
    emp = "lab_share_SOE"
else:
    out = "share_output_agg_o"
    cap = "share_fa_net_agg_o"
    emp = "share_employement_agg_o"
    
df_final_SOE = (df_final.merge(
    df_share_soe,
    on = [aggregation_param],
    how = 'left',
    indicator = True
)
                .assign(
                       output = lambda x:
                           pd.qcut(x[out],10, labels=False),
                       capital = lambda x:
                           pd.qcut(x[cap],10, labels=False),
                       employment = lambda x:
                           pd.qcut(x[emp],10, labels=False),
                       mean_output = lambda x:np.where(
                    x[out] > x[out].drop_duplicates().mean(),
                           1,0
                       ),
                    mean_capital = lambda x:np.where(
                    x[cap] > x[cap].drop_duplicates().mean(),
                           1,0
                       ),
                    mean_employment = lambda x:np.where(
                    x[emp] > x[emp].drop_duplicates().mean(),
                           1,0
                       ),
                    soe_city = lambda x:np.where(
                    x['output'] > decile,
                           'SOE dominated',"No SOE dominated"
                       )
                    
                    )
                .drop(columns = '_merge')[['geocode4_corr',
                                           'output',
                                           'TCZ_c',
                                          'soe_city',
                                          'target_c']].drop_duplicates(
    subset = 'geocode4_corr')
                .assign(geocode4_corr = lambda x: 
                        x['geocode4_corr'].astype('str'))
                

)
df_final_SOE['soe_city'].value_counts()
```

<!-- #region kernel="Python 3" -->
### 1998-2000

- TCZ
- No TCZ
- SOE
- No SOE
- Full 
<!-- #endregion -->

```python kernel="Python 3"
dic_ = {
    '1998-2001': [],
    '2002-2005': [],
    '2006-2010': [],
    'Target':[]
}
```

```python kernel="Python 3"
t1 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['1998', '2000'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 0)
 .pct_change()
 .dropna()
)

dic_['1998-2001'].append(np.round(t1.loc['No_TCZ'].values[0][0], 2))
dic_['1998-2001'].append(np.round(t1.loc['TCZ'].values[0][0], 2))
```

```python kernel="Python 3"
t2 = (df_pol
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['sum_so2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['1998', '2001']))
     ]
  .groupby(['soe_city',"year"])['sum_so2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['1998-2001'].append(np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['1998-2001'].append(np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
t3 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['1998', '2000'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 1)
 .sum()
 .pct_change()
 .dropna()
)
dic_['1998-2001'].append(np.round(t3.loc[2000].values[0], 2))
```

<!-- #region kernel="Python 3" -->
### 2001-2005

- TCZ
- No TCZ
- SOE
- No SOE
- Full 
<!-- #endregion -->

```python kernel="Python 3"
t1 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['2001', '2005'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['2002-2005'].append(np.round(t1.loc['No_TCZ'].values[0][0], 2))
dic_['2002-2005'].append(np.round(t1.loc['TCZ'].values[0][0], 2))
```

```python kernel="Python 3"
t2 = (df_pol
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['sum_so2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['2001', '2005']))
     ]
  .groupby(['soe_city',"year"])['sum_so2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['2002-2005'].append(np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['2002-2005'].append(np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
t3 = (df_TCZ_SO2_Zhaoruili
 .loc[lambda x: (~x['tcz'].isin(['OTHER']))
     & (x['year'].isin(['2001', '2005'#, '2001', '2005'
                       ]))]
 .set_index(['tcz', 'year'])
 .groupby(level = 1)
 .sum()
 .pct_change()
 .dropna()
)
dic_['2002-2005'].append(np.round(t3.loc[2005].values[0], 2))
```

<!-- #region kernel="Python 3" -->
### 2006-2010
<!-- #endregion -->

```python kernel="Python 3"
t1 = (df_cityname_and_code
 .drop(
    columns=['citycn',
             'cityen',
             'citycn_correct',
             'cityen_correct',
             'Province_cn',
             'Province_en'])
 .merge(yearbook9813.rename(columns = {'geocode4_corr' : 'extra_coda'}))
 .drop(columns = ['extra_coda'])
 .merge(df_TCZ_list_china[['geocode4_corr', 'TCZ']], how = "left")
 .merge(df_final_SOE, on = ['geocode4_corr'],how = 'left')
 .apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
 .assign(TCZ = lambda x: x['TCZ'].fillna(0))
 .replace({'TCZ': {0: 'No_TCZ', 1:'TCZ'}})
 .loc[lambda x: 
 (x['year'].isin(['2006', '2010']))]
  .groupby(['TCZ',"year"])['tso2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)

dic_['2006-2010'].append(np.round(t1.loc['No_TCZ'].values[0], 2))
dic_['2006-2010'].append(np.round(t1.loc['TCZ'].values[0], 2))
```

```python kernel="Python 3"
#### average target
t1 = (df_cityname_and_code
 .drop(
    columns=['citycn',
             'cityen',
             'citycn_correct',
             'cityen_correct',
             'Province_cn',
             'Province_en'])
 .merge(yearbook9813.rename(columns = {'geocode4_corr' : 'extra_coda'}))
 .drop(columns = ['extra_coda'])
 .merge(df_TCZ_list_china[['geocode4_corr', 'TCZ']], how = "left")
 .merge(df_final_SOE, on = ['geocode4_corr'],how = 'left')
 .apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
 .assign(TCZ = lambda x: x['TCZ'].fillna(0))
 .replace({'TCZ': {0: 'No_TCZ', 1:'TCZ'}})
 .loc[lambda x: 
 (x['year'].isin(['2006']))]
  .groupby(['TCZ',"year"])['target_c']
.mean()
     )
dic_['Target'].append(-np.round(t1.loc['No_TCZ'].values[0], 2))
dic_['Target'].append(-np.round(t1.loc['TCZ'].values[0], 2))
```

```python kernel="Python 3"
t2 = (yearbook9813
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['tso2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['2006', '2010']))
     ]
  .groupby(['soe_city',"year"])['tso2']
 .sum()
 .groupby(level = 0)
 .pct_change()
 .dropna()
)

dic_['2006-2010'].append(np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['2006-2010'].append(np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
### target
t2 = (yearbook9813
 .merge(df_final_SOE, 
        how = 'right'
       )
 .assign(sum_so2 = lambda x: x['tso2'].fillna(0))
 .loc[lambda x: 
 (x['year'].isin(['2006']))
     ]
  .groupby(['soe_city',"year"])['target_c']
  .mean()
     )
dic_['Target'].append(-np.round(t2.loc['No SOE dominated'].values[0], 2))
dic_['Target'].append(-np.round(t2.loc['SOE dominated'].values[0], 2))
```

```python kernel="Python 3"
t3 = (df_cityname_and_code
 .drop(
    columns=['citycn',
             'cityen',
             'citycn_correct',
             'cityen_correct',
             'Province_cn',
             'Province_en'])
 .merge(yearbook9813.rename(columns = {'geocode4_corr' : 'extra_coda'}))
 .drop(columns = ['extra_coda'])
 .merge(df_TCZ_list_china[['geocode4_corr', 'TCZ']], how = "left")
 .merge(df_final_SOE, on = ['geocode4_corr'],how = 'left')
 .apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
 .assign(TCZ = lambda x: x['TCZ'].fillna(0))
 .replace({'TCZ': {0: 'No_TCZ', 1:'TCZ'}})
 .loc[lambda x: 
 (x['year'].isin(['2006', '2010']))]
  .groupby(["year"])['tso2']
 .sum()
 #.groupby(level = 0)
 .pct_change()
 .dropna()
)
dic_['2006-2010'].append(np.round(t3.loc[2010], 2))
dic_['Target'].append(-.1)
```

```python kernel="Python 3"
import re, tex2pix, os
from PyPDF2 import PdfFileMerger
from wand.image import Image as WImage
```

```python kernel="Python 3"
for i in range(1, 19):
    try:
        os.remove("table_{}.pdf".format(i))
        os.remove("table_{}.tex".format(i))
        os.remove("table_{}.txt".format(i))
    except:
        pass

title = "SO2 reduction during the subsequent FYPs"
pd.DataFrame(dic_, index= ['No TCZ','TCZ',
                           'No Dominated SOE',
                           ' Dominated SOE',
                           'Full Sample']).to_latex('table_1.tex',
                                                    caption = title,
                                                    index=True,
                                                    label = "table_1",
                                                   float_format="{:,.2%}".format)
```

```python kernel="Python 3"
jupyter_preview = True
table_nte = """
Sources: Author's own computation \\
      The list of TCZ is provided by the State Council, 1998.
      "Official Reply to the State Council Concerning Acid Rain Control Areas
      and Sulfur Dioxide Pollution Control Areas".
      The information about the SO2 level are collected using various edition
      of the China Environment Statistics Yearbook.
      We compute the reduction of SO2 emission using the same methodology
      as Chen and al.(2018).
"""

with open('table_1.tex', 'r') as f:
    lines = f.readlines()
len_line = len(lines)    
for x, line in enumerate(lines):
    if x ==0:
        if jupyter_preview:
            header= "\documentclass[preview]{standalone} \n\\usepackage[utf8]{inputenc}\n" \
            "\\usepackage{booktabs,caption,threeparttable, siunitx, adjustbox}\n\n" \
            "\\begin{document}\n"
        else:
            header= "\documentclass[12pt]{article} \n\\usepackage[utf8]{inputenc}\n" \
            "\\usepackage{booktabs,caption,threeparttable, siunitx, adjustbox}\n\n" \
            "\\begin{document}"
    

        lines[x] =   header + lines[x].strip()
    if x == len_line- 1:
        footer = "\n\n\\end{document}"
        lines[x]  =  lines[x].strip() + footer
        
    label = bool(re.search(r"label",
                              line))
    tabluar = bool(re.search(r"end{tabular}",
                              line))
    #print(label)
    if label:
        lines[x] = lines[x].strip() + '\n\\begin{adjustbox}{width=\\textwidth, totalheight=\\textheight-2\\baselineskip,keepaspectratio}\n'

    if tabluar:
        lines[x] = lines[x].strip() + '\n\\end{adjustbox}\n'
        
    
        
with open('table_1.tex', "w") as f:
        for line in lines:
            f.write(line)
            
#### Replace
with open('table_1.tex', 'r') as file:
    lines = file.read()
    lines = lines.replace('nan\%', ' ')

with open('table_1.tex', 'w') as file:
        file.write(lines)
            
### add table note
if table_nte != None:
    with open('table_1.tex', 'r') as f:
        lines = f.readlines()


    for x, line in enumerate(lines):
        adjusted = bool(re.search(r"end{adjustbox}",
                              line))

        if adjusted:
            lines[x] = lines[x].strip() + "\n\\begin{0} \n \\small \n \\item \\\\ \n{1} \n\\end{2}\n".format(
            "{tablenotes}",
            table_nte,
            "{tablenotes}")
    with open('table_1.tex', "w") as f:
            for line in lines:
                f.write(line)
```

```python kernel="Python 3"
table_number = 1
resolution = 150

f = open('table_{}.tex'.format(table_number))
r = tex2pix.Renderer(f, runbibtex=False)
r.mkpdf('table_{}.pdf'.format(table_number))
r.mkpdf('table_{}.pdf'.format(table_number))
img = WImage(filename='table_{}.pdf'.format(table_number),
resolution = resolution)
display(img)
```

<!-- #region kernel="Python 3" -->
# Create report
<!-- #endregion -->

```python kernel="Python 3"
import os, time, shutil
from pathlib import Path

filename = '10_SBC_final'
source = filename + '.ipynb'
source_to_move = filename +'.html'
path = os.getcwd()
parent_path = str(Path(path).parent)
path_report = "{}/Reports".format(parent_path)
dest = os.path.join(path_report, filename)+'_{}_{}_.html'.format(
    aggregation_param,
    threshold_full)

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