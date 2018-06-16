import pandas as pd
import numpy as np
raw = pd.read_csv("oak park tax history.csv")
filtered = raw[raw['Agency'].isin(['D200', 'Village of Oak Park', 'Park District', 'D97', 'Oak Park Township'])]
pivot = filtered.pivot_table(index='Year', columns='Agency', values='Levy', aggfunc=np.sum, margins=True)
cpi = pd.read_csv("cpi.csv")
cpi = cpi.set_index(cpi.Year)
pivot = pivot.join(cpi.CPI)
awi = pd.read_csv("awi.csv")
awi = awi.set_index(awi.Year)
pivot = pivot.join(awi.AWI)

pivot.to_csv('oak park tax history summary.csv')
