import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot['Year'] != 'All']

log=np.log(pivot['All'])
year = np.array(pivot.Year).astype(int)
fit = np.polyfit(year, y=log, deg=1)
logfit=pd.DataFrame(index=pd.Series(range(1999,2038)),  data=np.exp(np.array(pd.Series(range(1999,2038))) * fit[0] + fit[1]))
levy = pd.DataFrame(pivot)
levy = levy.set_index(np.array(levy.Year).astype(int))
final=pd.DataFrame(index=pd.Series(range(1999,2038)),data={"Levy":levy['All'],"Fit":logfit[0]})
final.to_csv('projections.csv')
