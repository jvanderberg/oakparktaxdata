import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common

taxyear, baseyear = common.getBaseAndTaxYear()

final = pd.read_csv("oak park tax history summary.csv")
final = final[final.Year != 'All']

final = final.set_index(np.array(final.Year).astype(int))
final = final[final.index >= baseyear]
based97enrollment = final['D97 Enrollment'][baseyear]
baseawi = final.AWI[baseyear]
baseperstudent = final.D97[baseyear] / based97enrollment
perstudent = ((final.D97 / final['D97 Enrollment']
               ) - baseperstudent) / baseperstudent
perstudentadjusted = ((final.D97 / final['D97 Enrollment'])
                      * baseawi / final.AWI - baseperstudent) / baseperstudent
d97enrollment = (final['D97 Enrollment'] -
                 based97enrollment) / based97enrollment


plt.close()
plt.figure(figsize=(7, 6), dpi=200)
plt.title("D97 Per Student Levy Growth")
plt.ylabel('Percentage Increase')
line1 = plt.plot(perstudent * 100, color='#dc3912', linewidth=2)
line2 = plt.plot(perstudentadjusted * 100,  color='#3366cc', linewidth=2)

plt.xticks(np.arange(baseyear, taxyear+1, step=2))
plt.legend(['Per Student Levy', 'Per Student Wage Adjusted'])
plt.grid(axis='y', linewidth=0.5)
perstudentadjusted.to_csv(str(taxyear)+"/d97 per student levy growth.csv")
plt.savefig(str(taxyear)+'/charts/d97 per student levy growth.png')
