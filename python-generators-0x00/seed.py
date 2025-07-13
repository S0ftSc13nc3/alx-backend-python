import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connect to MySQL server (without specifying DB)"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # set your root password here
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect specifically to ALX_prodev database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # set your root password here
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create user_data table if it doesn't exist"""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV if user_id doesn't already exist"""
    cursor = connection.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Assume CSV has columns: user_id, name, email, age
            # If user_id is missing or empty, generate UUID
            user_id = row.get('user_id') or str(uuid.uuid4())
            name = row.get('name')
            email = row.get('email')
            age = row.get('age')

            # Check if this user_id already exists
            cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                continue  # skip insert if exists

            try:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
            except mysql.connector.Error as err:
                print(f"Error inserting row: {err}")
        connection.commit()
    cursor.close()

def stream_rows(connection):
    """Generator that yields rows one by one from user_data table"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    row = cursor.fetchone()
    while row:
        yield row
        row = cursor.fetchone()
    cursor.close()
