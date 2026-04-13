# Stata Exercises Project

Daily Stata coding exercises for Francesco's learning series.

## Exercise Numbering

Before creating a new exercise, check the `exercises/` folder to find the highest existing day number and continue from the next one. Do not overwrite or skip numbers.

## Critical Rule: Never Invent Dataset Properties

When writing exercises or feedback, **never assume or fabricate** properties of Stata datasets — including which variables have missing values, their ranges, observation counts, or storage types.

- If the dataset is listed below, consult the reference tables. Do not contradict them. For example, `wage` in `nlsw88` has **no** missing values — never write exercises that assume otherwise.
- If the dataset is NOT listed below, **run Stata in batch mode** to audit it before writing the exercise (see workflow below).

## Dataset Variety

Do not use the same dataset for more than 3 consecutive exercises. Rotate across the datasets listed below, choosing whichever fits the topic best. Both `sysuse` and `webuse` datasets are available.

**Suggested pairings** (not exhaustive):

| Topic                              | Good dataset choices                                    |
|------------------------------------|---------------------------------------------------------|
| Basic inspection, describe, list   | `auto`, `census`, `lbw`, `laborsup`                     |
| Summary statistics, distributions  | `nlsw88`, `nlsy80`, `mroz87`, `auto`, `citytemp`        |
| Missing values, data cleaning      | `nlsy80`, `nlswork`, `womenwk`, `breathe`, `citytemp`   |
| Categorical variables, labels      | `nlsw88`, `auto`, `psidextract`, `cancer`               |
| Generate/replace, variable creation| `nlsw88`, `mroz87`, `census`, `bplong`                  |
| Graphs, visualization              | `lifeexp`, `uslifeexp2`, `citytemp`, `auto`, `nlsy80`   |
| Labor supply, wages                | `mroz87`, `womenwk`, `laborsup`, `nlsw88`               |
| Panel data, longitudinal           | `psidextract`, `grunfeld`, `regsmpl`, `nlswork`         |
| Regression, inference              | `nlsy80`, `401k`, `mroz87`, `nlsw88`                    |
| Count data, health economics       | `docvisits`, `nhanes2`, `lbw`                           |
| Survival analysis                  | `cancer`                                                |
| Sample selection                   | `womenwk`, `mroz87`                                     |

## Batch-Mode Audit for Unlisted Datasets

Before writing any exercise that references specific variable properties of a dataset not documented below, run:

```bash
cat > /tmp/audit.do << 'DOEOF'
* For sysuse datasets:
sysuse DATASETNAME, clear
* For web datasets:
* webuse DATASETNAME, clear
describe
misstable summarize
summarize
DOEOF
cd /tmp && /Applications/StataNow/StataSE.app/Contents/MacOS/stata-se -b do audit.do 2>&1
cat /tmp/audit.log
```

Use the output to ground every claim about variables, missingness, ranges, and types. Never guess.

---

## Dataset Reference: `sysuse` Datasets

### nlsw88 (`sysuse nlsw88`)

NLSW, 1988 extract. **Obs**: 2,246 | **Vars**: 17

**Variables WITH missing values:**

| Variable   | Missing | Observed | Storage | Labels   | Description                   |
|------------|---------|----------|---------|----------|-------------------------------|
| grade      | 2       | 2,244    | byte    |          | Current grade completed       |
| industry   | 14      | 2,232    | byte    | indlbl   | Industry                      |
| occupation | 9       | 2,237    | byte    | occlbl   | Occupation                    |
| union      | 368     | 1,878    | byte    | unionlbl | Union worker                  |
| hours      | 4       | 2,242    | byte    |          | Usual hours worked            |
| tenure     | 15      | 2,231    | float   |          | Job tenure (years)            |

**Variables with NO missing values:**

