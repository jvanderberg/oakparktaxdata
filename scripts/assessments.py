import pandas as pd
import numpy as np
import common

taxyear = common.getTaxYear()


def convert(column, df):
    df[column] = df[column].astype(str)
    df[column] = df[column].str.replace("$", "").str.replace(
        "nan", "").str.replace("N/A","").str.replace(",", "").str.replace("\*\*", "")
    df[column][df[column] == ''] = "0"
    df[column] = df[column].astype(float)


ass1 = pd.read_csv(str(taxyear)+"/assessments.csv", low_memory=False)
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

combined['lastyearbillchange'] = combined['taxbill' +
                                          str(taxyear)] - combined['taxbill'+str(taxyear-1)]
combined['fiveyearbillchange'] = combined['taxbill' +
                                          str(taxyear)] - combined['taxbill'+str(taxyear-4)]
combined['lastyearbillchangepct'] = 100 * combined.lastyearbillchange / \
    combined['taxbill'+str(taxyear-1)]
combined['fiveyearbillchangepct'] = 100 * combined.fiveyearbillchange / \
    combined['taxbill'+str(taxyear-4)]


combined.to_csv(str(taxyear)+'/combinedassessments.csv')
