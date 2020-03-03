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

#startpin = '16-18-130-020-0000'
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
    retries = 0
    while retries < 5:
        try:
            url = 'https://www.cookcountyassessor.com/pin/' + \
                pin.PIN.replace("-", "")+ "/print"
            contents = simple_get(url)
            html = BeautifulSoup(contents, 'html.parser')

            row = pd.DataFrame()
            marketValues = html.find_all("span",text="Estimated  Market Value")
            parent = marketValues[0].parent
            value  = parent.findNext('span', class_="detail-row--detail")
            row['pin'] = [pin.PIN]
            row['marketvalue'] = [value.contents[0]]

            parent = marketValues[1].parent
            value  = parent.findNext('span', class_="detail-row--detail")
            row['marketvaluepreviousyear'] = [value.contents[0]]

            address = html.find("div", class_="address")
            address = address.contents[1].contents[0]
            addressparts = address.split(" ● ")
            row['address'] = " ".join(addressparts[0].split())
            row['city'] = addressparts[1]
            row['township'] = addressparts[2]
            spans = html.find_all( class_="detail-row--label")

            for item in items:
                for span in spans:
                    try:
                        if (span.contents[0] ==list(item.values())[0] ):

                        #label = html.find("span", text=list(item.values())[0], class_="detail-row--label" )
                            parent = span.parent
                            value  = parent.findNext('span', class_="detail-row--detail")
                            row[list(item.keys())[0]] = [value.contents[0]]

                    except:
                    
                        print('Error processing '+pin.PIN +
                            ' ' + list(item.keys())[0] + ' ' + url)

            results = results.append(row)
            break
        except KeyboardInterrupt:
            print("Exiting...")
            results.to_csv(str(taxyear)+'/assessments2.csv')

            exit(0)
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

