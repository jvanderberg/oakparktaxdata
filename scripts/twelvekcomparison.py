import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common
baseyear = common.getTaxYear()
projection = pd.read_csv(str(baseyear)+"/projectionssummary.csv")
projection = projection.set_index(projection.Year)
tenyears = baseyear + 10

plt.close()
plt.figure(figsize=(8, 6), dpi=200)
width = 0.7
print(projection)

p1 = plt.bar(x="Projected Current Growth",
             height=projection['12.5k'][tenyears], color='#dc3912')
p2 = plt.bar(x="Limited to CPI (Price)",
             height=projection['CPI 12.5k'][tenyears], color='#3366cc')
p3 = plt.bar(x="Limited to AWI (Wage) ",
             height=projection['AWI 12.5k'][tenyears], color='#990099')

plt.title('Projected '+str(tenyears)+' tax bill for current bill of $12,500')
# plt.xticks(years, (
#	str(baseyear), '5 years', '10 years', '15 years', '20 years'))


def annotate(bar):
    rects = bar.patches
    # For each bar: Place a label
    for rect in rects:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = -20
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "${:,.0f}".format(y_value)

        # Create annotation
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va,
            color='white',
            size=14)


annotate(p1)
annotate(p2)
annotate(p3)

# hide borders
for spine in plt.gca().spines.values():
    spine.set_visible(False)

plt.tick_params(top=False, bottom=False, left=False,
                right=False, labelleft=False, labelbottom=True)

plt.savefig(str(baseyear)+'/charts/twelvekcomparison.png')
