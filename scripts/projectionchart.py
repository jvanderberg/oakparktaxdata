import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

final = pd.read_csv("projections.csv")
final = final.set_index(final.Year)
plt.close()
plt.figure(figsize=(5,4), dpi=200)
plt.ylabel("Tax Levy $ (Millions)")
plt.title('Projected Future Tax Levy')
line1=plt.plot(final.Levy / 1000000, color='blue')
line2=plt.plot(final.Fit / 1000000, color='red')
plt.legend(['Actual', 'Projection'])
plt.grid(axis='y', linewidth=0.5)
plt.xticks([1999, 2018, 2038])
plt.savefig('charts/projected future levy.png')