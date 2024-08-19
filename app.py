# app.py

from flask import Flask, render_template_string
import snowflake.connector

# Initialize Flask app
app = Flask(__name__)

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    'user': 'KADAPB',
    'password': 'Flaskdocker1',
    'account': 'av81181.us-east-2.aws',
    'warehouse': 'XSMALL_WH',
    'database': 'SYSTEM_SERVICES',
    'schema': 'ELASTICSEARCH',
}


# Snowflake connection configuration

def fetch_logs():
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    
    # Set the database and schema
    cursor.execute("USE DATABASE SYSTEM_SERVICES")
    cursor.execute("USE SCHEMA ELASTICSEARCH")
    
    # Query the APPLICATION_LOGS table
    query = """
    SELECT "Timestamp", "Log Level", "Task ID", "Message", "Execution Time (seconds)"
    FROM LOGS
    """
    cursor.execute(query)
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    
    # Process rows into a dictionary by log level
    logs_by_level = {}
    for row in rows:
        timestamp, log_level, task_id, message, execution_time = row
        if log_level not in logs_by_level:
            logs_by_level[log_level] = []
        logs_by_level[log_level].append({
            'Timestamp': timestamp,
            'Task ID': task_id,
            'Message': message,
            'Execution Time (seconds)': execution_time
        })
    
    cursor.close()
    conn.close()
    
    return logs_by_level

@app.route('/')
def index():
    logs_by_level = fetch_logs()
    
    # HTML template to display logs in three columns per row
    html_template = '''
    <html>
    <head>
        <title>Application Logs</title>
        <style>
            .container {
                display: flex;
                flex-wrap: wrap;
                margin: -10px; /* Adjust negative margin to account for padding */
            }
            .column {
                flex: 1 1 30%; /* Flex basis of approximately 30% to fit three columns per row */
                box-sizing: border-box;
                padding: 10px;
                border: 1px solid #ddd;
                margin: 10px; /* Margin for spacing between columns */
                min-width: 250px; /* Ensure columns don't get too narrow */
            }
            h2 {
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin-bottom: 10px;
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            strong {
                display: block;
            }
        </style>
    </head>
    <body>
        <h1>Application Logs</h1>
        <div class="container">
            {% for log_level, logs in logs_by_level.items() %}
                <div class="column">
                    <h2>Log Level: {{ log_level }}</h2>
                    <ul>
                    {% for log in logs %}
                        <li>
                            <strong>Timestamp:</strong> {{ log['Timestamp'] }}<br>
                            <strong>Task ID:</strong> {{ log['Task ID'] }}<br>
                            <strong>Message:</strong> {{ log['Message'] }}<br>
                            <strong>Execution Time (seconds):</strong> {{ log['Execution Time (seconds)'] }}
                        </li>
                    {% endfor %}
                    </ul>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, logs_by_level=logs_by_level)

if __name__ == '__main__':
    app.run(debug=True)
