import pandas as pd

from data_loader.data_loader import SQLLoader


def getSchemaDataModel(df):
    pk_candidates = [col for col in df.columns if df[col].is_unique and df[col].notna().all()]
    total_records = len(df)

    return pk_candidates, total_records

def getDataQuality(df):
    quality_report = pd.concat([
        df.isnull().sum(),
        (df.isnull().mean() * 100).round(2),
    ], axis=1, keys=["Total Nulls", "Percentage (%)"])
    duplicate_rows = df[df.duplicated(keep=False)]
    num_duplicates = len(duplicate_rows)
    return quality_report, num_duplicates, duplicate_rows

def main():
    loader = SQLLoader()
    df = loader.load_table("site-list")
    print(df.head())
    pk_candidates, total_records = getSchemaDataModel(df)
    print("="*40)
    print("Schema Data Model Analysis:")
    print("Primary key candidate(s):", pk_candidates)
    print("Total records:", total_records)
    print("="*40)
    quality_report, num_duplicates, duplicate_rows = getDataQuality(df)
    print("Data Quality Report:")
    print(quality_report)
    print(f"\nNumber of duplicate rows: {num_duplicates}")
    if num_duplicates > 0:
        print("Duplicate rows:")
        print(duplicate_rows)

if __name__ == "__main__":
    main()
