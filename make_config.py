#!/bin/python

# Import the necessary functions
import yaml
import sys
import argparse
import logging
from jinja2 import Environment, FileSystemLoader

def check_args():
 parser = argparse.ArgumentParser(prog=sys.argv[0], description='Make REST-API calls with HTTPS')

 parser.add_argument('-t', '--template', type=str, required=True,
                     help="Jinja2 template file")
 parser.add_argument('-y', '--data', type=str, required=True,
                     help="Data for Jinja2 template as YAML")
 parser.add_argument('-f', '--filename', type=str, required=False,
                     help="If filename is used, rendered template will be written to file instead stdout")
 parser.add_argument('-d', '--debug', action='store_true',
                     help="Enable basic debugging")

 parser.set_defaults(debug=False)
 args = parser.parse_args()

 if args.debug:
  logging.basicConfig(level=logging.DEBUG)

 return args



def loadData(yaml_file):
 '''Reads yaml formatted file.

 Takes one  argument:
 yaml_file = path to yaml file


 Returns: YAML data
 '''
 # Load the YAML file and transform it to a python directory
 config_data = yaml.load(open(yaml_file))
 return config_data


def loadTemplate(template_file):
 '''Load the template.

 Returns jinja2 template object.
 '''
 # Set the working directory and some settings I don't know yet...
 env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
 # Load the configuration template
 template = env.get_template(template_file)
 return template


def main():
 # Read command line options
 args = check_args()
 # Load YAML into python directory
 config_data = loadData(args.data)
 # Load jinja2 template
 template_data = loadTemplate(args.template)
 # Rendering the final output with the previously generated YAML directory
 final_config = template_data.render(config_data)
 # Check if we print the final rendered data to stdout or into a file
 if args.filename:
  with open(args.filename, 'w') as f:
   f.write(final_config)
 else:
  print(final_config)



if __name__ == '__main__':
 main()

