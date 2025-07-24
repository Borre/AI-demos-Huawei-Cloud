import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

print("Database connection test")
print(f"Host: {DB_HOST}")
print(f"User: {DB_USER}")
print(f"Database: {DB_NAME}")

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")