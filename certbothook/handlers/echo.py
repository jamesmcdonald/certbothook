"""Debug handler to just print the service name"""

from __future__ import print_function

def handler(service, domain):
    """Debug handler to just print the service name"""
    print("Echo handler is handling service {} for {}".format(service, domain))

