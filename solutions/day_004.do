**********************************
* Exercise 4: Exploring Labor Market Variables - Describe, Summarize, and Tabulate
**********************************

* 1. load and inspect
sysuse nlsw88
describe
tabulate industry
tabulate occupation
tabulate industry occupation
* occupation and industry are both byte but are stored as labeled numeric. 
* occupation is more about the type of job performed (eg transport vs services),
* whereas industry describes the broader sector any given job belongs to. Each sector can capture jobs 
* associated to different occupations, and each occupation can include jobs spanning across various sectors.

* 2. summarize a continuous variable
summarize hours
* mean: 37.21811; SD: 10.50914; min: 1; max: 80
* the minimum value seems implausible; perhaps it is due to errors in recording survey responses

* 3. detailed distribution of hours
summarize hours, detail
* the median in 40; the mean is 37.21811; since the median > mean, the distribution of hours is left-skewed.
* This suggests that there is a significant portion of part-time workers in the sample (ie individuals working for only a few hours per week)

* 4. tabulate a categorial variable, then compared groups
tabulate race
summarize wage if race == 1 // white
summarize wage if race == 2 // black
summarize wage
* white people earn, on average, a higher wage compared to black people (8.082999 vs 6.844558).
* relative to the overall mean wage, white people earn, on average, 0.3 dollars more, whereas black people earn 1 dollar less.

* 5. occupation frequency and wage dispersion
tabulate occupation, sort 
* the three most common occupations are  Sales, Professional/Technical, and Laborers 
tab occupation, sort nolabel // to visualise the number corresponding to each occupation

summarize wage if occupation == 3, detail // Sales; median: 6.046698; IQR: 3.518515
summarize wage if occupation == 1, detail // Professional/Technical; median: 9.677936; IQR: 5.161032
summarize wage if occupation == 8, detail // Laborers; median:4.064628; IQR: 2.238325
* professional/technical occupation shows the greatest wage dispersion, perhaps because the wage
* for this profession depends on the specific degree of specialisation, which can vary greatly across technical occupations
