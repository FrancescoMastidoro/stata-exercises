**********************************
* Exercise 8: Missing Values, Impossible Values, and Data Types
**********************************

* 1. load and audit missingness:
sysuse nlsw88, clear
misstable summarize
* six variables contain missing values
* the variable "union" has the highest number of missing observations (368)

* 2. count missing manually:
count if missing(wage) // 0 observations
count if !missing(wage) //  2,246 observations
describe
display as text "total number of observations: " r(N)
* yes, they add up

* 3. flag and examine missing wage observations:
gen missing_wage = missing(wage)
tabulate missing_wage // the count matches
bysort missing_wage: summarize hours
* there are no observations with a missing value for wage,
* so the question cannot be answered.

* 4. detect impossible values:
summarize hours, detail
* minimum: 1; maximum: 80
count if hours > 80 & !missing(hours) // 0
count if hours == 0 | hours < 0 // 0

* 5. data types and labelled variables:
describe
* byte: race; married; never_married, grade, collgrad, south, smsa, c_city, industry
* occupation, union 
* float: wage; ttl_exp; tenure; flag_miss; flag_problem; missing_wage
* int: idcode
* string: none

* the variable race has value labels attached
tabulate race // labels are "white", "black", and "others"
numlabel, add
tabulate race 
* now I can see a number attached to each label;
* this is useful when performing any operation involving the variable race;
* because for any operation (for example, "if") I need to use numeric codes
* and not value labels