| Variable      | Obs   | Mean    | Min   | Max      | Storage | Labels   | Description                   |
|---------------|-------|---------|-------|----------|---------|----------|-------------------------------|
| idcode        | 2,246 | 2612.65 | 1     | 5159     | int     |          | NLS ID                        |
| age           | 2,246 | 39.15   | 34    | 46       | byte    |          | Age in current year           |
| race          | 2,246 | 1.28    | 1     | 3        | byte    | racelbl  | Race                          |
| married       | 2,246 | 0.64    | 0     | 1        | byte    | marlbl   | Married                       |
| never_married | 2,246 | 0.10    | 0     | 1        | byte    | nev_mar  | Never married                 |
| collgrad      | 2,246 | 0.24    | 0     | 1        | byte    | gradlbl  | College graduate              |
| south         | 2,246 | 0.42    | 0     | 1        | byte    | southlbl | Lives in the south            |
| smsa          | 2,246 | 0.70    | 0     | 1        | byte    | smsalbl  | Lives in SMSA                 |
| c_city        | 2,246 | 0.29    | 0     | 1        | byte    | ccitylbl | Lives in a central city       |
| wage          | 2,246 | 7.77    | 1.00  | 40.75    | float   |          | Hourly wage                   |
| ttl_exp       | 2,246 | 12.53   | 0.12  | 28.88    | float   |          | Total work experience (years) |

---

### auto (`sysuse auto`)

1978 automobile data. **Obs**: 74 | **Vars**: 12

**Variables WITH missing values:**

| Variable | Missing | Observed | Storage | Labels | Description   |
|----------|---------|----------|---------|--------|---------------|
| rep78    | 5       | 69       | int     |        | Repair record |

**Variables with NO missing values:**

| Variable     | Obs | Mean    | Min  | Max   | Storage | Labels | Description  |
|--------------|-----|---------|------|-------|---------|--------|--------------|
| price        | 74  | 6165.26 | 3291 | 15906 | int     |        | Price        |
| mpg          | 74  | 21.30   | 12   | 41    | int     |        | Mileage (mpg)|
| headroom     | 74  | 2.99    | 1.5  | 5     | float   |        | Headroom (in.)|
| trunk        | 74  | 13.76   | 5    | 23    | int     |        | Trunk space  |
| weight       | 74  | 3019.46 | 1760 | 4840  | int     |        | Weight (lbs.)|
| length       | 74  | 187.93  | 142  | 233   | int     |        | Length (in.) |
| turn         | 74  | 39.65   | 31   | 51    | int     |        | Turn circle  |
| displacement | 74  | 197.30  | 79   | 425   | int     |        | Displacement |
| gear_ratio   | 74  | 3.01    | 2.19 | 3.89  | float   |        | Gear ratio   |
| foreign      | 74  | 0.30    | 0    | 1     | byte    | origin | Car origin   |

Note: `make` is a string variable.

---

### census (`sysuse census`)

1980 Census data by state. **Obs**: 50 | **Vars**: 13 | **No missing values.**

| Variable | Obs | Mean     | Min    | Max      | Storage | Labels | Description         |
|----------|-----|----------|--------|----------|---------|--------|---------------------|
| region   | 50  | 2.66     | 1      | 4        | int     | cenreg | Census region       |
| pop      | 50  | 4518149  | 401851 | 23667902 | long    |        | Population          |
| poplt5   | 50  | 326278   | 35998  | 1708400  | long    |        | Pop, < 5 year       |
| pop5_17  | 50  | 945952   | 91796  | 4680558  | long    |        | Pop, 5–17 years     |
| pop18p   | 50  | 3245920  | 271106 | 17348000 | long    |        | Pop, 18+            |
| pop65p   | 50  | 509503   | 11547  | 2414250  | long    |        | Pop, 65+            |
| popurban | 50  | 3328253  | 172735 | 21607000 | long    |        | Urban population    |
| medage   | 50  | 29.54    | 24.2   | 34.7     | float   |        | Median age          |
| death    | 50  | 39474    | 1604   | 186428   | long    |        | Number of deaths    |
| marriage | 50  | 47701    | 4437   | 210864   | long    |        | Number of marriages |
| divorce  | 50  | 23679    | 2142   | 133541   | long    |        | Number of divorces  |

Note: `state` and `state2` are string variables.

---

### lifeexp (`sysuse lifeexp`)

Life expectancy, 1998. **Obs**: 68 | **Vars**: 6

**Variables WITH missing values:**

