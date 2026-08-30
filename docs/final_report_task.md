# Final report task — TEAM 05

## Objective

Produce a concise, integrated technical-report source for TEAM 05 (Giorgio Evola), ready to be placed in the course template and exported as a PDF of at most eight pages. The report must describe and remain consistent with the executed KNIME workflow in `ml-knime-workspace/project_1`.

## Confirmed decisions

- The report is an integrated narrative, not a concatenation of the three phase reports.
- Sections: title page; introduction and research questions; dataset and preprocessing; experimental design and KNIME workflow; results; discussion, limitations, and conclusion.
- Essential visuals only: one workflow figure, one preprocessing table, one final-model comparison table, and one confusion matrix for the selected model.
- TEAM 05 lists Giorgio Evola as its sole confirmed member.
- The selected model is full-feature Logistic Regression; Random Forest is the non-linear comparator; the reduced Logistic Regression is a sensitivity analysis only.

## Scope exclusions

- No additional tuning, normalization branch, or multicollinearity analysis.
- No unverified causal or coefficient-level claims.
- No PDF export, archive creation, or modification of the KNIME workflow in this task.

## Data and contracts

- 555 integrated observations; 26 numeric predictors; `top_tier` target.
- Target: `Yes` when `average_world_rank <= 100`, otherwise `No`.
- Leakage exclusions: the three world-rank variables and `average_world_rank`.
- Evaluation: fixed stratified 70/30 train/test split, seed 42, 167 test observations.

## Status legend

- `[ ]` not started
- `[~]` in progress
- `[x]` completed
- `[!]` blocked or needs replanning

## Checklist

- [x] Review prior phase reports, workflow artefacts, and past-report examples.
- [x] Draft the compact integrated report with the agreed narrative, tables, and figure reference.
- [x] Verify metric, terminology, and workflow consistency; record final validation results.
- [x] Add concise report-level traceability from preprocessing decisions to KNIME nodes and document the final target definition.
- [!] Add the corresponding node and metanode descriptions within the KNIME workflow; deferred while KNIME holds `project_1/.knimeLock`.
- [!] Apply the report-ready A4 template and export the submission PDF. The HTML template is complete; automated PDF conversion is blocked by the local headless renderer and background Word instance.

## Modalita' di avanzamento

Each implementation step requires explicit user authorization. The user authorized the final-report phase and confirmed TEAM 05 and the author data. This step produces a Markdown source only. At the end of each step, this plan is updated with results, changed files, and deviations. Unexpected scope changes require a recorded plan review before implementation.

## Revisione del piano

No scope deviation identified. The course requirement normally states a team size of at least two, while the user explicitly confirmed a sole listed member. The report records only the confirmed author; eligibility must be resolved directly with the course instructor if required.

### 2026-08-27 — Methodological and editorial refinement

The user approved a focused revision based on review feedback. It clarifies the meaning of ranking-system indicators, the integration and leakage rationale, the class distribution, and the fact that evaluation uses one fixed hold-out split. It also records the documented pre-split median-imputation limitation. These changes improve accuracy of reporting without changing the workflow, metrics, model selection, or scope.

### 2026-08-30 — Final precision edits

The user approved final accuracy edits: describe the data as university-year observations; make the RQ1 answer explicitly collective rather than individual-feature based; standardise the Random Forest and nonlinear terminology; and render references as Markdown links. No result or methodological decision changed.

### 2026-08-30 — Optional style refinements

The user approved three optional consistency edits: title capitalisation, university-year wording in the abstract, and smoother Random Forest configuration wording. No data, metric, or conclusion changed.

### 2026-08-30 — ROC figure integration

The user provided and authorised the use of a Logistic Regression ROC-curve image. The report will include it as the only performance figure, alongside the numerical model-comparison table. The prior statement that no graphical ROC curve was available is replaced accordingly.

### 2026-08-30 — Workflow figure replacement

The user provided `img/main_flow.png` as the report-ready workflow figure. It replaces the relative reference to the workflow's raw SVG export.

### 2026-08-30 — Test-set wording refinement

The user approved a concise wording refinement that describes the test-set class counts as observations, consistent with the report's university-year terminology.

### 2026-08-30 — Final A4 template and PDF export

The user authorised the final report format. An A4 HTML/CSS report was created with the approved cover information, workflow figure, ROC figure, tables, and references. Edge headless could not render a PDF because its GPU process fails in this execution environment. A background Microsoft Word conversion was also attempted with the installed Word application, but it blocked without creating output; its process was closed. The HTML file remains fully self-contained in layout and references local images through relative paths. Manual Word/browser PDF export is required unless a working local PDF renderer becomes available.

### 2026-08-30 — Traceability and target-definition correction

The user authorised report changes to address two gaps. The report now maps each preprocessing decision to the relevant KNIME node type and states the final average-rank consensus target used by the workflow. Workflow-file annotations are deferred because KNIME is currently running and holds an active lock on `project_1`.

### 2026-08-30 — Country-table confirmation

