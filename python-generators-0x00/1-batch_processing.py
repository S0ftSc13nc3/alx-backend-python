import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to fetch users from user_data in batches of batch_size"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # update your password
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)

        offset = 0
        while True:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def batch_processing(batch_size):
    """Process batches and yield users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
