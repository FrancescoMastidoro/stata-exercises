**********************************
* Exercise 9: Detecting and Handling Data Quality Problems
**********************************

* The `nlsy80` dataset contains cross-sectional data from the 1980 
* National Longitudinal Survey of Youth, covering wages, education, 
* cognitive scores, family background, and demographic characteristics for 935 individuals

* 1. Audit missingness across the dataset
webuse nlsy80, clear
describe // 935 observations; 20 variables
misstable summarize

* variables that contain missing values and exact missing counts per each:
* brthord: 83
* meduc: 78
* feduc: 194
count if feduc == .
display r(N)/_N*100 // ~21%

* 2. Examine the distribution of a key continuous variable
summarize wage, detail
* min: 115; max: 3078; mean: ~958; median: 905
* the mean is higher than the median, implying that the distribution of earnings
* is skewed to the right
* to see that graphically:
histogram wage

* 3. Flag missing background variables and examine their correlates
gen missing_feduc = missing(feduc)
tabulate missing_feduc

/*
missing_fed |
         uc |      Freq.     Percent        Cum.
------------+-----------------------------------
          0 |        741       79.25       79.25
          1 |        194       20.75      100.00
------------+-----------------------------------
      Total |        935      100.00
*/
* yes, the count matches the reference figure in #1

bysort missing_feduc: summarize educ
*equivalently:
tabstat educ, by(missing_feduc) stat(count mean median sd min max)

* respondents with missing father's education tend to have lower education
* than those with non-missing father's education (mean is 12.91 vs 13.61)

* 4. Detect potentially implausible values in hours and IQ
summarize hours, detail
summarize iq, detail

count if hours > 60
count if iq<50 | iq>145

* hours: there are 22 observations with hours > 60, with the maximum value being 80. 
* These values are implausible as the variable "hours" describes the average weekly hours of work.
* Therefore, this warrants further investigation.
* The minimum value for "hours" is 20, which is perfectly consistent with part-time jobs.

* iq: there are no observations with iq falling outside of its normal range [50,145].
* The distribution of iq values within this range is realistic,
* with most respondents (80%) having IQ values between 82 and 120,
* and half respondents having IQ values between 92 and 112 (interquartile range).

* 5. Cross-tabulate missingness patterns
gen missing_meduc = missing(meduc)
tabulate missing_feduc missing_meduc
misstable patterns feduc meduc

/*

. tabulate missing_feduc missing_meducs

missing_fe |     missing_meduc
       duc |         0          1 |     Total
-----------+----------------------+----------
         0 |       722         19 |       741 
         1 |       135         59 |       194 
-----------+----------------------+----------
     Total |       857         78 |       935 

*/

* Joint missingness concerns 59 observations in total.
* IF missingness for these variables were independent, I would expect to have
* N observations with joint missingness, where:
* N = P(both feduc and meduc missing) = P(meduc M) * P(feduc M) = 78/935 * 194/935 = .01730905, 
* or 1.730905% of all 935 observations, which corresponds to ~16.2 observations.
* But we observe 59 observations with joint missingness, which is roughly 3.7x 16.2, 
* ie 3.7x the number of observations with both variables missing that we would observe under independence.
* So clearly missingness tends to co-occur with respect to these two variables.

* Note: the same finding would be reached by focusing on joint non-missingness.

summarize lwage if missing(meduc) & missing(feduc) // mean: 6.57
summarize lwage if missing(meduc) & !missing(feduc) // mean: 6.78
summarize lwage if !missing(meduc) & missing(feduc) // mean: 6.75
summarize lwage if !missing(meduc) & !missing(feduc) // mean: 6.80

* the log of wage is systematically lower when both meduc and feduc are missing.
