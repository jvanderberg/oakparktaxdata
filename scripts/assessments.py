import pandas as pd
import numpy as np
import common

taxyear = common.getTaxYear()


def convert(column, df,newname=None):
    if newname is None:
        newname = column
    if df[column].dtype != 'float':
        df[newname] = df[column].astype(str)
        df[newname] = df[column].str.replace("$", "").str.replace(
            "nan", "").str.replace("N/A","").str.replace(",", "").str.replace("\\*\\*", "")
        df.loc[df[column] == '', column] = "0"
        df[newname] = df[column].astype(float)
    else:
        df[newname] = df[column]



ass1 = pd.read_csv(str(taxyear)+"/assessmentsnew.csv", low_memory=False)
ass1['pin'] = ass1['Parcel #']

ass2 = pd.read_csv(str(taxyear)+"/cookcountyassessments.csv",
                   low_memory=False, )
ass1 = ass1.set_index(ass1.pin)
ass2 = ass2.set_index(ass2.pin)

combined = ass1.join(ass2, rsuffix='2', how="outer")

convert('taxbill'+str(taxyear), combined)
convert('taxbill'+str(taxyear-1), combined)
convert('taxbill'+str(taxyear-2), combined)
convert('taxbill'+str(taxyear-3), combined)
convert('taxbill'+str(taxyear-4), combined)


combined['lastyearbillchange'] = combined['taxbill' +
                                          str(taxyear)] - combined['taxbill'+str(taxyear-1)]
combined['fiveyearbillchange'] = combined['taxbill' +
                                          str(taxyear)] - combined['taxbill'+str(taxyear-4)]
combined['lastyearbillchangepct'] = 100 * combined.lastyearbillchange / \
    combined['taxbill'+str(taxyear-1)]
combined['fiveyearbillchangepct'] = 100 * combined.fiveyearbillchange / \
    combined['taxbill'+str(taxyear-4)]


combined.to_csv(str(taxyear)+'/combinedassessments.csv')
