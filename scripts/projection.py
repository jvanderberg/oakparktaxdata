import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common
baseyear = common.getTaxYear()


pivot = pd.read_csv("oak park tax history summary.csv")
pivot = pivot[pivot['Year'] != 'All']
pivot.Year = pd.to_numeric(pivot.Year)
pivot = pivot[pivot.Year <= baseyear]
loglevy = np.log(pivot['All'])
logcpi = np.log(pivot['CPI'])
logawi = np.log(pivot['AWI'])
year = np.array(pivot.Year).astype(int)
loglevyfit = np.polyfit(year, y=loglevy, deg=1)
print(loglevyfit)
logcpifit = np.polyfit(year, y=logcpi, deg=1)
logawifit = np.polyfit(year, y=logawi, deg=1)
levyfit = pd.DataFrame(index=pd.Series(range(1999, baseyear+25)),  data=np.exp(
    np.array(pd.Series(range(1999, baseyear+25))) * loglevyfit[0] + loglevyfit[1]))

cpilevyfit = pd.DataFrame(index=pd.Series(range(1999, baseyear+25)),  data=np.exp(
    np.array(pd.Series(range(1999, baseyear+25))) * logcpifit[0] + loglevyfit[1]))

cpifit = pd.DataFrame(index=pd.Series(range(1999, baseyear+25)),  data=np.exp(
    np.array(pd.Series(range(1999, baseyear+25))) * logcpifit[0] + logcpifit[1]))
awifit = pd.DataFrame(index=pd.Series(range(1999, baseyear+25)),  data=np.exp(
    np.array(pd.Series(range(1999, baseyear+25))) * logawifit[0] + logawifit[1]))
levy = pd.DataFrame(pivot)
levy = levy.set_index(np.array(levy.Year).astype(int))
inflator = levyfit[0] / levyfit[0][baseyear]
inflator = inflator[inflator.index >= baseyear]
cpiinflator = cpifit[0] / cpifit[0][baseyear]
cpiinflator = cpiinflator[cpiinflator.index >= baseyear]
awiinflator = awifit[0] / awifit[0][baseyear]
awiinflator = awiinflator[awiinflator.index >= baseyear]
levyrate = np.exp(loglevyfit[0])-1
cpirate = np.exp(logcpifit[0])-1
awirate = np.exp(logawifit[0])-1
levydouble = np.log(2) / np.log(1 + levyrate)
cpidouble = np.log(2) / np.log(1 + cpirate)
awidouble = np.log(2) / np.log(1 + awirate)

# Dump the best fit rates to a file based on 1999-2017 observations
rates = pd.DataFrame(index=pd.Series(("Levy", "CPI (Prices)", "AWI (Wages)"), name='Type'), data={"Rate": (round(
    100*levyrate, 4), round(100*cpirate, 4), round(100*awirate, 4)), "Doubling Time": (round(levydouble), round(cpidouble), round(awidouble))})
rates.to_csv(str(baseyear)+"/bestfitrates.csv")

# create the detailed yearly projections table
final = pd.DataFrame(index=pd.Series(range(1999, baseyear+25), name='Year'), data={
                     "Levy": levy['All'], "AWI": levy["AWI"], "AWI Fit": awifit[0], "CPI": levy["CPI"], "CPI Fit": cpifit[0], "Levy Fit": levyfit[0], "CPI Projection": cpiinflator * levyfit[0][baseyear], "AWI Projection": awiinflator * levyfit[0][baseyear], "10k": 10000*inflator, "12.5k": 12500 * inflator, "15k": 15000 * inflator, "17.5k": 17500 * inflator, "20k": 20000*inflator, "25k": 25000*inflator,
                     "CPI 10k": 10000*cpiinflator, "CPI 12.5k": 12500 * cpiinflator, "CPI 15k": 15000 * cpiinflator, "CPI 17.5k": 17500 * cpiinflator, "CPI 20k": 20000*cpiinflator, "CPI 25k": 25000*cpiinflator,
                     "AWI 10k": 10000*awiinflator, "AWI 12.5k": 12500 * awiinflator, "AWI 15k": 15000 * awiinflator, "AWI 17.5k": 17500 * awiinflator, "AWI 20k": 20000*awiinflator, "AWI 25k": 25000*awiinflator})

final.to_csv(str(baseyear)+'/projections.csv')

# Create a summary table for every 10 years
years = (baseyear, baseyear+10, baseyear+20)
summary = pd.DataFrame(index=pd.Series(years, name='Year'), data={"Levy": levyfit[0], "CPI Levy": cpiinflator * levyfit[0][baseyear], "AWI Levy": awiinflator * levyfit[0][baseyear],
                                                                  "12.5k": 12500 * inflator, "CPI 12.5k": 12500 * cpiinflator, "AWI 12.5k": 12500 * awiinflator})

summary = pd.DataFrame(index=pd.Series(years, name='Year'), data={"Levy": summary["Levy"], "CPI Levy": summary["CPI Levy"], "AWI Levy": summary["AWI Levy"], "12.5k": summary["12.5k"], "CPI 12.5k": summary["CPI 12.5k"], "AWI 12.5k": summary["AWI 12.5k"],
                                                                  "Levy %": 100*(summary["Levy"] - summary["Levy"][years[0]]) / summary["Levy"][years[0]],
                                                                  "CPI %": 100*(summary["CPI Levy"] - summary["CPI Levy"][years[0]]) / summary["CPI Levy"][years[0]],
                                                                  "AWI %": 100*(summary["AWI Levy"] - summary["AWI Levy"][years[0]]) / summary["AWI Levy"][years[0]],
                                                                  })
summary.to_csv(str(baseyear)+'/projectionssummary.csv')
