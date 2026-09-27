# Bank GoodCredit – Credit Risk Assessment & Scoring

## Project Overview

**Project Type:** Classification / Credit Risk Ranking  
**Domain:** Banking – Risk  
**Project Reference:** PM-PR-0015  
**Target Variable:** `Bad_label`

Bank GoodCredit wants to predict the creditworthiness / credit risk of current credit-card customers and reduce credit default risk.

The target variable is:

- `0` – Good credit history
- `1` – Bad credit history (30 DPD+ bucket)

The official project benchmark is **Gini = 37.9%**.

This project builds a customer-level machine learning solution that combines demographic/application information with historical account, payment-history, and credit-enquiry behaviour. The model produces a probability of bad credit and ranks customers by predicted risk.

---

## Problem Statement

Build a machine learning model that predicts the probability that a current credit-card customer will have bad credit history (`Bad_label = 1`) using:

1. Customer demographic/application attributes
2. Historical account and payment behaviour
3. Historical credit-enquiry behaviour

The project is primarily a **credit-risk ranking problem**, so model quality is evaluated using **ROC-AUC, Gini, and 10-decile rank ordering**, rather than relying only on classification accuracy.

---

## Dataset

The project uses three main data sources.

### 1. Cust_Demographics.csv

Customer/application-level data containing:

- `customer_no`
- `dt_opened`
- `entry_time`
- `feature_1` ... `feature_79`
- `Bad_label`

The demographic features are anonymized/obscured in the supplied project data, so no unsupported business meanings are assigned to `feature_1`–`feature_79`.

### 2. Cust_Account.csv

Historical account and payment information including:

- Account type and ownership
- Account opening/closing/reporting dates
- Current balance
- High credit amount
- Credit limit
- Cash limit
- Amount past due
- Payment history
- Payment frequency
- Actual payment amount
- Interest rate

### 3. Cust_Enquiry.csv

Historical credit-enquiry information including:

- Enquiry date
- Enquiry purpose
- Enquiry amount
- Customer identifier

`Cust_Enquiry.csv.xlsx` is treated only as a parallel export/check and is not used as a second copy of the modelling data.

---

## Project Architecture

```text
                 ┌─────────────────────────┐
                 │ Cust_Demographics.csv    │
                 │ Customer + Target        │
                 └────────────┬────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
Cust_Account.csv      Cust_Enquiry.csv       Demographic Features
       │                      │
       ▼                      ▼
Customer-level         Customer-level
Account Features       Enquiry Features
       │                      │
       └──────────────┬───────┘
                      ▼
           Customer-level Feature Matrix
                      │
                      ▼
            Data Quality / Leakage Check
                      │
                      ▼
              Feature Engineering
                      │
                      ▼
             Train / Validation / Test
                      │
                      ▼
             Feature Selection
                      │
                      ▼
       Baseline + Boosting Model Comparison
                      │
                      ▼
             Hyperparameter Tuning
                      │
                      ▼
                 Final Model
                      │
             ┌────────┴─────────┐
             ▼                  ▼
        Gini / AUC        Rank Ordering
                             / Deciles
```

---

## Data Preparation

The account and enquiry tables contain multiple records for the same customer. Therefore, raw one-to-many records are **not directly joined** to the demographic table.

Instead:

- Account data is aggregated by `customer_no`
- Enquiry data is aggregated by `customer_no`
- The aggregated features are merged with the customer-level demographics table
- The final modelling table is verified to contain **one row per customer**

The pipeline also checks for duplicate rows, missing values, invalid dates, unexpected values, and potential target/future-information leakage.

---

## Feature Engineering

Feature engineering focuses on customer behaviour and credit-risk signals.

### Account Features

Examples include:

- Total account count
- Active account count
- Closed account count
- Total current balance
- Mean/max current balance
- Total high credit
- Total/mean credit limit
- Cash-limit aggregates
- Total amount past due
- Actual payment aggregates
- Account age/activity features

### Credit Utilization

Utilization-related features capture the relationship between outstanding balance and available credit.

Example:

```text
Credit Utilization
= Total Current Balance / Total Credit Limit
```

Additional utilization and log-transformed features are used where appropriate.

### Payment History