| Variable  | Missing | Observed | Storage | Description              |
|-----------|---------|----------|---------|--------------------------|
| gnppc     | 5       | 63       | int     | GNP per capita           |
| safewater | 28      | 40       | byte    | % with safe water        |

**Variables with NO missing values:**

| Variable  | Obs | Mean  | Min  | Max | Storage | Description              |
|-----------|-----|-------|------|-----|---------|--------------------------|
| region    | 68  | 1.50  | 1    | 3   | byte    | Region                   |
| popgrowth | 68  | 0.97  | -0.5 | 3   | float   | Avg. annual pop growth   |
| lexp      | 68  | 72.28 | 54   | 79  | int     | Life expectancy at birth |

Note: `country` is a string variable.

---

## Dataset Reference: `webuse` Datasets

### lbw (`webuse lbw`)

Hosmer & Lemeshow data. **Obs**: 189 | **Vars**: 11 | **No missing values.**

| Variable | Obs | Mean   | Min | Max  | Storage | Description                 |
|----------|-----|--------|-----|------|---------|-----------------------------|
| id       | 189 | 121.08 | 4   | 226  | int     | ID                          |
| low      | 189 | 0.31   | 0   | 1    | byte    | Low birth weight (< 2500g)  |
| age      | 189 | 23.24  | 14  | 45   | byte    | Age of mother               |
| lwt      | 189 | 129.82 | 80  | 250  | int     | Weight at last menstrual pd |
| race     | 189 | 1.85   | 1   | 3    | byte    | Race                        |
| smoke    | 189 | 0.39   | 0   | 1    | byte    | Smoked during pregnancy     |
| ptl      | 189 | 0.20   | 0   | 3    | byte    | Premature labor history     |
| ht       | 189 | 0.06   | 0   | 1    | byte    | Has hypertension            |
| ui       | 189 | 0.15   | 0   | 1    | byte    | Uterine irritability        |
| ftv      | 189 | 0.79   | 0   | 6    | byte    | Physician visits in 1st tri |
| bwt      | 189 | 2944.3 | 709 | 4990 | int     | Birth weight (grams)        |

---

### nhanes2 (`webuse nhanes2`)

NHANES II. **Obs**: 10,351 | **Vars**: 58

**Variables WITH missing values (15 variables):**

| Variable | Missing | Observed | Description            |
|----------|---------|----------|------------------------|
| tgresult | 5,301   | 5,050    | Triglycerides (mg/dL)  |
| hdresult | 1,631   | 8,720    | HDL cholesterol        |
| hlthstat | 2       | 10,349   | Health status          |
| heartatk | 2       | 10,349   | Heart attack           |
| diabetes | 2       | 10,349   | Diabetes               |
| corpuscl | 89      | 10,262   | Red blood cells        |
| albumin  | 335     | 10,016   | Albumin                |
| vitaminc | 378     | 9,973    | Vitamin C              |
| zinc     | 1,149   | 9,202    | Zinc                   |
| copper   | 1,220   | 9,131    | Copper                 |
| porphyrn | 81      | 10,270   | Porphyrin              |
| lead     | 5,403   | 4,948    | Lead (μg/dL)           |
| fhtatk   | 4,917   | 5,434    | Family history, heart  |
| loglead  | 5,403   | 4,948    | Log of lead            |
| highlead | 5,403   | 4,948    | High lead indicator    |

Remaining 43 variables have no missing values (demographics, anthropometrics, blood pressure, etc.).

---

### bplong (`webuse bplong`)

Fictional blood-pressure data. **Obs**: 240 | **Vars**: 5 | **No missing values.**

| Variable | Obs | Mean   | Min | Max | Storage | Description       |
|----------|-----|--------|-----|-----|---------|-------------------|
| patient  | 240 | 60.50  | 1   | 120 | int     | Patient ID        |
| sex      | 240 | 0.50   | 0   | 1   | byte    | Sex               |
| agegrp   | 240 | 2.00   | 1   | 3   | byte    | Age group         |
| when     | 240 | 1.50   | 1   | 2   | byte    | Before/After      |
| bp       | 240 | 153.90 | 125 | 185 | int     | Blood pressure    |

---

### cancer (`webuse cancer`)

Patient survival in drug trial. **Obs**: 48 | **Vars**: 8 | **No missing values.**

