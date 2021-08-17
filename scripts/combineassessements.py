from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import random
import common
import re

taxyear = common.getTaxYear()

# Don't start processing pins until you hit 'startpin'

results = pd.DataFrame()

for x in range(1, 3):
    print(str(taxyear)+'/assessments'+str(x)+'.csv')
    results_new = pd.read_csv(str(taxyear)+'/assessments'+str(x)+'.csv')
    results_new['pin'] = results_new['pin'].astype(str).apply(lambda x: x.replace("-", ""))
    results = results.append(results_new)

results = results.set_index('pin')
results = results[results.index.duplicated(keep = 'last')==False]
results.to_csv(str(taxyear)+'/assessments_new.csv')
