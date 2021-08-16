from splinter import Browser
import pandas as pd
import time
import sys
import splinter as splinter
import common
import selenium

taxyear = common.getTaxYear()

pins = pd.read_csv("oppins.csv")
results = pd.DataFrame()

# Don't start processing pins until you hit 'startpin'
startpin = '16-17-124-011-0000'
try:
    startpin
    results=pd.read_csv(str(taxyear)+'/cookcountyassessments.csv')
except NameError:
    startpin = None

url = "http://www.cookcountypropertyinfo.com/default.aspx"


# Visit URL
processpin = False
if startpin == None:
    processpin = True

browser = Browser('firefox', headless=True)

for index, pin in pins.iterrows():

    valid = False
    retries = 0
    while (valid == False and retries < 10):
        try:
            valid = True
            if startpin != None and pin.PIN == startpin:
                processpin = True

            if (processpin == True):
                if (index % 50 == 0):
                    #Prevent a memory leak - a real hack, but oh well
                    browser.quit()
                    browser = Browser('firefox', headless=True)
                print(pin.PIN, index)
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
                                list(item.values())[0]).first.html
                            row[list(item.keys())[0]] = [value]

                        except splinter.exceptions.ElementDoesNotExist:
                            row[list(item.keys())[0]] = ""
                            print('Error processing '+str(pin.PIN) + \
                                ' ' + list(item.keys())[0] + ' ' + url + '')

                    results = results.append(row)
                # print results
                print("save")
                results.to_csv(str(taxyear)+'/cookcountyassessments.csv', index=False)
        except selenium.common.exceptions.WebDriverException:
            retries = retries + 1
            if (retries==10):
                raise
            valid=False
            print('Error, retry ' + str(retries))
            time.sleep(5)
