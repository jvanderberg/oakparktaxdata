import pandas as pd
import time


pins = pd.read_csv("oppins.csv")
pins2 = pd.read_csv("oppins2.csv")

# print(pins2['PINS'])
intersection = set(pins2["PINS"]).difference(pins["PIN"])

print(intersection)
