import pandas as pd

def validate_data():
    df = pd.read_csv('data/cleaned_bank_reviews.csv')
    
    print("=== DATA VALIDATION ===")
    print(f"Total reviews: {len(df)}")
    print(f"Banks covered: {df['bank'].nunique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Rating distribution:\n{df['rating'].value_counts().sort_index()}")
    
    # Check if we meet requirements
    assert len(df) >= 1200, f"Only {len(df)} reviews, need 1200+"
    assert df['bank'].nunique() == 3, "Not all banks are represented"
    
    print("✅ All validation checks passed!")

if __name__ == "__main__":
    validate_data()