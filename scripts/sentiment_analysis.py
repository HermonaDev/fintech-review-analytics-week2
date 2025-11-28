# scripts/sentiment_analysis.py
import pandas as pd
from transformers import pipeline
import time

def analyze_sentiment_batch(texts):
    """Analyze sentiment for a batch of texts using DistilBERT"""
    classifier = pipeline("sentiment-analysis", 
                         model="distilbert-base-uncased-finetuned-sst-2-english")
    results = classifier(texts)
    return results

def main():
    # Load cleaned data
    df = pd.read_csv('data/cleaned_bank_reviews.csv')
    print(f"Analyzing sentiment for {len(df)} reviews...")
    
    # Sample first 400 reviews for interim submission
    sample_df = df.head(400).copy()
    
    # Analyze sentiment in batches to avoid memory issues
    batch_size = 50
    sentiments = []
    scores = []
    
    for i in range(0, len(sample_df), batch_size):
        batch = sample_df['review'].iloc[i:i+batch_size].tolist()
        print(f"Processing batch {i//batch_size + 1}/{(len(sample_df)//batch_size)+1}")
        
        try:
            results = analyze_sentiment_batch(batch)
            for result in results:
                sentiments.append(result['label'])
                scores.append(result['score'])
        except Exception as e:
            print(f"Error in batch {i//batch_size + 1}: {e}")
            # Fallback: add neutral sentiment for failed batches
            sentiments.extend(['NEUTRAL'] * len(batch))
            scores.extend([0.5] * len(batch))
        
        time.sleep(1)  # Be nice to the API
    
    # Add results to dataframe
    sample_df['sentiment_label'] = sentiments
    sample_df['sentiment_score'] = scores
    
    # Save results
    sample_df.to_csv('data/reviews_with_sentiment.csv', index=False)
    print(f"Sentiment analysis complete for {len(sample_df)} reviews")
    
    # Print summary
    print("\nSentiment Distribution:")
    print(sample_df['sentiment_label'].value_counts())
    print(f"\nAverage sentiment score: {sample_df['sentiment_score'].mean():.3f}")

if __name__ == "__main__":
    main()