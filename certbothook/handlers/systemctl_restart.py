"""Handler to call systemctl restart on a service"""
from __future__ import print_function

import subprocess
import sys

def handler(service, domain):
    """Handler to call systemctl restart on a service"""
    status = subprocess.call(['/bin/systemctl', 'restart', service])
    if status != 0:
       print("WARNING: Restart of {} returned {}".format(service, status), file=sys.stderr)
