import paramiko
from string import punctuation
import psycopg2
from config import host, user, password, db_name
from getpass import getpass
try:
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

        with open('text.txt', 'r') as fp:
            vm_pass = fp.read().rstrip()
        with open('str.txt', 'r') as us:
            vm_user = us.read().rstrip()

# Подключаемся по ssh к esxi

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='37.48.102.168', username=vm_user, password=vm_pass)

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
                res = [i.strip(punctuation) for i in file.read().split()]
                chunks = np.array_split(res, len(res) // 33)
                for i in range(len(chunks)):
                    for j in range(len(chunks[i])):
                        line_chunks = chunks[i][j]
                        print(line_chunks, end=' ')
                        out.write(line_chunks)
                        out.write(' ')

        with open('line.txt') as file:
        server_num = open("ip.txt", "r")
        line1 = server_num.readline()
        print(res)

        insert_qwery ="""
                  INSERT INTO esxi_base(ip, srv_name, process_id, work_id) VALUES (%s, %s, %s, %s)  
                    """

        records_to_insert = (line1, res[0],  res[6], res[3])
        cursor.execute(insert_qwery, records_to_insert)



except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:

    if connection:
        connection.close()
    print("[INFO] PostgreSQL connection closed")

