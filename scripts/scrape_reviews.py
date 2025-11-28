# scrape_reviews.py
import pandas as pd
from google_play_scraper import app, Sort, reviews_all
import time

# App IDs for the three banks
# You may need to verify these IDs are correct
app_ids = {
    'cbe': 'com.combanketh.mobilebanking',
    'boa': 'com.boa.apollo',
    'dashen': 'com.cr2.amolelight'
}


def scrape_app_reviews(app_id, bank_name):
    """
    Scrapes reviews for a given app ID and bank name.
    """
    print(f"Scraping reviews for {bank_name} (App ID: {app_id})...")
    
    try:
        # First, try to get app info to verify the app exists
        app_info = app(app_id)
        print(f"App found: {app_info['title']}")
        
        # Use reviews_all to get a large set of reviews
        result = reviews_all(
            app_id,
            sleep_milliseconds=200,  # Increased pause to be more polite
            lang='en',
            country='us',
            sort=Sort.MOST_RELEVANT
        )
        
        # Convert to DataFrame
        df = pd.DataFrame(result)
        df['bank'] = bank_name
        print(f"Successfully scraped {len(df)} reviews for {bank_name}")
        return df
        
    except Exception as e:
        print(f"Error scraping {bank_name} (App ID: {app_id}): {str(e)}")
        return pd.DataFrame()

def main():
    all_reviews = []
    
    for bank_key, bank_name in [('cbe', 'Commercial Bank of Ethiopia'), 
                                ('boa', 'Bank of Abyssinia'), 
                                ('dashen', 'Dashen Bank')]:
        app_id = app_ids[bank_key]
        bank_reviews = scrape_app_reviews(app_id, bank_name)
        
        if not bank_reviews.empty:
            all_reviews.append(bank_reviews)
        
        # Be polite to Google's servers
        time.sleep(2)
    
    if all_reviews:
        # Combine all DataFrames
        final_df = pd.concat(all_reviews, ignore_index=True)
        
        # Select and rename columns
        final_df = final_df[['content', 'score', 'at', 'bank']]
        final_df.columns = ['review', 'rating', 'date', 'bank']
        
        # Add source column
        final_df['source'] = 'Google Play'
        
        # Convert date to YYYY-MM-DD format
        final_df['date'] = final_df['date'].dt.strftime('%Y-%m-%d')
        
        # Save to CSV
        final_df.to_csv('bank_reviews.csv', index=False)
        print(f"Successfully saved {len(final_df)} reviews to bank_reviews.csv")
        
        # Print summary
        print("\nSummary by bank:")
        print(final_df['bank'].value_counts())
    else:
        print("No reviews were scraped successfully.")

if __name__ == "__main__":
    main()