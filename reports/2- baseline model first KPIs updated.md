# Baseline model and first KPIs

## 1. Objective and modeling setup

The goal of the modeling phase is to build a binary classifier capable of distinguishing **Top-tier** universities from the rest using performance indicators from the Times, Shanghai, and CWUR rankings. The target variable `top_tier` is defined as `Yes` for institutions with average world rank less than or equal to 100 and `No` otherwise.

The preprocessing pipeline produced 555 observations. The data were split into training and test sets using a stratified partition. Two initial models were evaluated:

- a dummy majority-class baseline;
- a Logistic Regression model using the full set of numeric predictors.

The dummy classifier provides a minimum reference, while Logistic Regression represents the first genuine predictive model.

## 2. Feature set and target

### Selected predictors

The final modeling table used **26 numeric predictors**. They were selected from the Times, Shanghai, and CWUR indicators, together with the year and the two numeric components derived from the female/male ratio.

#### Times

- `times_teaching`
- `times_international`
- `times_research`
- `times_citations`
- `times_income`
- `times_student_staff_ratio`
- `times_num_students`
- `times_international_students`
- `times_female_value`
- `times_male_value`

#### Shanghai

- `shang_alumni`
- `shang_award`
- `shang_hici`
- `shang_ns`
- `shang_pub`
- `shang_pcp`

#### CWUR

- `cwur_quality_of_education`
- `cwur_alumni_employment`
- `cwur_quality_of_faculty`
- `cwur_publications`
- `cwur_influence`
- `cwur_citations`
- `cwur_broad_impact`
- `cwur_patents`
- `cwur_score`

#### Additional predictor

- `year`

The final KNIME workflow uses 26 numeric predictors. The Times feature set includes both `times_international`, a ranking indicator, and `times_international_students`, which represents the percentage of international students. These are distinct variables. The earlier version of the report referred to 24 predictors and to a derived `times_female_percentage` feature; the final workflow instead uses the two effective columns `times_female_value` and `times_male_value`.

### Excluded columns

To prevent data leakage and maintain a coherent feature space, the following variables were excluded:

- `university_name`;
- `times_world_rank`;
- `shang_world_rank`;
- `cwur_world_rank`;
- `average_world_rank`;
- `shang_national_rank`;
- `cwur_national_rank`.

The target column `top_tier` was retained in the table but used exclusively as the response variable.

> “The modeling feature set consisted of 26 numeric predictors from the Times, Shanghai, and CWUR ranking systems, together with `year`, `times_female_value`, and `times_male_value`. Identifiers, world-ranking variables, and excluded national ranks were removed to prevent data leakage, because the target was constructed from the ranking variables.”

## 3. Train/test split

The final preprocessed table was partitioned using the KNIME `Partitioning` node:

- training proportion: 70%;
- test proportion: 30%;
- sampling mode: stratified;
- stratification column: `top_tier`;
- random seed: 42.

The stratified split preserves similar class proportions in the training and test sets and allows the same test set to be reused for subsequent model comparison.

## 4. Dummy baseline

Because KNIME did not provide a dedicated dummy classifier node in the workflow, the baseline was implemented by assigning every test observation to the majority class identified in the training data.

The majority class was identified using:

1. `GroupBy` on `top_tier`;
2. `Sorter` to order the class frequencies;
3. `Row Filter` to retain the most frequent class;
4. `Rule Engine` to create a constant prediction on the test set.

The majority class was `No`.

### Performance

The dummy classifier achieved:

- accuracy: 0.611;
- Cohen’s kappa: 0.000;
- precision for `Yes`: 0.000;
- recall for `Yes`: 0.000;
- F1-score for `Yes`: 0.000.

Its confusion matrix was:

|  | Predicted No | Predicted Yes |
|---|---:|---:|
| Actual No | 102 | 0 |
| Actual Yes | 65 | 0 |

The dummy classifier correctly classified the majority class but failed to detect any Top-tier university. It therefore provides a useful minimum reference but is not a meaningful predictive model.

## 5. Logistic Regression

### Configuration

The Logistic Regression model was trained using the KNIME `Logistic Regression Learner` node and evaluated using the corresponding Predictor and `Scorer` nodes.

The model used:

- target column: `top_tier`;
- reference category: `No`;
- 26 numeric predictors;
- intercept term enabled;
- default learner settings;
- no additional normalization in the baseline branch.

The model was applied to the held-out test set using the Logistic Regression Predictor.

### Performance

The test-set confusion matrix was:

|  | Predicted Yes | Predicted No |
|---|---:|---:|
| Actual Yes | 64 | 1 |
| Actual No | 2 | 100 |

The model achieved:

- accuracy: 0.982;
- Cohen’s kappa: 0.962;
- precision for `Yes`: 0.970;
- recall for `Yes`: 0.985;
- F1-score for `Yes`: 0.977.

The model correctly identified 64 Top-tier universities and missed one. It produced two false positives among the non–Top-tier universities.

> “The Logistic Regression model achieved an accuracy of 0.982 and a Cohen’s kappa of 0.962 on the held-out test set. For the positive class `Yes`, precision was 0.970, recall was 0.985, and the F1-score was 0.977. The model therefore detected almost all Top-tier universities while producing only two false positives.”

## 6. Comparison with the dummy baseline

| Model | Predictors | Accuracy | Precision Yes | Recall Yes | F1 Yes | Cohen’s kappa |
|---|---:|---:|---:|---:|---:|---:|
| Dummy majority baseline | — | 0.611 | 0.000 | 0.000 | 0.000 | 0.000 |
| Logistic Regression | 26 | 0.982 | 0.970 | 0.985 | 0.977 | 0.962 |

Logistic Regression substantially improves over the dummy baseline, especially in the detection of the positive Top-tier class.

## 7. Methodological note

The very high Logistic Regression performance must be interpreted in light of the target construction. `top_tier` is defined by thresholding the average of the three world-ranking variables, while the predictors are other indicators from the same ranking systems. The model is therefore solving a task that is intrinsically aligned with the available predictors.

The results demonstrate strong reconstruction of the defined Top-tier threshold. They should not automatically be interpreted as evidence of independent prediction of a future or external measure of university quality.

The coefficient-level interpretation is addressed in the subsequent model-comparison report. The current baseline result concerns predictive performance and uses the full 26-feature modeling table.
