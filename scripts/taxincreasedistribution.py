import pandas as pd
import numpy as np
import common


def convert(column, df):
    df[column] = df[column].astype(str)
    df[column] = df[column].str.replace("$", "").str.replace(
        "nan", "").str.replace(",", "").str.replace("\*\*", "")
    df[column][df[column] == ''] = "0"
    df[column] = df[column].astype(float)


taxyear = common.getTaxYear()
combined = pd.read_csv(str(taxyear)+"/combinedassessments.csv",  thousands=',')
fiveyearsago = taxyear - 4
lastyear = taxyear - 1
sf = combined[combined['use'] == 'Single Family']
sf = sf[combined['lastyearbillchangepct'] < 200]
sf = sf[combined['fiveyearbillchangepct'] < 400]
sf = sf[combined['lastyearbillchangepct'] > -100]
sf = sf[combined['fiveyearbillchangepct'] > -100]

print(sf['lastyearbillchangepct'].describe(
    percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99]))
print(sf['fiveyearbillchangepct'].describe(
    percentiles=[.01, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99]))
print(sf.median())
import matplotlib.pyplot as plt
plt.close()
plt.figure(figsize=(6, 5), dpi=200)
width = 0.75

plt.scatter(y=sf['fiveyearbillchangepct'], s=0.5,
            x=sf['taxbill'+str(fiveyearsago)])
plt.ylabel("Percentage increase "+str(fiveyearsago)+"-"+str(taxyear))
plt.xlabel(str(fiveyearsago)+' Tax bill $')
plt.title('Tax increase distributions last 5 years')

plt.savefig(str(taxyear) + '/charts/five year increase.png')

plt.close()
plt.figure(figsize=(6, 5), dpi=200)
width = 0.75

plt.scatter(y=sf['lastyearbillchangepct'], s=0.5, x=sf['taxbill2016'])
plt.ylabel('Percentage increase '+str(lastyear)+'-'+str(taxyear))
plt.xlabel(str(lastyear)+' Tax bill $')
plt.title('Tax increase distributions past year')

plt.savefig(str(taxyear) + '/charts/last year increase.png')
