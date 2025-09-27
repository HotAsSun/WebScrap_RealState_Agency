import mysql.connector
import logging

logging.basicConfig(filename='logs.log',level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

config = {'user':'root',"password":"sina885","host":"localhost","database":"apartment"}


def insert_apartment(id,price,area,room,condition,place,link):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        SQL_QUERY = """INSERT INTO APARTMENT VALUES (%s, %s, %s, %s, %s, %s,%s)
                            ON DUPLICATE KEY UPDATE
                                `PRICE` = VALUES(`PRICE`),
                                `AREA` = VALUES(`AREA`),
                                `ROOM` = VALUES(`ROOM`),
                                `CONDITION` = VALUES(`CONDITION`),
                                `PLACE` = VALUES(`PLACE`),
                                `LINK`  = VALUES(`LINK`);
        """

        cursor.execute(SQL_QUERY,(id,price,area,room,condition,place,link))
        conn.commit()
        logging.info("inserted succesfully to apartment table ")
        print("added succesfully")
    except Exception as e :
        logging.error(f"couldnt insert due to {e}")
    finally:
        cursor.close()
        conn.close()
