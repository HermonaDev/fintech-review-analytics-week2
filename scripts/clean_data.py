# scripts/clean_data.py
import pandas as pd

def clean_review_data():
    # Load the scraped data
    df = pd.read_csv('data/bank_reviews.csv')
    
    print(f"Original data: {len(df)} reviews")
    
    # 1. Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=['review', 'bank'])
    print(f"Removed {initial_count - len(df)} duplicate reviews")
    
    # 2. Handle missing data
    missing_before = df.isnull().sum()
    df = df.dropna(subset=['review'])  # Remove rows where review text is missing
    missing_after = df.isnull().sum()
    
    print("\nMissing values before cleaning:")
    print(missing_before)
    print("\nMissing values after cleaning:")
    print(missing_after)
    
    # 3. Ensure date format is consistent (already done in scraping, but double-check)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # 4. Save cleaned data
    cleaned_file = 'data/cleaned_bank_reviews.csv'
    df.to_csv(cleaned_file, index=False)
    
    print(f"\nCleaned data saved: {len(df)} reviews")
    print("\nFinal count by bank:")
    print(df['bank'].value_counts())
    
    # Calculate data quality metrics
    total_reviews = len(df)
    missing_percentage = (missing_after.sum() / (len(df.columns) * total_reviews)) * 100
    print(f"\nData Quality: {missing_percentage:.2f}% missing data (target: <5%)")
    
    return df

if __name__ == "__main__":
    clean_review_data()