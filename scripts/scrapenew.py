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
import asyncio
import aiohttp as aiohttp

taxyear = common.getTaxYear()

pins = pd.read_csv("oppins.csv")

# Don't start processing pins until you hit 'startpin'
# startpin = '16-05-100-038-0000'
try:
    startpin
except NameError:
    startpin = None



async def simple_get(url):

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100,limit_per_host=100)) as session:
        async with session.get(url) as resp:
            body = await resp.text()
            return body

# def simple_get(url):
#     """
#     Attempts to get the content at `url` by making an HTTP GET request.
#     If the content-type of response is some kind of HTML/XML, return the
#     text content, otherwise return None.
#     """
#     try:
#         with closing(get(url, stream=True)) as resp:
#             if is_good_response(resp):
#                 return resp.content
#             else:
#                 return None

#     except RequestException as e:
#         log_error('Error during requests to {0} : {1}'.format(url, str(e)))
#         return None


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





def get_values(cells, property_data, process, taxyear):
    property_data[str(taxyear) + ' ' + process +' Total MV'] = cells[2].get_text(strip=True)
    property_data[str(taxyear) + ' ' + process +' Land AV'] = cells[3].get_text(strip=True)
    property_data[str(taxyear) + ' ' + process +' Bldg AV'] = cells[4].get_text(strip=True)
    property_data[str(taxyear) + ' ' + process +' Total AV'] = cells[5].get_text(strip=True)
    property_data[str(taxyear) + ' ' + process +' HIE AV'] = cells[6].get_text(strip=True)
def extract_data(html_content, property_data):
    soup = BeautifulSoup(str(html_content), 'html.parser')
    table_rows = soup.find_all('tr')
    
 
    for row in table_rows:
        cells = row.find_all('td')
        # print(len(cells))
        if len(cells) == 2:
            heading = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            property_data[heading] = value
        if len(cells) == 8:
            year = cells[0].get_text(strip=True)
            process = cells[1].get_text(strip=True)
            if (year == str(taxyear) or year == str(taxyear-1) or year == str(taxyear-2) or year == str(taxyear-2) or year == str(taxyear-3)):
                get_values(cells, property_data, process, year)

    
    return property_data

async def process_url(url, pin):
    contents = await simple_get(url)
    print(pin)

    html = BeautifulSoup(contents, 'html.parser')

    items = [{'PARCEL_CC': 'div[name="PARCEL_CC"]'},
                {'MAILDETAIL': 'div[name="MAILDETAIL"]'},
                {'ASMT_VALUES_CCD': 'div[name="ASMT_VALUES_CCD"]'},
                {'VALUE_SUMMARY_CC': 'div[name="VALUE_SUMMARY_CC"]'},
                {'FULL_LEGAL_CD': 'div[name="FULL_LEGAL_CD"]'},
                {'LAND_CCD': 'div[name="LAND_CCD"]'},
                {'RESIDENTIAL_CC': 'div[name="RESIDENTIAL_CC"]'},
                {'SALES_DETAILS': 'div[name="NOTICE_SUMMARY_CC"]'},
                {'NOTICE_SUMMARY_CC': 'div[name="NOTICE_SUMMARY_CC"]'},
                {'COMM_BLDG_SUMMARY': 'div[name="COMM_BLDG_SUMMARY"]'},
                {'COMMERCIAL': 'div[name="COMMERCIAL"]'}
        ]
    property_data = {}
   
    for item in items:
        span = html.select(list(item.values())[0])
        # print(span)
        if (len(span)==0): continue
        try:
            values = extract_data(span[0], property_data)

        except:
            print('Error processing '+pin.PIN +
                    ' ' + list(item.keys())[0] + ' ' + url)
    row = pd.DataFrame()

    row = row.append(property_data, ignore_index=True)    
    return row

processpin = False


async def main():
    results = pd.DataFrame()

    processpin = False
    if startpin is None:
        processpin = True
    tasks = []
    start_time = time.time()
    for index, pin in pins.iterrows():
        if startpin is not None and pin.PIN == startpin:
            processpin = True

        if processpin == False:
            continue
   
        url = 'https://assessorpropertydetails.cookcountyil.gov/Datalets/PrintDatalet.aspx?pin=' + \
            pin.PIN.replace("-", "") + "&gsp=PROFILEALL_CC&taxyear=2023&jur=016&ownseq=0&card=1&roll=RP&State=1&item=1&items=-1&all=all&ranks=Datalet"
        task = asyncio.create_task(process_url(url, pin.PIN))
        tasks.append(task)
        if index % 8 == 0 and index != 0:
            task_results = await asyncio.gather(*tasks)
            for task_result in task_results:
                results = results.append(task_result, ignore_index=True)
            print('------- ' + str(index) + ' -------')
            time_difference = time.time() - start_time
            print(f'Scraping time: %.2f seconds.' % (time_difference / 8))
            results.to_csv(str(taxyear)+'/assessmentsnew.csv')
            start_time = time.time()
            tasks=[]
 

loop = asyncio.get_event_loop()
loop.run_until_complete(main())