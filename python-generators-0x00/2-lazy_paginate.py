import seed

def paginate_users(page_size, offset):
    """Fetch one page of users from user_data with given page_size and offset"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """Generator that lazily fetches pages of user data"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
