import csv
import re

direction = r'C:\Users\macsw\OneDrive\Desktop\language_bot\dictionaries\eng_dictionary.txt'

with open(direction, 'r', encoding='utf-8') as file, open('eng_dictionary.csv', 'w', encoding='utf-8', newline='') as new_file:
    writer = csv.writer(new_file, delimiter=';')


    for i in file.readlines():
        row = i.split(';')
        if len(row) == 3:
            row = [row[0], row[2]]
        writer.writerow([q.strip().strip('"') for q in row])


