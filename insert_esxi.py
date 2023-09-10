import paramiko
from string import punctuation
import psycopg2
#from config import host, user, password, db_name
import yaml
import numpy as np
from getpass import getpass
try:
    with open('config.yml', 'r') as fp:
        host_service = yaml.safe_load(fp)
    connection = psycopg2.connect(
        host=['rest']['host'],
        user=['rest']['user'],
        password=['rest']['password'],
        database=['rest']['db_name'],
        )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version:{cursor.fetchone()}")

# Подключаемся по ssh к esxi

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host_service['rest']['esxi_168'], username=host_service['rest']['esxi_user'], password=host_service['rest']['esxi_pass'])

        stdin, stdout, stderr = ssh_client.exec_command("esxcli vm process list")
        output = stdout.read().decode()
        print(output)
# Пишем инфу в файл
        esxi_info = open("test.txt", "w", newline=None)
        esxi_info.write(str(output))
        esxi_info.close()


        with open('line.txt', 'w') as out:
            with open('test.txt') as file:
                # Выводим информацию из файла в одну строку
                with open('test.txt') as file:
                    res = [i.strip(punctuation) for i in file.read().split()]
                    chunks = np.array_split(res, len(res) // 33)
                for i in range(len(chunks)):
                    for j in range(len(chunks[i])):
                        line_chunks = chunks[i][j]
                        print(line_chunks, end=' ')
                        out.write(line_chunks)
                        out.write(' ')

        insert_qwery ="""
                  INSERT INTO esxi_base(ip, srv_name, process_id, work_id) VALUES (%s, %s, %s, %s)  
                    """

        records_to_insert = (['rest']['esxi_168'], res[0],  res[6], res[3])
        cursor.execute(insert_qwery, records_to_insert)



except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:

    if connection:
        connection.close()
    print("[INFO] PostgreSQL connection closed")

