# scripts/thematic_analysis.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_keywords(df):
    """Extract top keywords using TF-IDF"""
    
    # Focus on negative reviews for pain points
    negative_reviews = df[df['sentiment_label'] == 'NEGATIVE']['review']
    
    # TF-IDF for unigrams and bigrams
    vectorizer = TfidfVectorizer(
        max_features=50,
        stop_words='english',
        ngram_range=(1, 2),  # single words and two-word phrases
        min_df=2  # ignore terms that appear in only 1 review
    )
    
    tfidf_matrix = vectorizer.fit_transform(negative_reviews)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top keywords by average TF-IDF score
    scores = np.mean(tfidf_matrix.toarray(), axis=0)
    top_keywords = sorted(zip(feature_names, scores), 
                         key=lambda x: x[1], reverse=True)[:20]
    
    return top_keywords

def manual_theme_clustering(keywords):
    """Manually cluster keywords into themes"""
    themes = {
        'Technical Issues': ['crash', 'error', 'not working', 'login problem', 'update issue', 'bug', 'freeze', 'doesn work', 'technical'],
        'Transaction Problems': ['transfer', 'transaction failed', 'money', 'payment', 'slow transfer', 'balance', 'transaction', 'transactions', 'failed'],
        'User Experience': ['slow', 'difficult', 'interface', 'update', 'better', 'use', 'time', 'phone', 'history', 'working'],
        'Customer Support': ['customer service', 'help', 'support', 'response', 'fix']
    }
    
    # Match keywords to themes
    theme_keywords = {theme: [] for theme in themes}
    unassigned = []
    
    for keyword, score in keywords:
        assigned = False
        for theme, theme_words in themes.items():
            if any(theme_word in keyword for theme_word in theme_words):
                theme_keywords[theme].append((keyword, score))
                assigned = True
                break
        if not assigned:
            unassigned.append((keyword, score))
    
    # Add unassigned common words to relevant themes
    for keyword, score in unassigned:
        if keyword in ['app', 'bank', 'cbe']:
            theme_keywords['User Experience'].append((keyword, score))
    
    return theme_keywords

def main():
    df = pd.read_csv('data/reviews_with_sentiment.csv')
    
    print("=== THEMATIC ANALYSIS ===")
    print(f"Analyzing {len(df)} reviews...")
    
    # Extract keywords
    top_keywords = extract_keywords(df)
    print("\nTop 20 Keywords from Negative Reviews:")
    for keyword, score in top_keywords:
        print(f"  {keyword}: {score:.4f}")
    
    # Cluster into themes
    themes = manual_theme_clustering(top_keywords)
    
    print("\nIdentified Themes:")
    for theme, keywords in themes.items():
        if keywords:
            print(f"\n{theme}:")
            for keyword, score in keywords[:3]:  # Top 3 per theme
                print(f"  - {keyword} (score: {score:.4f})")

if __name__ == "__main__":
    main()