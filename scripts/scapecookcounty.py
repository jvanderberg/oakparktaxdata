from splinter import Browser
import pandas as pd
import time
import sys
import splinter as splinter
import common

taxyear = getTaxYear()

pins = pd.read_csv("oppins.csv")

# Don't start processing pins until you hit 'startpin'
#startpin = '16-18-430-001-0000'
try:
    startpin
except NameError:
    startpin = None

results = pd.DataFrame()
url = "http://www.cookcountypropertyinfo.com/default.aspx"

with Browser() as browser:
    # Visit URL
    browser.visit(url)
    processpin = False
    if startpin == None:
        processpin = True

    results = pd.DataFrame()

    for index, pin in pins.iterrows():
        valid = False
        retries = 0
        while (valid == False and retries < 10):
            valid = True
            if startpin != None and pin.PIN == startpin:
                processpin = True

                # As it can take awhile to get the the target pin, refresh the connection to the browser
                # or it times out
            if (processpin == False and index % 500 == 0):
                browser.visit(url)
            if (processpin == True):
                print pin.PIN, index
                # print 2, pin
                browser.visit(url)
                parts = pin.PIN.split('-')
                browser.fill(
                    "ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox1", parts[0])
                browser.fill(
                    "ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox2", parts[1])
                browser.fill(
                    "ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox3", parts[2])
                browser.fill(
                    "ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox4", parts[3])
                browser.fill(
                    "ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox5", parts[4])

                button = browser.find_by_name(
                    'ctl00$ContentPlaceHolder1$PINAddressSearch$btnSearch')

                button.click()

                baseyear = int(taxyear)

                # Interact with elements
                if browser.is_element_present_by_id("ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_1", 10):
                    items = [{'taxbill'+str(baseyear): 'ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_0'},
                             {'taxbill'+str(
                                 baseyear-1): 'ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_1'},
                             {'taxbill'+str(
                                 baseyear-2): 'ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_2'},
                             {'taxbill'+str(
                                 baseyear-3): 'ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_3'},
                             {'taxbill'+str(
                                 baseyear-4): 'ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_4'},
                             {'homeownerexemption': 'ContentPlaceHolder1_TaxCalculator_lblHomeownerExemption'},
                             {'seniorfreezeexemption': 'ContentPlaceHolder1_TaxCalculator_lblSeniorFreezeExemption'},
                             {'seniorcitizenexemption': 'ContentPlaceHolder1_TaxCalculator_lblSeniorCitizenExemption'},
                             {'taxbeforeexemptions': 'ContentPlaceHolder1_TaxCalculator_lblTaxBeforeExemptions'},
                             {'taxafterexemptions': 'ContentPlaceHolder1_TaxCalculator_lblTaxAfterExemptions'},
                             {'estimatedvalue': 'ContentPlaceHolder1_TaxYearInfo_propertyEstimatedValue'},
                             {'assessedvalue': 'ContentPlaceHolder1_TaxYearInfo_propertyAssessedValue'},
                             {'lotsize': 'ContentPlaceHolder1_TaxYearInfo_propertyLotSize'},
                             {'buildingsize': 'ContentPlaceHolder1_TaxYearInfo_propertyBuildingSize'},
                             {'class': 'ContentPlaceHolder1_TaxYearInfo_propertyClass'},
                             {'taxcode': 'ContentPlaceHolder1_TaxYearInfo_propertyTaxCode'},
                             {'address': 'ContentPlaceHolder1_PropertyInfo_propertyAddress'},
                             {'city': 'ContentPlaceHolder1_PropertyInfo_propertyCity'},
                             {'zip': 'ContentPlaceHolder1_PropertyInfo_propertyZip'},
                             {'township': 'ContentPlaceHolder1_PropertyInfo_propertyTownship'},
                             {'pin': 'ContentPlaceHolder1_lblResultTitle'}
                             ]

                    row = pd.DataFrame()
                    for item in items:
                        try:
                            value = browser.find_by_id(
                                item.values()[0]).first.html
                            row[item.keys()[0]] = [value]

                        except splinter.exceptions.ElementDoesNotExist:
                            print 'Error processing '+pin.PIN + \
                                ' ' + item.keys()[0] + ' ' + url + ''

                    results = results.append(row)
            # print results
        results.to_csv(taxyear+'/assessments2.csv')
