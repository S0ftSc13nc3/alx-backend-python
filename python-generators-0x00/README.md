# Python Generators - ALX_prodev Database Seeder

This project sets up a MySQL database named `ALX_prodev`, creates a table called `user_data`, and populates it with data from a CSV file. It also includes a generator function that streams rows from the database one by one.

## Features

- Connects to the MySQL server and creates the `ALX_prodev` database if it doesn’t exist.
- Creates a `user_data` table with the following columns:
  - `user_id` (Primary Key, UUID, indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Inserts data from a CSV file (`user_data.csv`), avoiding duplicate entries.
- Provides a generator to fetch rows from the database one at a time.

## Setup Instructions

1. Make sure you have MySQL installed and running locally.
2. Update the MySQL credentials in `seed.py` (`user` and `password`) to match your setup.
3. Prepare your `user_data.csv` file with these headers:  
   `user_id,name,email,age`  
   If `user_id` is missing, a UUID will be generated automatically.
4. Run the main script to set up the database, table, and load data:  
   ```bash
   python3 0-main.py
