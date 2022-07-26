import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import common

taxyear = common.getTaxYear()

pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot['Year'] != 'All']
plt.close()
plt.figure(figsize=(7, 6), dpi=200)
width = 0.75
d200 = pivot['D200']
d97 = pivot['D97']
town = pivot['Oak Park Township']
park = pivot['Park District']
village = pivot['Village of Oak Park']
total = d200 + d97 + town + park + village
d200 = 100*pivot['D200'] / total
d97 = 100*pivot['D97'] / total
town = 100*pivot['Oak Park Township'] / total
park = 100*pivot['Park District'] / total
village = 100*pivot['Village of Oak Park'] / total
year = np.array(pivot.Year).astype(int)
p1 = plt.bar(year, d200, width, color='#3366cc')
p2 = plt.bar(year, d97, width, color='#dc3912', bottom=d200)
p3 = plt.bar(year, town, width, color='#ff9900', bottom=d200 + d97)
p4 = plt.bar(year, park, width, color='#109618', bottom=town + d200 + d97)
p5 = plt.bar(year, village, width, color='#990099',
             bottom=park + town + d200 + d97)

plt.ylabel("Tax Levy %")
plt.xticks(np.arange(2000, taxyear+1, step=5))
plt.grid(axis='y', linewidth=0.5)
plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('D200', 'D97',
                                                 'Oak Park Township', 'Park District', 'Village of Oak Park'), loc='lower left')

plt.savefig(str(taxyear)+'/charts/percentage levy by year.png')
