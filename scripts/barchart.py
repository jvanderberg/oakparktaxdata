import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot['Year'] != 'All']
plt.close()
plt.figure(figsize=(10,6), dpi=200)
width = 0.75
year = np.array(pivot.Year).astype(int)
p1 = plt.bar(year,pivot['D200']/1000000, width, color='#3366cc')
p2 = plt.bar(year,pivot['D97']/1000000, width, color='#dc3912', bottom=pivot['D200']/1000000)
p3 = plt.bar(year,pivot['Oak Park Township']/1000000, width, color='#ff9900', bottom=pivot['D200']/1000000+pivot['D97']/1000000)
p4 = plt.bar(year,pivot['Park District']/1000000, width, color='#109618', bottom=pivot['Oak Park Township']/1000000+pivot['D200']/1000000+pivot['D97']/1000000)
p5 = plt.bar(year,pivot['Village of Oak Park']/1000000, width, color='#990099', bottom=pivot['Park District']/1000000+pivot['Oak Park Township']/1000000+pivot['D200']/1000000+pivot['D97']/1000000)

plt.ylabel("Tax Levy $ (Millions)")
plt.title('Total Oak Park Tax Levy by Year')
plt.xticks([1999, 2005, 2010, 2016])
plt.grid(axis='y', linewidth=0.5)
plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('D200', 'D97', 'Oak Park Township', 'Park District', 'Village of Oak Park'))

plt.savefig('charts/total levy by year.png')