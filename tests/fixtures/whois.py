import unittest
import time
import SocketServer
import re
import string

not_found = """\
# Not found [%s]
--- ~
"""

_db = {'domaintest.net': {'domain': 'domaintest.net',
                          'registrar': 'A new Registrar',
                          'whoisserver': '',
                          'ns0': 'zero.dns.registrar.net',
                          'ns1': 'un.dns.registrar.net',
                          'transferStatus': 'ok',
                          'update': '',
                          'create': '',
                          'expire': ''}}

tpl_response = {
    'default': string.Template("""\
Whois Server Version 2.0

Domain names in the .com and .net domains can now be registered
with many different competing registrars. Go to http://www.internic.net
for detailed information.

   Domain Name: $domain
   Registrar: $registrar
   Whois Server: $whoisserver
   Name Server: $ns0
   Name Server: $ns1
   Status: $transferStatus
   Updated Date: $update
   Creation Date: $create
   Expiration Date: $expire""")}


class UnkownDomain(Exception):
    pass


class WhoisServiceBase:

    def _get_domain(self, domain):
        if not re.match('^[a-z0-9\-]+(\.[a-z0-9]{2,63})+$', domain):
            raise RuntimeError("Invalid domain '%s'" % domain)
        if domain not in _db:
            raise UnkownDomain(domain)
        return domain

    def get_response(self, domain):
        d = _db[domain].copy()
        rv = tpl_response[d.pop('tpl_domain', 'default')].substitute(**d)
        return rv


class WhoisService(WhoisServiceBase, SocketServer.BaseRequestHandler):

    def read(self):
        buf = self.request.recv(1024)
        buf = buf.splitlines()
        domain = buf.pop()
        domain = domain.replace('domain ', '')
        return domain

    def handle(self):
        try:
            domain = self._get_domain(self.read())
            self.request.send(self.get_response(domain))
        except UnkownDomain, ude:
            self.request.send(not_found % str(ude))
        except Exception:
            import traceback
            traceback.print_exc()
            self.request.send("Internal server error")


class FixtureWhois(unittest.TestCase):

    hostname = '127.0.0.1'
    port = 4343

    def setUp(self):
        """
        Starting the whois server in a thread
        """

        from multiprocessing import Process

        self.process = Process(target=self.start_process)
        self.process.start()
        time.sleep(1)

    def start_process(self):
        self.server = SocketServer.TCPServer((self.hostname, self.port),
                                             WhoisService,
                                             bind_and_activate=False)

        self.server.allow_reuse_address = True
        self.server.server_bind()
        self.server.server_activate()
        self.server.serve_forever()

    def tearDown(self):
        """
        Terminate the whois server
        """
        self.process.terminate()
