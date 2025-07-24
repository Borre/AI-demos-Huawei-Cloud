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

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    cursor = connection.cursor()
    cursor.execute("DESCRIBE telegram.articles")
    columns = cursor.fetchall()
    
    print("Table structure for telegram.articles:")
    for column in columns:
        print(column)
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()