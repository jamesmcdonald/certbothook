# certbothook

A python library to simplify the common task of running hooks
when [https://certbot.eff.org/](certbot) renews your
[https://letsencrypt.org/](Let's Encrypt) certificates.

## An example

```
#!/usr/bin/env python3
from certbothook import CertbotHook

hooks = [
  CertbotHook('web', ['me.example.com','you.example.com'], ['nginx']),
  CertbotHook('mail', ['mail.example.com'], ['dovecot', 'exim4']),
]

for hook in hooks:
    hook()
```

This example will restart `nginx` if certificates for me.example.com or
you.example.com are renewed. It will restart `dovecot` and `exim4` if
mail.example.com is renewed. That's it!

## Other parameters

You can override the service handler with the `handler` parameter. The default
handler, `systemctl_restart` will try to restart the service with `systemctl`.
There are 2 other handlers in the handlers package, and `echo` handler for
testing and a `laserjet` handler for pushing a certificate to your printer
(which works for me, but is not exactly "production grade").

You can easily make a custom handler; any method that takes (service, domain)
will work. Have a look at the examples.

There is another optional parameter `once`, which defaults to `True`. This
causes the list of services in a given hook to only be restarted once per run,
instead of once per domain. You can set this to `False` if you want your
handler to be called for every matching service, domain combination.
