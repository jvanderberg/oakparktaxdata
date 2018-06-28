import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
rate = 12.191
equalizer = 2.9084
bucketsize = 2500

assessments = pd.read_csv("assessments.csv",  thousands=',')
assessments = assessments[assessments.use == 'Single Family']
assessments['taxbill'] = assessments.combinedassessedvalue * \
    rate / 100 * equalizer

assessments['range'] = (assessments.taxbill / bucketsize)
assessments['range'] = np.where(
    np.logical_and(assessments['range'] > 0, assessments['range'] < 1000000), assessments['range'], 0)
assessments.range = assessments.range.astype(int) * bucketsize
assessments['temp'] = (
    assessments.range * bucketsize).map('{:,.0f} to'.format)
assessments['temp2'] = (
    (assessments.range + 1) * bucketsize).map(' {:,.0f}'.format)

assessments['rangedescription'] = assessments.temp + assessments.temp2
assessments = assessments.drop(columns=['temp', 'temp2'], axis=1)
pivot = assessments.pivot_table(
    columns='range', values='taxbill', aggfunc='count')
print pivot
pivot = pivot.transpose()
print pivot.index

print pivot
# cpi = pd.read_csv("cpi.csv")
# cpi = cpi.set_index(cpi.Year)
# pivot = pivot.join(cpi.CPI)
# awi = pd.read_csv("awi.csv")
# awi = awi.set_index(awi.Year)
# pivot = pivot.join(awi.AWI)
# d97enrollment = pd.read_csv("d97demographics.csv")
# d97enrollment = d97enrollment.set_index(d97enrollment.Year)
# pivot = pivot.join(pd.Series(d97enrollment['D97 Enrollment']))

plt.close()
plt.figure(figsize=(6, 5), dpi=200)
width = 1
plt.bar(pivot.index, pivot.taxbill, color='#3366cc', bottom=0)

plt.ylabel("Tax Levy $ (Millions)")
plt.title('Total Oak Park Tax Levy by Year')
plt.grid(axis='y', linewidth=0.5)
plt.legend(['Count'])

plt.savefig('charts/taxbillcounts.png')
# pivot.to_csv('oak park tax history summary.csv')
pivot.to_csv('assessmentpivot.csv')
assessments.to_csv('temp.csv')
