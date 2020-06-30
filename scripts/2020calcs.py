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
ass2 = pd.read_csv(str(taxyear)+"/characteristics.csv", parse_dates = ['most_recent_sale_date'],
                   low_memory=False, )
ass1['pin'] = ass1['pin'].astype(str).apply(lambda x: x.replace("-", ""))
ass1 = ass1.set_index(ass1.pin)
ass2['pin'] = ass2['pin'].astype(str)
ass2 = ass2.set_index(ass2.pin)

combined = ass1.join(ass2, rsuffix='2', how="outer")


#combined = combined.drop(combined.columns[0], axis='columns')
#combined = combined.drop(combined.columns[0], axis='columns')
convert('marketvalue', combined)
convert('marketvaluepreviousyear', combined)
convert('buildingassessedvalue', combined)
convert('buildingsqft', combined)
convert('combinedassessedvalue', combined)
convert('landassessedvalue', combined)
convert('landsqft', combined)


# combined = combined[combined.index.duplicated(keep = 'last')==False]
#combined['ratio'] = combined['marketvaluepreviousyear'] / combined['Sale Price']
combined['multiplier'] = combined['combinedassessedvalue'] / combined['marketvalue'] 
combined['eavpreviousyear'] = combined['multiplier'] * combined['marketvaluepreviousyear'] * 2.9109 
combined['combinedassessedvalueprevyear'] = combined['multiplier'] * combined['marketvaluepreviousyear']

combined['homeownerexemption'] = 0
combined.loc[combined['use'] =='Single Family','homeownerexemption'] = 1

combined['estimatedtaxpreviousyear'] = .12686 *( combined['eavpreviousyear']- combined['homeownerexemption'] * 10000)
combined['estimatednewtax'] = .0965 *( combined['combinedassessedvalue'] * 2.9109 - combined['homeownerexemption'] * 10000)
combined['neighborhood']
combined['url'] = 'https://www.cookcountyassessor.com/pin/'+combined['pin']
combined = combined.drop(combined.columns[0], axis='columns')
combined['assessmentpersqft'] = combined['buildingassessedvalue'] / combined['buildingsqft']
combined['mapurl'] = 'https://maps.google.com/?t=k&z=20&ll='+combined['centroid_y'].astype(str)+','+combined['centroid_x'].astype(str)+'&q='+combined['centroid_y'].astype(str)+','+combined['centroid_x'].astype(str)
#
#  combined = combined[combined['ratio'] < 0.7]
# combined = combined[['Sale Date', 'address', 'ratio', 'Sale Price', 'marketvalue', 'marketvaluepreviousyear', 'city','township','classification','Property Class','buildingsqft','Building Square Feet','landsqft','Land Square Feet','neighborhood','Neighborhood Code','taxcode','landassessedvalue','buildingassessedvalue','combinedassessedvalue','description','residencetype','use','Use','exteriorconstruction','fullbaths','Full Baths', 'halfbaths','Half Baths','basement','Basement','attic','Attic Type','Attic Finish','centralair','Central Air','fireplaces','Fireplaces', 'garage','age','Age', 'Deed No.', 'Longitude','Latitude']].copy()
summary = combined.groupby(['classification']).sum()

simple = combined[[ 'address', 'url', 'classification', 'description', 'neighborhood','exteriorconstruction', 'assessmentpersqft','buildingassessedvalue','buildingsqft',
 'fullbaths' ,'halfbaths', 'basement','attic','centralair','fireplaces','garage','age', 'mapurl','centroid_x','centroid_y','most_recent_sale_date','most_recent_sale_price','marketvalue', 'marketvaluepreviousyear', 'combinedassessedvalue', 'combinedassessedvalueprevyear', 'estimatednewtax', 'estimatedtaxpreviousyear' ] ]
   
combined.to_csv(str(taxyear)+'/combined.csv')
simple.to_csv(str(taxyear)+'/simple.csv')
summary.to_csv(str(taxyear)+'/taxsummary.csv')

