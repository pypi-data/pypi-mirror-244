import pandas as pd


new_crosswalk = pd.read_csv('crosswalk.csv.1', comment='#', delimiter=',')
escape_crosswalk = pd.read_csv('escape_codemeta_crosswalk.csv', comment='#', delimiter=';')

# # match column Property from escape_crowalk  with column codemeta-V2 from new_crosswalk
# df1 = pd.merge(escape_crosswalk, new_crosswalk, left_on='Property', right_on='codemeta-V2')

# join new_crosswalk with escape_crosswalk by matching column Property from escape_crowalk  with column codemeta-V2 from new_crosswalk
# all columns from escape_crosswalk should be kept intact, the column Property from new_crosswalk should be renamed to codemeta-V3
# 

df2 = pd.merge(escape_crosswalk, new_crosswalk.rename(columns={'Property': 'Property' }), left_on='Property', right_on='codemeta-V2', how='outer')

