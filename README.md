# Shopify Orders to SQLite Integration

This project demonstrates how to fetch orders from the Shopify API, extract required fields, and save them into a local SQLite database. It also includes functions to interact with the database and view stored data.

## Features:
- Fetch Shopify orders using Shopify's REST API.
- Extract relevant fields such as Order ID, Order Name, and Order Status.
- Store the data in an SQLite database (`shopify_orders.db`).
- Retrieve and display the data from the SQLite database.

## Prerequisites:
Before running this project, make sure you have the following:
- A **Shopify API Key** and **Store Name**. You can get these from your Shopify admin panel.
- Python 3.x installed on your machine.
- An active internet connection to fetch data from the Shopify API.

## Setup:

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Install dependencies:
    Navigate to the project folder and create a virtual environment:
    ```bash
    python -m venv venv
    ```

    Then activate the virtual environment:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

    Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Create a `.env` file in the root directory of your project.
    - Add your Shopify API key and store name to the `.env` file:
    
    ```plaintext
    APIKEY=your_shopify_api_key
    STORE=your_shopify_store_name
    ```

## Running the Script:

1. To run the script and fetch orders from Shopify, simply execute the Python script:
    ```bash
    python shopify_to_db_integration.py
    ```

2. The script will:
    - Fetch Shopify orders.
    - Extract the `id`, `name`, and `financial_status` fields.
    - Save the extracted data into a local SQLite database (`shopify_orders.db`).

3. After execution, the data will be saved in `shopify_orders.db`, and you can query it using the built-in functions to view the stored orders.

## Interacting with the Database:

The script includes a function `interact_with_db()` that connects to the SQLite database and displays the first 5 rows of the `shopify_orders` table.

To view the saved orders, ensure you have run the script at least once, and then interact with the database by calling the function within the script.

```python
interact_with_db('shopify_orders.db')
