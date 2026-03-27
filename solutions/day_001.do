**********************************
* Exercise 1: Loading Data and First Exploration
**********************************

* 1. import the auto dataset
sysuse auto

* display the first 10 observations
list in 1/10

* 2. inspect the variables
describe
* the dataset has 74 observations and 12 variables

* 3. summarize continuous variables
summarize price mpg weight
* price has the highest coefficient of variation

* 4. tabulate a categorical value
tabulate foreign

* 5. conditional summary
by foreign: sum price mpg
* foreign cars are on average more expensive
