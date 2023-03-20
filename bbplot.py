import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


d = {'age': [78, 90, 100, 101, 67, 89, 32, 45, 76, 14, 99],
     'name': ['Rob', 'John', 'Gertrude', 'Max', 'Madison', 'Ron', 'Randi', 'Carla', 'Andrea', 'Susan', 'Eric'],
     'gender': ['male', 'male', 'female', 'male', 'female', 'male', 'female', 'female', 'female', 'female', 'male'],
     'blood_glucose': [90, 190, 45, 90, 100, 123, 90, 85, 67, 98, 199],
     'wbc_count': [4500, 11000, 7000, 10001, 12000, 8000, 3000, 2100, 8700, 9000, 2000]}

df = pd.DataFrame(data=d)

msk = df['wbc_count'] >= 10000
msk_1 = df['wbc_count'] <= 4000
df['wbc_grouping'] = np.where(msk, 'elevated', (np.where(msk_1, 'low', 'normal')))

df_cut = df[['wbc_grouping', 'wbc_count']].copy(deep=True)
sns.boxplot(x='wbc_grouping', y='wbc_count', data=df_cut)

