# Oak Park Tax Data

Oak Park, IL Tax Data and Analysis

The file "oak park tax history.csv" contains historical tax levy data for Oak park taxing agencies.

## Columns

-   _Year_ The tax year
-   _Agency_ The Taxing agency rollup
-   _Detail_ The specific tax agency if rolled up
-   _Levy_ The total levy in dollars
-   _Rate_ The tax rate
-   _EAV_ Total equalized assessed value of the properties subject to the tax rate

In all cases Levy = Rate \* EAV

The file "oak park tax history summary.csv" contains the totals by year in a pivoted format.

## Columns

-   _Year_ The tax year
-   _D200_ The Oak park portion of the OPRF levy for that year
-   _D97_ The Oak Park Elementary/Middle school levy
-   _Oak Park Township_ The township levy, including general assistance and mental health
-   _Park District_ The Oak Park park district
-   _Village of Oak Park_ The Village levy with the library levy added in
-   _Grand Total_ The total levy for that year

## _Source_

The source of this data is the Cook County Clerk, using their online tool for 2006-2016, and a historical records request for previous years.

https://www.cookcountyclerk.com/service/tax-agency-reports

## Notes

-   For simplicity, the "Agency" column rolls up the Library into the Village of Oak Park, and the mental health and general assistance funds into the Township, the 'Detail' column breaks those out if you want to do summaries that perserve this detail.
-   The 'D200' Agency is the Oak Park only portion of OPRF's levy. The 'D200 Total' agency is the full OPRF levy. If you are making summary rollups of this data, only include one or the other.