The user confirmed that the country table was loaded only for optional enrichment and was deliberately not used in the final integration or modelling table. The report now states this explicitly.

## Registro avanzamento

### 2026-08-27 — Context and layout review

- Reviewed the three existing technical reports and the final-consolidation note.
- Inspected `project_1` workflow metadata and its exported SVG; it shows preprocessing, filtering, partitioning, baseline/logistic-regression branch, Random Forest, scorer, and ROC evaluation.
- Located two previous PDF report examples; one is seven pages, supporting a 6–7 page target for this report.
- Files changed: this plan.

### 2026-08-27 — Integrated report draft and validation

- Created `reports/4-final-report-draft.md` with title page, six integrated sections, one workflow-figure reference, a preprocessing table, a final comparison table, and the selected-model confusion matrix.
- Kept the narrative to approximately 1,483 words, which is suitable for a 6–7 page layout once placed in the course template.
- Verified that all key dataset, split, feature-count, metric, model-selection, leakage, and limitation statements match the preceding phase reports. `git diff --check` completed with no whitespace errors.
- Deviation: no official course template was available in the repository, so the report remains Markdown source and references the existing KNIME `workflow.svg`.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-27 — Approved review corrections

- Applied the approved terminology, style, experimental-design, class-distribution, and leakage-rationale corrections.
- Added the pre-split median-imputation limitation and the training-only imputation improvement for future work.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Final precision edits

- Applied the approved university-year, RQ1, Gini-index, terminology, and reference-format changes.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Optional style refinements

- Applied the approved title, abstract, and Random Forest wording refinements.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — ROC figure integration

- Added Figure 2 from `img/ROC_Curve.png`, with an AUC-aware caption and random-classifier reference.
- Replaced the obsolete no-plot statement in the limitations section.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Workflow figure replacement

- Replaced the raw workflow-SVG reference with `img/main_flow.png` and simplified the figure caption.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Test-set wording refinement

- Replaced the test-set class-distribution sentence with the approved concise formulation.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Final A4 template and PDF export

- Created `reports/TEAM-05-final-report.html`, an A4 print template aligned with the concise course-report layout.
- Included `img/main_flow.png` and `img/ROC_Curve.png` as the two approved figures.
- Attempted automated PDF export with Edge and Word; neither generated a PDF because of local rendering/automation failures unrelated to report content.
- Files changed: `docs/final_report_task.md`; `reports/TEAM-05-final-report.html`.

### 2026-08-30 — Traceability and target-definition correction

- Added a `KNIME implementation` column to the preprocessing table in the Markdown report.
- Documented the final average-rank consensus target used by the executed workflow.
- Did not edit workflow files because `knime.exe` is running and `project_1/.knimeLock` is active.
- Preserved the user-created `reports/2025-2026 - TEAM 05.html` and `.pdf`; they must be regenerated after these source edits.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Target-definition wording refinement

- Removed drafting-history language and retained only the consensus-based target definition used throughout the final workflow and results.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Final HTML regeneration

- Recreated `reports/2025-2026 - TEAM 05.html` from the updated Markdown content, including the KNIME-traceability table, country-table note, and consensus target wording.
- Preserved the prior Word-generated HTML as `reports/2025-2026 - TEAM 05.previous.html` because it used a non-UTF-8 encoding and could not be safely patched.
- The existing PDF remains a prior export and must be regenerated from the new HTML after the workflow annotations are complete.
- Files changed: `docs/final_report_task.md`; `reports/2025-2026 - TEAM 05.html`.

### 2026-08-30 — Figure, RQ1, and reference refinement

- Renamed Figure 1 to reflect the modelling branch actually shown, rather than the entire end-to-end workflow.
- Added an explicit Results-level qualification that RQ1 is answered only at collective predictor-set level, not with individual coefficient-level inference.
- Added official methodology references for THE, ARWU/ShanghaiRanking, and CWUR as institutional background sources; they are not presented as historical year-for-year dataset methodology.
- The HTML copy has been resaved by Word in a non-UTF-8 encoding and will be regenerated from this updated Markdown source after final review.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Results-flow refinement

- Removed the brief RQ1 inference limitation after the comparison table to avoid repeating the fuller explanation in the Discussion section.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.

### 2026-08-30 — Final HTML regeneration after release of Word lock

- Recreated `reports/2025-2026 - TEAM 05.html` as UTF-8 from the current report content after the user closed Word.
- Included the revised Figure 1 caption, removal of the repeated Results-level RQ1 sentence, and the three added ranking-methodology references.
- Preserved the pre-regeneration Word-generated file as `reports/2025-2026 - TEAM 05.pre-regeneration.html`.
- Files changed: `docs/final_report_task.md`; `reports/2025-2026 - TEAM 05.html`.

### 2026-08-30 — Country-table confirmation

- Documented the fourth `CSV Reader` and the intentional exclusion of the country table from final modelling.
- Files changed: `docs/final_report_task.md`; `reports/4-final-report-draft.md`.
