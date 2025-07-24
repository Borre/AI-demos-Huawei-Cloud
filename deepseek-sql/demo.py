import os
import sys
import json
import requests
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

def load_config():
    """Load configuration from environment variables."""
    return {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_NAME': os.getenv('DB_NAME'),
        'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY')
    }

# Get environment variables
config = load_config()
DB_HOST = config['DB_HOST']
DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']
DB_NAME = config['DB_NAME']
DEEPSEEK_API_KEY = config['DEEPSEEK_API_KEY']

# Connect to MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        sys.exit(1)

# Generate SQL using DeepSeek API
def generate_sql(natural_language_query):
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # System prompt to guide the model to generate SQL for the telegram.articles table
    system_prompt = {
        "role": "system",
        "content": (
            "You are a SQL expert. Generate a valid MySQL query for the telegram.articles table "
            "based on the user's natural language request. Only return the SQL query, nothing else. "
            "The table structure is: id (int), title (varchar), description (text), url (text), "
            "created_at (timestamp), category (varchar), embedding (text), user_id (bigint), "
            "summary (text), notion_page_id (varchar), modified_at (timestamp), source (varchar), "
            "image_url (text). "
            "Make sure to only query the telegram.articles table and not any other tables. "
            "Do not include any markdown formatting like ```sql or ```. "
            "Only use columns that actually exist in the table. "
            "Do not include any placeholder text, comments, or explanations. "
            "Return only a single valid SQL statement that can be executed directly. "
            "Example: For 'give me some descriptions of my articles of deepseek', return: "
            "SELECT description FROM telegram.articles WHERE title LIKE '%deepseek%' OR description LIKE '%deepseek%' OR category LIKE '%deepseek%';"
        )
    }
    
    user_prompt = {
        "role": "user",
        "content": natural_language_query
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [system_prompt, user_prompt],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        sql_query = result['choices'][0]['message']['content'].strip()
        # Remove markdown code block formatting if present
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]  # Remove ```sql
        if sql_query.startswith("```"):
            sql_query = sql_query[3:]  # Remove ```
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]  # Remove ```
        # Remove any lines with comments or placeholders
        lines = sql_query.split('\n')
        clean_lines = [line for line in lines if not ('--' in line or 'YOUR_' in line)]
        sql_query = '\n'.join(clean_lines).strip()
        return sql_query
    except Exception as e:
        print(f"Error generating SQL: {e}")
        sys.exit(1)

# Execute SQL query and return results
def execute_query(connection, sql_query):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        
        # If it's a SELECT query, fetch results (limit to 5)
        if sql_query.strip().upper().startswith("SELECT"):
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            # Limit to last 5 results
            if len(results) > 5:
                results = results[-5:]
                
            return columns, results
        else:
            # For INSERT, UPDATE, DELETE, commit the transaction
            connection.commit()
            return None, f"Query executed successfully. Rows affected: {cursor.rowcount}"
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"
    finally:
        if cursor:
            cursor.close()

# Format and display results
def display_results(columns, results):
    if columns is None:
        print(results)
        return
    
    # Filter to only show title and url columns if they exist
    title_index = None
    url_index = None
    
    for i, col in enumerate(columns):
        if col.lower() == 'title':
            title_index = i
        elif col.lower() == 'url':
            url_index = i
    
    # If neither title nor url columns exist, show all columns (but still limit to 5)
    if title_index is None and url_index is None:
        # Calculate column widths for better formatting
        col_widths = []
        for i, col in enumerate(columns):
            width = len(col)
            for row in results:
                width = max(width, len(str(row[i])))
            col_widths.append(width)
        
        # Print header
        header_parts = []
        separator_parts = []
        for i, col in enumerate(columns):
            header_parts.append(col.ljust(col_widths[i]))
            separator_parts.append("-" * col_widths[i])
        
        header = " | ".join(header_parts)
        separator = "-+-".join(separator_parts)
        
        print(header)
        print(separator)
        
        # Print rows
        for row in results:
            row_parts = []
            for i, item in enumerate(row):
                row_parts.append(str(item).ljust(col_widths[i]))
            print(" | ".join(row_parts))
        return
    
    # Create new columns list with only title and url
    filtered_columns = []
    filtered_indices = []
    
    if title_index is not None:
        filtered_columns.append('title')
        filtered_indices.append(title_index)
    
    if url_index is not None:
        filtered_columns.append('url')
        filtered_indices.append(url_index)
    
    # Calculate column widths for better formatting
    col_widths = []
    for i, col in enumerate(filtered_columns):
        width = len(col)
        for row in results:
            width = max(width, len(str(row[filtered_indices[i]])))
        col_widths.append(width)
    
    # Print header
    header_parts = []
    separator_parts = []
    for i, col in enumerate(filtered_columns):
        header_parts.append(col.ljust(col_widths[i]))
        separator_parts.append("-" * col_widths[i])
    
    header = " | ".join(header_parts)
    separator = "-+-".join(separator_parts)
    
    print(header)
    print(separator)
    
    # Print rows with only title and url values
    for row in results:
        row_parts = []
        for i, idx in enumerate(filtered_indices):
            row_parts.append(str(row[idx]).ljust(col_widths[i]))
        print(" | ".join(row_parts))

def main():
    print("DeepSeek SQL Demo")
    print("Type 'exit' to quit\n")
    
    # Connect to database
    connection = connect_to_db()
    
    try:
        while True:
            # Get user input
            user_input = input("Enter your query (natural language): ").strip()
            
            if user_input.lower() == 'exit':
                break
            
            if not user_input:
                continue
            
            # Generate SQL from natural language
            print("Generating SQL query...")
            sql_query = generate_sql(user_input)
            print(f"Generated SQL: {sql_query}\n")
            
            # Execute query
            print("Executing query...")
            columns, results = execute_query(connection, sql_query)
            
            # Display results
            print("Results (showing up to 5 entries):")
            display_results(columns, results)
            print()
            
    finally:
        connection.close()

if __name__ == "__main__":
    main()