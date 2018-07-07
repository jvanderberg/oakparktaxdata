import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#rate = 12.191
#equalizer = 2.9084
bucketsize = 2500
pctbucketsize = 5

assessments = pd.read_csv("combinedassessments.csv",  thousands=',')
assessments = assessments[assessments.use == 'Single Family']
assessments['taxbill'] = assessments.taxbill2017

assessments['range'] = (assessments.taxbill / bucketsize)
assessments['range'] = np.where(
    np.logical_and(assessments['range'] > 0, assessments['range'] < 1000000), assessments['range'], 0)
assessments.range = assessments.range.astype(int) * bucketsize
assessments['lastyearrange'] = assessments.lastyearbillchangepct / pctbucketsize
assessments['lastyearrange'] = np.where(
    np.logical_and(assessments['lastyearrange'] > -60 / pctbucketsize, assessments['lastyearrange'] < 70 / pctbucketsize), assessments['lastyearrange'], 0)
assessments.lastyearrange = assessments.lastyearrange.astype(int) * pctbucketsize

assessments['temp'] = (
    assessments.range).map('{:,.0f} to'.format)
assessments['temp2'] = (
    (assessments.range/bucketsize + 1) * bucketsize).map(' {:,.0f}'.format)

assessments['rangedescription'] = assessments.temp + assessments.temp2
assessments = assessments.drop(columns=['temp', 'temp2'], axis=1)
assessments = assessments.sort_values(by=['range'])
pivot = assessments.pivot_table( columns=['range'], values='taxbill', aggfunc='count')
pivot = pivot.transpose()
pivot['rangestr'] = (pivot.index).map('${:,.0f}'.format)

pivot2 = assessments.pivot_table( columns=['lastyearrange'], values='taxbill', aggfunc='count')

plt.close()
plt.figure(figsize=(10, 8), dpi=200)
width = 1
plt.bar(pivot.rangestr, pivot.taxbill, color='#3366cc', align='edge')
plt.xticks(rotation=45)
plt.ylabel("Number of Homes")
plt.title('Count of Oak Park Single Family Homes by Tax Bill Amount')
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig('charts/taxbillcounts.png')
pivot.to_csv('assessmentpivot.csv')

pivot2 = pivot2.transpose()
print(pivot2)
plt.close()
plt.figure(figsize=(10, 8), dpi=200)
pivot2['lastyearrangestr'] = (pivot2.index).map('{:.0f}%'.format)
width = 1
plt.bar(pivot2.lastyearrangestr, pivot2.taxbill, color='#3366cc', align='edge')
plt.xticks(rotation=45)
plt.ylabel("Number of Homes")
plt.title('Count of Oak Park Single Family Homes by Tax Bill Percentage Change, 2016-2017')
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig('charts/taxbillpercentagecounts.png')
