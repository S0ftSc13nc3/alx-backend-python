import mysql.connector

def stream_users():
    """Generator that yields user_data rows one by one as dictionaries"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # adjust your MySQL root password here
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
