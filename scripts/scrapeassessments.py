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

pins = pd.read_csv("newpins.csv")
pins['PIN'] = pins['PIN'].astype(str)
# Don't start processing pins until you hit 'startpin'
startpin = '16-08-121-047-0000'
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

items = [
    {'classification': 'Property Classification'},
    {'landsqft': 'Square Footage (Land)'},
    {'neighborhood': 'Neighborhood'},
    {'taxcode': 'Taxcode'},
    {'landassessedvalue': 'Land Assessed Value'},
    {'buildingassessedvalue': 'Building Assessed Value'},
    {'combinedassessedvalue': 'Total Assessed Value'},
    {'description': 'Description'},
    {'residencetype': 'Residence Type'},
    {'use': 'Use'},
    {'exteriorconstruction': 'Exterior Construction'},
    {'fullbaths': 'Full Baths'},
    {'halfbaths': 'Half Baths'},
    {'basement': 'Basement'},
    {'attic': 'Attic'},
    {'centralair': 'Central Air'},
    {'fireplaces': 'Number of Fireplaces'},
    {'garage': 'Garage Size/Type'},
    {'age': 'Age'},
    {'buildingsqft': 'Building Square Footage'},
    {'assessmentpass': 'Assessment Pass'}
]


for index, pin in pins.iterrows():
    if startpin != None and pin.PIN == startpin:
        processpin = True

    if processpin == False:
        continue
    print(pin.PIN)

    url = 'https://www.cookcountyassessor.com/pin/' + \
        pin.PIN.replace("-", "")
    time.sleep(0.25)
    contents = simple_get(url)
    print(url)

    html = BeautifulSoup(contents, 'html.parser')

    items = [{'pin': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div.col-md-4.col-md-offset-4 > div > div:nth-child(1) > span.detail-row--detail'},
             {'address': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div.col-md-4.col-md-offset-4 > div > div:nth-child(2) > span.detail-row--detail'},
             {'city': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div.col-md-4.col-md-offset-4 > div > div:nth-child(3) > span.detail-row--detail'},
             {'township': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div.col-md-4.col-md-offset-4 > div > div:nth-child(4) > span.detail-row--detail'},
             {'classification': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > span.detail-row--detail.large'},
             {'landsqft': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > span.detail-row--detail.large'},
             {'neighborhood': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(3) > span.detail-row--detail.large'},
             {'taxcode': 'body > div.dialog-off-canvas-main-canvas > div.main-container.container.js-quickedit-main-content > div > section > div.region.region-content > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(4) > span.detail-row--detail.large'},     
             {'landassessedvalue': '#collapseOne > div > div > div:nth-child(4) > div.col-xs-4'},
             {'buildingassessedvalue': '#collapseOne > div > div > div:nth-child(5) > div.col-xs-4'},
             {'combinedassessedvalue': '#collapseOne > div > div > div:nth-child(3) > div.col-xs-4'},
             {'landassessedvaluepreviousyear': '#collapseOne > div > div > div:nth-child(4) > div.col-xs-5'},
             {'buildingassessedvaluepreviousyear': '#collapseOne > div > div > div:nth-child(5) > div.col-xs-5'},
             {'combinedassessedvaluepreviousyear': '#collapseOne > div > div > div:nth-child(3) > div.col-xs-5'},
             {'marketvalue': '#collapseOne > div > div > div:nth-child(2) > div.col-xs-4'},
             {'marketvaluepreviousyear': '#collapseOne > div > div > div:nth-child(2) > div.col-xs-5'},
             {'description': '#collapseTwo > div > div:nth-child(1) > span.detail-row--detail'},
             {'residencetype': '#collapseTwo > div > div:nth-child(2) > span.detail-row--detail'},
             {'use': '#collapseTwo > div > div:nth-child(3) > span.detail-row--detail'},
             {'exteriorconstruction': '#collapseTwo > div > div:nth-child(4) > span.detail-row--detail'},
             {'fullbaths': '#collapseTwo > div > div:nth-child(5) > span.detail-row--detail'},
             {'halfbaths': '#collapseTwo > div > div:nth-child(6) > span.detail-row--detail'},
             {'basement': '#collapseTwo > div > div:nth-child(7) > span.detail-row--detail'},
             {'attic': '#collapseTwo > div > div:nth-child(8) > span.detail-row--detail'},
             {'centralair': '#collapseTwo > div > div:nth-child(9) > span.detail-row--detail'},
             {'fireplaces': '#collapseTwo > div > div:nth-child(10) > span.detail-row--detail'},
             {'garage': '#collapseTwo > div > div:nth-child(11) > span.detail-row--detail'},
             {'age': '#collapseTwo > div > div:nth-child(12) > span.detail-row--detail'},
             {'buildingsqft': '#collapseTwo > div > div:nth-child(13) > span.detail-row--detail'},
             {'assessmentpass': '#collapseTwo > div > div:nth-child(14) > span.detail-row--detail'},
             {'exemption1year': '#collapseFour > div > div > div > div:nth-child(2) > div.col-xs-3.pt-header'},
             {'exemption1owner': '#collapseFour > div > div > div > div:nth-child(2) > div:nth-child(2)'},
             {'exemption1senior': '#collapseFour > div > div > div > div:nth-child(2) > div:nth-child(3)'},
             {'exemption1seniorfreeze': '#collapseFour > div > div > div > div:nth-child(2) > div:nth-child(4)'},
             {'exemption2year': '#collapseFour > div > div > div > div:nth-child(3) > div.col-xs-3.pt-header'},
             {'exemption2owner': '#collapseFour > div > div > div > div:nth-child(3) > div:nth-child(2)'},
             {'exemption2senior': '#collapseFour > div > div > div > div:nth-child(3) > div:nth-child(3)'},
             {'exemption2seniorfreeze': '#collapseFour > div > div > div > div:nth-child(3) > div:nth-child(4)'},
             {'exemption3year': '#collapseFour > div > div > div > div:nth-child(4) > div.col-xs-3.pt-header'},
             {'exemption3owner': '#collapseFour > div > div > div > div:nth-child(4) > div:nth-child(2)'},
             {'exemption3senior': '#collapseFour > div > div > div > div:nth-child(4) > div:nth-child(3)'},
             {'exemption3seniorfreeze': '#collapseFour > div > div > div > div:nth-child(4) > div:nth-child(4)'},
             {'exemption4year': '#collapseFour > div > div > div > div:nth-child(5) > div.col-xs-3.pt-header'},
             {'exemption4owner': '#collapseFour > div > div > div > div:nth-child(5) > div:nth-child(2)'},
             {'exemption4senior': '#collapseFour > div > div > div > div:nth-child(5) > div:nth-child(3)'},
             {'exemption4seniorfreeze': '#collapseFour > div > div > div > div:nth-child(5) > div:nth-child(4)'},

             ]

    row = pd.DataFrame()
    for item in items:
        span = html.select(list(item.values())[0])
        try:
            row[list(item.keys())[0]] = [span[0].get_text().strip()]

        except:
            retries = retries + 1
            print("Retrying: "+ str(retries))
            print( sys.exc_info()[0])
            if (retries >= 5):
                results.to_csv(str(taxyear)+'/assessments2.csv')

                print("Retries failing, exiting...")
                exit(1)
            time.sleep(5)


    if index % 100 == 0:
        print('------- ' + str(index) + ' -------')
        results.to_csv(str(taxyear)+'/assessments2.csv')

results.to_csv(str(taxyear)+'/assessments2.csv')

