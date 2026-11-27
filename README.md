# UAE Real Estate 10-Year Trend Prediction

CDS 4003 | Data Science for Business Application | Higher Colleges of Technology

- **Project repository:** [h7amdahh/-real_estate_10yr_prediction](https://github.com/h7amdahh/-real_estate_10yr_prediction)
- **Team GitHub accounts:** [h7amdahh](https://github.com/h7amdahh), [afra-star23](https://github.com/afra-star23), [raaweya](https://github.com/raaweya)
- **Deployment:** Streamlit Community Cloud (deployment completed, as confirmed by the team).

## 1. Business problem and objectives

Real estate decisions involve substantial financial commitments. This project develops a classification tool for UAE household profiles using financial and property-related information. It predicts the recorded synthetic ten-year trend label (`Increased` or `Dropped`) to support initial scenario assessments by property buyers and household advisers.

The objectives are to prepare at least 200,000 records with 20 original columns, compare at least two classifiers, select a model using macro F1, evaluate it on held-out data, and deploy an interactive prediction application.

## 2. Dataset

The [dataset](real_estate_10yr_prediction.csv) is AI-generated synthetic data prepared for the course project with instructor permission, as confirmed by the team. It is included in the repository.

| Attribute | Description |
|---|---|
| Original dimensions | 300,000 rows × 20 columns |
| Cleaned records | 268,187 |
| Target | `RealEstate_10Yr_Trend` |
| Classes | Increased and Dropped |
| Model inputs | 11 original predictors |

Dataset documentation:

- [Data dictionary](data_dictionary.md)
- [Data quality audit](data_quality_audit.md)
- [Synthetic data provenance](synthetic_data_provenance.md)

## 3. Repository structure

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
├── data_dictionary.md
├── data_quality_audit.md
└── synthetic_data_provenance.md
```

| File | Purpose |
|---|---|
| `real_estate.ipynb` | Data preparation, EDA, feature engineering, model development, tuning and evaluation |
| `cleaning.py` | Reusable input cleaning |
| `financial_features.py` | Reusable financial feature engineering |
| `model.pkl` | Saved trained classification pipeline |
| `app.py` | Streamlit prediction interface |
| `requirements.txt` | Application dependencies |

## 4. Running the project

The team researched package versions for compatibility. Python 3.12 is specified in the notebook. Run commands from the repository root.

### Run the notebook

Install the notebook dependencies using the team's `requirements-notebook.txt` file. If it is not included in your checkout, obtain it from the team before running the notebook.

```bash
python -m pip install -r requirements-notebook.txt
python -m notebook real_estate.ipynb
```

Select the matching Python kernel and run the cells in order. The dataset-loading cell must reference the included `real_estate_10yr_prediction.csv` file. Running the notebook recreates the trained model and deployment files. Use the scikit-learn version used to train the saved pipeline; the original saved model uses 1.6.1. Ensure the requirements file and notebook's requirements-writing cell use compatible versions before retraining or deploying.

### Run the application locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The Streamlit Community Cloud entry point is `app.py`. Keep the saved model, Python helper modules and dependency file in the repository root.

## 5. Data preparation and exploration

- Removed 5,887 exact duplicate records and 25,926 records with unusable targets, leaving 268,187 labeled records.
- Standardized categorical labels and numeric formats, handled invalid values and flagged outliers using the IQR rule.
- Used median numerical imputation, most-frequent categorical imputation, standard scaling and one-hot encoding within the model pipeline.
- Analyzed class balance, emirate-level label proportions, income distribution, mortgage rates and financial correlations.
- Created six financial features: savings-to-income ratio, budget-to-income ratio, estimated monthly debt, income after debt, years to save the budget, and estimated monthly interest.

## 6. Model development and evaluation

A stratified 80/20 split (random state 42) produced 214,549 training records and 53,638 held-out test records. Initial model comparison and five-fold cross-validation used a stratified training sample of 12,000 records.

| Model | Mean CV macro F1 |
|---|---:|
| Dummy classifier | 0.3831 |
| Logistic regression | 0.7120 |
| Decision tree | 0.6909 |
| Random forest | 0.7020 |
| Histogram gradient boosting | 0.7189 |

Histogram gradient boosting achieved the highest mean macro F1. GridSearchCV selected 15 maximum leaf nodes, and the final model was fitted to the full training partition.

| Held-out test metric | Result |
|---|---:|
| Accuracy | 75.51% |
| Macro F1 | 72.62% |
| ROC-AUC | 81.46% |

These results are from the saved notebook. The notebook also contains confusion matrices, classification reports, permutation importance and a demographic error audit.

## 7. Deployment and business value

The Streamlit app loads the fitted pipeline from `model.pkl`, accepts four categorical and seven numerical inputs, and presents a predicted trend and class probabilities. Users can compare household financial scenarios and examine the model output. The results represent predictions of synthetic labels, not validated forecasts of future property prices or investment advice.

## 8. Repository history

The original email account used by Hamdah was closed. A new email and GitHub account were created, and the project files were manually reuploaded. Consequently, the current repository history does not preserve the original development commits. The team also confirms that Codex was used to prepare the unfinished README with instructor permission.
