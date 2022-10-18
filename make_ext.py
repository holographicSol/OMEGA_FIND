import os

with open('./db/web.csv', 'r') as fo:
    for line in fo:
        line = line.strip()
        line = line.replace(',', '",')
        line = '"' + line
        line = line.replace('%', '')
        print(line)