#!/bin/python

import csv
import yaml


def settings():
 csv_file = 'test.csv'
 # Return name of CSV file
 return csv_file

def translateCSV(filename):
 with open(filename, 'r') as csv_file:
  csv_data = csv.reader(csv_file)
  for row in csv_data:
   if csv_data.line_num == 1:
    headers = row
    h_index = len(headers)
   else:
    index = 0
    try:
     filename = row[0] + '.yaml'
    except IndexError:
     exit()
    with open(filename, 'w') as new_file:
     new_file.write('---\n') 
     while index < h_index:
      if ' ' in row[index]:
       new_file.write(headers[index] + ': "' + row[index] + '"\n') 
      else:
       new_file.write(headers[index] + ': ' + row[index] + '\n') 
      index += 1

def main():
 filename = settings()
 translateCSV(filename)


if __name__ == "__main__":
 main()
