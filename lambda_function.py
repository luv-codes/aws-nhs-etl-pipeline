import boto3
import pandas as pd
import io
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']
    print(f"File received: s3://{bucket}/{key}")
    
    
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(response['Body'].read()))
    
    
    total_records = len(df)
    total_columns = len(df.columns)
    
   
    age_band_counts = df['age_band'].value_counts().to_dict()
    
    
    blood_pressure_stats = {
    "systolic_mean":  round(df['systolic_bp'].mean(), 2),
    "systolic_min":   int(df['systolic_bp'].min()),
    "systolic_max":   int(df['systolic_bp'].max()),
    "diastolic_mean": round(df['diastolic_bp'].mean(), 2),
    "diastolic_min":  int(df['diastolic_bp'].min()),
    "diastolic_max":  int(df['diastolic_bp'].max()),
}
    
    
    missing_values = df.isnull().sum().to_dict()
    
    
    summary = {
        "total_records":        total_records,
        "total_columns":        total_columns,
        "age_band_distribution": age_band_counts,
        "blood_pressure_stats":  blood_pressure_stats,
        "missing_values":        missing_values,
    }
    
    print(f"Total records: {total_records}")
    print(f"Summary: {json.dumps(summary, indent=2)}")
    
   
    output_bucket = 'luv-pipeline-output'
    filename      = key.split('/')[-1]
    
    s3.put_object(
        Bucket=output_bucket,
        Key=f"processed/{filename}_summary.json",
        Body=json.dumps(summary, indent=2)
    )
    
    print(f"Output saved to s3://{output_bucket}/processed/{filename}_summary.json")
    return {"statusCode": 200, "body": f"Processed {total_records} records successfully"}