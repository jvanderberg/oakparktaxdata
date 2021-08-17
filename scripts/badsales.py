import pandas as pd
import numpy as np
import common

taxyear = common.getTaxYear()


def convert(column, df):
    df[column] = df[column].astype(str)
    df[column] = df[column].str.replace("$", "").str.replace(
        "nan", "").str.replace(",", "").str.replace("\*\*", "")
    df[column][df[column] == ''] = "0"
    df[column] = df[column].astype(float)


ass1 = pd.read_csv(str(taxyear)+"/assessments.csv", low_memory=False)
ass2 = pd.read_csv(str(taxyear)+"/sales.csv", parse_dates = ['Sale Date'],
                   low_memory=False, )
ass1['PIN'] = ass1['PIN'].astype(str).apply(lambda x: x.replace("-", ""))
ass1 = ass1.set_index(ass1.PIN)
ass2['PIN'] = ass2['PIN'].astype(str)
ass2 = ass2.set_index(ass2.PIN)

combined = ass1.join(ass2, rsuffix='2', how="left")


combined = combined.drop(combined.columns[0], axis='columns')
combined = combined.drop(combined.columns[0], axis='columns')
convert('marketvalue', combined)
convert('marketvaluepreviousyear', combined)
convert('buildingassessedvalue', combined)
convert('buildingsqft', combined)
convert('combinedassessedvalue', combined)
convert('landassessedvalue', combined)
convert('landsqft', combined)

combined = combined[combined['PIN2'].notnull()]
combined = combined.sort_values(by=['PIN', 'Sale Date'])
combined = combined[combined.index.duplicated(keep = 'last')==False]
combined['ratio'] = combined['marketvaluepreviousyear'] / combined['Sale Price']
combined = combined[combined['ratio'] < 0.7]
combined = combined[['Sale Date', 'address', 'ratio', 'Sale Price', 'marketvalue', 'marketvaluepreviousyear', 'city','township','classification','Property Class','buildingsqft','Building Square Feet','landsqft','Land Square Feet','neighborhood','Neighborhood Code','taxcode','landassessedvalue','buildingassessedvalue','combinedassessedvalue','description','residencetype','use','Use','exteriorconstruction','fullbaths','Full Baths', 'halfbaths','Half Baths','basement','Basement','attic','Attic Type','Attic Finish','centralair','Central Air','fireplaces','Fireplaces', 'garage','age','Age', 'Deed No.', 'Longitude','Latitude']].copy()


combined.to_csv(str(taxyear)+'/combinedsales.csv')
