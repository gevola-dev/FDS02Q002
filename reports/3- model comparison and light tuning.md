# Model comparison and light tuning

## 1. Objective

This phase compares a linear classifier with a non-linear ensemble model and investigates whether a small number of Random Forest configurations can improve predictive performance.

The Logistic Regression model is retained as the main reference because it is both predictive and relatively interpretable. A Random Forest classifier is added to assess whether a non-linear model can exploit interactions that are not captured by the linear model.

The comparison addresses the following project question:

> Do linear and non-linear models obtain different results on the Top-tier versus non–Top-tier classification task?

The target variable is `top_tier`, with `Yes` indicating a Top-tier university and `No` otherwise. It is defined from the average of the Times, Shanghai, and CWUR world rankings.

## 2. Experimental setup

The experiments use the preprocessed dataset containing 555 observations. The data were split with the KNIME `Partitioning` node using:

- 70% training data;
- 30% test data;
- stratified sampling on `top_tier`;
- random seed 42.

The same training/test partition was reused for Logistic Regression, Random Forest, and the reduced-feature sensitivity analysis. This makes the model comparison directly reproducible and prevents differences in the results from being caused by different test sets.

The modeling table uses the full set of available numeric predictors after the preprocessing and leakage-control steps. The world-ranking variables used to construct the target were excluded from the predictor set, as was `average_world_rank`. Identifier columns and excluded national-ranking variables were also removed.

The effective modeling table used 26 predictors, including:

- Times indicators;
- Shanghai indicators;
- CWUR indicators;
- `year`;
- `times_female_value`;
- `times_male_value`.

The earlier baseline report described 24 predictors and a single `times_female_percentage` feature. The current KNIME workflow shows that the effective features are `times_female_value` and `times_male_value`; this discrepancy should be corrected in the consolidated report.

## 3. Models and workflow

The workflow follows the KNIME learner–predictor pattern:

```text
Preprocessing
    ↓
Column Filter
    ↓
Partitioning
    ├── Training set → Logistic Regression Learner
    │                    ↓
    │              Logistic Regression Predictor
    │                    ↓
    │                 Scorer
    │
    └── Training set → Random Forest Learner
                         ↓
                   Random Forest Predictor
                         ↓
                       Scorer
```

The same test set is connected to the corresponding Predictor nodes. The `Scorer` node compares the actual `top_tier` column with the predicted class column.

For the Random Forest branch, the actual target column is `top_tier` and the predicted class column is `prediction_top_tier`.

## 4. Logistic Regression reference model

The Logistic Regression model was trained using the full feature set and default learner settings. The target reference category was `No`, so the model contrasts the `Yes` class with the `No` class.

The test-set confusion matrix was:

|  | Predicted Yes | Predicted No |
|---|---:|---:|
| Actual Yes | 64 | 1 |
| Actual No | 2 | 100 |

The resulting metrics were:

| Metric | Logistic Regression |
|---|---:|
| Accuracy | 0.982 |
| Precision for Yes | 0.970 |
| Recall for Yes | 0.985 |
| F1-score for Yes | 0.977 |
| Cohen’s kappa | 0.962 |

The Logistic Regression model correctly identified 64 Top-tier universities and missed one. It incorrectly classified two non–Top-tier universities as Top-tier.

## 5. Random Forest reference model

The Random Forest was implemented with the KNIME `Random Forest Learner` and `Random Forest Predictor` nodes.

The selected reference configuration was:

- split criterion: Gini Index;
- number of models: 100;
- maximum tree depth: 5;
- minimum node size: default/not constrained;
- static random seed: 42.

The test-set confusion matrix was:

|  | Predicted Yes | Predicted No |
|---|---:|---:|
| Actual Yes | 64 | 1 |
| Actual No | 3 | 99 |

The resulting metrics were:

| Metric | Random Forest |
|---|---:|
| Accuracy | 0.976 |
| Precision for Yes | 0.955 |
| Recall for Yes | 0.985 |
| F1-score for Yes | 0.970 |
| Cohen’s kappa | 0.950 |

The Random Forest achieved the same recall as Logistic Regression, but produced one additional false positive and therefore lower precision, F1-score, accuracy, and Cohen’s kappa.

## 6. Light hyperparameter tuning

A small manual tuning experiment was performed with the KNIME `Random Forest Learner` node. The same train/test split and random seed were retained for all configurations.

| Configuration | Number of trees | Maximum depth | Accuracy | Precision Yes | Recall Yes | F1 Yes | Cohen’s kappa |
|---|---:|---:|---:|---:|---:|---:|---:|
| RF-50-depth5 | 50 | 5 | 0.976 | 0.955 | 0.985 | 0.970 | 0.950 |
| RF-100-depth5 | 100 | 5 | 0.976 | 0.955 | 0.985 | 0.970 | 0.950 |
| RF-250-depth5 | 250 | 5 | 0.976 | 0.955 | 0.985 | 0.970 | 0.950 |
| RF-100-depth10 | 100 | 10 | 0.976 | 0.955 | 0.985 | 0.970 | 0.950 |
| RF-100-depth3 | 100 | 3 | 0.970 | 0.955 | 0.969 | 0.962 | 0.937 |

The four configurations with depth 5 or 10 produced the same predictions on the held-out test set. The configuration with maximum depth 3 was slightly worse:

|  | Predicted Yes | Predicted No |
|---|---:|---:|
| Actual Yes | 63 | 2 |
| Actual No | 3 | 99 |

Increasing the number of trees from 50 to 250 did not improve the test-set predictions. Increasing the maximum depth from 5 to 10 also produced no measurable improvement. Reducing the depth to 3 caused one additional false negative.