| Variable  | Obs | Mean  | Min | Max | Storage | Description           |
|-----------|-----|-------|-----|-----|---------|-----------------------|
| studytime | 48  | 15.50 | 1   | 39  | byte    | Months to event       |
| died      | 48  | 0.65  | 0   | 1   | byte    | Died                  |
| drug      | 48  | 1.88  | 1   | 3   | byte    | Drug type             |
| age       | 48  | 55.88 | 47  | 67  | byte    | Patient age           |

Note: `_st`, `_d`, `_t`, `_t0` are survival-time system variables.

---

### citytemp (`webuse citytemp`)

City temperature data. **Obs**: 956 | **Vars**: 6

**Variables WITH missing values:**

| Variable | Missing | Observed | Storage | Description               |
|----------|---------|----------|---------|---------------------------|
| heatdd   | 3       | 953      | int     | Heating degree days       |
| cooldd   | 3       | 953      | int     | Cooling degree days       |
| tempjan  | 2       | 954      | float   | Average January temp (°F) |
| tempjuly | 2       | 954      | float   | Average July temp (°F)    |

**Variables with NO missing values:**

| Variable | Obs | Mean | Min | Max | Storage | Description    |
|----------|-----|------|-----|-----|---------|----------------|
| division | 956 | 5.14 | 1   | 9   | byte    | Census division|
| region   | 956 | 2.62 | 1   | 4   | byte    | Census region  |

---

### nlswork (`webuse nlswork`)

NLS Young Women panel, 1968–1988. **Obs**: 28,534 | **Vars**: 21

**Variables WITH missing values (14 variables):**

| Variable | Missing | Observed | Description                |
|----------|---------|----------|----------------------------|
| union    | 9,296   | 19,238   | Union member               |
| wks_work | 703     | 27,831   | Weeks worked last year     |
| wks_ue   | 5,704   | 22,830   | Weeks unemployed           |
| tenure   | 433     | 28,101   | Job tenure (years)         |
| ind_code | 341     | 28,193   | Industry code              |
| occ_code | 121     | 28,413   | Occupation code            |
| hours    | 67      | 28,467   | Usual hours worked         |
| age      | 24      | 28,510   | Age in current year        |
| msp      | 16      | 28,518   | Married, spouse present    |
| nev_mar  | 16      | 28,518   | Never married              |
| not_smsa | 8       | 28,526   | Not in SMSA                |
| c_city   | 8       | 28,526   | Central city               |
| south    | 8       | 28,526   | Lives in the south         |
| grade    | 2       | 28,532   | Current grade completed    |

Remaining 7 variables (`idcode`, `year`, `birth_yr`, `race`, `collgrad`, `ttl_exp`, `ln_wage`) have no missing values.

---

### uslifeexp2 (`webuse uslifeexp2`)

US life expectancy, 1900–1940. **Obs**: 41 | **Vars**: 2 | **No missing values.**

| Variable | Obs | Mean  | Min  | Max  | Storage | Description      |
|----------|-----|-------|------|------|---------|------------------|
| year     | 41  | 1920  | 1900 | 1940 | int     | Year             |
| le       | 41  | 55.29 | 39.1 | 63.7 | float   | Life expectancy  |

---

### mroz87 (`webuse mroz87`)

Mroz 1987 PSID — classic female labor supply. **Obs**: 753 | **Vars**: 28 | **No missing values.**

