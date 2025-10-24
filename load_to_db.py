import pandas as pd
import sqlite3

# Step 1: Load the CSV file
df = pd.read_csv("indian_gov_schemes.csv")

print("✅ CSV loaded successfully!")
print("Rows:", len(df))
print("Columns:", list(df.columns))
print("\nSample data:\n", df.head())

# Step 2: Connect to (or create) a SQLite database
conn = sqlite3.connect("gov_schemes.db")  # creates a file gov_schemes.db

# Step 3: Store data into a SQL table
df.to_sql("schemes", conn, if_exists="replace", index=False)
print("\n✅ Data inserted into 'schemes' table!")

# Step 4: Run a few SQL queries
sample = pd.read_sql("SELECT * FROM schemes LIMIT 5;", conn)
print("\nHere are 5 sample rows from your database:\n", sample)

count = pd.read_sql("SELECT COUNT(*) AS total_rows FROM schemes;", conn)
print("\nTotal rows in the database:\n", count)

conn.close()
print("\n✅ Done! Database file 'gov_schemes.db' created.")
