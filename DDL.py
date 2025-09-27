import mysql.connector
import logging


logging.basicConfig(filename='logs.log',level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

config = {'user':'root',"password":"sina885","host":"localhost","database":"apartment"}
#data = {...} #id price room condition place
def create_database(DB_name):
    try:
        config = {'user':'root',"password":"sina885","host":"localhost",}
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        SQL_Query = f"DROP DATABASE IF EXISTS {DB_name}"
        cursor.execute(SQL_Query)
        SQL_Query = f"CREATE DATABASE IF NOT EXISTS {DB_name}"
        cursor.execute(SQL_Query)
        conn.commit()
        print(f"database {DB_name} created succesfully")
        logging.info(f"database {DB_name} created succesfully")
    except Exception as e:
        logging.error(f"couldnt create the database {e}")
    finally:
        cursor.close()
        conn.close()

def create_table_apartment():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        SQL_Query =f"""CREATE TABLE APARTMENT (
                        `ID`            INT UNSIGNED NOT NULL ,
                        `PRICE`         BIGINT  UNSIGNED NOT NULL,
                        `AREA`          INT UNSIGNED NOT NULL,
                        `ROOM`          VARCHAR(30),
                        `CONDITION`     VARCHAR(30),
                        `PLACE`         VARCHAR(30),
                        `LINK`          VARCHAR(60) NOT NULL,
                        PRIMARY KEY (`ID`)
                        );"""
        cursor.execute(SQL_Query)
        conn.commit()
        print("created the TABLE seccefully")
        logging.info("created the TABLE seccefully")
    except Exception as e: 
        logging.error(f"couldnt create the table due to {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_database("apartment")
    create_table_apartment()