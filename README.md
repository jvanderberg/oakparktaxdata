# Oak Park Tax Data

Oak Park, IL Tax Data an Analysis

The file "oak park tax history.csv" contains historical tax levy data for Oak park taxing agencies.

## Columns

-   _Year_ The tax year
-   _Agency_ The Taxing agency rollup
-   _Detail_ The specific tax agency if rolled up
-   _Levy_ The total levy in dollars
-   _Rate_ The tax rate
-   _EAV_ Total equalized assessed value of the properties subject to the tax rate

In all cases Levy = Rate \* EAV

## _Source_

The source of this data is the Cook County Clerk, using their online tool for 2006-2016, and a historical records request for previous years.

https://www.cookcountyclerk.com/service/tax-agency-reports

## Notes

-   For simplicity, the "Agency" column rolls up the Library into the Village of Oak Park, and the mental health and general assistance funds into the Township, the 'Detail' column breaks those out if you want to do summaries that perserve this detail.
-   The 'D200' Agency is the Oak Park only portion of OPRF's level. The D200 Total agency is the full OPRF levy. If you are making summary rollups of this data, only include one or the other.