The payment-history variables are parsed into customer-level delinquency features.

The implementation distinguishes known statuses from unknown history. In particular, `XXX` is treated as **unknown/missing**, rather than being interpreted as zero days past due.

Derived features include concepts such as:

- Payment history length
- Average DPD
- 0–29 DPD behaviour
- 30+ DPD counts
- 60+ DPD counts
- 90+ DPD counts
- Maximum DPD
- Delinquency-account ratios
- Timing of first 30+ DPD

### Enquiry Features

Customer-level enquiry features include:

- Total enquiry count
- Recent enquiry counts
- Enquiry amount aggregates
- Unique enquiry-purpose count
- Frequent enquiry purpose
- Enquiry recency
- Enquiry frequency / velocity
- Difference between enquiry dates and application dates

The project brief also suggests enquiry-recency and utilization features as useful modelling candidates.

---

## Exploratory Data Analysis

The notebook follows the template's EDA structure and includes meaningful univariate, bivariate, and relationship analysis.

The analysis covers:

- Target-class distribution
- Missing-value patterns
- Account balances
- Amount past due
- Credit utilization
- Account counts
- Enquiry counts
- Enquiry amounts
- Enquiry recency
- Payment-history structure
- Account-type distribution
- Enquiry-purpose distribution
- Utilization distribution

Each chart is accompanied by:

1. Why the chart was selected
2. What insight the chart provides
3. How the insight can support business impact / modelling decisions

---

## Data Leakage Prevention

Credit-risk modelling is sensitive to future-information leakage.

The notebook checks relevant application, account, payment, reporting, closing, and enquiry dates before creating behavioural features.

The following principles are followed:

- `Bad_label` is never used as a predictor
- Future information is excluded from feature construction
- Feature engineering is performed at customer level
- Test data is kept out of feature selection and tuning
- Training-only fitting is used for learned preprocessing and feature selection

---

## Feature Selection

Feature selection is performed using training data.

CatBoost and XGBoost feature importance/gain are combined into a blended selection score.

The project uses a **66-feature selected matrix**, aligned with the supplied project's 66-feature benchmark configuration.

The final notebook generates a feature matrix containing:

- Feature
- Feature group
- Selection importance/gain
- CatBoost importance
- XGBoost gain
- Description

---

## Machine Learning Models

The notebook evaluates multiple classification algorithms, including:

- Logistic Regression
- Decision Tree
- Random Forest
- LightGBM
- XGBoost
- CatBoost

The strongest candidate models are subsequently tuned using cross-validation.

The final model is selected using out-of-sample performance rather than training accuracy.

---

## Evaluation Metrics

### ROC-AUC

Measures the model's ability to rank positive and negative cases across classification thresholds.

### Gini

For this project:

```text
Gini = 2 × ROC-AUC − 1
```

The official benchmark is:

```text
Gini = 37.9%
```

### Precision

Measures how many customers predicted as bad are actually bad.

### Recall

Measures how many actual bad customers are identified by the model.

### F1 Score

Balances precision and recall.

### PR-AUC

Useful when the bad-credit class is relatively uncommon.

### KS Statistic

Measures separation between the score distributions of the two target classes.

### Rank Ordering

Customers are sorted using predicted probability of `Bad_label = 1` and grouped into 10 risk deciles.

The notebook uses the convention:

```text
Decile 1  = Highest predicted risk
...
Decile 10 = Lowest predicted risk
```

---

## Latest Observed Model Performance

The latest full notebook run displayed:

| Metric | Result |
|---|---:|
| ROC-AUC | **0.6948** |
| Gini | **38.97%** |
| Official Benchmark Gini | **37.90%** |
| Difference | **+1.07 Gini points** |
| Selected Features | **66** |

The observed run therefore exceeded the supplied benchmark Gini.

> Re-run the notebook from a clean kernel before publishing new results, because metrics are generated dynamically from the current data and code.

---

## Rank Ordering

The final model produces a customer-level risk score:

```text
predicted_bad_probability
```

Customers are ranked from highest to lowest predicted probability of `Bad_label = 1`.

The notebook generates a 10-decile table containing:

