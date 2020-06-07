import csv
import numpy as np
import pandas
import matplotlib.pyplot as plt

df = pandas.read_csv('dataset/pol_2020-6-6_19-19.csv', index_col='thread_num')

#countries = np.squeeze(df[['country']].to_numpy())
fig, ax = plt.subplots()
df['country'].value_counts().plot(ax=ax, kind='bar')
plt.xticks(size=10)
plt.show()