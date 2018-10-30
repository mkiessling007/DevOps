#!/bin/python

import csv
import yaml
import sys
import argparse
import logging

def check_args():
 parser = argparse.ArgumentParser(prog=sys.argv[0], description='Takes a CSV file ad writes a YAML file for each line. The filename should be within the CSV, eg in row 1')

 parser.add_argument('-c', '--data', type=str, required=True,
                     help="Data as CSV file")
 parser.add_argument('-f', '--filename', type=int, required=False,
                     help="Number of line which to use as filname, defaults to row 1")
 parser.add_argument('-d', '--debug', action='store_true',
                     help="Enable basic debugging")

 parser.set_defaults(debug=False)
 args = parser.parse_args()

 if args.debug:
  logging.basicConfig(level=logging.DEBUG)

 return args


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
     # If we have a ";" in the string, we probably have an Excel format and hence no valid string for a hostname
     if ';' in new_filename:
      print('Found ";" in first coloum, probably a Excel formatted CSV?')
      exit()
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
 # Check command line arguments
 args = check_args()
 translateCSV(args.data)


if __name__ == "__main__":
 main()
