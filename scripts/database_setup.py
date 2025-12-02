import psycopg2
from psycopg2 import sql
import pandas as pd
import os

def create_connection():
    """Create connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="bank_reviews",
            user="postgres",
            password="postgres",  
            port="5432"
        )
        print("✅ Connected to PostgreSQL database")
        return conn
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL service is running")
        print("2. Check password (you set during installation)")
        print("3. Try default password 'postgres'")
        return None

def create_tables(conn):
    """Create database tables in PostgreSQL"""
    commands = (
        """
        DROP TABLE IF EXISTS reviews CASCADE;
        """,
        """
        DROP TABLE IF EXISTS banks CASCADE;
        """,
        """
        CREATE TABLE banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(100) NOT NULL,
            app_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
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
        """,
        """
        CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
        """,
        """
        CREATE INDEX idx_reviews_sentiment ON reviews(sentiment_label);
        """,
        """
        CREATE INDEX idx_reviews_date ON reviews(review_date);
        """
    )
    
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("✅ Tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False

def insert_data(conn):
    """Insert data into PostgreSQL"""
    # Insert banks
    banks = [
        ("Commercial Bank of Ethiopia", "CBE Mobile"),
        ("Bank of Abyssinia", "BOA Mobile"),
        ("Dashen Bank", "Dashen Mobile")
    ]
    
    try:
        cur = conn.cursor()
        
        # Insert banks
        for bank_name, app_name in banks:
            cur.execute(
                "INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) RETURNING bank_id",
                (bank_name, app_name)
            )
            bank_id = cur.fetchone()[0]
            print(f"✅ Inserted {bank_name} with ID: {bank_id}")
        
        # Get bank mapping
        cur.execute("SELECT bank_name, bank_id FROM banks")
        bank_map = {row[0]: row[1] for row in cur.fetchall()}
        
        # Insert reviews
        df = pd.read_csv('data/full_sentiment_analysis.csv')
        print(f"\nInserting {len(df)} reviews...")
        
        insert_count = 0
        for _, row in df.iterrows():
            bank_id = bank_map.get(row['bank'])
            if not bank_id:
                continue
            
            # Handle date
            review_date = None
            if 'date' in row and pd.notna(row['date']):
                try:
                    review_date = pd.to_datetime(row['date'])
                except:
                    review_date = None
            
            cur.execute("""
                INSERT INTO reviews 
                (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                bank_id,
                str(row['review'])[:5000],
                int(row['rating']),
                review_date,
                row.get('sentiment_label', 'NEUTRAL'),
                float(row.get('sentiment_score', 0.5))
            ))
            insert_count += 1
            
            # Progress update
            if insert_count % 500 == 0:
                print(f"  Inserted {insert_count} reviews...")
        
        conn.commit()
        cur.close()
        print(f"✅ Successfully inserted {insert_count} reviews")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        conn.rollback()
        return False

def run_queries(conn):
    """Run test queries on PostgreSQL"""
    queries = {
        "Total Reviews": "SELECT COUNT(*) FROM reviews",
        "Reviews per Bank": """
            SELECT b.bank_name, COUNT(r.review_id) as review_count
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY review_count DESC
        """,
        "Average Rating per Bank": """
            SELECT b.bank_name, 
                   ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
                   COUNT(r.review_id) as review_count
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY avg_rating DESC
        """,
        "Sentiment Analysis": """
            SELECT 
                sentiment_label,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
            FROM reviews
            GROUP BY sentiment_label
            ORDER BY count DESC
        """
    }
    
    print("\n📊 POSTGRESQL TEST QUERIES:")
    try:
        cur = conn.cursor()
        for query_name, query in queries.items():
            print(f"\n{query_name}:")
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                print(f"  {row}")
        cur.close()
    except Exception as e:
        print(f"❌ Query error: {e}")

def main():
    print("=" * 60)
    print("POSTGRESQL DATABASE SETUP FOR BANK REVIEWS")
    print("=" * 60)
    
    conn = create_connection()
    if not conn:
        return
    
    try:
        # Create tables
        if not create_tables(conn):
            return
        
        # Insert data
        if not insert_data(conn):
            return
        
        # Run test queries
        run_queries(conn)
        
        print("\n" + "=" * 60)
        print("✅ POSTGRESQL SETUP COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    finally:
        if conn:
            conn.close()
            print("✅ Database connection closed")

if __name__ == "__main__":
    main()