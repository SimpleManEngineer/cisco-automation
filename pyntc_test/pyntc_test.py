#NOT WORKING
from pyntc import ntc_device_by_name as NTCNAME
import json

csr1kv = NTCNAME('csr1kv', '.ntc.conf')
#csr1kv1 = NTCNAME('csr1kv1')
#csr1kv2 = NTCNAME('csr1kv2')

print(json.dumps(csr1kv.facts, indent=4))