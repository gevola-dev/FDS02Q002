# Initial preprocessing report

## 1. Objective and dataset

The project uses the **World University Rankings** dataset to build a binary classification model that distinguishes **Top-tier** universities from the others. An institution is classified as Top-tier when its average world rank is less than or equal to 100.

The following files were used:

- `timesData.csv`;
- `shanghaiData.csv`;
- `cwurData.csv`;
- `school_and_country_table.csv`, available for optional enrichment with country information.

The research questions concern the metrics that distinguish Top-tier universities, the predictive value of the ranking indicators, and the comparison between linear and non-linear classification models.

## 2. File ingestion

Separate `CSV Reader` nodes were used for the source files. Technical index columns such as `row_id` were excluded because they do not represent university characteristics and could be incorrectly interpreted as informative predictors.

## 3. Cleaning and normalization

The integration key was:

```text
university_name + year
```

University names were normalized conservatively using:

```text
strip(lowerCase($university_name$))
```

This transformation converts names to lowercase and removes leading and trailing spaces while preserving semantic terms such as `university` and `institute`.

## 4. Column selection and renaming

Redundant geographic columns such as `country` and `region` were removed from the Times and CWUR datasets before integration.

Source-specific prefixes were applied to preserve data lineage and avoid name collisions:

- `times_`;
- `shang_`;
- `cwur_`.

The join keys `university_name` and `year` were excluded from the prefixing operation.

## 5. Dataset integration

The three ranking datasets were integrated through inner joins:

```text
timesData
    INNER JOIN shanghaiData
    INNER JOIN cwurData
```

The join keys were `university_name` and `year`. The resulting integrated table contains 555 observations representing universities present in all three ranking sources for the same year.

An inner join was preferred to a full outer join because it produces a more compact table with fewer missing values and ensures that each observation contains information from all three ranking systems.

The country table was loaded but was not used in the final modeling table. Any enrichment using country would require a separate verification of key uniqueness.

## 6. Ranking conversion

Times and Shanghai world-ranking values were originally stored as strings and sometimes represented intervals such as:

```text
100-210
```

The lower bound was extracted using a `String Manipulation` node, for example:

```text
regexReplace($times_world_rank$, "-.*", "")
```

The resulting values were converted to numeric format using `String to Number`. The CWUR world rank was treated as a numeric variable.

## 7. Average ranking and target creation

The variable `average_world_rank` was computed as:

```text
round(
    ($times_world_rank$ +
     $shang_world_rank$ +
     $cwur_world_rank$) / 3,
    3
)
```

The binary target was created with a `Rule Engine` node:

```text
$average_world_rank$ <= 100 => "Yes"
TRUE => "No"
```

Thus, universities with an average rank less than or equal to 100 were assigned `Yes`; all other universities were assigned `No`.

## 8. Missing-value analysis

The following missing values were identified among the 555 observations:

| Column | Missing | Percentage |
|---|---:|---:|
| `times_income` | 38 | 6.85% |
| `times_total_score` | 198 | 35.68% |
| `times_student_staff_ratio` | 8 | 1.44% |
| `shang_total_score` | 337 | 60.72% |
| `shang_ns` | 1 | 0.18% |
| `cwur_broad_impact` | 105 | 18.92% |
| `times_international_students` | 10 | 1.80% |
| `times_num_students` | 10 | 1.80% |
| `times_female_male_ratio` | approximately 40 | approximately 7.21% |

The missing values in `times_total_score` and `shang_total_score` were structurally related to records where the corresponding ranking was published as an interval. These were therefore treated as structural missing values rather than missing-at-random observations.

The following columns were removed using `Column Filter`:

```text
times_total_score
shang_total_score
shang_national_rank
```

The first two columns were removed because of their high proportion of structural missing values. `shang_national_rank` was removed because it is source-specific and not necessary for the homogeneous feature schema.

## 9. Text-to-numeric transformations

### International students

The percent sign was removed from values such as `43%` using:

```text
regexReplace($times_international_students$, "%", "")
```

The resulting column was converted to numeric format.

### Number of students

The `times_num_students` column was converted to `Double` using the comma as decimal separator when required.

### Female/male ratio

The original `times_female_male_ratio` string, for example:

```text
13 : 87
```

was split into two numeric predictors:

```text
times_female_value = 13
times_male_value = 87
```

These are the effective feature names used by the current KNIME modeling workflow. The previous report referred to a derived `times_female_percentage` variable, but that name does not describe the final table used by the learners.

## 10. Missing-value imputation

After removing structurally incomplete columns and converting text-based variables, residual numeric missing values were imputed with the median using the `Missing Value` node.

The imputed variables included:

```text
times_income
times_student_staff_ratio
shang_ns
cwur_broad_impact
times_international_students
times_num_students
times_female_value
times_male_value
```

Median imputation was selected because it is less sensitive to outliers than mean imputation. The target variable was not imputed.

## 11. Final preprocessing workflow

```text
CSV Reader
    ↓
String Manipulation
    ↓
Column Filter
    ↓
Column Rename (Regex)
    ↓
Inner Join
    ↓
String Manipulation for ranking values
    ↓
String to Number
    ↓
Math Formula
    ↓
Rule Engine
    ↓
Column Filter
    ↓
String Manipulation for text-based features
    ↓
String to Number
    ↓
Missing Value
    ↓
Statistics for validation
```

The final preprocessed dataset contains 555 observations with missing values handled according to the decisions described above.

## 12. Modeling preparation and leakage control

Before modeling, the following checks were required:

1. verify that the final table contains no unresolved missing values;
2. inspect the distribution of `top_tier` classes;
3. define the final predictor set;
4. exclude variables that cause data leakage;
5. perform a stratified train/test split;
6. apply any learned statistical transformations consistently to training and test data.

The following variables were excluded from the predictors because they directly define the target or are derived from those rankings:

```text
times_world_rank
shang_world_rank
cwur_world_rank
average_world_rank
```

Using them as predictors would produce data leakage and artificially inflated performance estimates.

The final modeling workflow used 26 numeric predictors, including `times_international`, `times_female_value`, and `times_male_value`. The `times_international` variable is distinct from `times_international_students`: the first is a Times ranking indicator, while the second represents the percentage of international students. The two gender-ratio components replace the earlier report's incorrect reference to `times_female_percentage`.