| Variable | Obs | Mean    | Min   | Max    | Storage | Labels | Description                        |
|----------|-----|---------|-------|--------|---------|---------|------------------------------------|
| lfp      | 753 | 0.57    | 0     | 1      | byte    | lfp     | Wife's labor force participation   |
| whrs75   | 753 | 740.58  | 0     | 4950   | int     |         | Wife's hours worked 1975           |
| wifeage  | 753 | 42.54   | 30    | 60     | byte    |         | Wife's age                         |
| wedyrs   | 753 | 12.29   | 5     | 17     | byte    |         | Wife's education (years)           |
| wwage75  | 753 | 2.37    | 0     | 25     | float   |         | Wife's hourly wage 1975            |
| husage   | 753 | 45.12   | 30    | 60     | byte    |         | Husband's age                      |
| hedyrs   | 753 | 12.49   | 3     | 17     | byte    |         | Husband's education (years)        |
| hwage75  | 753 | 7.48    | 0.41  | 40.51  | float   |         | Husband's hourly wage 1975         |
| faminc   | 753 | 23081   | 1500  | 96000  | float   |         | Family income 1975                 |
| kl6      | 753 | 0.24    | 0     | 3      | byte    |         | Kids < 6 years old                 |
| k618     | 753 | 1.35    | 0     | 8      | byte    |         | Kids 6–18 years old                |
| mtr      | 753 | 0.68    | 0.44  | 0.94   | float   |         | Marginal tax rate facing wife      |
| wexper   | 753 | 10.63   | 0     | 45     | byte    |         | Wife's work experience (years)     |
| nwinc    | 753 | 20.13   | -0.03 | 96     | double  |         | Non-wife household income ($1000s) |

Additional variables: taxinc, fedtax, hsib, hfedyrs, hmedyrs, wsib, wwage76, hhrs75, wmedyrs, wfedyrs, unemprt, smsa (labeled), weduc (labeled), wmeduc (labeled).

---

### nlsy80 (`webuse nlsy80`)

NLSY 1980 cross-section. **Obs**: 935 | **Vars**: 20

**Variables WITH missing values:**

| Variable | Missing | Observed | Description         |
|----------|---------|----------|---------------------|
| brthord  | 83      | 852      | Birth order         |
| meduc    | 78      | 857      | Mother's education  |
| feduc    | 194     | 741      | Father's education  |

**Variables with NO missing values:**

| Variable | Obs | Mean   | Min  | Max  | Storage | Description                  |
|----------|-----|--------|------|------|---------|------------------------------|
| wage     | 935 | 957.95 | 115  | 3078 | int     | Monthly earnings             |
| hours    | 935 | 43.93  | 20   | 80   | byte    | Avg weekly hours             |
| iq       | 935 | 101.28 | 50   | 145  | int     | IQ score                     |
| kww      | 935 | 35.74  | 12   | 56   | byte    | Knowledge of world work      |
| educ     | 935 | 13.47  | 9    | 18   | byte    | Years of education           |
| exper    | 935 | 11.56  | 1    | 23   | byte    | Years of work experience     |
| tenure   | 935 | 7.23   | 0    | 22   | byte    | Years with current employer  |
| age      | 935 | 33.08  | 28   | 38   | byte    | Age in years                 |
| married  | 935 | 0.89   | 0    | 1    | byte    | Married                      |
| black    | 935 | 0.13   | 0    | 1    | byte    | Black                        |
| south    | 935 | 0.34   | 0    | 1    | byte    | Lives in south               |
| urban    | 935 | 0.72   | 0    | 1    | byte    | Lives in SMSA                |
| sibs     | 935 | 2.94   | 0    | 14   | byte    | Number of siblings           |
| lwage    | 935 | 6.78   | 4.74 | 8.03 | float   | Log wage                     |
| college  | 935 | 0.26   | 0    | 1    | byte    | Attended college             |

---

### psidextract (`webuse psidextract`)

PSID panel extract. **Obs**: 4,165 | **Vars**: 22 | **No missing values.**

| Variable | Obs   | Mean   | Min  | Max  | Storage | Labels | Description              |
|----------|-------|--------|------|------|---------|--------|--------------------------|
| exp      | 4,165 | 19.85  | 1    | 51   | byte    |        | Years full-time work exp |
| wks      | 4,165 | 46.81  | 5    | 52   | byte    |        | Weeks worked             |
| occ      | 4,165 | 0.51   | 0    | 1    | byte    | occ    | Occupation               |
| ind      | 4,165 | 0.40   | 0    | 1    | byte    | ind    | Industry                 |
| south    | 4,165 | 0.29   | 0    | 1    | byte    | south  | Lives in south           |
| smsa     | 4,165 | 0.65   | 0    | 1    | byte    | smsa   | Lives in SMSA            |
| ms       | 4,165 | 0.81   | 0    | 1    | byte    | ms     | Married                  |
| fem      | 4,165 | 0.11   | 0    | 1    | byte    | fem    | Female                   |
| union    | 4,165 | 0.36   | 0    | 1    | byte    | union  | Union contract           |
| ed       | 4,165 | 12.85  | 4    | 17   | byte    |        | Years of education       |
| blk      | 4,165 | 0.07   | 0    | 1    | byte    | blk    | Black                    |
| lwage    | 4,165 | 6.68   | 4.61 | 8.54 | float   |        | Log wage                 |
| id       | 4,165 | 298    | 1    | 595  | int     |        | Person ID                |
| t        | 4,165 | 4      | 1    | 7    | byte    |        | Time period              |

