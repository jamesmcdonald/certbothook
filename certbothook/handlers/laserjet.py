"""Handler to renew certificate on an HP LaserJet

Note that this is entirely based on experimentation with an HP
Color LaserJet MFP M477fdw may not work for you at all.

To use HTTPS here (which you should), you have to add the
printer's existing intermediate(s) to your CA certs,
because the printer doesn't send them.

On Debian, for example:

# cp chain.pem /usr/local/share/ca-certificates/letsencrypt.crt
# update-ca-certificates

Then you can create an HTTPS-enabled handler function like:

from certbothook.handlers.laserjet import makehandler
laserjet = makehandler(scheme='https', verify='/etc/ssl/certs')
"""

from __future__ import print_function

import string
import os
from random import choice
import requests
import OpenSSL

def makehandler(scheme='http', verify=None):
    """Return a laserjet handler, optionally customised"""
    def _lj(service, domain):
        """Advanced multiplexer for one service"""
        if service == 'certificate':
            _laserjet_push(domain, scheme, verify)
        else:
            raise ValueError("Unknown laserjet service {}".format(service))
    return _lj

handler = makehandler() # pylint: disable=invalid-name

def _laserjet_push(domain, scheme, verify=None):
    """Handler to push certificate to an HP Laserjet"""
    # Put the certificate, chain and private key into a PKCS12 to send to the printer
    lineage = os.environ['RENEWED_LINEAGE']
    cert_file = '{}/cert.pem'.format(lineage)
    pkey_file = '{}/privkey.pem'.format(lineage)
    chain_file = '{}/chain.pem'.format(lineage)
    pkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(pkey_file).read())
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(cert_file).read())
    chain = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(chain_file).read())
    pkcs12 = OpenSSL.crypto.PKCS12()
    pkcs12.set_privatekey(pkey)
    pkcs12.set_certificate(cert)
    pkcs12.set_ca_certificates([chain])

    # Generate a simple 20 character password
    password = ''.join(choice(string.ascii_letters + string.digits) for _ in range(20))

    files = {'FileName': ('import.pfx', pkcs12.export(passphrase=password))}

    url = '{}://{}/hp/device/Certificate.pfx'.format(scheme, domain)
    result = requests.post(url, data={'Password': password}, files=files, verify=verify)
    print("Printer responded with HTTP {}".format(result.status_code))
