from poplib import POP3, POP3_SSL
import sys
from veve.plugin import Plugin
from veve.response import Response


class Login(Plugin):
    def __init__(self):
        self.args = None

    def description(self):
        return "POP3 password authentication"

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

        result = self.__pop3_login(user, password, server)

        if result is True:
            return Response.ok(f'{server} - {user} : {password}'), ""

        return Response.error(f'{server} - {user} : {password} - {self.__clean_bytes(result)}'), ""

    def options(self, parser):
        parser.add_argument('--server', help='IMAP server to use', required=False)
        parser.add_argument('--server-included', help='Server included in file', required=False, action='store_true')
        parser.add_argument('--target', help='File containing email:password combinations', required=False)
        parser.add_argument('--delimiter', help='Delimiter used in file', required=False, default=':')
        parser.add_argument('--ssl', help='Use SSL', required=False, action='store_true')
        parser.add_argument("--debug-level", help="Debug level", required=False, default=0, type=int)


    def __pop3_login(self, user, password, server):
        try:
            if self.args.ssl:
                pop3 = POP3_SSL(server)
            else:
                pop3 = POP3(server)

            pop3.set_debuglevel(self.args.debug_level)
            pop3.user(user)
            pop3.pass_(password)
            pop3.quit()
            return True
        except Exception as e:
            return e


    def __clean_bytes(self, b):
        try:
            return str(b).split('b\'')[1].split('\'')[0]
        except Exception:
            return str(b)
