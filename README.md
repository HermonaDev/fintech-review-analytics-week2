# Fintech Customer Experience Analytics

Analysis of Google Play Store reviews for Ethiopian banking apps to identify customer satisfaction drivers and pain points.

## 📊 Project Overview

Omega Consultancy engaged this analysis to help three Ethiopian banks improve their mobile app customer experience:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

**Objective:** Scrape, analyze, and visualize 1,200+ user reviews to provide actionable recommendations for app improvement.

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/YOUR_USERNAME/fintech-review-analytics-week2.git
cd fintech-review-analytics-week2
pip install -r requirements.txt
```

### 2. Run Full Pipeline

```bash
# 1. Data collection
python scripts/scrape_reviews.py

# 2. Data cleaning
python scripts/clean_data.py

# 3. Sentiment analysis
python scripts/sentiment_analysis.py --sample 2000

# 4. Thematic analysis
python scripts/thematic_analysis.py

# 5. Database setup
python scripts/database_setup.py

# 6. Visualizations & insights
python scripts/final_visualizations.py
```

## 📁 Project Structure

```
fintech-review-analytics-week2/
├── scripts/               # Analysis pipeline
│   ├── scrape_reviews.py      # Google Play scraping
│   ├── clean_data.py          # Data preprocessing
│   ├── sentiment_analysis.py  # DistilBERT sentiment analysis
│   ├── thematic_analysis.py   # TF-IDF keyword extraction
│   ├── database_setup.py      # PostgreSQL/SQLite setup
│   └── final_visualizations.py # Insights & charts
├── data/                  # Processed datasets
│   ├── cleaned_bank_reviews.csv
│   ├── full_sentiment_analysis.csv
│   └── bank_reviews.db (SQLite)
├── outputs/              # Generated visualizations
│   ├── sentiment_rating_by_bank.png
│   ├── sentiment_trends.png
│   ├── wordclouds.png
│   └── rating_distribution_by_bank.png
├── docs/                 # Reports
│   ├── interim_report.md
│   └── final_report.md
├── tests/                # Unit tests
├── github/workflows/     # CI/CD pipeline
└── requirements.txt      # Dependencies
```

## 📈 Key Findings

### Sentiment Analysis (2,000 reviews)

- **Overall:** 54.7% Positive, 45.3% Negative
- **By Bank:**
  - Dashen Bank: 67.3% Positive (Highest)
  - CBE: 56.5% Positive
  - BOA: 44.4% Positive (Lowest)

### Average Ratings

1. **Dashen Bank:** 4.26 ⭐
2. **CBE:** 3.85 ⭐  
3. **BOA:** 3.15 ⭐

### Top Pain Points

1. **Transaction delays & failures**
2. **App crashes after updates**
3. **Slow performance**
4. **Authentication issues**

## 💡 Recommendations

### Commercial Bank of Ethiopia

1. Fix transaction processing system to prevent false failures
2. Improve app stability with better regression testing
3. Enhance customer support with in-app chat

### Bank of Abyssinia

1. Optimize app performance (reduce loading time by 50%)
2. Resolve login/authentication issues
3. Simplify UI/UX navigation

### Dashen Bank

1. Optimize app size (reduce from current 45MB)
2. Fix transfer feature reliability
3. Implement biometric authentication

## 🗄️ Database Schema

### PostgreSQL Tables

```sql
-- Banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table  
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score DECIMAL(5,4),
    source VARCHAR(50) DEFAULT 'Google Play',
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Technologies Used

- **Python 3.9+**: Data processing & analysis
- **PostgreSQL 15**: Relational database
- **Google Play Scraper**: Review collection
- **Transformers (DistilBERT)**: Sentiment analysis
- **scikit-learn**: TF-IDF & topic modeling
- **Matplotlib/Seaborn**: Data visualization
- **Git/GitHub**: Version control & collaboration

## 📋 Requirements

See `requirements.txt` for full dependency list.

## 📄 Reports

- **[Interim Report](docs/WEEK%202%20INTERIM%20REPORT_%20CUSTOMER%20EXPERIENCE%20ANALYTICS%20FOR%20FINTECH%20APPS.pdf)**: Task 1 & partial Task 2
- **[Final Report](docs/WEEK_2_FINAL%20REPORT_%20CUSTOMER%20EXPERIENCE%20ANALYTICS%20FOR%20ETHIOPIAN%20FINTECH%20APPS.pdf)**: Complete analysis with recommendations


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is for educational purposes as part of 10 Academy training.

## 🙏 Acknowledgments

- **10 Academy** for the learning opportunity
- **Omega Consultancy** for the business context
- **Google Play Store** as data source