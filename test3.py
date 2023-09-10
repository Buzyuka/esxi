import paramiko
from string import punctuation
import yaml
from toolz import partition
import numpy as np

with open('config.yml', 'r') as fp:
    host_service = yaml.safe_load(fp)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host_service['rest']['esxi_168'], username=host_service['rest']['esxi_user'], password=host_service['rest']['esxi_pass'])

stdin, stdout, stderr = ssh_client.exec_command("esxcli vm process list")
output = stdout.read().decode()

# пишем все данные в файл
esxi_info = open("test.txt", "w")
esxi_info.write(str(output))
esxi_info.close()

with open('test.txt') as file:
    res = [i.strip(punctuation) for i in file.read().split()]
    chunks = np.array_split(res,len(res) // 33)

    print(chunks[0])

