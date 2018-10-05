#!/bin/python

import csv
import yaml
import sys


def settings():
 '''Set configuration settings.

 Takes no argument

 Returns a string
 '''
 # Check wether we have a argument we can use as filename
 if len(sys.argv) > 1:
  csv_file = sys.argv[1]
 else: 
  # Set the source CSV file if we don't have a command line argument
  csv_file = 'test.csv'
 # Return name of CSV file
 return csv_file

def translateCSV(filename):
 '''Translate a CSV file int one or more YAML files. Each line in the CSV file
 will be written as one YAML file. The name for the YAML file will be taken from the
 first column of each line from the CSV file.

 Takes a filename as argument.

 Returns nothing
 '''
 # Let's open the CSV file
 with open(filename, 'r') as csv_file:
  # Read the CSV file as csv object
  csv_data = csv.reader(csv_file)
  # Go through each line from the CSV
  for row in csv_data:
   # The first line holds the headers, so check if we are in line number one
   if csv_data.line_num == 1:
    # If we are at first line save it as list an count elements in that list
    headers = row
    h_index = len(headers)
   else:
    # If we are not in first line initiate a index counter
    index = 0
    try:
     # Check if we have an element in this line. If yes read it and add .yaml to create a filename for the new YAML file
     new_filename = row[0] + '.yaml'
    except IndexError:
     # If there's no new elemnt in this CSV line stop the script. We should be done.
     exit()
    # Create the new YAML file
    with open(new_filename, 'w') as new_file:
     # Write --- as first line
     new_file.write('---\n') 
     # Now go through all the elements
     while index < h_index:
      # If we have data with whitespace in it, use ""
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
