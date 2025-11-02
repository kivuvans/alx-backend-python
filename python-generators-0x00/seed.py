
#!/usr/bin/python3
"""
seed.py
Creates a MySQL database `ALX_prodev`, a `user_data` table,
and populates it with data from `user_data.csv`.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connect to the MySQL server (not to a specific database yet)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password'  # 🔁 Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL server successfully")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database successfully")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Check for duplicates
                cursor.execute("SELECT * FROM user_data WHERE email = %s;", (email,))
                result = cursor.fetchone()
                if result:
                    continue

                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query, (user_id, name, email, age))

        connection.commit()
        print("Data inserted successfully from CSV")
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()


if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            connection.close()
