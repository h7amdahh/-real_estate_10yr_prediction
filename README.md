# UAE Real Estate 10-Year Trend Prediction

CDS 4003 · Python 3.11 · CRISP-DM  
**Team members and roles:** [Add names, roles and contribution links.]  
**GitHub repository:** [Add verified public URL.]  
**Streamlit app:** Tested locally. [Add public URL after deployment.]

## A. Project Setup

The project runs from `UAE_Real_Estate_Classroom.ipynb`. The notebook generates the files needed by the Streamlit app. The original GitHub setup history still needs confirmation from the team.

**GitHub setup record:** [Add the actual repository name, IDE used to clone it, and link to the first README commit.] To reproduce the guide’s setup, create a public repository on GitHub, clone it locally, open it in VS Code, and save this file as `README.md` in the repository root. Its first line should contain the project title. Replace the placeholders before running:

```bash
git clone https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
code .
git add README.md
git commit -m "Add project README"
git push -u origin main
```

## B. Business Understanding

**Measurable question:** Given a household’s financial profile, emirate and property preferences, how accurately can a classifier identify its recorded ten-year trend as **Increased** or **Dropped** on unseen profiles?

The app lets a user enter a profile and inspect the predicted label and its probability. The file contains no dated purchase or resale prices to verify how the label was created. **Team objective:** [Add your approved stakeholder, intended decision and success criterion in your own words.]

## C. Data Understanding

The notebook loads the supplied CSV with `pd.read_csv("real_estate_10yr_prediction.csv", low_memory=False)`. It contains **300,000 rows and 20 columns**. The notebook uses `df.info()`, `df.describe(include="all")`, missing-value counts, duplicate counts and unique category values to inspect it.

| Fields | Meaning and use |
|---|---|
| `RealEstate_10Yr_Trend` | Target label used to train and evaluate the classifier |
| Annual income, monthly savings, estimated budget | Household finances and intended property budget, in AED |
| Debt-to-income ratio, credit score, existing properties, mortgage rate | Debt burden, credit score, property count and annual interest rate |
| Emirate, current housing, employment sector, preferred property type | Four categorical inputs describing the scenario |
| `Record_ID` | Identifies a record. Excluded from predictors because it has no financial or property meaning |
| Age, gender, marital status, dependents, education, residency, years at residence | Excluded to preserve the working model’s 11 inputs. Gender and residency were retained separately for the error audit. |

**Dataset evidence:** [Add verified source, license, access instructions and search evidence. If synthetic, include prior written instructor approval.]

## D. Data Preparation and Cleaning

1. Removed **5,887 exact duplicate rows** with `df.drop_duplicates().copy()`. Working on copies preserved the original values for before-and-after checks.
2. Standardized target spelling and case. For example, `Increase` became `Increased` and `Drop Down` became `Dropped`. Removed **25,926** rows with missing or unusable targets after deduplication. This left **268,187 labeled profiles**.
3. Removed currency symbols, commas and percent signs before converting values to numbers. Standardized category labels such as `Dxb` → `dubai` and `apt` → `apartment`.
4. Set impossible values to missing. Checks included negative financial amounts, fractional counts, residence duration greater than age, and credit scores outside the assumed 300–900 scale. The IQR rule flagged unusual values for review. Plausible high incomes were retained.
5. Filled missing numerical inputs with the training median and missing categories with the training mode. One-hot encoding converted category names into indicator columns. These steps were fitted inside each training fold.
6. Calculated six features: annual savings divided by annual income, budget divided by annual income, estimated monthly debt, monthly income after debt, years to save the budget, and estimated monthly interest on the full budget. Zero denominators produced missing ratios for the numerical imputer to handle.

## E. Exploratory Data Analysis (EDA)

| Chart in the notebook | What it shows |
|---|---|
| Horizontal bar chart of missing values | Which inputs still needed imputation after cleaning |
| Target count chart | 166,562 profiles labeled Dropped and 101,625 labeled Increased |
| Bar chart by emirate | Percentage of training profiles labeled Increased in each emirate |
| Annual income histogram | Distribution of income on a log scale so large values remain visible |
| Mortgage rate box plot | Spread of annual interest rates in the two label groups |
| Spearman correlation heatmap | Relationships among income, savings, budget and mortgage rate |

The emirate, income, mortgage and correlation charts use the training partition. The app also displays the emirate chart interactively.

## F. Modeling Steps

