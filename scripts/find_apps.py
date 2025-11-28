# find_apps.py
from google_play_scraper import search

def find_bank_apps():
    queries = [
        "Commercial Bank of Ethiopia",
        "Bank of Abyssinia",
        "Dashen Bank"
    ]
    
    for query in queries:
        print(f"\nSearching for: {query}")
        try:
            results = search(query)
            for result in results:
                print(f"Title: {result['title']}")
                print(f"App ID: {result['appId']}")
                print(f"Score: {result['score']}")
                print("---")
        except Exception as e:
            print(f"Error searching for {query}: {e}")

if __name__ == "__main__":
    find_bank_apps()