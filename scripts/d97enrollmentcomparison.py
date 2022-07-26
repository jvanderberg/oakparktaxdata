import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common

taxyear, baseyear = common.getBaseAndTaxYear()

final = pd.read_csv("oak park tax history summary.csv")
final = final[final.Year != 'All']

final = final.set_index(np.array(final.Year).astype(int))
final = final[final.index >= baseyear]
based97enrollment = final['D97 Enrollment'][baseyear]
based97 = final.D97[baseyear]
basecpi = final.CPI[baseyear]
baseawi = final.AWI[baseyear]
d97 = (final.D97 - based97) / based97
cpi = (final.CPI - basecpi) / basecpi
awi = (final.AWI - baseawi) / baseawi
d97enrollment = (final['D97 Enrollment'] -
                 based97enrollment) / based97enrollment


plt.close()
plt.figure(figsize=(7, 6), dpi=200)
plt.title("D97 Levy Compared with Prices, Wages, and Enrollment")
plt.ylabel('Percentage Increase')
line1 = plt.plot(d97 * 100, color='#dc3912', linewidth=2)
line3 = plt.plot(cpi * 100, color='#3366cc', linewidth=2)
line4 = plt.plot(awi * 100, color='#990099', linewidth=2)
line5 = plt.plot(d97enrollment * 100,  color='#109618', linewidth=2)
plt.xticks(np.arange(baseyear, taxyear+1, step=2))
plt.legend(['D97 Levy', 'Prices', 'Wages', 'Enrollment'])
plt.grid(axis='y', linewidth=0.5)

plt.savefig(str(taxyear)+'/charts/d97 enrollment wage and price comparisons.png')
