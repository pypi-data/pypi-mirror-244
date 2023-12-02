import sqlite3
import os

def list_tables(database_url):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        # Query to retrieve all table names
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        cursor.execute(query)
        # Fetch all table names
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    
def create_table(database_url, table_name, columns):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        column_definitions = ', '.join(columns)
        query = f"CREATE TABLE {table_name} ({column_definitions})"
        cursor.execute(query)

def insert(database_url, table_name, data):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(query, data)

def insert_many(database_url, table_name, data_list):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(data_list[0]))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.executemany(query, data_list)

def select_all(database_url, table_name):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        return cursor.fetchall()

def select_with_pagination(database_url, table_name, from_index, to_index):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} LIMIT {to_index - from_index + 1} OFFSET {from_index - 1}"
        cursor.execute(query)
        return cursor.fetchall()

def select_by_column(database_url, table_name, column_name, column_value):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
        cursor.execute(query, (column_value,))
        return cursor.fetchall()

def select(database_url, table_name, where_dict):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        placeholders = ' AND '.join([f"{key} = ?" for key in where_dict.keys()])
        query = f"SELECT * FROM {table_name} WHERE {placeholders}"
        cursor.execute(query, tuple(where_dict.values()))
        return cursor.fetchall()

def update(database_url, table_name, update_dict, where_dict):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        set_clause = ', '.join([f"{key} = ?" for key in update_dict.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in where_dict.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(query, tuple(list(update_dict.values()) + list(where_dict.values())))

def delete(database_url, table_name, where_dict):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        placeholders = ' AND '.join([f"{key} = ?" for key in where_dict.keys()])
        query = f"DELETE FROM {table_name} WHERE {placeholders}"
        cursor.execute(query, tuple(where_dict.values()))

def truncate(database_url, table_name):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name}"
        cursor.execute(query)

def delete_table(database_url, table_name):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        query = f"DROP TABLE {table_name}"
        cursor.execute(query)

def sql_query(database_url, raw_sql_query):
    with sqlite3.connect(database_url) as conn:
        cursor = conn.cursor()
        cursor.execute(raw_sql_query)
        return cursor.fetchall()


database_url = os.path.join("./", "my_database.db")
table_name = "employees"
columns = ["id INTEGER", "name TEXT", "salary REAL"]

# Create the "employees" table
#create_table(database_url, table_name, columns)

print(list_tables(database_url))