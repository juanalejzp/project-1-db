import os
import mysql.connector
from mysql.connector import Error

def insert_workers_in_bulk(df, campaings_id, table_name='workers'):
    connection = None
    cursor = None

    try:

        df['campaings_id'] = campaings_id
        
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            insert_query = f"""
            INSERT INTO {table_name} (code, full_name, emails, position, campaign_id)
            VALUES (%s, %s, %s, %s, %s)
            """

            workers_data = df.to_records(index=False).tolist()

            cursor.executemany(insert_query, workers_data)
            
            connection.commit()

            print(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()