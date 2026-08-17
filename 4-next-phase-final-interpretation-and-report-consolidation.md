# Next phase: final interpretation and report consolidation

## 1. Objective

The next phase will consolidate the completed modeling work into a coherent final study. The current phase, model comparison and light tuning, is complete: Logistic Regression was selected as the preferred model, Random Forest was retained as the non-linear comparator, and the main evaluation metrics were computed on the same held-out test set.

The next phase should focus on interpretation, consistency, documentation, and final report preparation rather than extensive additional tuning.

## 2. Priority tasks

### 2.1 Consolidate the research-question answers

Prepare explicit answers to the three research questions:

1. Which metrics distinguish Top-tier universities from the others?
2. How predictive are the available ranking indicators for the Top-tier classification task?
3. Do linear and non-linear models achieve different results?

The third question can already be answered from the completed comparison. Logistic Regression achieved slightly better results than Random Forest while maintaining the same recall for the positive class.

The first question requires caution because the Logistic Regression coefficients are unstable. We should not interpret the coefficient signs or p-values as reliable evidence of statistically significant individual effects.

### 2.2 Document the final model selection

The final report should explain why the full-feature Logistic Regression was selected:

- accuracy: 0.982;
- precision for `Yes`: 0.970;
- recall for `Yes`: 0.985;
- F1-score for `Yes`: 0.977;
- Cohen’s kappa: 0.962;
- ROC-AUC: 0.999.

The Random Forest comparator achieved:

- accuracy: 0.976;
- precision for `Yes`: 0.955;
- recall for `Yes`: 0.985;
- F1-score for `Yes`: 0.970;
- Cohen’s kappa: 0.950;
- ROC-AUC: 0.997.

The selection should be justified by performance, simplicity, reproducibility, and the same positive-class recall.

### 2.3 Record the reduced-feature sensitivity analysis

The experiment removing `times_male_value` should remain documented as a sensitivity analysis, not as the final model.

The reduced Logistic Regression achieved:

- accuracy: 0.982;
- precision for `Yes`: 0.984;
- recall for `Yes`: 0.969;
- F1-score for `Yes`: 0.977;
- Cohen’s kappa: 0.962.

Removing the feature reduced false positives from two to one, but increased false negatives from one to two. Because detecting Top-tier universities is the main priority, the full-feature model remains preferable.

### 2.4 Document coefficient limitations

The `Logistic Regression Learner` produced a `Coefficients and Statistics` table, but the estimates were unstable:

- standard errors were extremely large;
- z-scores were approximately zero;
- p-values were equal to 1 for the reported variables.

The report should explain that this pattern is consistent with strong multicollinearity, different feature scales, and possible quasi-separation. The coefficients should not be used to claim statistical significance or causal effects.

Normalization and advanced multicollinearity analysis should be presented as optional future work, not as unfinished requirements for the current project phase.

## 3. Optional follow-up analysis

A standardized Logistic Regression branch may be considered only if a more detailed feature interpretation is required.

The possible KNIME workflow would be:

```text
Partitioning
    ├── Training set → Normalizer → Logistic Regression Learner
    └── Test set → Normalizer (Apply) → Logistic Regression Predictor
```

The `Normalizer` must estimate parameters on the training data, while `Normalizer (Apply)` applies the same parameters to the test data. This branch would be a separate analytical experiment and must not silently replace the official baseline model.

A multicollinearity analysis could also be performed in a later phase, potentially using correlation analysis or variance-inflation diagnostics. Neither analysis is required to close the present project.

## 4. KNIME workflow consolidation

Review and annotate the final workflow so that every major section is clear:

```text
Preprocessing
    ↓
Column Filter
    ↓
Partitioning
    ├── Baseline models and first KPIs
    ├── Random Forest comparison
    ├── Random Forest tuning cases
    └── Reduced-feature sensitivity analysis
```

The workflow should include annotations for:

- target definition;
- leakage prevention;
- 70/30 stratified partition;
- random seed 42;
- Logistic Regression configuration;
- Random Forest configuration;
- Scorer metrics;
- ROC-AUC evaluation;
- final model selection;
- limitations.

The project guidelines require the report to refer to the KNIME workflow and require nodes and metanodes to be annotated with their purpose and assumptions.

## 5. Report consolidation

The final report should be assembled from the updated sections:

- preprocessing;
- baseline model and first KPIs;
- model comparison and light tuning;
- final interpretation and conclusions.

During consolidation:

- use one target name consistently, preferably `top_tier` in accordance with the KNIME workflow;
- use 26 predictors consistently;
- use `times_female_value` and `times_male_value` consistently;
- avoid references to `times_female_percentage` unless explicitly discussing the earlier discarded description;
- distinguish the full-feature model from the reduced-feature sensitivity analysis;
- distinguish predictive performance from coefficient-level inference;
- state that the ROC Curve node returned numerical AUC values but no graphical ROC plot was available;
- preserve the same reported metric values across all sections.

## 6. Final validation checklist

Before submission, verify:

- the final report and KNIME workflow use the same target name;
- the final report describes 26 predictors;
- `times_female_value` and `times_male_value` are the documented gender-related predictors;
- world-ranking variables and `average_world_rank` are excluded from the model inputs;
- the train/test split is described as stratified 70/30 with seed 42;
- all reported confusion matrices sum to 167 test observations;
- Logistic Regression and Random Forest results use the same test set;
- the Random Forest tuning table contains all five tested configurations;
- ROC-AUC values are reported as numerical results without claiming that a ROC plot was produced;
- coefficient instability is documented;
- normalization and advanced collinearity analysis are clearly marked as optional future work;
- the final model selection is consistent with the reported metrics;
- no unsupported claim of causal interpretation is included.

## 7. Expected final conclusion

The final conclusion should state that the full-feature Logistic Regression is the preferred model for the defined task. It achieved the best overall predictive performance and the same recall as Random Forest, while remaining simpler to reproduce and explain.

Random Forest provides a useful non-linear comparison but did not improve the results under the tested configurations. The reduced-feature experiment showed that `times_male_value` can be removed without changing accuracy, F1-score, or Cohen’s kappa, but the resulting model has lower recall and is therefore not selected when identifying Top-tier universities is the main priority.

The final interpretation must emphasize that the very high performance is partly expected because the target is constructed from ranking variables that are closely related to the predictors. The model should therefore be understood as a strong classifier for the operationally defined Top-tier label, not as an independent measure of university quality.
