import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common

taxyear, baseyear = common.getBaseAndTaxYear()

final = pd.read_csv("oak park tax history summary.csv")
final = final[final.Year != 'All']
final = final.set_index(np.array(final.Year).astype(int))
baselevy = final.All[baseyear]
basecpi = final.CPI[baseyear]
baseawi = final.AWI[baseyear]
levy = (final.All - baselevy) / baselevy
cpi = (final.CPI - basecpi) / basecpi
awi = (final.AWI - baseawi) / baseawi

cpiadjusted = final.All * basecpi / final.CPI
awiadjusted = final.All * baseawi / final.AWI

plt.close()
plt.figure(figsize=(7, 6), dpi=200)
plt.ylabel("Percentage increase")
plt.title('Comparison of Levy to Wage and Price Increases')
line1 = plt.plot(levy * 100, color='#dc3912', linewidth=2)
line2 = plt.plot(cpi * 100, color='#3366cc', linewidth=2)
line2 = plt.plot(awi * 100, color='#990099', linewidth=2)
plt.xticks([1999, 2005, 2010, 2016])
plt.legend(['Levy', 'Prices', 'Wages'])
plt.grid(axis='y', linewidth=0.5)

plt.savefig(str(taxyear)+'/charts/wage and price comparisons.png')

plt.close()
plt.figure(figsize=(7, 6), dpi=200)
plt.ylabel("Percentage increase")
plt.title('Inflation Adjusted Levy')
line1 = plt.plot(100 * (cpiadjusted - baselevy) /
                 baselevy, color='#dc3912', linewidth=2)
line2 = plt.plot(100 * (awiadjusted - baselevy) /
                 baselevy, color='#3366cc', linewidth=2)
plt.xticks([1999, 2005, 2010, 2016])
plt.legend(['Price Adjusted', 'Wage Adjusted'])
plt.grid(axis='y', linewidth=0.5)

plt.savefig(str(taxyear)+'/charts/wage and price adjusted.png')
