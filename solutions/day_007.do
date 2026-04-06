**********************************
* Exercise 7: Diagnosing Data Quality — Missingness, Impossible Values, and Variable Types
**********************************

* 1. identify missing values across all variables
sysuse nlsw88, clear
describe
misstable summarize, all
* I explore other uses of "misstable"
misstable tree
misstable patterns
* share of observations missing for wage: 0%

* 2. locate impossible values
summarize hours // min: 1; max: 80
summarize ttl_exp // min: 0.11; max: 28.88
* ttl_exp measures the total work experience in years; hours measures the usual hours per week worked.
* hours less than 15 and more than 40 are suspicious; ttl_exp lower than 5 is suspicious too,
* given that the dataset contains data on women aged 34 to 46.
list in 1/10 if hours < 15 | hours > 40
list in 1/10 if ttl_exp < 5
summarize age

* 3. examine a labelled categorical variable's underlying codes
tabulate race
numlabel _all, add
tabulate race
summarize race // mean: 1.28, which is informative about the relative 
* frequency of each race (white, black, or other). Since 1.28 < 2, 
* clearly the majority of the sample is white.

* 4. cross-check missingness against a grouping variable
tabulate south
tabulate south, missing
* the two outputs are identical because south has no missing values.

gen flag_miss = missing(union)
tabstat wage, by(flag_miss) stat(mean n)
* mean for non-missing union: 7.6
* mean for missing union: 8.8
* given the difference in more than 1 dollar, it appears that missingness in union
* is not random with respect to wages

* 5. flag and count problematic observations
gen flag_problem = missing(wage) | hours>168
tabulate flag_problem // only four observations are flagged
br flag_problem hours wage
* the problem is that wage is never missing, and hours never exceed 80
* so, the 4 observations flagged have wage non missing and hours missing. 
* in fact, Stata stored missing values as very high values.
* I would not drop these rows.
