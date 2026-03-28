**********************************
* Exercise 2: Exploring data structure and summary statistics
**********************************

* 1. load and inspect
sysuse nlsw88
describe
* there are 2246 observations and 17 variables; the storage type for wage is float

* 2. summarize continuous variables
summarize wage age ttl_exp

* 3. detailed summary
summarize wage, detail
* 25th percentile:  4.259257; 75th percentile: 9.597424.
* the median is 6.27227 while the mean is 7.766949; this indicates that the wage distribution is left-skewed

* 4. tabulate a categorical variable
tabulate industry
*twoway tabulation
tabulate industry union
* professional services is the industry with the highest number of union members

* 5. conditional summary
summarize wage if union == 1
summarize wage if union == 0
* the raw wage gap is 1.469625 (union workers have an average wage of 8.674294 vs 7.204669 for non-union workers)
* typical confounders include years of education, years of experience, residence city/region, occupation, race, and age.
* for example, it might be that unionised workers are more likely to reside in bigger cities (where wages are higher), 
* and/or they are on average more educated and more experienced (which could explain that they have a higher average wage).
