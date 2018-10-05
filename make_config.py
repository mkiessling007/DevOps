#!/bin/python

# Import the necessary functions
import yaml
import sys
from jinja2 import Environment, FileSystemLoader


def options():
 '''These are the options for the script. To be replaced with
 meaningfull cli argument parser in future.
 
 Takes no arguments

 Returns: tuple (template_file, yaml_file)
 '''
 # Check if we have a YAML file via command arguments. If yes, take it.
 if len(sys.argv) > 1:
  yaml_file = sys.argv[1]
 else:
  # This is the YAML File with configuration specifics
  yaml_file = 'xpca01-m201-2d01-lbsb.yaml'
 # This is the basic device vonfiguration template
 template_file = 'access_switch.j2'
 # Return both variables as tuple
 return (template_file, yaml_file)


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
 # Read the optins
 settings = options()
 # Load YAML into python directory
 config_data = loadData(settings[1])
 # Load jinja2 template
 template_data = loadTemplate(settings[0])
 # Rendering the final output with the previously generated YAML directory
 print (template_data.render(config_data))



if __name__ == '__main__':
 main()

