# Stata Exercises Project

Daily Stata coding exercises for Francesco's learning series.

## Critical Rule: Never Invent Dataset Properties

When writing exercises or feedback, **never assume or fabricate** properties of Stata datasets — including which variables have missing values, their ranges, observation counts, or storage types.

### If the dataset is listed below

Consult the reference tables. Do not contradict them. For example, `wage` in `nlsw88` has **no** missing values — never write exercises that assume otherwise.

### If the dataset is NOT listed below

Before writing any exercise that references specific variable properties, **run Stata in batch mode** to audit the dataset:

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

## Dataset Reference

### nlsw88 (`sysuse nlsw88`)

**Observations**: 2,246 | **Variables**: 17

#### Variables WITH missing values

| Variable   | Missing | Observed | Storage | Value label | Description                   |
|------------|---------|----------|---------|-------------|-------------------------------|
| grade      | 2       | 2,244    | byte    |             | Current grade completed       |
| industry   | 14      | 2,232    | byte    | indlbl      | Industry                      |
| occupation | 9       | 2,237    | byte    | occlbl      | Occupation                    |
| union      | 368     | 1,878    | byte    | unionlbl    | Union worker                  |
| hours      | 4       | 2,242    | byte    |             | Usual hours worked            |
| tenure     | 15      | 2,231    | float   |             | Job tenure (years)            |

#### Variables with NO missing values

| Variable      | Obs   | Mean    | Min   | Max      | Storage | Value label | Description                   |
|---------------|-------|---------|-------|----------|---------|-------------|-------------------------------|
| idcode        | 2,246 | 2612.65 | 1     | 5159     | int     |             | NLS ID                        |
| age           | 2,246 | 39.15   | 34    | 46       | byte    |             | Age in current year           |
| race          | 2,246 | 1.28    | 1     | 3        | byte    | racelbl     | Race                          |
| married       | 2,246 | 0.64    | 0     | 1        | byte    | marlbl      | Married                       |
| never_married | 2,246 | 0.10    | 0     | 1        | byte    | nev_mar     | Never married                 |
| collgrad      | 2,246 | 0.24    | 0     | 1        | byte    | gradlbl     | College graduate              |
| south         | 2,246 | 0.42    | 0     | 1        | byte    | southlbl    | Lives in the south            |
| smsa          | 2,246 | 0.70    | 0     | 1        | byte    | smsalbl     | Lives in SMSA                 |
| c_city        | 2,246 | 0.29    | 0     | 1        | byte    | ccitylbl    | Lives in a central city       |
| wage          | 2,246 | 7.77    | 1.00  | 40.75    | float   |             | Hourly wage                   |
| ttl_exp       | 2,246 | 12.53   | 0.12  | 28.88    | float   |             | Total work experience (years) |

---

### auto (`sysuse auto`)

**Observations**: 74 | **Variables**: 12

#### Variables WITH missing values

| Variable | Missing | Observed | Storage | Value label | Description      |
|----------|---------|----------|---------|-------------|------------------|
| rep78    | 5       | 69       | int     |             | Repair record    |

#### Variables with NO missing values

| Variable     | Obs | Mean    | Min  | Max   | Storage | Value label | Description      |
|--------------|-----|---------|------|-------|---------|-------------|------------------|
| price        | 74  | 6165.26 | 3291 | 15906 | int     |             | Price            |
| mpg          | 74  | 21.30   | 12   | 41    | int     |             | Mileage (mpg)    |
| headroom     | 74  | 2.99    | 1.5  | 5     | float   |             | Headroom (in.)   |
| trunk        | 74  | 13.76   | 5    | 23    | int     |             | Trunk space      |
| weight       | 74  | 3019.46 | 1760 | 4840  | int     |             | Weight (lbs.)    |
| length       | 74  | 187.93  | 142  | 233   | int     |             | Length (in.)     |
| turn         | 74  | 39.65   | 31   | 51    | int     |             | Turn circle      |
| displacement | 74  | 197.30  | 79   | 425   | int     |             | Displacement     |
| gear_ratio   | 74  | 3.01    | 2.19 | 3.89  | float   |             | Gear ratio       |
| foreign      | 74  | 0.30    | 0    | 1     | byte    | origin      | Car origin       |

Note: `make` is a string variable (no summary statistics).

---

### census (`sysuse census`)

**Observations**: 50 | **Variables**: 13 | **No missing values** in any variable.

| Variable | Obs | Mean       | Min    | Max        | Storage | Value label | Description          |
|----------|-----|------------|--------|------------|---------|-------------|----------------------|
| region   | 50  | 2.66       | 1      | 4          | int     | cenreg      | Census region        |
| pop      | 50  | 4518149    | 401851 | 23667902   | long    |             | Population           |
| poplt5   | 50  | 326278     | 35998  | 1708400    | long    |             | Pop, < 5 year        |
| pop5_17  | 50  | 945952     | 91796  | 4680558    | long    |             | Pop, 5–17 years      |
| pop18p   | 50  | 3245920    | 271106 | 17348000   | long    |             | Pop, 18+             |
| pop65p   | 50  | 509503     | 11547  | 2414250    | long    |             | Pop, 65+             |
| popurban | 50  | 3328253    | 172735 | 21607000   | long    |             | Urban population     |
| medage   | 50  | 29.54      | 24.2   | 34.7       | float   |             | Median age           |
| death    | 50  | 39474      | 1604   | 186428     | long    |             | Number of deaths     |
| marriage | 50  | 47701      | 4437   | 210864     | long    |             | Number of marriages  |
| divorce  | 50  | 23679      | 2142   | 133541     | long    |             | Number of divorces   |

Note: `state` and `state2` are string variables (no summary statistics).

---

### lifeexp (`sysuse lifeexp`)

**Observations**: 68 | **Variables**: 6

#### Variables WITH missing values

| Variable  | Missing | Observed | Storage | Value label | Description             |
|-----------|---------|----------|---------|-------------|-------------------------|
| gnppc     | 5       | 63       | int     |             | GNP per capita          |
| safewater | 28      | 40       | byte    |             | % with safe water       |

#### Variables with NO missing values

| Variable  | Obs | Mean  | Min  | Max | Storage | Value label | Description             |
|-----------|-----|-------|------|-----|---------|-------------|-------------------------|
| region    | 68  | 1.50  | 1    | 3   | byte    |             | Region                  |
| popgrowth | 68  | 0.97  | -0.5 | 3   | float   |             | Avg. annual pop growth  |
| lexp      | 68  | 72.28 | 54   | 79  | int     |             | Life expectancy at birth|

Note: `country` is a string variable (no summary statistics).
