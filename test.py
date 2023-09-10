###############################################################
#  esxcli vm process list                                     #
#  esxcli vm process kill --type=soft hard forced --world-id= #
#  esxcli system maintenancemode set -e true                  #
#  esxcli system shutdown poweroff --reason=maintenanc        #
###############################################################
#how to connect to vmware esxi using paramiko
#connect to vmware esxi vsphere ssh using python
#how to automate vmware esxi automation using python script
#vmware automation tutorial
#vmware simple automation
#vmware world-id for getting guest os details
#vmware host machine shutdown script using python
#maintenance mode command and vm shuutdown command examples

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
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='37.48.102.168', username=vm_user, password=vm_pass)

        stdin, stdout, stderr = ssh_client.exec_command("esxcli vm process list")
        output = stdout.read().decode()
        print(output)
       # esxi_info = open("test.txt", "w", newline=None)
       # esxi_info.write(str(output))
       # esxi_info.close()

# Выводим информацию из файла в одну строку
        with open('line.txt') as file:
            res = [i.strip(punctuation) for i in file.read().split()]
        server_num = open("ip.txt", "r")
        line1 = server_num.readline()
        print(res)

        insert_qwery ="""
                  INSERT INTO esxi_base(ip, srv_name, process_id, work_id) VALUES (%s, %s, %s, %s)  
                    """

        records_to_insert = (line1, res[0],  res[6], res[3])
    # print(line.strip())
    #if srv_name == False:
        cursor.execute(insert_qwery, records_to_insert)

    #else:

            #Update table server23_logsа

        #update_qwery = """
                #UPDATE esxi_base
                #SET time_disconnection=%s, load_bytes=%s, sent_bytes=%s
                #WHERE id IN(
            	#SELECT id FROM esxi_base
            	#WHERE sertificate_name=%s AND
            	#(time_disconnection is NULL)
            	#ORDER BY time_connection DESC
                #)
                #    """
        #records_to_update = (data_log[0], data_log[5], data_log[6], data_log[1] )
        #cursor.execute(update_qwery, records_to_update)


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:

    if connection:
        connection.close()
    print("[INFO] PostgreSQL connection closed")