The configuration `RF-100-depth5` was retained as the reference Random Forest because it achieved the best observed performance while keeping the model size moderate.

## 7. Full versus reduced Logistic Regression

A sensitivity analysis was performed by removing `times_male_value` from the feature set while keeping the same partition and evaluation procedure.

The reduced model produced:

| Metric | Logistic Regression reduced |
|---|---:|
| Accuracy | 0.982 |
| Precision for Yes | 0.984 |
| Recall for Yes | 0.969 |
| F1-score for Yes | 0.977 |
| Cohen’s kappa | 0.962 |

Its confusion matrix was:

|  | Predicted Yes | Predicted No |
|---|---:|---:|
| Actual Yes | 63 | 2 |
| Actual No | 1 | 101 |

Removing `times_male_value` preserved accuracy, F1-score, and Cohen’s kappa. It increased precision but reduced recall for the positive class. Since identifying Top-tier universities is the main objective, the full-feature Logistic Regression remains preferable because it misses fewer positive cases.

## 8. ROC-AUC evaluation

The KNIME `ROC Curve` node was applied to the probability columns produced by the Predictor nodes. The positive class was `Yes`, and the probability used was `P(top_tier=Yes)`.

The Random Forest produced:

```text
ROC-AUC = 0.997
```

The Logistic Regression produced:

```text
ROC-AUC = 0.999
```

The ROC-AUC comparison was:

| Model | Probability column | ROC-AUC |
|---|---|---:|
| Logistic Regression | `P(top_tier=Yes)` | 0.999 |
| Random Forest, 100 trees, depth 5 | `P(top_tier=Yes)` | 0.997 |

The `ROC Curve` node returned only the numerical area-under-the-curve table in the current KNIME configuration; a graphical ROC curve was not available. Therefore, no ROC plot is reported. The numerical AUC values were retained as an additional evaluation metric.

The two models show excellent ranking ability. Logistic Regression is slightly better than Random Forest according to ROC-AUC, although the difference is small.

## 9. Coefficient diagnostics

The `Logistic Regression Learner` produced a `Coefficients and Statistics` table. The model used `No` as the reference category, so the coefficients describe the contrast between `Yes` and `No`.

However, the coefficient estimates were not considered reliable for inferential interpretation. The table showed extremely large standard errors, z-scores approximately equal to zero, and p-values equal to 1 for the reported variables. This pattern is consistent with strong multicollinearity, different feature scales, and possible quasi-separation.

The coefficients should therefore not be used to claim that an individual metric is statistically significant or has a causal effect on Top-tier status. In particular, the sign of a coefficient should not be interpreted as a robust standalone relationship in this unstandardized, highly correlated feature set.

Normalization and a more advanced multicollinearity analysis were deliberately not included in the current phase. They are optional follow-up analyses that may be performed in a later phase if a deeper interpretation of the Logistic Regression coefficients is required. The full-feature Logistic Regression remains valid as the main predictive reference because its evaluation concerns predictive performance, not inferential coefficient significance.

## 10. Final comparison

| Model | Accuracy | Precision Yes | Recall Yes | F1 Yes | Cohen’s kappa | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression, full features | 0.982 | 0.970 | 0.985 | 0.977 | 0.962 | 0.999 |
| Logistic Regression, excluding `times_male_value` | 0.982 | 0.984 | 0.969 | 0.977 | 0.962 | Not calculated |
| Random Forest, 100 trees, depth 5 | 0.976 | 0.955 | 0.985 | 0.970 | 0.950 | 0.997 |

The full-feature Logistic Regression is selected as the preferred model. It has the same recall as the Random Forest and better performance on every other reported metric. It is also simpler to describe and reproduce than the Random Forest.

The Random Forest remains important as a non-linear comparison model. Its tuning showed that the tested changes in tree count and depth did not produce a measurable improvement on the held-out test set.

The reduced Logistic Regression is retained only as a sensitivity analysis. Removing `times_male_value` reduces false positives from two to one, but also increases false negatives from one to two. Because detecting Top-tier universities is the main priority, the full-feature model is preferred.

## 11. Limitations and interpretation

The very high performance must be interpreted in light of the target construction. The `top_tier` label is derived from the average of the Times, Shanghai, and CWUR ranking variables, while the predictors are other indicators from the same ranking systems. Consequently, the task is intrinsically aligned with the available predictors.

The results should therefore not be interpreted as evidence that the model can predict an independent or future notion of university quality. They show that the available ranking indicators are highly effective at reconstructing the defined Top-tier threshold.

The evaluation also relies on a single fixed stratified 70/30 split. This guarantees a transparent comparison across models, but it does not quantify variability across multiple splits or cross-validation folds. A future extension could use cross-validation on the training data and a final untouched test set.

## 12. Conclusion

The model comparison and light tuning phase is complete. Logistic Regression achieved the best overall results, with accuracy 0.982, F1-score 0.977, Cohen’s kappa 0.962, and ROC-AUC 0.999. Random Forest achieved accuracy 0.976, F1-score 0.970, Cohen’s kappa 0.950, and ROC-AUC 0.997.

The selected model is the full-feature Logistic Regression. The Random Forest configuration `RF-100-depth5` is retained as the best non-linear comparator. The reduced Logistic Regression analysis demonstrated that removing `times_male_value` preserves accuracy and F1-score but lowers recall, so it is not selected as the final model when detecting Top-tier universities is the priority.

Coefficient instability is documented as a limitation of the current interpretation. Normalization and advanced multicollinearity analysis are explicitly left as optional follow-up work rather than requirements for closing this phase.
