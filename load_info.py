import paramiko
from string import punctuation
from toolz import partition
import numpy as np

with open('line.txt', 'w') as out:
  with open('test.txt') as file:
    res = [i.strip(punctuation) for i in file.read().split()]
    chunks = np.array_split(res, len(res) // 33)
    for i in range(len(chunks)):
      for j in range(len(chunks[i])):
        line_chunks = chunks[i][j]
        print(line_chunks, end=' ')
        out.write(line_chunks)
        out.write(' ')
      print()
      out.write('\n')