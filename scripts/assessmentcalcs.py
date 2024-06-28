import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common

taxyear = common.getTaxYear()
bucketsize = 2500
pctbucketsize = 5
fiveyearsago = taxyear - 4
assessments = pd.read_csv(
    str(taxyear)+"/combinedassessments.csv",  thousands=',')
assessments = assessments[assessments.Use == 'SINGLE FAMILY']
assessments['taxbill'] = assessments['taxbill'+str(taxyear)]

assessments['range'] = (assessments.taxbill / bucketsize)
assessments['range'] = np.where(
    np.logical_and(assessments['range'] > 0, assessments['range'] < 1000000), assessments['range'], 0)
assessments.range = assessments.range.astype(int) * bucketsize
assessments['fiveyearrange'] = assessments.fiveyearbillchangepct / pctbucketsize
assessments['fiveyearrange'] = np.where(
    np.logical_and(assessments['fiveyearrange'] > -41 / pctbucketsize, assessments['fiveyearrange'] < 111 / pctbucketsize), assessments['fiveyearrange'], 0)
assessments.fiveyearrange = assessments.fiveyearrange.astype(
    int) * pctbucketsize
assessments['lastyearrange'] = assessments.lastyearbillchangepct / pctbucketsize
assessments['lastyearrange'] = np.where(
    np.logical_and(assessments['lastyearrange'] > -60 / pctbucketsize, assessments['lastyearrange'] < 70 / pctbucketsize), assessments['lastyearrange'], 0)
assessments.lastyearrange = assessments.lastyearrange.astype(
    int) * pctbucketsize

assessments['temp'] = (
    assessments.range).map('{:,.0f} to'.format)
assessments['temp2'] = (
    (assessments.range/bucketsize + 1) * bucketsize).map(' {:,.0f}'.format)

assessments['rangedescription'] = assessments.temp + assessments.temp2
assessments = assessments.drop(columns=['temp', 'temp2'], axis=1)
assessments = assessments.sort_values(by=['range'])
pivot = assessments.pivot_table(
    columns=['range'], values='taxbill', aggfunc='count')
pivot = pivot.transpose()
pivot['rangestr'] = (pivot.index).map('${:,.0f}'.format)

pivot2 = assessments.pivot_table(
    columns=['fiveyearrange'], values='taxbill', aggfunc='count')

plt.close()
plt.figure(figsize=(10, 8), dpi=200)
width = 1
plt.bar(pivot.rangestr, pivot.taxbill, color='#3366cc', align='edge')
plt.xticks(rotation=45)
plt.ylabel("Number of Homes")
plt.title('Count of Oak Park Single Family Homes by Tax Bill Amount')
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig(str(taxyear)+'/charts/taxbillcounts.png')
pivot.to_csv(str(taxyear)+'/assessmentpivot.csv')

pivot2 = pivot2.transpose()
print(pivot2)
plt.close()
plt.figure(figsize=(10, 8), dpi=200)
pivot2['fiveyearrangestr'] = (pivot2.index).map('{:.0f}%'.format)
width = 1
plt.bar(pivot2.fiveyearrangestr, pivot2.taxbill, color='#3366cc', align='edge')
plt.xticks(rotation=45)
plt.ylabel("Number of Homes")
plt.title(
    'Count of Oak Park Single Family Homes by Tax Bill Percentage Change, '+str(fiveyearsago)+'-'+str(taxyear))
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig(str(taxyear)+'/charts/taxbillpercentagecountsfiveyear.png')

pivot2 = assessments.pivot_table(
    columns=['lastyearrange'], values='taxbill', aggfunc='count')

plt.close()
plt.figure(figsize=(10, 8), dpi=200)
width = 1
plt.bar(pivot.rangestr, pivot.taxbill, color='#3366cc', align='edge')
plt.xticks(rotation=45)
plt.ylabel("Number of Homes")
plt.title('Count of Oak Park Single Family Homes by Tax Bill Amount')
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig(str(taxyear)+'/charts/taxbillcounts.png')
pivot.to_csv(str(taxyear)+'/assessmentpivot.csv')

pivot2 = pivot2.transpose()
print(pivot2)
plt.close()
plt.figure(figsize=(10, 8), dpi=200)
pivot2['lastyearrangestr'] = (pivot2.index).map('{:.0f}%'.format)
width = 1
plt.bar(pivot2.lastyearrangestr, pivot2.taxbill, color='#3366cc', align='edge')
plt.xticks(rotation=45)
plt.ylabel("Number of Homes")
plt.title(
    'Count of Oak Park Single Family Homes by Tax Bill Percentage Change, '+str(taxyear-1)+'-'+str(taxyear))
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig(str(taxyear)+'/charts/taxbillpercentagecounts.png')
