import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 450)
pd.set_option('display.width', 95)
pd.options.display.float_format = '{:,.3f}'.format

#read in csv
df = pd.read_csv(r'/Users/rkrulee/Desktop/hospitalizations.csv')

#filter to relevant covid years
df['year'] = df['date'].str[0:4]

#create msks/filters & filter dataframe
years = ['2020','2021','2022']
msk = df['year'].isin(years)
df_1 = df.loc[msk]
assert(df_1.year.isin(years).sum() == len(df_1))
