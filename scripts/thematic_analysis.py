# scripts/thematic_analysis.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def extract_keywords(df, n_keywords=20):
    """Extract top keywords using TF-IDF"""
    
    # Focus on negative reviews for pain points
    negative_reviews = df[df['sentiment_label'] == 'NEGATIVE']['review'].fillna('')
    
    if len(negative_reviews) < 10:
        return []
    
    # TF-IDF for unigrams and bigrams
    vectorizer = TfidfVectorizer(
        max_features=n_keywords*2,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2
    )
    
    tfidf_matrix = vectorizer.fit_transform(negative_reviews)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top keywords by average TF-IDF score
    scores = np.mean(tfidf_matrix.toarray(), axis=0)
    top_keywords = sorted(zip(feature_names, scores), 
                         key=lambda x: x[1], reverse=True)[:n_keywords]
    
    return top_keywords

def topic_modeling_analysis(df, n_topics=4):
    """Perform topic modeling using NMF"""
    
    negative_reviews = df[df['sentiment_label'] == 'NEGATIVE']['review'].fillna('')
    
    if len(negative_reviews) < 20:
        return {}
    
    # TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(
        max_features=100,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.8
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(negative_reviews)
    
    # Apply NMF
    try:
        nmf = NMF(n_components=n_topics, random_state=42, alpha=.1, l1_ratio=.5)
        nmf_features = nmf.fit_transform(tfidf_matrix)
        
        # Get top words for each topic
        feature_names = tfidf_vectorizer.get_feature_names_out()
        
        topics = {}
        for topic_idx, topic in enumerate(nmf.components_):
            top_features_ind = topic.argsort()[:-11:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            topics[f'Topic_{topic_idx+1}'] = top_features
    except:
        topics = {}
    
    return topics

def analyze_by_bank(df):
    """Analyze keywords separately for each bank"""
    banks = df['bank'].unique()
    bank_keywords = {}
    
    for bank in banks:
        bank_reviews = df[df['bank'] == bank]
        bank_negative = bank_reviews[bank_reviews['sentiment_label'] == 'NEGATIVE']
        
        if len(bank_negative) < 5:
            bank_keywords[bank] = []
            continue
        
        vectorizer = TfidfVectorizer(
            max_features=10,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        tfidf_matrix = vectorizer.fit_transform(bank_negative['review'].fillna(''))
        feature_names = vectorizer.get_feature_names_out()
        scores = np.mean(tfidf_matrix.toarray(), axis=0)
        
        top_keywords = sorted(zip(feature_names, scores), 
                            key=lambda x: x[1], reverse=True)[:8]
        
        bank_keywords[bank] = top_keywords
    
    return bank_keywords

def main():
    # Load sentiment data
    df = pd.read_csv('data/full_sentiment_analysis.csv')
    
    print("=== ADVANCED THEMATIC ANALYSIS ===")
    print(f"Total reviews: {len(df)}")
    print(f"Negative reviews: {len(df[df['sentiment_label'] == 'NEGATIVE'])}")
    
    # 1. Overall keyword extraction
    print("\n1. TOP KEYWORDS FROM NEGATIVE REVIEWS:")
    top_keywords = extract_keywords(df, n_keywords=15)
    
    for i, (keyword, score) in enumerate(top_keywords, 1):
        print(f"  {i:2d}. {keyword:20s} {score:.4f}")
    
    # 2. Topic modeling
    print("\n2. TOPIC MODELING (NMF):")
    topics = topic_modeling_analysis(df, n_topics=4)
    
    if topics:
        for topic_name, words in topics.items():
            print(f"\n  {topic_name}:")
            print(f"    {', '.join(words[:5])}")
    else:
        print("  Not enough negative reviews for topic modeling")
    
    # 3. Bank-specific analysis
    print("\n3. BANK-SPECIFIC KEYWORDS:")
    bank_keywords = analyze_by_bank(df)
    
    for bank, keywords in bank_keywords.items():
        if keywords:
            print(f"\n  {bank}:")
            for keyword, score in keywords[:5]:
                print(f"    - {keyword:20s} {score:.4f}")
        else:
            print(f"\n  {bank}: Not enough negative reviews")
    
    # 4. Business theme mapping
    print("\n4. BUSINESS THEME MAPPING:")
    themes = {
        'Technical Issues': ['crash', 'error', 'bug', 'freeze', 'technical', 'not working'],
        'Transaction Problems': ['transaction', 'transfer', 'money', 'payment', 'balance', 'failed'],
        'User Experience': ['slow', 'update', 'time', 'app', 'working', 'use', 'difficult'],
        'Account & Security': ['login', 'account', 'password', 'security', 'access', 'otp'],
        'Customer Support': ['customer service', 'help', 'support', 'response', 'fix', 'contact']
    }
    
    for theme, terms in themes.items():
        print(f"\n  {theme}:")
        matching_keywords = []
        for keyword, score in top_keywords:
            if any(term in keyword for term in terms):
                matching_keywords.append((keyword, score))
        
        if matching_keywords:
            for keyword, score in matching_keywords[:3]:
                print(f"    - {keyword} (score: {score:.4f})")
        else:
            print(f"    No direct matches in top keywords")

if __name__ == "__main__":
    main()