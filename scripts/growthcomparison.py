import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import common

taxyear, baseyear = common.getBaseAndTaxYear()

pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot.Year != 'All']
pivot = pivot.set_index(np.array(pivot.Year).astype(int))
pivot.Year = pd.to_numeric(pivot.Year)
pivot = pivot[pivot.Year >= baseyear]

d200 = pivot['D200']
d97 = pivot['D97']
town = pivot['Oak Park Township']
park = pivot['Park District']
village = pivot['Village of Oak Park']
total = d200 + d97 + town + park + village
basetotal = total[baseyear]
based200 = d200[baseyear]
based97 = d97[baseyear]
baselevy = total[baseyear]
basevillage = village[baseyear]
basetown = town[baseyear]
basepark = park[baseyear]

total = 100*(total - basetotal) / basetotal
d200 = 100*(d200 - based200) / based200
d97 = 100*(d97 - based97) / based97
town = 100*(town - basetown) / basetown
park = 100*(park - basepark) / basepark
village = 100*(village - basevillage) / basevillage

plt.close()
plt.figure(figsize=(7, 6), dpi=200)
plt.ylabel("Percentage increase")
plt.title('Comparison of Levy Growth Between Oak Park Taxing Bodies')

p1 = plt.plot(d200, color='#3366cc')
p2 = plt.plot(d97, color='#dc3912')
p3 = plt.plot(town, color='#ff9900')
p4 = plt.plot(park, color='#109618')
p5 = plt.plot(village, color='#990099')

plt.xticks(np.arange(baseyear, taxyear, step=5))
plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('D200', 'D97',
                                                 'Oak Park Township', 'Park District', 'Village of Oak Park'), loc='upper left')
plt.grid(axis='y', linewidth=0.5)

plt.savefig(str(taxyear)+'/charts/levy growth comparison.png')
