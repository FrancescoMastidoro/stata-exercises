**********************************
* Exercise 5: Reading a Dataset's Structure — Describe, Summarize, and Tabulate with Life Expectancy Data
**********************************

* 1. load and inspect
sysuse lifeexp, clear
describe
* the dataset has 68 observations and 6 variables
* variables stored as string: country
* variables stored as numeric: region, popgrowth, lexp, gnppc, safewater
* non-obvious concepts described by variables:
* - popgrowth: average annual population growth in percentage terms
* - lexp:  of life expectancy at birth
* - gnppc: GNP (gross national product) per capita

* 2. summarize a continuous variable
summarize lexp
* mean: 72.27941; SD: 4.715315; min: 54; max: 79
* the min-max range (79-54=25) seems reasonable given welk-known large disparities 
* in global health system's quality across different countries

* 3. detailed distribution of life expectancy
summarize lexp, detail
* the mean equals 72.27941 whereas the median is 73. Mean and median are almost identical,
* suggesting the the distribution of lexp across these 68 countries is rather symmetric, 
* with slight negative skewness (since mean < median). However, the statistic of skewness 
* equals -.9080208, so there is in fact strong negative skewness. This is evident even by 
* looking at the quartiles (the distance between the second and third quartile
* is smaller than the distance between the first and the second quartile).
* So, most countries cluster near the top of the distribution.

* 4. tabulate a categorial variable and compare group means
tabulate region, sort
tabulate region, sort nolabel
* 44 countries (~65% of all countries) are in Europe and Central Asia.
* 14 (~21%) are in North America, and 10 (~15%) are in South America.

bysort region: summarize lexp 
* the region with the highest average life expectancy at birth is Europe and Central Asia (73.06818).
* the overall mean (computed at point 2) is 72.27941, so the gap is +0.78877 (almost one year).

* 5. GNP distribution within regions
tabulate region, sort
* the region with the highest number of observations is Europe and Central Asia (44 countries)
summarize gnppc if region == 1, detail
summarize gnppc, detail
* the median GNP per capita for Europe and Central Asia is 3910; the IQR is 20120
* the median GNP per capita for the whole sample is 3360; the IQR is 12740
* so, Europe and Central Asia is richer than the sample as a whole, and 
* income is more dispersed in Europe and central asia than in the world as a whole
