from data_loader.data_loader import SQLLoader
import pandas as pd

def getSchemaDataModel(df):
    pk_candidates = [col for col in df.columns if df[col].is_unique and df[col].notna().all()]
    total_records = len(df)

    if "ID" in pk_candidates:
        return ["ID"], total_records

    return pk_candidates, total_records

def getDataQuality(df):
    quality_report = pd.concat([df.isnull().sum(), df.isnull().mean() * 100], axis=1, keys=['Total Nulls', 'Percentage (%)'])
    return quality_report

def main():
    loader = SQLLoader()
    apex_df = loader.load_table("apex-sss")
    print(apex_df.head())
    pk_candidates, total_records = getSchemaDataModel(apex_df)
    print(f"="*40)
    print("Schema Data Model Analysis:")
    print("Primary key candidate(s):", pk_candidates)
    print("Total records:", total_records)
    print(f"="*40)
    quality_report = getDataQuality(apex_df)
    print("Data Quality Report:")
    quality_report = getDataQuality(apex_df)
    print(quality_report)

if __name__ == "__main__":
    main()
