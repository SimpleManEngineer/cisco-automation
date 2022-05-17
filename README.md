# cisco-automation
configure cisco switch/router via MS Excel and Ansible.

This simple script in python uses Ansible to read/write running configuration of cisco L2/L3 device. Not completed yet.

Usage:
1. run generate_excel.py script to read/write config from cisco device to excel file.
2. make changes in ios_config.xlsx file i.e interface configuration
3. run update_ios_config.py script to write changes to aforementioned device' startup config (for now no such file is present in repository as it is in developement)
