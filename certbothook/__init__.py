#!/usr/bin/env python3
"""A deploy hook for certbot to run a handler on renewal"""

from __future__ import print_function

import os

from .handlers import systemctl_restart

__all__ = ['CertbotHook']

class CertbotHook(object):
    """Take an action when certbot renews a certificate"""
    # pylint: disable=too-few-public-methods

    def __init__(self, name, domains, services, once=True, handler=systemctl_restart):
        """Create and configure a CertbotHook

        Required parameters:

        :param name: A name for this hook
        :param domains: A list of domains for which this hook
                        should be run.
        :param services: The list of services to run the handler
                         for when a match is found.

        Optional parameters:

        :param once: Run the handlers only once when a match
                     is found. Default is True. This avoids
                     restarting services multiple times.
        :param handler: Specify a handler to use. The default
                        handler tries to restart the service
                        with systemd. This should be either a
                        function taking parameters (service, domain),
                        or a module containing a matching function named 'handler'.
        """
        # pylint: disable=too-many-arguments
        self.name = name
        self.domains = domains
        self.services = services
        self.once = once
        self.handler = handler

    def __call__(self, renewed=None):
        """Check for matching domains and run handlers

        This can either take a list of renewed domains via
        the parameter 'renewed' or will look in the enviroment
        for RENEWED_DOMAINS, which is set by certbot.
        """
        if renewed is None:
            if 'RENEWED_DOMAINS' not in os.environ:
                raise ValueError('No domains to renew and no RENEWED_DOMAIN environment variable')
            renewed = os.environ['RENEWED_DOMAINS'].split()

        for domain in renewed:
            if domain in self.domains:
                print('Hook {} matches {}'.format(
                    self.name, domain)
                     )
                for service in self.services:
                    # Allow handler to be either a module with
                    # a 'handler' function or just a function
                    if hasattr(self.handler, 'handler'):
                        self.handler.handler(service, domain)
                    else:
                        self.handler(service, domain)
                if self.once:
                    break
