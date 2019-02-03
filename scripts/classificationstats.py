
import pandas as pd
import numpy as np
ass1 = pd.read_csv("combinedassessments.csv", low_memory=False)
ass1 = ass1[ass1.buildingsqft > 0]
ass1 = ass1.set_index(ass1.pin)
ass1['valuationratio'] = ass1.buildingassessedvalue / ass1.buildingsqft
agg = {'valuationratio': [
    'mean', 'median', 'min', 'max'], 'description': 'first', 'buildingassessedvalue': ['count', 'mean', 'median', 'min', 'max'], 'buildingsqft': [
    'mean', 'median', 'min', 'max'],

}
grouped = grouped[grouped['buildingassessedvalue']['count'] > 100]
grouped.to_csv('classstats.csv')
