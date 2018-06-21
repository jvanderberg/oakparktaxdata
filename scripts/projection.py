import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot['Year'] != 'All']
baseyear = 2017
log = np.log(pivot['All'])
year = np.array(pivot.Year).astype(int)
fit = np.polyfit(year, y=log, deg=1)
logfit = pd.DataFrame(index=pd.Series(range(1999, 2038)),  data=np.exp(
    np.array(pd.Series(range(1999, 2038))) * fit[0] + fit[1]))
levy = pd.DataFrame(pivot)
levy = levy.set_index(np.array(levy.Year).astype(int))
tenkfit = pd.DataFrame(index=pd.Series(range(baseyear, 2038)),  data=np.exp(
    np.array(pd.Series(range(baseyear, 2038))) * fit[0] + fit[1]))
inflator = logfit[0] / logfit[0][baseyear]
inflator = inflator[inflator.index >= baseyear]

final = pd.DataFrame(index=pd.Series(range(1999, 2038), name='Year'), data={
                     "Levy": levy['All'], "Fit": logfit[0], "10k": 10000*inflator, "12.5k": 12500 * inflator, "15k": 15000 * inflator, "17.5k": 17500 * inflator, "20k": 20000*inflator, "25k": 25000*inflator})

final.to_csv('projections.csv')
