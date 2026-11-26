# Data dictionary

Dataset: `real_estate_10yr_prediction.csv` | 300,000 raw records | 20 columns.

Types describe intended meaning; several raw numeric columns are stored as text because of inconsistent formatting. Examples are observed in the supplied CSV. `Predictor` indicates use by the final model. `Audit` indicates an excluded field used for error analysis.

| Column | Intended type / unit | Description / example | Role |
|---|---|---|---|
| `Record_ID` | String | Synthetic record identifier, e.g. RE-1069438 | Identifier; excluded |
| `Age` | Integer, years | Age of household profile, e.g. 38 | Excluded |
| `Gender` | Category | Gender, e.g. Male, Female | Audit |
| `Marital_Status` | Category | Marital status, e.g. Single, Married | Excluded |
| `Dependents` | Integer, count | Number of dependents, e.g. 2 | Excluded |
| `Education_Level` | Category | Education level, e.g. Bachelor, High School | Excluded |
| `City_Emirate` | Category | UAE emirate, e.g. Dubai, Abu Dhabi | Predictor |
| `Residency_Status` | Category | Residency classification, e.g. Citizen, Expat_LongTerm | Audit |
| `Current_Housing` | Category | Current housing arrangement, e.g. Renting, Owns_Outright | Predictor |
| `Years_At_Residence` | Decimal, years | Duration at current residence, e.g. 6.7 | Excluded |
| `Employment_Sector` | Category | Employment category, e.g. Salaried_Private, Self_Employed | Predictor |
| `Annual_Income_AED` | Decimal, AED/year | Annual income, e.g. 106307.50 | Predictor |
| `Monthly_Savings_AED` | Decimal, AED/month | Monthly savings, e.g. 3389.79 | Predictor |
| `Debt_To_Income_Ratio` | Decimal, ratio | Income share allocated to debt, e.g. 0.184 (18.4%) | Predictor |
| `Credit_Score` | Integer, score | Credit score, e.g. 770; cleaning accepts 300–900 | Predictor |
| `Existing_Properties` | Integer, count | Number of properties already owned, e.g. 1 | Predictor |
| `Preferred_Property_Type` | Category | Preferred property, e.g. Apartment, Villa | Predictor |
| `Estimated_Budget_AED` | Decimal, AED | Estimated property budget, e.g. 498000 | Predictor |
| `Mortgage_Interest_Rate_Pct` | Decimal, percent | Annual mortgage interest rate, e.g. 6.44 (6.44%) | Predictor |
| `RealEstate_10Yr_Trend` | Binary category | Synthetic recorded trend, normalized to Increased or Dropped | Target |

## Derived model features

All six are created by `financial_features.py`. Let income = annual income, savings = monthly savings × 12, and budget = estimated property budget.

| Feature | Formula | Unit |
|---|---|---|
| `Savings_to_income` | savings / income | Ratio |
| `Budget_to_income` | budget / income | Ratio |
| `Monthly_debt_AED` | income / 12 × debt-to-income ratio | AED/month |
| `Income_after_debt_AED` | income / 12 − monthly debt | AED/month |
| `Years_to_save_budget` | budget / savings | Years |
| `Monthly_interest_AED` | budget × mortgage interest rate / 100 / 12 | AED/month |

Ratios with a nonpositive denominator are set to missing. Missing numerical features are handled by the pipeline's median imputer. Monthly interest is an estimate using the full budget, not a complete mortgage payment calculation.
