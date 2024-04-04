import subprocess as sp
from logger import logger

USER = ""
PASSWORD = ""
HOST = ""
DB = ""
TABLE = ""

def insert_row(timestamp: int, ozone: int):
    sql_query = f"INSERT IGNORE INTO {TABLE} (timestamp, UV, ozone) VALUES ({timestamp}, 0, {ozone})"
    mysql_cmd = [
        'mysql',
        f"--user={USER}",
        f"--password={PASSWORD}",
        f"--host={HOST}",
        f"--database={DB}",
        "--execute",
        sql_query
    ]

    try:
        logger.info(f"Inserting ({timestamp}, 0, {ozone}) into {TABLE}")
        sp.run(mysql_cmd, check=True)
        logger.info("Row inserted into MySQL table successfully")
    except sp.CalledProcessError as e:
        logger.error(f"Error executing MySQL command: {e}")

if __name__ == "__main__":
    insert_row(1711906920, 256)