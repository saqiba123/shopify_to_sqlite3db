import requests
import pandas as pd
from sqlalchemy import create_engine
import dotenv
import os
import sqlite3

dotenv.load_dotenv()

# AUTHENTICATION - API KEY
SHOPIFY_API_KEY = os.getenv('APIKEY')
SHOPIFY_STORE = os.getenv('STORE')

def fetch_shopify_orders():
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-04/orders.json"
    headers = {'X-Shopify-Access-Token': SHOPIFY_API_KEY}
    response = requests.get(url, headers=headers, params={"status": "any", "limit": 50})
    if response.status_code == 200:
        print("Shopify orders fetched successfully.")
        return response.json()
    else:
        raise ValueError(f"Error fetching orders:\n Status: {response.status_code}, Error: {response.json()}")

# Extract order ID, order name, and status
def extract_required_fields(shopify_data):
    shopify_df = pd.json_normalize(shopify_data['orders'])
    required_columns = ['id', 'name', 'financial_status']  # Adjust these field names if necessary
    shopify_df = shopify_df[required_columns]
    return shopify_df

def store_to_db(dataframe, db_path):
    engine = create_engine(f'sqlite:///{db_path}')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS shopify_orders (
        id INTEGER PRIMARY KEY,
        name TEXT,
        financial_status TEXT
    )''')
    existing_ids_query = "SELECT id FROM shopify_orders"
    try:
        existing_ids = pd.read_sql_query(existing_ids_query, conn)
    except Exception:
        existing_ids = pd.DataFrame(columns=['id'])
    conn.close()
    new_data = dataframe[~dataframe['id'].isin(existing_ids['id'])]
    if not new_data.empty:
        if new_data.isnull().values.any():
            print("Missing data found. Handling missing data before insertion.")
            new_data = new_data.fillna('')  
        
        new_data.to_sql('shopify_orders', engine, if_exists='append', index=False)
        print(f"{len(new_data)} new records saved to the database.")
    else:
        print("No new records to insert (all IDs already exist).")

# Function to interact with the database
def interact_with_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    df = pd.read_sql_query("SELECT * FROM shopify_orders;", conn)
    print("First 5 rows of 'shopify_orders':")
    print(df.head())
    conn.close()

if __name__ == "__main__":
    try:
        shopify_orders = fetch_shopify_orders()
        shopify_df = extract_required_fields(shopify_orders)
        store_to_db(shopify_df, 'shopify_orders.db') 
        interact_with_db('shopify_orders.db')
    except Exception as e:
        print(f"An error occurred: {e}")
