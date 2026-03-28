**********************************
* Exercise 3: Frequencies, Distributions, and Cross-Tabulations
**********************************

* 1. Load and inspect
sysuse census
describe
* the dataset contains 50 observations and 13 variables.
* each observation represents each US state.
* all variables are numerical except "state" and "state2"

* 2. Summarize population
summarize pop, detail
* the mean is 4'518'149 while the median is 3'066'433. Since the median is smaller than the mean,
* the distribution of the population by US states is right-skewed. 
* The standard deviation is very large, and this further indicates that there is 
* large dispersion in population across states.
* So, the single number that tells the most about the "typical" state population is the median.
* The mean might be misleading because it is significantly sensitive to outliers (eg California)

* 3. Detailed distribution
* see answer to point 2

* 4. Tabulate a categorical variable and combine with summarize
* first option:
bysort region: summarize pop

* second option
summarize pop if region == 1 // region "NE"
summarize pop if region == 2 // region "N cntrl"

* region "NE" has a higher average state population compared to region "N contrl" (5459476 vs 4905473)

* 5. Weighted frequencies
tabulate region // this already shows the percentage of observations for each category
/*

     Census |
     region |      Freq.     Percent        Cum.
------------+-----------------------------------
         NE |          9       18.00       18.00
    N Cntrl |         12       24.00       42.00
      South |         16       32.00       74.00
       West |         13       26.00      100.00
------------+-----------------------------------
      Total |         50      100.00

*/

* then I can simply run:
* sum pop if region == n for each n = 1,2,3,4
* then I can compute the total population in each region by computing r(N)*r(mean) after each sum run
sum pop if region == 1
di r(N) * r(mean) // 49,135,283

sum pop if region == 2
di r(N) * r(mean) // 58,865,670

sum pop if region == 3
di r(N) * r(mean) // 74,734,029

sum pop if region == 4
di r(N) * r(mean) // 43,172,490

* clearly, the region with the largest share of US population is region 3 (ie South), comprising 16 US states
* alternative method:
tabulate region [fweight=pop]

/*

     Census |
     region |      Freq.     Percent        Cum.
------------+-----------------------------------
         NE | 49,135,283       21.75       21.75
    N Cntrl | 58,865,670       26.06       47.81
      South | 74,734,029       33.08       80.89
       West | 43,172,490       19.11      100.00
------------+-----------------------------------
      Total |225,907,472      100.00

*/
