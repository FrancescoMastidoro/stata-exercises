**********************************
* Exercise 6: Diagnosing Data Quality — Missingness, Impossible Values, and Variable Types
**********************************

* 1. audit the variable types
sysuse nlsw88, clear
describe

* variables stored as strings: none
* variables stored as numeric without value labels: idcode, age, grade, wage, hours, ttl_exp, tenure
* variables stored as numeric with value labels: race, married, never_married, collgrad, south, smsa, c_city, industry, occupation, union

* list of all value labels:
label list

* when I use an "if" condition with a variable,
* I always need to filter using the integer code (eg "if race == 2") and not the label strings

* 2. count and locate missing values
misstable summarize
* variable with highest number of missing observations: "union"
codebook union
count if missing(union)
di r(N)/_N*100
* 368 observations are missing for the variable "union". They represent 16.38% of all observations. Some women might be unwilling to share information on whether they are unionised or not, perhaps fearing judgement or negative consequences at work.

* 3. flag and examine missing observations
gen flag_miss = missing(union)
tabulate flag_miss
summarize wage if flag_miss == 1 // mean= 8.795387 
summarize wage if flag_miss == 0 // mean= 7.565423
* missingness for "union" seems to be related to the wage level. Women whose union status is not reported have, on average, a higher hourly wage (by around 1.20$) than women whose union status is provided.

* 4. check for impossible or suspicious values
summarize hours, detail
* minimum: 1; maximum: 80; 1st percentile: 5 (1% of workers work for exactly or less than 5 hours a week); 99th percentile: 60 (1% of workers work for exactly or more than 60 hours a week)
* weekly hours below 5 or above 40 look suspicious: exclude if hours < 5 | hours >40 

summarize wage, detail
* minimum: 1.01; maximum: 40.75; 1st percentile: 1.93; 99th percentile: 38.71
* hourly wages below 2$ and above 30$ look suspicious given 1988 wages.
* useful potential additional info: tabstat wage, by(occupation) stat(mean max min)
* exclude if wage < 2 | wage > 30

* 5. cross-tabulate missingness with a categorical variable
* two-way tabulation
tabulate occupation flag_miss, row
* missing rate for union in general (from point 2): 16.38%
* occupations where the missing rate is higher than 16.38%:
* clerical/Unskilled; Transport; Laborers; Farm laborers; Service; Household workers
* So, an occupational wage analysis should take account of the fact that, for some occupation, missingness for the union status is higher. So, for those occupations, analyses by status could be biased upward or downward.
