import mysql.connector

def run_query(host: str, user: str, password: str, database: str, query: str)->tuple:
    """
    return records from the database.
    """
    try:
        my_db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
        my_cursor = my_db.cursor()
        my_cursor.execute(query)
        my_result = my_cursor.fetchall()
        return my_result
    except Exception as Error:
        return Error
