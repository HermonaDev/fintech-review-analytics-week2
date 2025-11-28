import pandas as pd

def interim_summary():
    # Load sentiment data
    df = pd.read_csv('data/reviews_with_sentiment.csv')
    
    print("=== INTERIM ANALYSIS SUMMARY ===")
    print(f"Reviews analyzed: {len(df)}")
    
    # Sentiment by bank
    print("\nSentiment by Bank:")
    sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])
    print(sentiment_by_bank)
    
    # Rating vs Sentiment
    print("\nRating vs Sentiment:")
    rating_sentiment = pd.crosstab(df['rating'], df['sentiment_label'])
    print(rating_sentiment)
    
    # Basic insights
    print(f"\nKey Insights:")
    print(f"- {df['sentiment_label'].value_counts()['NEGATIVE']/len(df)*100:.1f}% of reviews are negative")
    print(f"- Average rating: {df['rating'].mean():.1f} stars")
    print(f"- Most common rating: {df['rating'].mode().iloc[0]} stars")

if __name__ == "__main__":
    interim_summary()