import psycopg2
import datetime
import json
import csv
from config import host, user, password, db_name
from datetime import datetime, timedelta

try:
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version:{cursor.fetchone()}")

        # insert data into table
        data = open("test.txt", "r")
        while True:
            line = data.readline()
            #print(line.strip())
            if not line:
                break
            data_log = line.split(' ')
            cursor = connection.cursor()
            server_name = data_log[0]
            server_num = open("ip.txt", "r")
            line = server_num.readline()
            #print(line)
            #print(len(log_connect.strip()))

            insert_qwery ="""
                  INSERT INTO esxi_base(server_number, time_connection, time_disconnection, sertificate_name, ip, port, ip_vpn, load_bytes,\
                   sent_bytes, os_platforms, cli_version, mac_cli) VALUES (%s, %s, %s, %s, %s, %s, %s,\
                    %s, %s, %s, %s, %s)  
                    """
            records_to_insert = (line, data_log[0],  None, data_log[1], data_log[2], data_log[3], data_log[4], data_log[5],
                                 data_log[6], data_log[7], data_log[8], data_log[9])
            # print(line.strip())
            if len(log_connect.strip()) == 9:
                cursor.execute(insert_qwery, records_to_insert)

            else:

            #Update table server23_logsа

                update_qwery = """
                        UPDATE esxi_base
                        SET time_disconnection=%s, load_bytes=%s, sent_bytes=%s
                        WHERE id IN(
            	        SELECT id FROM esxi_base 
            	        WHERE sertificate_name=%s AND
            	        (time_disconnection is NULL) 
            	        ORDER BY time_connection DESC
                        )
                        """
                records_to_update = (data_log[0], data_log[5], data_log[6], data_log[1] )
                cursor.execute(update_qwery, records_to_update)


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")