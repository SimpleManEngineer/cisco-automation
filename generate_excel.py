from ntc_templates.parse import parse_output
import json
import subprocess
import os
import pandas as pd
from openpyxl import load_workbook
import xmltodict
import json

playbook = 'get_ios_config.yaml'
excel_file = 'ios_config.xlsx'
platform = 'cisco_ios'
runningconfig_file = 'show_running_config.xml'
path = './outputs/'

def prettyprint_json(json_content):
    return json.dumps(json_content, indent=1, sort_keys=True)

def xml_to_json(xml_file):
    with open('./outputs/' + runningconfig_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

    json_string = json.dumps(data_dict)
    json_obj = json.loads(json_string)
    return json_obj

def txt_to_json_list(txt_file_name, command):
    txt_file = open(txt_file_name, 'r')
    data = txt_file.read()
    txt_file.close()
    return parse_output(platform=platform, command=command, data=data)

def json_list_to_excel(json_data, sheetname):
    #print(json_data)
    df = pd.DataFrame(json_data)
    book = load_workbook(excel_file)
    writer = pd.ExcelWriter(excel_file, engine='openpyxl') 
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, sheetname)
    writer.save()

def parse_ansible_cli_output(output): #TODO
    print("Data collected successfuly!")
    return

def interfaces_sheet():
    interfaces_list = txt_to_json_list('./outputs/' + 'show_interfaces.txt', command='show interfaces')
    ip_interface_list = txt_to_json_list('./outputs/' + 'show_ip_interface.txt', command='show ip interfaces')

    #retrieve ip-helper addresses
    #empty 2-d array:
    ip_helper_addresses = [[0 for x in range(2)] for y in range(len(ip_interface_list))]

    for interface in range(len(ip_interface_list)):
        for key in ip_interface_list[interface]:
            if key == 'intf':
                ip_helper_addresses[interface][0] = ip_interface_list[interface][key]
            elif key == 'ip_helper':
                ip_helper_addresses[interface][1] = ip_interface_list[interface][key]


    #insert data to interfaces_list
    for interface in range(len(interfaces_list)):
        interfaces_list[interface]['ip_helper_addr'] = ip_helper_addresses[interface][1]

    json_list_to_excel(interfaces_list, 'interfaces')
    #print(prettyprint_json(interfaces_list))
    print("Interfaces sheet has been updated successfuly!")

def access_lists_sheet():
    json_data = txt_to_json_list('./outputs/' + 'show_access_lists.txt', command = 'show access-lists')
    json_list_to_excel(json_data, 'access_lists')
    print("Access-lists sheet has been updated successfuly!")

def portchannel_sheet():
    json_data = txt_to_json_list('./outputs/' + 'show_etherchannel_summary.txt', command = 'show etherchannel summary')
    print(prettyprint_json(json_data))
    json_list_to_excel(json_data, 'access_lists')
    print("Port-channel sheet has been updated successfuly!")

def routing_table():
    json_data = txt_to_json_list('./outputs/' + 'show_ip_route.txt', command = 'show ip route')
    json_list_to_excel(json_data, 'nat')
    print("Routing-table sheet has been updated successfuly!")

def nat_sheet():
    json_data = txt_to_json_list('./outputs/' + 'show_ip_nat_translations.txt', command = 'show ip nat translations')
    #print(prettyprint_json(json_data))
    json_list_to_excel(json_data, 'nat')   
    print("Nat sheet has been updated successfuly!") 

def ospf_sheet(): #TODO
    runningconf = xml_to_json(path+runningconfig_file)
    print(prettyprint_json(runningconf['Device-Configuration']['router']))

    with open('./templates/ospf_pid_template.json', 'r') as json_file:
        pid_template = json.loads(json_file)

    print(pid_template)
    #for pid in len(runningconf['Device-Configuration']['router']):
    #    new_ospf_config[pid] = 


#print("Collecting data from host...")
os.system('ansible-playbook ' + playbook)
#output = subprocess.check_output('ansible-playbook '+playbook+'; exit 0', stderr=subprocess.STDOUT, shell=True)
#parse_ansible_cli_output(output)

interfaces_sheet()
access_lists_sheet() # not working with textfsm 1.1.2
#portchannel_sheet() #not working with textfsm 1.1.0/1.1.2
#nat_sheet() # no command for nat found
routing_table()
ospf_sheet()

#update_config('ospf', 'show_ip_ospf_database.txt', 'show ip ospf database') #- template not found

