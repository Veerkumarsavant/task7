import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

DB_FILE = "sales_data.db"
TABLE_NAME = "sales"
CHART_FILE = "final_revenue_chart.png"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute(f"""
CREATE TABLE {TABLE_NAME} (
    sale_id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
""")
sales_data = [
    ('Laptop', 5, 1200.00), ('Monitor', 10, 250.00),
    ('Laptop', 2, 1200.00), ('Keyboard', 15, 75.00),
    ('Monitor', 3, 250.00), ('Mouse', 20, 20.00),
    ('Laptop', 1, 1200.00)
]
cursor.executemany(f"INSERT INTO {TABLE_NAME} (product, quantity, price) VALUES (?, ?, ?);", sales_data)
conn.commit()
conn.close()
try:
    conn = sqlite3.connect(DB_FILE)
    query = f"""
    SELECT 
        product, 
        SUM(quantity * price) AS revenue 
    FROM {TABLE_NAME} 
    GROUP BY product
    ORDER BY revenue DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    print("--- SQL Query Results ---")
    print(df.to_markdown(index=False))

    # Plot Bar Chart
    plt.figure(figsize=(9, 5))
    df.plot(
        kind='bar',
        x='product',
        y='revenue',
        ax=plt.gca(),
        legend=False,
        color='maroon'
    )

    # Formatting
    plt.title('Product Revenue Contribution', fontsize=16)
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Revenue (USD)', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(CHART_FILE)
    print(f"\nSuccessfully generated and saved bar chart: '{CHART_FILE}'")

except sqlite3.Error as e:
    print(f"ERROR: Could not complete operation due to database error: {e}")