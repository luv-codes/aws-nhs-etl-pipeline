# 🏥 AWS Serverless ETL Pipeline — NHS Data Processing

An event-driven, serverless ETL pipeline built on AWS that automatically 
ingests, processes, and analyses 100,500 NHS patient records in under 2 seconds.

## 🏗️ Architecture

S3 (Input Bucket)
      ↓  [ObjectCreated Event Trigger]
AWS Lambda (nhs-csv-pipeline-processor)
      ↓  [Pandas Processing]
├── Age-band distribution
├── Blood pressure statistics
├── 30-day readmission rates
├── Data quality checks (26 fields)
      ↓
S3 (Output Bucket) → summary_report.json
      ↓
Amazon CloudWatch (Logging & Monitoring)
      ↓
SNS Alert (if readmission rate > 15%)

## 🛠️ Tech Stack

| Service | Purpose |
|---|---|
| Amazon S3 | Input/output data storage |
| AWS Lambda | Serverless compute & processing |
| AWS IAM | Least-privilege security policies |
| Amazon CloudWatch | Logging & monitoring |
| Boto3 | AWS SDK for Python |
| Pandas | Data processing & analysis |

## Data
Full dataset not included due to size. 
A 100-row sample is provided in sample_data/ 
to demonstrate the expected input format.

## 📊 What the Pipeline Analyses

- Total records processed: **100,500**
- Age-band distribution across 6 demographic cohorts
- Systolic/diastolic blood pressure (mean, min, max)
- 30-day readmission rate
- Top 3 most common clinical conditions
- Missing value detection across all 26 columns

## 🔐 IAM Security

Least-privilege IAM policy — Lambda role restricted to:
- `s3:GetObject` on input bucket only
- `s3:PutObject` on output bucket only
- `sns:Publish` on specific SNS topic only
- `logs:*` via AWSLambdaBasicExecutionRole

## 🚀 How to Run

1. Create two S3 buckets: `luv-pipeline-input` and `luv-pipeline-output`
2. Deploy `lambda_function.py` to AWS Lambda (Python 3.12)
3. Add `AWSSDKPandas-Python312` Lambda Layer
4. Attach IAM role with policy from `iam_policy.json`
5. Configure S3 event trigger on input bucket (ObjectCreated, suffix: .csv)
6. Upload any CSV with NHS-format columns to trigger the pipeline

## 📁 Sample Output

```json
{
  "total_records": 100500,
  "total_columns": 26,
  "age_band_distribution": {
    "50-64": 25309,
    "65-79": 21888,
    "35-49": 20142
  },
  "blood_pressure_stats": {
    "systolic_mean": 134.9,
    "systolic_min": 105,
    "systolic_max": 193
  },
  "readmission_rate_pct": 16.3,
  "top_3_conditions": {
    "Hypertension": 18142,
    "Type 2 Diabetes": 15063,
    "Coronary Artery Disease": 12051
  }
}
```

## 👨‍💻 Author

**Luv Agrawal** — BSc Computer Science, University of West London  
[LinkedIn](https://linkedin.com/in/luvagrawaluwl) • [GitHub](https://github.com/luv-codes)
