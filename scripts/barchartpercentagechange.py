import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import common

taxyear, baseyear = common.getBaseAndTaxYear()

pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot.Year != 'All']
pivot = pivot.set_index(np.array(pivot.Year).astype(int))
pivot.Year = pd.to_numeric(pivot.Year)
pivot = pivot[pivot.Year  >= baseyear - 1]

change = pivot.pct_change()
change = change[change.index  >= baseyear ]
pivot = pivot[pivot.Year  >= baseyear ]
plt.close()
plt.figure(figsize=(7, 6), dpi=200)
width = 0.75
d200 = change['D200'] * 100
d97 = change['D97'] * 100
town = change['Oak Park Township'] * 100
park = change['Park District'] * 100
village = change['Village of Oak Park'] * 100
year = np.array(pivot.Year).astype(int)
p1 = plt.plot(d200, color='#3366cc')
p2 = plt.plot(d97, color='#dc3912')
p3 = plt.plot(town, color='#ff9900')
p4 = plt.plot(park, color='#109618')
p5 = plt.plot(village, color='#990099')
plt.xticks(np.arange(baseyear, taxyear, step=5))
plt.ylabel("Yearly Percentage Increase")
plt.title('Yearly % Increase Oak Park Taxing Bodies')

plt.xticks(np.arange(baseyear, taxyear+1, step=5))
plt.grid(axis='y', linewidth=0.5)
plt.ylim(top=30)
plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('D200', 'D97',
                                                 'Oak Park Township', 'Park District', 'Village of Oak Park'), loc='lower left')

plt.savefig(str(taxyear)+'/charts/percentage change levy by year.png')
plt.close()

plt.figure(figsize=(7, 6), dpi=200)
all = change['All'] * 100
N=4
rolling = pd.Series(all.values).rolling(window=N).mean().iloc[N-1:].values
print(taxyear-baseyear-rolling.size)
rolling = np.pad(rolling, (taxyear-baseyear-rolling.size+1,0), 'constant', constant_values=np.NaN)
print(all)
df = pd.DataFrame({'total': all, 'rolling': rolling})
print(df)
year = np.array(pivot.Year).astype(int)
p1 = plt.plot(df['total'], color='#3366cc')
p2 = plt.plot(df['rolling'], color='#dc3912')
plt.xticks(np.arange(baseyear, taxyear, step=5))
plt.ylabel("Percentage Increase")
plt.title('Yearly % Increase Oak Park Total Levy')

plt.xticks(np.arange(baseyear, taxyear+1, step=5))
plt.grid(axis='y', linewidth=0.5)
plt.legend((p1[0], p2[0]),('Year over Year', str(N)+' Yr. Rolling avg'), loc='lower left')

plt.savefig(str(taxyear)+'/charts/percentage change total levy by year.png')
