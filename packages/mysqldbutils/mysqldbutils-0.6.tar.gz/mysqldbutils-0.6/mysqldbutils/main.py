import mysql.connector
from urllib.parse import quote


def get_database_url(host, port, database_name, username, password):
    database_url = {
    "host": host,
    "user": username,
    "password": password,
    "database": database_name,
    "port": port
    }
    return database_url

def list_tables(database_url):
    connection = mysql.connector.connect(**database_url)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    connection.close()
    return tables

def create_table(database_url, table_name, columns):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to create a table
        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

        # Execute the query
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

        print(f"Table '{table_name}' created successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def insert(database_url, table_name, data):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to insert data
        columns = ", ".join(data.keys())
        values = ", ".join(["%s" for _ in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        # Execute the query with the data values
        cursor.execute(query, tuple(data.values()))

        # Commit the changes to the database
        connection.commit()

        print("Data inserted successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def insert_many(database_url, table_name, data_list):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get the column names for the table
        cursor.execute(f"DESC {table_name}")
        column_names = [column[0] for column in cursor.fetchall()]

        # Construct the SQL query to insert many rows
        placeholders = ", ".join(["%s" for _ in column_names])
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"

        # Flatten the list of dictionaries into a list of values
        values = [tuple(row.get(col, None) for col in column_names) for row in data_list]

        # Execute the query with the values
        cursor.executemany(query, values)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def select_all(database_url, table_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to select all rows
        query = f"SELECT * FROM {table_name}"

        # Execute the query
        cursor.execute(query)

        # Fetch all rows
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def select_with_pagination(database_url, table_name, from_index, to_index):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to select rows with pagination
        query = f"SELECT * FROM {table_name} LIMIT {from_index - 1}, {to_index - from_index + 1}"

        # Execute the query
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def select_by_column(database_url, table_name, column_name, column_value):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to select rows by column value
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"

        # Execute the query
        cursor.execute(query, (column_value,))

        # Fetch the result
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def select(database_url, table_name, where_dict):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to select rows with conditions
        conditions = [f"{key} = %s" for key in where_dict.keys()]
        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"

        # Execute the query with the condition values
        cursor.execute(query, tuple(where_dict.values()))

        # Fetch the result
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def update(database_url, table_name, update_dict, where_dict):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to update rows with conditions
        update_values = ", ".join([f"{key} = %s" for key in update_dict.keys()])
        conditions = [f"{key} = %s" for key in where_dict.keys()]
        where_clause = " AND ".join(conditions)
        query = f"UPDATE {table_name} SET {update_values} WHERE {where_clause}"

        # Execute the query with the update and condition values
        cursor.execute(query, tuple(update_dict.values()) + tuple(where_dict.values()))

        # Commit the changes to the database
        connection.commit()

        print("Data updated successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def delete(database_url, table_name, where_dict):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to delete rows with conditions
        conditions = [f"{key} = %s" for key in where_dict.keys()]
        where_clause = " AND ".join(conditions)
        query = f"DELETE FROM {table_name} WHERE {where_clause}"

        # Execute the query with the condition values
        cursor.execute(query, tuple(where_dict.values()))

        # Commit the changes to the database
        connection.commit()

        print("Data deleted successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def truncate(database_url, table_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to truncate (remove all rows) from the table
        query = f"TRUNCATE TABLE {table_name}"

        # Execute the query
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

        print("Table truncated successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def delete_table(database_url, table_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to delete the table
        query = f"DROP TABLE IF EXISTS {table_name}"

        # Execute the query
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

        print(f"Table '{table_name}' deleted successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

def sql_query(database_url, raw_sql_query):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(**database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Execute the raw SQL query
        cursor.execute(raw_sql_query)

        # Fetch the result if the query is a SELECT query
        if cursor.description:
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result_as_dict = [dict(zip(column_names, row)) for row in result]
            return result_as_dict
        else:
            # Return the number of rows affected for non-SELECT queries
            return f"Query executed successfully. {cursor.rowcount} row(s) affected."

    except Exception as e:
        # Handle the error
        return f"Error: {e}"

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")
