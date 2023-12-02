import psycopg2
from urllib.parse import quote

def get_database_url(host, port, database_name, username, password):
    encoded_password = quote(password, safe='')
    DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database_name}"
    return DATABASE_URL

def list_tables(database_url):
    tables = []
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Query to get all table names
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        tables = [table[0] for table in cursor.fetchall()]

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

    return tables

def create_table(database_url, table_name, columns):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to create the table
        query = f"CREATE TABLE {table_name} ({', '.join(columns)})"

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
        if connection:
            cursor.close()
            connection.close()

def insert(database_url, table_name, data):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

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
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def insert_many(database_url, table_name, data_list):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get the column names for the table
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        column_names = [column[0] for column in cursor.fetchall()]

        # Exclude the "id" column if it is auto-incrementing
        column_names = [col for col in column_names if col.lower() != "id"]

        # Construct the SQL query to insert many rows
        placeholders = ", ".join(["%s" for _ in column_names])
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"

        # Flatten the list of dictionaries into a list of values
        values = [tuple(row[key] for key in column_names) for row in data_list]

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
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def select_all(database_url, table_name):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get the column names for the table
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        column_names = [column[0] for column in cursor.fetchall()]

        # Construct the SQL query to select all data from the table
        query = f"SELECT * FROM {table_name}"

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        result = cursor.fetchall()

        # Convert each row to a dictionary
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def select_with_pagination(database_url, table_name, from_index, to_index):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get the column names for the table
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        column_names = [column[0] for column in cursor.fetchall()]

        # Construct the SQL query to select data with pagination
        query = f"SELECT * FROM {table_name} LIMIT {to_index - from_index + 1} OFFSET {from_index}"

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        result = cursor.fetchall()

        # Convert each row to a dictionary
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def select_by_column(database_url, table_name, column_name, column_value):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get the column names for the table
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        column_names = [column[0] for column in cursor.fetchall()]

        # Construct the SQL query to select data by column
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"

        # Execute the query with the column value
        cursor.execute(query, (column_value,))

        # Fetch all the results
        result = cursor.fetchall()

        # Convert each row to a dictionary
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def select(database_url, table_name, where_dict):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get the column names for the table
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        column_names = [column[0] for column in cursor.fetchall()]

        # Construct the SQL query to select data by dictionary
        conditions = [f"{key} = %s" for key in where_dict.keys()]
        where_clause = " AND ".join(conditions)

        query = f"SELECT * FROM {table_name} WHERE {where_clause}"

        # Execute the query with the condition values
        cursor.execute(query, tuple(where_dict.values()))

        # Fetch all the results
        result = cursor.fetchall()

        # Convert each row to a dictionary
        result_as_dict = [dict(zip(column_names, row)) for row in result]

        return result_as_dict

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")
    
def update(database_url, table_name, update_dict, where_dict):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to update data
        set_clause = ", ".join([f"{key} = %s" for key in update_dict.keys()])
        where_clause = " AND ".join([f"{key} = %s" for key in where_dict.keys()])

        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

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
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def delete(database_url, table_name, where_dict):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to delete data by dictionary
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
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def truncate(database_url, table_name):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to truncate the table
        query = f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"

        # Execute the query
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

        print(f"Table '{table_name}' truncated successfully.")

    except Exception as e:
        # Rollback the changes in case of an error
        connection.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def delete_table(database_url, table_name):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the SQL query to delete the table
        query = f"DROP TABLE {table_name}"

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
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

def sql_query(database_url, raw_sql_query):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(database_url)

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
        if connection:
            cursor.close()
            connection.close()