- Customer count
- Bad count
- Good count
- Bad rate
- Lift
- Cumulative bad percentage
- Benchmark bad rate

This allows the model's risk-separation behaviour to be compared with the project benchmark.

---

## Project Outputs

The notebook generates an output directory containing files such as:

```text
outputs/
└── final_run/
    ├── validation_model_comparison.csv
    ├── benchmark_comparison.csv
    ├── rank_ordering.csv
    ├── feature_matrix_gain.csv
    ├── selected_66_features.csv
    └── test_predictions_ranked.csv
```

### `test_predictions_ranked.csv`

Contains customer-level model predictions and risk ranking information.

Typical fields include:

- `customer_no`
- Actual target
- `predicted_bad_probability`
- Risk decile

### `rank_ordering.csv`

Contains the 10-decile risk-ranking analysis.

### `feature_matrix_gain.csv`

Contains selected features and model importance/gain information.

### `selected_66_features.csv`

Contains the selected 66-feature model matrix.

---

## Key Project Insights

The project demonstrates that historical credit behaviour contains useful predictive information for credit-risk ranking.

Important engineered signal groups include:

- Payment/delinquency behaviour
- Credit utilization
- Account history
- Account activity
- Enquiry frequency
- Enquiry recency
- Enquiry-purpose behaviour

The project also demonstrates why a credit-risk model should not be judged only by accuracy, particularly when the bad-credit class is relatively uncommon.

---

## Business Impact

The model provides a **risk-ranking score** rather than an automatic approval/decline decision.

The predicted risk ranking can support a bank's broader credit-risk process by helping identify customers who require different levels of review or risk-management attention.

The model output should be treated as a decision-support signal, with final actions determined by the bank's policies and controls.

---

## Limitations

- Demographic features are anonymized, limiting direct business interpretation.
- The available project data is historical and may not represent future populations.
- Model performance depends on the supplied observation period and data quality.
- Credit-risk relationships can change over time.
- A model benchmark comparison does not by itself establish production readiness.
- Further out-of-time validation and monitoring would be appropriate before real-world deployment.

---

## Future Work

Potential future improvements include:

- Larger out-of-time validation windows
- More extensive hyperparameter search
- Probability calibration
- Model stability monitoring
- Population Stability Index (PSI)
- Explainability using SHAP
- Drift detection
- Model monitoring and retraining pipelines
- Deployment as an API or batch scoring service
- Integration with a governed credit-risk decision workflow

---

## Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- Scikit-learn
- Matplotlib
- LightGBM
- XGBoost
- CatBoost
- Joblib
- Jupyter Notebook

---

## Repository Structure

```text
Bank-GoodCredit-Credit-Risk/
│
├── Bank_GoodCredit_Credit_Risk_FINAL_Template_Fixed.ipynb
├── Cust_Demographics.csv
├── Cust_Account.csv
├── Cust_Enquiry.csv
├── Cust_Enquiry.csv.xlsx
├── requirements.txt
├── README.md
│
└── outputs/
    └── final_run/
        ├── validation_model_comparison.csv
        ├── benchmark_comparison.csv
        ├── rank_ordering.csv
        ├── feature_matrix_gain.csv
        ├── selected_66_features.csv
        └── test_predictions_ranked.csv
```

---

## How to Run

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Bank-GoodCredit-Credit-Risk
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter

```bash
jupyter notebook
```

### 4. Open the notebook

Open:

```text
Bank_GoodCredit_Credit_Risk_FINAL_Template_Fixed.ipynb
```

### 5. Run the complete notebook

Use:

```text
Kernel → Restart Kernel
Kernel → Run All
```

The notebook generates the EDA, feature engineering, model evaluation, Gini, rank ordering, feature-gain matrix, and prediction outputs.

---

## Expected Final Deliverables

The completed project provides:

- Data exploration insights
- Data-cleaning and wrangling logic
- Customer-level feature engineering
- Leakage checks
- Selected 66-feature matrix
- Model comparison
- Cross-validation and tuning
- Final model
- ROC-AUC and Gini
- Rank-ordering / decile analysis
- Feature importance / gain
- Customer-level risk predictions
- Benchmark comparison

These deliverables correspond to the core requirements of the supplied Bank GoodCredit project brief.
