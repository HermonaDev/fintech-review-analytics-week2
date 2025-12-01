# scripts/sentiment_analysis.py
import pandas as pd
from transformers import pipeline
import time
from tqdm import tqdm

def analyze_sentiment_batch(texts, classifier):
    """Analyze sentiment for a batch of texts"""
    results = classifier(texts)
    return results

def analyze_full_dataset(sample_size=None):
    """Analyze sentiment for full or sampled dataset"""
    # Load cleaned data
    df = pd.read_csv('data/cleaned_bank_reviews.csv')
    
    if sample_size:
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    print(f"Analyzing sentiment for {len(df)} reviews...")
    
    # Initialize model once
    classifier = pipeline("sentiment-analysis", 
                         model="distilbert-base-uncased-finetuned-sst-2-english")
    
    # Process in batches
    batch_size = 32
    sentiments = []
    scores = []
    
    for i in tqdm(range(0, len(df), batch_size), desc="Processing"):
        batch = df['review'].iloc[i:i+batch_size].tolist()
        batch = [str(text)[:512] for text in batch]  # Truncate to model limit
        
        try:
            results = analyze_sentiment_batch(batch, classifier)
            for result in results:
                sentiments.append(result['label'])
                scores.append(result['score'])
        except Exception as e:
            print(f"Error in batch {i}: {e}")
            sentiments.extend(['NEUTRAL'] * len(batch))
            scores.extend([0.5] * len(batch))
        
        # Brief pause every 10 batches
        if i > 0 and i % (batch_size * 10) == 0:
            time.sleep(1)
    
    # Add results to dataframe
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    
    return df

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Sentiment analysis for bank reviews')
    parser.add_argument('--sample', type=int, default=2000, 
                       help='Number of reviews to sample (default: 2000)')
    parser.add_argument('--output', type=str, default='data/full_sentiment_analysis.csv',
                       help='Output file path')
    
    args = parser.parse_args()
    
    # Analyze dataset
    result_df = analyze_full_dataset(sample_size=args.sample)
    
    # Save results
    result_df.to_csv(args.output, index=False)
    print(f"\nSaved {len(result_df)} analyzed reviews to {args.output}")
    
    # Generate summary report
    print("\n=== SENTIMENT ANALYSIS REPORT ===")
    print(f"Total reviews analyzed: {len(result_df)}")
    
    sentiment_counts = result_df['sentiment_label'].value_counts()
    for label, count in sentiment_counts.items():
        percentage = count / len(result_df) * 100
        print(f"{label}: {count} ({percentage:.1f}%)")
    
    print("\n=== BY BANK ===")
    for bank in result_df['bank'].unique():
        bank_data = result_df[result_df['bank'] == bank]
        neg_count = (bank_data['sentiment_label'] == 'NEGATIVE').sum()
        neg_pct = neg_count / len(bank_data) * 100
        print(f"{bank}: {len(bank_data)} reviews, {neg_count} negative ({neg_pct:.1f}%)")

if __name__ == "__main__":
    main()