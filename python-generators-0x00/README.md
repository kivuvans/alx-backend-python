
# Python Generators – Task 0: Getting Started with Python Generators

## Objective
Create a Python script that connects to a MySQL database, sets up the required schema, and populates it with sample user data.

## Files
- `seed.py`: Contains all database setup, table creation, and data seeding logic.
- `user_data.csv`: Input CSV file containing sample user data.

## Features
- Connects to MySQL Server
- Creates database `ALX_prodev` if it doesn’t exist
- Creates table `user_data`
- Populates it from `user_data.csv`
- Uses UUID for unique `user_id`

## How to Run
```bash
$ python3 0-main.py

```
 output:
 ```bash
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('UUID1', 'John Doe', 'john@example.com', 30), ...]
```
