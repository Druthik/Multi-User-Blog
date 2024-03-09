# search_posts.py

import mysql.connector
import db_configtk

def search_posts(query):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()

        # Search for posts where the username or heading matches the query
        sql_query = "SELECT username,heading FROM posts WHERE username LIKE %s OR heading LIKE %s"
        cursor.execute(sql_query, (f'%{query}%', f'%{query}%'))

        # Fetch the results
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return results
    except mysql.connector.Error as err:
        print("Error:", err)
        return []





