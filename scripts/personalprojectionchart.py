import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common
baseyear = common.getTaxYear()
projection = pd.read_csv(str(baseyear)+"/projections.csv")
projection = projection.set_index(projection.Year)
projection = projection[projection.index >= baseyear]


def project(col, baseyear):
    plt.close()
    plt.figure(figsize=(6, 5), dpi=200)
    p = projection[col]
    years = [str(baseyear), str(baseyear+5), str(baseyear+10),
             str(baseyear+15), str(baseyear+20)]
    p1 = plt.bar(years, p[p.index.isin(years)])

    plt.title('Projected Future Tax  $'+col+' in '+str(baseyear))
    plt.xticks(years, (
        str(baseyear), '5 years', '10 years', '15 years', '20 years'))
    rects = p1.patches
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
            color='white')

    # hide borders
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.tick_params(top=False, bottom=False, left=False,
                    right=False, labelleft=False, labelbottom=True)

    plt.savefig(str(baseyear)+'/charts/personal projection'+col+'.png')


project('10k', baseyear)
project('12.5k', baseyear)
project('15k', baseyear)
project('17.5k', baseyear)
project('20k', baseyear)
