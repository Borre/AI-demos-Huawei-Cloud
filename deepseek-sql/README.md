# DeepSeek SQL Demo

This is a simple demo application that allows you to query a MySQL database using natural language. The application uses the DeepSeek API to convert your natural language query into SQL, executes it against your database, and displays the results.

## Setup

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file with the following variables:

```
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## Usage

Run the application:

```
python demo.py
```

Then enter your natural language queries at the prompt. For example:
- "Give me some descriptions of my articles of deepseek"
- "Show me the 5 most recent articles"
- "Count how many articles we have"

Type 'exit' to quit the application.

Note: For SELECT queries that return article data, the application will only display the 'title' and 'url' fields, even if the SQL query retrieves more columns. Results are limited to the last 5 entries for better readability.

## How it works

1. The application reads your database credentials and DeepSeek API key from the `.env` file
2. When you enter a natural language query, it sends it to the DeepSeek API
3. DeepSeek generates an appropriate SQL query for your request
4. The application executes that SQL query against your MySQL database
5. Results are formatted and displayed in the console, showing only the 'title' and 'url' fields for SELECT queries, with improved formatting and limited to the last 5 entries