The notebook used a stratified **80/20 split** with `random_state=42`: **214,549 training profiles** and **53,638 held-out test profiles**. For faster classroom comparisons, it selected 12,000 training profiles and split them into 9,600 fitting rows and 2,400 validation rows.

Numerical inputs used `StandardScaler`. Logistic regression provided a baseline, and a dummy classifier showed the score from always choosing the majority class. The alternatives were decision tree, random forest and histogram gradient boosting. Each model used the same rows and preprocessing steps. Classification reports showed precision, recall and F1 for both labels. Confusion matrices showed which label each model missed.

## G. Model Validation and Tuning

Five shuffled, stratified folds on the 12,000-row training sample measured stability. **Macro F1** gave each label equal weight despite the class imbalance.

| Model | Mean cross-validation macro F1 | Fold standard deviation |
|---|---:|---:|
| Dummy classifier | 0.3831 | 0.0001 |
| Logistic regression | 0.7120 | 0.0084 |
| Decision tree | 0.6909 | 0.0111 |
| Random forest | 0.7017 | 0.0102 |
| Histogram gradient boosting | **0.7189** | 0.0086 |

`GridSearchCV` compared 7 and 15 maximum leaf nodes for gradient boosting. The respective mean macro F1 scores were **0.7174** and **0.7189**. The final pipeline used **15 maximum leaf nodes** and **75 maximum iterations** and was fitted on all 214,549 training rows.

| Held-out test metric | Result |
|---|---:|
| Accuracy | 75.51% |
| Macro F1 | 0.7262 |
| ROC-AUC | 0.8146 |
| Precision for Increased | 72.7% |
| Recall for Increased | 56.7% |
| F1 for Increased | 0.637 |

Of 20,325 test profiles labeled Increased, the model identified 11,527 and missed 8,798. The notebook also compared missed increases by gender and residency and shuffled individual inputs to measure their influence on macro F1. **Team interpretation:** [Explain what these errors mean for your intended use.]

## H. Pipeline Creation for Deployment

The pipeline first calls `clean_inputs` and `add_features`. Its `ColumnTransformer` sends numbers through median imputation and scaling, and categories through mode imputation and `OneHotEncoder(handle_unknown="ignore")`. The final step is the fitted gradient boosting classifier. Packaging these steps together ensures that a profile entered in the app receives the same transformations as a training profile.

## I. Saving Model

The notebook saved the whole fitted pipeline, then loaded it and predicted a sample profile:

```python
joblib.dump(deployment_pipeline, "real_estate_model.pkl", compress=3)
classifier = joblib.load("real_estate_model.pkl")
classifier.predict(example)
```

The reloaded pipeline reproduced the original working model’s labels and probabilities on all 53,638 test profiles.

## J. Streamlit Application Development

The notebook created `app.py` using `%%writefile`. The app loads the saved pipeline with `st.cache_resource`. Users select four categories and enter seven numerical values. Clicking **Predict** calls `predict()` for the label and `predict_proba()` for the probability chart. An expandable section shows training results by emirate and the validation comparison.

To reproduce the project, put the notebook and `real_estate_10yr_prediction.csv` in the same folder. Select a Python 3.11 kernel, install the packages listed in the first cell if needed, and choose **Run All**. Then launch the app from that folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

All 39 code cells ran successfully. The prediction button, result and probability chart were verified in a local browser.

## K. Deployment

The notebook wrote `requirements.txt` with exact versions for pandas, NumPy, SciPy, scikit-learn, Joblib, Matplotlib, Seaborn and Streamlit. **Public deployment is pending.**

1. Review permission to share the notebook’s sample records. From the repository root, stage the reviewed project files, commit and push them. Keep the model and its helper scripts together so the app can reload the pipeline.

   ```bash
   git add README.md UAE_Real_Estate_Classroom.ipynb app.py cleaning.py financial_features.py
   git add real_estate_model.pkl comparison.csv emirates.csv requirements.txt
   git commit -m "Add real estate notebook and Streamlit app"
   git push -u origin main
   ```

2. In Streamlit Community Cloud, connect the GitHub account and select the project repository, branch `main`, entry point `app.py` and Python **3.11**.
3. Start deployment and wait for package installation and app startup. If the logs show a dependency error, correct `requirements.txt`, push the fix and redeploy.
4. Open the public URL while signed out and submit a prediction. Add the verified URL at the top of this README and confirm the README appears on the GitHub repository home page.

**AI-use declaration:** [Complete in your own words in the README and report.] Coding assistance included simplifying the notebook, preserving the feature formulas, running the pipeline, verifying local predictions and preparing this technical README.
