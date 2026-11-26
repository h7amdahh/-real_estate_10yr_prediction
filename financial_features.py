def add_features(X):
    X = X.copy()
    income = X.Annual_Income_AED
    savings = X.Monthly_Savings_AED * 12
    budget = X.Estimated_Budget_AED

    X["Savings_to_income"] = savings / income.where(income > 0)
    X["Budget_to_income"] = budget / income.where(income > 0)
    X["Monthly_debt_AED"] = income / 12 * X.Debt_To_Income_Ratio
    X["Income_after_debt_AED"] = income / 12 - X.Monthly_debt_AED
    X["Years_to_save_budget"] = budget / savings.where(savings > 0)
    X["Monthly_interest_AED"] = budget * X.Mortgage_Interest_Rate_Pct / 100 / 12
    return X
