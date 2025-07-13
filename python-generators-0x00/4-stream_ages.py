import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # replace with your MySQL password
            database='ALX_prodev'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield age

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def compute_average_age():
    """Computes and prints the average age using the generator"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")

# Run the computation
if __name__ == '__main__':
    compute_average_age()
