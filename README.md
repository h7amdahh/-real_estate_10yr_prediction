# UAE Real Estate 10-Year Trend Prediction

CDS 4003 | Data Science for Business Application | Python 3.12

- **Team:** [Insert all team members, GitHub usernames, roles and contribution evidence.]
- **GitHub repository:** [Insert the new repository URL.]
- **Live Streamlit application:** Deployed, as confirmed by the team. [Insert the public Streamlit URL.]

## Business problem

The project classifies a household profile into one of two recorded synthetic 10-year real estate trend labels: `Increased` or `Dropped`. The Streamlit app accepts a household's financial and property-related information and displays a predicted class and model probabilities. The results measure agreement with synthetic labels, not verified future property prices.

[Insert the instructor-approved business objective, intended stakeholders and measurable success criteria.]

## Dataset

- File: `real_estate_10yr_prediction.csv` (included in the project repository).
- Source: AI-generated synthetic dataset prepared for the course project, as confirmed by the team.
- Instructor permission: the team confirmed that synthetic data was permitted. Retain the original written approval if available.
- License: not specified in the supplied project files. [Insert the applicable permission/license after confirmation.]
- Raw dataset: 300,000 rows, 20 columns, including the target and record identifier.
- Target: `RealEstate_10Yr_Trend`.
- [Add actual dataset search evidence and the original AI generation code or prompt record.]

See [data dictionary](docs/data_dictionary.md), [synthetic data provenance](docs/synthetic_data_provenance.md), and [observed quality issues](docs/data_quality_audit.md). The audit is reproducible using `scripts/audit_dataset.py`; it is not the original data generation script.

## Repository files

```text
.
├── README.md
├── real_estate.ipynb
├── real_estate_10yr_prediction.csv
├── cleaning.py
├── financial_features.py
├── model.pkl
├── app.py
├── requirements.txt
├── requirements-notebook.txt
├── docs/
│   ├── data_dictionary.md
│   ├── synthetic_data_provenance.md
│   └── data_quality_audit.md
└── scripts/
    └── audit_dataset.py
```

## Reproduce the project

Use Python 3.12, as specified in the notebook. Open a terminal in the repository root. The team researched package versions for compatibility. The notebook dependencies file extends the existing app requirements with visualization and Jupyter packages. The app requirements should retain `scikit-learn==1.6.1` for the saved model.

```bash
python -m pip install -r requirements-notebook.txt
python -m notebook real_estate.ipynb
```

Select the Python kernel for that environment and run the notebook from top to bottom. Keep the uncompressed CSV in the repository root. Running the notebook recreates `cleaning.py`, `financial_features.py`, `model.pkl`, `app.py` and `requirements.txt`. The notebook's requirements-writing cell must also retain scikit-learn 1.6.1.

To run the saved app without retraining:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

To reproduce the raw data audit:

```bash
python scripts/audit_dataset.py
```

## Data preparation and exploration

- Removed 5,887 exact duplicate records, then 25,926 records with missing targets after target normalization; 268,187 labeled records remained.
- Standardized inconsistent category labels and numeric formats, checked invalid values, and flagged outliers using IQR.
- Used 11 raw predictors; excluded the record identifier and direct demographic fields. Gender and residency status were retained separately for an error audit.
- Created six financial features: savings-to-income ratio, budget-to-income ratio, monthly debt, income after debt, years to save the budget and estimated monthly interest.
- Used median numerical imputation, most-frequent categorical imputation, standard scaling and one-hot encoding inside a scikit-learn pipeline.
- Explored missing values, class balance, emirate-level label proportions, income distribution, mortgage rates and financial correlations. Target relationship plots use the training partition.

## Model development and evaluation

A stratified 80/20 split (random state 42) produced 214,549 training records and 53,638 held-out test records. Initial comparison and five-fold cross-validation used a 12,000-record training sample. Saved notebook cross-validation results:

| Model | Mean macro F1 |
|---|---:|
| Dummy classifier | 0.3831 |
| Logistic regression | 0.7120 |
| Decision tree | 0.6909 |
| Random forest | 0.7020 |
| Histogram gradient boosting | 0.7189 |

GridSearchCV selected 15 maximum leaf nodes. The final histogram gradient boosting classifier was fitted on the full training set and evaluated on the held-out test set.

| Test metric | Result |
|---|---:|
| Accuracy | 75.51% |
| Macro F1 | 72.62% |
| ROC-AUC | 81.46% |

These figures are from the saved notebook outputs. The notebook also includes classification reports, confusion matrices, a demographic error audit and permutation importance.

## Deployment

`app.py` loads the fitted pipeline from `model.pkl`. It provides four categorical inputs and seven numerical inputs, then displays the predicted trend and a probability chart. Keep `app.py`, `model.pkl`, `cleaning.py`, `financial_features.py` and `requirements.txt` together. The Streamlit Community Cloud entry point is `app.py`.

## Repository history and documentation

The team reports that Hamdah's original email account was closed. She created a new email and GitHub account and manually reuploaded the project. The new repository's commit history therefore does not preserve the original development history. [Add available original contribution evidence and any instructor confirmation.]

The team reports that Codex was used to prepare the unfinished README with the instructor's permission. [Complete the required AI-use declaration separately with an accurate record of all tools and uses.]
