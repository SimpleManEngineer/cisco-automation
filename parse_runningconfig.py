from hashlib import new
import json
import xmltodict

def prettyprint_json(json_content):
    return json.dumps(json_content, indent=1, sort_keys=True)

def xml_to_json(xml_file):
    with open('./outputs/' + runningconfig_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

    json_string = json.dumps(data_dict)
    json_obj = json.loads(json_string)
    return json_obj

runningconfig_file = 'show_running_config.xml'
path = './outputs/'

json_data = xml_to_json(path+runningconfig_file)
print(prettyprint_json(json_data['Device-Configuration']['router']))

"""
xml = ET.parse(path + runningconfig_file)
root = xml.getroot()

ns = re.match('{.*}',root.tag).group(0)

device_config = root.find("{}Device-Configuration".format(ns))
#router = device_config.find("{}router".format(ns))

print("router: {}".format(device_config.text))
#print(json_data['Device-Configuration']['router']['ConfigRouter-Configuration'])
"""
new_ospf_config = {}



new_ospf_config['test'] = 12



