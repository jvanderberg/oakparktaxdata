import pandas as pd
import numpy as np


def convert(column, df):
    df[column] = df[column].astype(str)
    df[column] = df[column].str.replace("$", "").str.replace(
        "nan", "").str.replace(",", "").str.replace("\*\*", "")
    df[column][df[column] == ''] = "0"
    df[column] = df[column].astype(float)


ass1 = pd.read_csv("assessments.csv", low_memory=False)
ass2 = pd.read_csv("cookcountyassessments.csv",
                   low_memory=False, )
ass1 = ass1.set_index(ass1.pin)
ass2 = ass2.set_index(ass2.pin)

combined = ass1.join(ass2, rsuffix='2', how="outer")

convert('taxbill2017', combined)
convert('taxbill2016', combined)
convert('taxbill2015', combined)
convert('taxbill2014', combined)
convert('taxbill2013', combined)
convert('marketvalue', combined)
convert('marketvaluepreviousyear', combined)
convert('buildingassessedvaluepreviousyear', combined)
convert('buildingassessedvalue', combined)
convert('buildingsqft', combined)
convert('combinedassessedvaluepreviousyear', combined)
convert('combinedassessedvalue', combined)
convert('landassessedvaluepreviousyear', combined)
convert('landassessedvalue', combined)
convert('landsqft', combined)
convert('assessedvalue', combined)
convert('buildingsize', combined)
convert('estimatedvalue', combined)
convert('homeownerexemption', combined)
convert('lotsize', combined)
convert('seniorcitizenexemption', combined)
convert('seniorfreezeexemption', combined)
convert('taxafterexemptions', combined)
convert('taxbeforeexemptions', combined)

combined['lastyearbillchange'] = combined.taxbill2017 - combined.taxbill2016
combined['fiveyearbillchange'] = combined.taxbill2017 - combined.taxbill2013
combined['lastyearbillchangepct'] = 100 * combined.lastyearbillchange / \
    combined.taxbill2016
combined['fiveyearbillchangepct'] = 100 * combined.fiveyearbillchange / \
    combined.taxbill2013


combined.to_csv('combinedassessments.csv')
sf = combined[combined['use'] == 'Single Family']
sf = sf[combined['lastyearbillchangepct'] < 200]
sf = sf[combined['fiveyearbillchangepct'] < 400]
sf = sf[combined['lastyearbillchangepct'] > -100]
sf = sf[combined['fiveyearbillchangepct'] > -100]

print(sf['lastyearbillchangepct'].describe(
    percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99]))
print(sf['fiveyearbillchangepct'].describe(
    percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99]))
import matplotlib.pyplot as plt
plt.close()
plt.figure(figsize=(6, 5), dpi=200)
width = 0.75

plt.scatter(y=sf['fiveyearbillchangepct'], s=0.5, x=sf['taxbill2013'])
plt.ylabel("Percentage increase 2013-2017")
plt.xlabel('2013 Tax bill $')
plt.title('Tax increase distributions last 5 years')

plt.savefig('charts/five year increase.png')

plt.close()
plt.figure(figsize=(6, 5), dpi=200)
width = 0.75

plt.scatter(y=sf['lastyearbillchangepct'], s=0.5, x=sf['taxbill2016'])
plt.ylabel("Percentage increase 2016-2017")
plt.xlabel('2016 Tax bill $')
plt.title('Tax increase distributions past year')

plt.savefig('charts/last year increase.png')
