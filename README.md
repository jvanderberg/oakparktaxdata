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

In all cases Levy = Rate / EAV

The file "oak park tax history summary.csv" contains the totals by year in a pivoted format.

## Columns

-   _Year_ The tax year
-   _D200_ The Oak park portion of the OPRF levy for that year, this is calculated by taking the (Village of OP EAV / D200 Eav) * D200 Levy
-   _D97_ The Oak Park Elementary/Middle school levy
-   _Oak Park Township_ The township levy, including general assistance and mental health
-   _Park District_ The Oak Park park district
-   _Village of Oak Park_ The Village levy with the library levy added in
-   _All_ The total levy for that year
-   _CPI_ The CPI-U for that year from the BLS https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-201804.pdf
-   _AWI_ The Average Wage Index from the Social Security Administration https://www.ssa.gov/oact/cola/AWI.html

The file 'projections.csv' contains an exponential best fit to the existing data.

## Columns

-   _Year_ The Levy year
-   _Levy_ The Levy in that year
-   _Fit_ The best exponential fit for the year, fit to the existing data and projected out 20 years.

## _Source_

The source of this data is the Cook County Clerk, using their online tool for 2006-2016, and a historical records request for previous years.

https://www.cookcountyclerk.com/service/tax-agency-reports

These files are available in the "data" directory.

cpi.csv is derived from the CPI-U found at https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-201804.pdf

awi.csv is derived from https://www.ssa.gov/oact/cola/AWI.html

d97demographics.csv is derived from https://www.op97.org/teach-learn/state-report-cards

## Notes

-   For simplicity, the "Agency" column rolls up the Library into the Village of Oak Park, and the mental health and general assistance funds into the Township, the 'Detail' column breaks those out if you want to do summaries that perserve this detail.
-   The 'D200' Agency is the Oak Park only portion of OPRF's levy. The 'D200 Total' agency is the full OPRF levy. If you are making summary rollups of this data, only include one or the other.

# Generating the charts and derived data

1.  Install python v3
2.  pip install pandas
3.  pip install numpy
4.  pip install matplotlib
5.  Run the scripts in the order below


YYYY is the current tax year
python scripts/scrapecookcounty.py YYYY
python scripts/scrapeassessments.py YYYY
python scripts/assessments.py YYYY
python scripts/assessmentcalcs.py YYYY
python scripts/pivot.py YYYY
python scripts/barchart.py YYYY
python scripts/barchartpercentage.py YYYY
python scripts/taxincreasedistribution.py YYYY
python scripts/projection.py YYYY  
python scripts/projectionchart.py YYYY
python scripts/personalprojectionchart.py YYYY
python scripts/d97enrollmentcomparison.py YYYY 2002
python scripts/d97perstudent.py YYYY 2002
python scripts/twelvekcomparison.py YYYY
python scripts/growthcomparison.py YYYY 2006
python scripts/barchartpercentagechange.py YYYY 2000