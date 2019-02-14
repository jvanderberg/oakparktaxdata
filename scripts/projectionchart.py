import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common

taxyear = common.getTaxYear()
final = pd.read_csv(str(taxyear)+"/projections.csv")
final = final.set_index(final.Year)

plt.close()
plt.figure(figsize=(5, 4), dpi=200)
plt.ylabel("Tax Levy $ (Millions)")
plt.title('Projected Future Tax Levy')
line1 = plt.plot(final['Levy'] / 1000000, color='blue')
line2 = plt.plot(final['Levy Fit'] / 1000000, color='red')
plt.plot(final['CPI Projection'] / 1000000, color='green')
plt.plot(final['AWI Projection'] / 1000000, color='orange')
plt.legend(['Actual', 'Projection', 'CPI (Price) Limited Growth',
            'AWI (Wage) Limited Growth'])
plt.grid(axis='y', linewidth=0.5)
plt.xticks([1999, 2008, 2018, 2028, 2038])
plt.savefig(str(taxyear)+'/charts/projected future levy.png')

final = final[final.Year < 2029]
plt.close()
plt.figure(figsize=(5, 4), dpi=200)
plt.ylabel("Tax Levy $ (Millions)")
plt.title('Projected Future Tax Levy')
line1 = plt.plot(final['Levy'] / 1000000, color='blue')
line2 = plt.plot(final['Levy Fit'] / 1000000, color='red')
plt.plot(final['CPI Projection'] / 1000000, color='green')
plt.plot(final['AWI Projection'] / 1000000, color='orange')
plt.legend(['Actual', 'Projection', 'CPI (Price) Limited Growth',
            'AWI (Wage) Limited Growth'])
plt.grid(axis='y', linewidth=0.5)
plt.xticks([1999, 2008, 2018, 2028])
plt.savefig(str(taxyear)+'/charts/projected ten year levy.png')
