# scripts/create_interim_visualizations.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# Set style for professional reports
plt.style.use('seaborn-v0_8')
rcParams['figure.figsize'] = (10, 6)
sns.set_palette("husl")

def create_review_count_chart():
    """Create bar chart of reviews by bank"""
    df = pd.read_csv('data/cleaned_bank_reviews.csv')
    
    review_counts = df['bank'].value_counts()
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(review_counts.index, review_counts.values, color=['#2E86AB', '#A23B72', '#F18F01'])
    plt.title('Review Counts by Bank', fontsize=16, fontweight='bold')
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('outputs/review_counts.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return review_counts

def create_rating_distribution():
    """Create rating distribution chart"""
    df = pd.read_csv('data/cleaned_bank_reviews.csv')
    
    plt.figure(figsize=(10, 6))
    rating_counts = df['rating'].value_counts().sort_index()
    
    bars = plt.bar(rating_counts.index.astype(str), rating_counts.values, color='#2E86AB')
    plt.title('Overall Rating Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Star Rating', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('outputs/rating_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return rating_counts

def create_sentiment_breakdown():
    """Create sentiment analysis results chart"""
    df = pd.read_csv('data/reviews_with_sentiment.csv')
    
    # Sentiment distribution
    sentiment_counts = df['sentiment_label'].value_counts()
    
    plt.figure(figsize=(8, 8))
    colors = ['#FF6B6B', '#4ECDC4']  # Red for negative, Teal for positive
    plt.pie(sentiment_counts.values, labels=sentiment_counts.index, 
            autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Sentiment Distribution (400 Reviews)', fontsize=16, fontweight='bold')
    plt.savefig('outputs/sentiment_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return sentiment_counts

def create_rating_sentiment_heatmap():
    """Create heatmap of rating vs sentiment"""
    df = pd.read_csv('data/reviews_with_sentiment.csv')
    
    # Cross tabulation
    cross_tab = pd.crosstab(df['rating'], df['sentiment_label'])
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cross_tab, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Number of Reviews'})
    plt.title('Rating vs Sentiment Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Sentiment Label', fontsize=12)
    plt.ylabel('Star Rating', fontsize=12)
    plt.tight_layout()
    plt.savefig('outputs/rating_sentiment_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return cross_tab

def main():
    # Create outputs directory
    import os
    os.makedirs('outputs', exist_ok=True)
    
    print("Creating interim visualizations...")
    
    # Generate all charts
    review_counts = create_review_count_chart()
    rating_dist = create_rating_distribution()
    sentiment_dist = create_sentiment_breakdown()
    heatmap_data = create_rating_sentiment_heatmap()
    
    print("Visualizations created in 'outputs/' folder:")
    print("- review_counts.png")
    print("- rating_distribution.png") 
    print("- sentiment_distribution.png")
    print("- rating_sentiment_heatmap.png")
    
    # Print data summaries for report tables
    print("\nDATA SUMMARIES FOR REPORT:")
    print(f"\nReview Counts by Bank:\n{review_counts}")
    print(f"\nRating Distribution:\n{rating_dist}")
    print(f"\nSentiment Distribution:\n{sentiment_dist}")
    print(f"\nRating vs Sentiment:\n{heatmap_data}")

if __name__ == "__main__":
    main()