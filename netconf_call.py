#!/bin/python
#
# Copyright (c) 2017  Joe Clarke <jclarke@cisco.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# This script retrieves the ENTITY-MIB tree from a device via NETCONF and
# prints it out in a "pretty" XML tree.
#
# Modifications (c) 2018  Michael Kiessling (michael.kiessling3@f-i-ts.de)

from ncclient import manager
import xml.dom.minidom
import logging
import argparse
import sys
import xmltodict

def search_filter():
    xml_filter = '''
<filter>
   <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      <type/>
      <admin-status/>
      <oper-status/>
      <last-change/>
     </interface>
   </interfaces-state>
 </filter>
'''
    return xml_filter



def device_config():
    dev_config = '''
<config>
 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>Loopback20</name>
      <description>NETCONF Test</description>
      <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
    </interface>
 </interfaces>
</config>
'''
    return dev_config



def check_args():
    parser = argparse.ArgumentParser(prog=sys.argv[0], description='Print ENTITY-MIB data via NETCONF from a device')

    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (NETCONF server username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (NETCONF server password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Enable ncclient debugging")
    parser.add_argument('-c', '--capabilities', action='store_true',
                        help="Show server capabilities")

    parser.set_defaults(debug=False)
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        
    return args


def get_capabilities(args):
    print('-----------------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------SERVER CAPABILITIES-------------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------------------')
    with manager.connect_ssh(host=args.host, port=args.port, username=args.username, hostkey_verify=False, password=args.password) as m:
        for cap in m.server_capabilities:
         print(cap)
    print('-----------------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------SERVER CAPABILITIES-------------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------------------')


def get_config(args, x_filter):
    if args.capabilities:
     get_capabilities(args)
    with manager.connect_ssh(host=args.host, port=args.port, username=args.username, hostkey_verify=False, password=args.password) as m:
        try:
         c = m.get(x_filter)
        #c = m.get_config("running", x_filter)
        except Exception as e:
         print('Failed to execute <get> RPC: {}'.format(e))

        received_config = xml.dom.minidom.parseString(c.data_xml).toprettyxml()
        return received_config


def write_config(args, d_config):
    if args.capabilities:
     get_capabilities(args)
    with manager.connect_ssh(host=args.host, port=args.port, username=args.username, hostkey_verify=False, password=args.password) as m:
        try:
         c = m.edit_config(d_config, target='running')
        except Exception as e:
         print('Failed to execute <edit-config> RPC: {}'.format(e))



if __name__ == '__main__':
    args = check_args()
    x_filter = search_filter()
    d_config = device_config()

    xml_config = get_config(args, x_filter)
    print(xml_config)
    #get_capabilities(args)
    #write_config(args, d_config)

    '''c_dict = xmltodict.parse(c.data_xml)
    for interface in (c_dict['data']['interfaces']['interface']):
     print (interface['name'])
     try:
      print (interface['description'])
     except KeyError:
      print ('No description set')
     try:
      print (interface['ipv4']['address']['ip'] + ' ' + interface['ipv4']['address']['netmask'])
     except KeyError:
      print ('IPv4 not assigned')
    #for cap in m.server_capabilities:
     #print(cap)'''
