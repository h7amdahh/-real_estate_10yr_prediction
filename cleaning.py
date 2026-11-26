import numpy as np
import pandas as pd

def clean_inputs(X):
    X = X.copy()
    for col in ["Annual_Income_AED", "Estimated_Budget_AED", "Mortgage_Interest_Rate_Pct"]:
        text = X[col].astype("string").str.replace(r"AED|,|%", "", regex=True).str.strip()
        X[col] = pd.to_numeric(text, errors="coerce").astype(float)

    for col in X.select_dtypes("number"):
        X[col] = X[col].where(X[col].ge(0) & np.isfinite(X[col]))
    for col in ["Age", "Dependents", "Existing_Properties", "Credit_Score"]:
        if col in X:
            X[col] = X[col].where(X[col] % 1 == 0)
    X["Credit_Score"] = X.Credit_Score.where(X.Credit_Score.between(300, 900))
    X["Mortgage_Interest_Rate_Pct"] = X.Mortgage_Interest_Rate_Pct.where(X.Mortgage_Interest_Rate_Pct <= 100)
    if "Age" in X:
        X["Age"] = X.Age.where(X.Age.between(18, 120))
        X.loc[X.Years_At_Residence > X.Age, "Years_At_Residence"] = np.nan

    aliases = {"City_Emirate":{"dxb":"dubai"}, "Current_Housing":{"rent":"renting"},
               "Preferred_Property_Type":{"apt":"apartment"}, "Education_Level":{"hs":"high school"},
               "Gender":{"m":"male", "f":"female"}}
    for col in X.select_dtypes("object"):
        X[col] = X[col].str.strip().str.lower().replace(aliases.get(col, {}))
        X[col] = X[col].replace({"unknown":np.nan, "":np.nan})
    return X
