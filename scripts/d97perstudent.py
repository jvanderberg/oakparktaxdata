import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

baseyear = 2002
final = pd.read_csv("oak park tax history summary.csv")
final = final[final.Year != 'All']

final = final.set_index(np.array(final.Year).astype(int))
final = final[ final.index > 2001]
based97enrollment = final['D97 Enrollment'][baseyear]
baseperstudent = final.D97[baseyear] / based97enrollment

perstudent = ((final.D97 /  final['D97 Enrollment']) - baseperstudent) / baseperstudent
d97enrollment = (final['D97 Enrollment'] - based97enrollment) / based97enrollment


plt.close()
plt.figure(figsize=(7,6), dpi=200)
plt.title("D97 Per Student Levy Growth")
plt.ylabel('Percentage Increase')
line2=plt.plot(perstudent * 100, color='#dc3912', linewidth=2)
line5=plt.plot(d97enrollment * 100,  color='#3366cc', linewidth=2)

plt.xticks([2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016])
plt.legend(['Per Student Levy', 'Enrollment'])
plt.grid(axis='y', linewidth=0.5)

plt.savefig('charts/d97 per student levy growth.png')
