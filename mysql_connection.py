import mysql.connector
from logger import logger

def upload_csv(csv_file_path: str):
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            databse='',
            raise_on_warnings=True
        )

        if connection.is_connected():
            cursor = connection.cursor()
            logger.info('Connected to MySQL database')
            
            with open(csv_file_path, "r") as file:
                next(file) # skip header row
                rows = [line.strip().split(',') for line in file]
                for row in rows:
                    try:
                        cursor.execute("INSERT IGNORE INTO  (timestamp, UV, OZONE) VALUES (%s, %s, %s)", row)
                    except mysql.connector.Error as err:
                        logger.error(f"Failed to insert row: {row}, Error: {err}")
            connection.commit()
            logger.info("CSV data loaded into MySQL table successfully")
    except mysql.connector.Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            # Close connection
            cursor.close()
            connection.close()
            logger.info('MySQL database connection closed')