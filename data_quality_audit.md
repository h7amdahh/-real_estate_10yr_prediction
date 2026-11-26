# Observed synthetic data quality issues

File: `real_estate_10yr_prediction.csv`

SHA-256: `f8456c7ebebedc4b5ccf2362b6eab3ed5ab7d81bcde773a9fc8938b03a233f46`

Counts refer to the raw CSV unless otherwise specified. The audit observes defects; it does not establish how or why they were injected.

| Check | Count |
|---|---:|
| Rows | 300,000 |
| Columns | 20 |
| Exact duplicate rows beyond first occurrence | 5,887 |
| Repeated record IDs beyond first occurrence | 5,887 |
| Missing cells | 426,515 |
| Missing or unusable targets after deduplication | 25,926 |
| Usable labeled rows after deduplication | 268,187 |
| Normalized Dropped labels after deduplication | 166,562 |
| Normalized Increased labels after deduplication | 101,625 |

## Missing values by raw column

| Column | Missing | Percent |
|---|---:|---:|
| `Record_ID` | 0 | 0.00% |
| `Age` | 23,107 | 7.70% |
| `Gender` | 22,906 | 7.64% |
| `Marital_Status` | 20,968 | 6.99% |
| `Dependents` | 12,626 | 4.21% |
| `Education_Level` | 27,811 | 9.27% |
| `City_Emirate` | 23,236 | 7.75% |
| `Residency_Status` | 31,411 | 10.47% |
| `Current_Housing` | 27,995 | 9.33% |
| `Years_At_Residence` | 13,340 | 4.45% |
| `Employment_Sector` | 15,287 | 5.10% |
| `Annual_Income_AED` | 14,319 | 4.77% |
| `Monthly_Savings_AED` | 30,645 | 10.21% |
| `Debt_To_Income_Ratio` | 19,646 | 6.55% |
| `Credit_Score` | 20,786 | 6.93% |
| `Existing_Properties` | 23,448 | 7.82% |
| `Preferred_Property_Type` | 26,365 | 8.79% |
| `Estimated_Budget_AED` | 31,855 | 10.62% |
| `Mortgage_Interest_Rate_Pct` | 14,322 | 4.77% |
| `RealEstate_10Yr_Trend` | 26,442 | 8.81% |

## Inconsistent values and formats

| Field / observed variant | Count |
|---|---:|
| `City_Emirate`: `Dxb` | 2,829 |
| `City_Emirate`: `dubai` | 5,504 |
| `City_Emirate`: `ABU DHABI` | 2,743 |
| `Current_Housing`: `rent` | 8,326 |
| `Current_Housing`: `Renting ` | 5,379 |
| `Preferred_Property_Type`: `apt` | 5,413 |
| `Preferred_Property_Type`: `VILLA` | 5,445 |
| `Gender`: `M` | 11,003 |
| `Gender`: `F` | 11,038 |
| `Gender`: `Unknown` | 5,604 |
| `Education_Level`: `HS` | 5,451 |
| `Education_Level`: `bachelor` | 5,348 |
| `RealEstate_10Yr_Trend`: `Increase ` | 901 |
| `RealEstate_10Yr_Trend`: `Drop Down` | 872 |
| `RealEstate_10Yr_Trend`: `dropped` | 865 |
| `RealEstate_10Yr_Trend`: `increased` | 841 |
| `RealEstate_10Yr_Trend`: `DROPPED` | 838 |
| `RealEstate_10Yr_Trend`: `INCREASED` | 832 |
| `Annual_Income_AED` contains currency, comma or percent formatting | 4,506 |
| `Estimated_Budget_AED` contains currency, comma or percent formatting | 4,007 |
| `Mortgage_Interest_Rate_Pct` contains currency, comma or percent formatting | 3,492 |

## Invalid values and extremes

| Check | Count or observed range |
|---|---:|
| Age outside 18–120 | 1,793 |
| Credit score outside 300–900 | 2,198 |
| Negative dependents | 2,906 |
| Negative debt-to-income ratio | 455 |
| Negative annual income | 558 |
| Residence duration greater than recorded age | 896 |
| Recorded age range | -5 to 999 |
| Parsed annual income range (AED) | -45,000.00 to 150,000,000.00 |

A large value alone does not establish that a record is invalid. Counts may overlap. The notebook performs IQR checks after its cleaning rules.
