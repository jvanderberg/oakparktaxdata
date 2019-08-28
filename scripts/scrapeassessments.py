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

taxyear = common.getTaxYear()

pins = pd.read_csv("oppins.csv")

# Don't start processing pins until you hit 'startpin'
# startpin = '16-05-100-035-0000'
try:
    startpin
except NameError:
    startpin = None


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


processpin = False
if startpin == None:
    processpin = True

results = pd.DataFrame()

for index, pin in pins.iterrows():
    if startpin != None and pin.PIN == startpin:
        processpin = True

    if processpin == False:
        continue
    print(pin.PIN)

    url = 'https://www.cookcountyassessor.com/Property.aspx?mode=details&pin=' + \
        pin.PIN.replace("-", "")
    time.sleep(0.25)
    contents = simple_get(url)
    html = BeautifulSoup(contents, 'html.parser')

    items = [{'pin': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoPIN'},
             {'address': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoAddress'},
             {'city': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoCity'},
             {'township': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoTownship'},
             {'classification': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoClassification'},
             {'landsqft': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoSqFt'},
             {'neighborhood': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoNBHD'},
             {'taxcode': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoTaxcode'},
             {'year': 'ctl00_phArticle_ctlPropertyDetails_lblPropInfoCurYear'},
             {'landassessedvalue': 'ctl00_phArticle_ctlPropertyDetails_lblAsdValLandFirstPass'},
             {'buildingassessedvalue': 'ctl00_phArticle_ctlPropertyDetails_lblAsdValBldgFirstPass'},
             {'combinedassessedvalue': 'ctl00_phArticle_ctlPropertyDetails_lblAsdValTotalFirstPass'},
             {'landassessedvaluepreviousyear': 'ctl00_phArticle_ctlPropertyDetails_lblAsdValLandCertified'},
             {'buildingassessedvaluepreviousyear': 'ctl00_phArticle_ctlPropertyDetails_lblAsdValBldgCertified'},
             {'combinedassessedvaluepreviousyear': 'ctl00_phArticle_ctlPropertyDetails_lblAsdValTotalCertified'},
             {'marketvalue': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharMktValCurrYear'},
             {'marketvaluepreviousyear': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharMktValPrevYear'},
             {'description': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharDesc'},
             {'residencetype': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharResType'},
             {'use': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharUse'},
             {'apartments': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharApts'},
             {'exteriorconstruction': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharExtConst'},
             {'fullbaths': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharFullBaths'},
             {'halfbaths': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharHalfBaths'},
             {'basement': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharBasement'},
             {'attic': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharAttic'},
             {'centralair': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharCentAir'},
             {'fireplaces': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharFrpl'},
             {'garage': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharFrpl'},
             {'age': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharAge'},
             {'buildingsqft': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharBldgSqFt'},
             {'assessmentpass': 'ctl00_phArticle_ctlPropertyDetails_lblPropCharAsmtPass'}
             ]

    row = pd.DataFrame()
    for item in items:
        span = html.find_all(attrs={'id': list(item.values())[0]})
        try:
            row[list(item.keys())[0]] = [span[0].get_text()]

        except:
            print('Error processing '+pin.PIN +
                  ' ' + list(item.keys())[0] + ' ' + url)

    results = results.append(row)
    results.to_csv(str(taxyear)+'/assessments.csv')

    if index % 10 == 0:
        print('------- ' + str(index) + ' -------')
