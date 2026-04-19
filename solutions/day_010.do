**********************************
* Exercise 10: Diagnosing Data Quality - Missing Values, Impossible Values, and Variable Types
**********************************

* 1. Audit variable types and structure
sysuse auto, clear
* The `auto` dataset contains information on 74 automobiles from 1978, 
* including price, fuel efficiency, and repair records
describe // 74 observations; 12 variables

* strings:
* make: stores car producer (eg mercedes) followed by the car model
codebook make
* the variable takes 74 unique values
* string variables can create problems for numeric analysis
* as there could be slight inconsistencies (for example variations in the
* position of embedded blanks) across entries that are meant to indicate the 
* same thing (in this case, the same care producer and model).
* Thus, these variables require careful auditing before being used
* in data analysis.

* labeled nummeric types:
* foreign: stores the origin of the car (foreign or domestic)
codebook foreign

* 2. Find an count missing values
misstable summarize
* only the variable rep78 (repair record in 1978, taking values between 1 and 5)
* has missing values, for 5 observations
codebook rep78
count if missing(rep78) // verified: 5 observations with missing rep78
* if the repair record is missing, this might indicate that that
* car was repaired multiple times and was perhaps faulty, 
* and hence data on repair record was left intentionally missing. 

* 3. Inspect the distribution of the variable with missing values
summarize rep78, detail
codebook rep78
* mean: 3.405797; median: 3; min: 1; max: 5; N: 69
di _N - r(N) // 5 observations were excluded from the summary due to missingness
histogram rep78
* the distribution appears roughly symmetric. 
* the mean exceeds the median by ~4 decimal points, suggesting
* that the distribution is slightly skewed to the right.

* rep78 takes values between 1 and 5 (included). It reports the number 
* of repairs recorded in 1978.

* 4. Check for implausible values in a continuous variable
summarize mpg // mpg captures mileage, ie miles per gallon
codebook mpg
* min: 12; max: 41
tabulate mpg
count if mpg < 15
* 8 observations have mpg < 15; 6 have mpg equal to 14 and 2 have mpg equal to 12.
* These values look reasonable as they are rather close to the rest of the distribution of mpg.
* Moreover, I check that, for these observations, other car attributes, 
* particularly weight and length, are consistent with mpg being low (ie cars being very inefficient):
codebook length weight
sort mpg
list mpg weight length rep78 make price if mpg < 15
* for these observations, both weight and length are high, as expected. 
* This suggests that values of mpg < 15 are genuine outliers, rather than data entries. 

count if mpg > 35 // 1
* only 1 observation has mpg > 35, having mpg equal to 41. 
* This value falls rather far from the rest of the distribution (the closest value is 35).
* However, it is likely to be a genuine outlier rather than a data entry, since
* both weight and length are very low for this observation, consistently with
* the car being genuinely very efficient (high mpg):
list mpg weight length rep78 make price if mpg > 35 // weight: 2040 (2nd decile); length: 155 (1st decile)

* 5. Compare distributions across a labeled group
tabulate foreign
tabulate foreign, nolabel
* categories:
* foreign (numeric code: 1)
* domestic (numeric code: 0)

summarize rep78 if foreign == 0 // domestic
summarize rep78 if foreign == 1 //foreign
* missing values for rep78 are handled automatically
* domestic: N: 48; mean: 3.020833
* foreign: N: 21; mean: 4.285714
* the mean value for rep78 is larger for foreign cars,
* suggesting that foreign cars on average are repaired more often
tab foreign if missing(rep78) // 4 observations out of 5 are domestic.
* Therefore, missingness of rep78 seems to be concentrated in the group of 
* domestic cars. Therefore, the mean of rep78 for domestic cars
* might be higher than it seems (hence the difference between foreign and
* domestic cars smaller than it seems), assuming that observations with missing rep78
* have missing values for rep78 precisely because they were repaired multiple times
* (ie they have high values of rep78).