Panel structure: id x t (7 periods). Also includes time dummies tdum1–tdum7 and exp2.

---

### womenwk (`webuse womenwk`)

Women and work. **Obs**: 2,000 | **Vars**: 6

**Variables WITH missing values:**

| Variable | Missing | Observed | Storage | Description                                  |
|----------|---------|----------|---------|----------------------------------------------|
| wage     | 657     | 1,343    | float   | Hourly wage (missing for non-working women)  |

**Variables with NO missing values:**

| Variable  | Obs   | Mean  | Min | Max | Storage | Description              |
|-----------|-------|-------|-----|-----|---------|--------------------------|
| county    | 2,000 | 4.50  | 0   | 9   | byte    | County of residence      |
| age       | 2,000 | 36.21 | 20  | 59  | byte    | Age in years             |
| education | 2,000 | 13.08 | 10  | 20  | byte    | Years of schooling       |
| married   | 2,000 | 0.67  | 0   | 1   | byte    | Married, spouse present  |
| children  | 2,000 | 1.64  | 0   | 5   | byte    | Children under 12        |

Note: `wage` is missing by design for non-employed women — ideal for sample selection exercises.

---

### 401k (`webuse 401k`)

Firm-level 401(k) participation. **Obs**: 4,075 | **Vars**: 10 | **No missing values.**

| Variable  | Obs   | Mean    | Min   | Max    | Storage | Labels  | Description              |
|-----------|-------|---------|-------|--------|---------|---------|--------------------------|
| partic    | 4,075 | 1525.4  | 100   | 262659 | float   |         | Employees participating  |
| totemp    | 4,075 | 5151.5  | 105   | 443040 | float   |         | Total firm employees     |
| employ    | 4,075 | 2007.2  | 100   | 286451 | float   |         | Eligible employees       |
| mrate     | 4,075 | 0.46    | 0     | 2      | float   |         | Plan match rate per $    |
| prate     | 4,075 | 0.84    | 0.004 | 1      | float   |         | Participation rate       |
| age       | 4,075 | 8.19    | 1     | 71     | byte    |         | Plan age (years)         |
| sole      | 4,075 | 0.37    | 0     | 1      | byte    | forsole | Only pension plan        |
| ltotemp   | 4,075 | 6.97    | 4.65  | 13.0   | float   |         | Log total employees      |

Also includes agesq and ltotempsq.

---

### docvisits (`webuse docvisits`)

Doctor visits. **Obs**: 4,412 | **Vars**: 10 | **No missing values.**

| Variable | Obs   | Mean  | Min | Max | Storage | Description             |
|----------|-------|-------|-----|-----|---------|-------------------------|
| docvis   | 4,412 | 3.96  | 0   | 134 | int     | Number of doctor visits |
| age      | 4,412 | 4.08  | 2.5 | 6.4 | float   | Age (in decades)        |
| income   | 4,412 | 34.34 | -50 | 281 | float   | Income ($1000s)         |
| female   | 4,412 | 0.47  | 0   | 1   | byte    | Female                  |
| black    | 4,412 | 0.05  | 0   | 1   | byte    | Black                   |
| hispanic | 4,412 | 0.25  | 0   | 1   | byte    | Hispanic                |
| married  | 4,412 | 0.64  | 0   | 1   | byte    | Married                 |
| physlim  | 4,412 | 0.17  | 0   | 1   | byte    | Physical limitation     |
| private  | 4,412 | 0.79  | 0   | 1   | byte    | Private insurance       |
| chronic  | 4,412 | 0.33  | 0   | 1   | byte    | Chronic condition       |
