from imaplib import IMAP4_SSL
import sys
from veve.plugins import Plugin
from veve.plugins import Manager
from veve import Response


class Login(Plugin):
    def __init__(self):
        self.args = None

    def description(self):
        return 'IMAP password authentication.'

    def setup(self, args):
        server = args.server
        server_included = args.server_included

        if server is None and server_included is False:
            print('Error: Server not specified')
            sys.exit(1)

        if server and server_included:
            print('Error: Cannot use both server and server-included options')
            sys.exit(1)

        self.args = args

    def run(self, credentials):
        server = self.args.server

        if self.args.server_included:
            server, user, password = credentials.split(self.args.delimiter)
        else:
            user, password = credentials.split(self.args.delimiter)

        server = server.strip()
        user = user.strip()
        password = password.strip()

        result = self.__imap_login(user, password, server)

        if result is True:
            return Response.ok(f'{server} - {user} : {password}'), ""

        return Response.error(f'{server} - {user} : {password} - {self.__clean_bytes(result)}'), ""

    def options(self, parser):
        parser.add_argument('--server', help='IMAP server to use', required=False)
        parser.add_argument('--server-included', help='Server included in file', required=False, action='store_true')
        parser.add_argument('--target', help='File containing email:password combinations', required=False)
        parser.add_argument('--delimiter', help='Delimiter used in file', required=False, default=':')

    def __imap_login(self, user, password, server):
        try:
            imap = IMAP4_SSL(server)
            imap.login(user, password)
            imap.logout()
            return True
        except IMAP4_SSL.error as e:
            return e

    def __clean_bytes(self, b):
        try:
            return str(b).split('b\'')[1].split('\'')[0]
        except Exception:
            return str(b)


Manager.register("imap.login", Login())
