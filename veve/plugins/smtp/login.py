from smtplib import SMTP, SMTP_SSL
import sys
from veve.plugin import Plugin
from veve.response import Response


class Login(Plugin):
    SMTP_TLS_PORT = 587
    SMTP_SSL_PORT = 465
    SMTP_PLAIN_PORT = 25

    def __init__(self):
        self.args = None

    def description(self):
        return "SMTP password authentication"

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
            try:
                server, user, password = credentials.split(self.args.delimiter)
            except ValueError:
                return Response.error(f'Invalid format: {credentials}'), ""
        else:
            try:
                user, password = credentials.split(self.args.delimiter)
            except ValueError:
                return Response.error(f'Invalid format: {credentials}'), ""

        server = server.strip()
        user = user.strip()
        password = password.strip()

        result = self.__smtp_login(user, password, server)

        if result is True:
            return Response.ok(f'{server} - {user} : {password}'), ""

        return Response.error(f'{server} - {user} : {password} - {result}'), ""

    def options(self, parser):
        parser.add_argument('--server', help='IMAP server to use', required=False)
        parser.add_argument('--server-included', help='Server included in file', required=False, action='store_true')
        parser.add_argument('--target', help='File containing email:password combinations', required=False)
        parser.add_argument('--delimiter', help='Delimiter used in file', required=False, default=':')
        parser.add_argument('--ssl', help='Use SSL', required=False, action='store_true')
        parser.add_argument('--tls', help='Use TLS', required=False, action='store_true')
        parser.add_argument('--debug-level', help='Debug level', required=False, default=0, type=int)

    def __smtp_login(self, user, password, server):
        if self.args.ssl:
            try:
                smtp_ssl = SMTP_SSL(server, self.SMTP_SSL_PORT)
                smtp_ssl.set_debuglevel(self.args.debug_level)
                smtp_ssl.ehlo()
                smtp_ssl.login(user, password)
                smtp_ssl.quit()
                return True
            except Exception as e:
                return e

        if self.args.tls:
            try:
                smtp = SMTP(server, self.SMTP_TLS_PORT)
                smtp.set_debuglevel(self.args.debug_level)
                smtp.ehlo()
                smtp.starttls()
                smtp.login(user, password)
                smtp.quit()
                return True
            except Exception as e:
                return e

        try:
            smtp = SMTP(server, self.SMTP_PLAIN_PORT)
            smtp.set_debuglevel(self.args.debug_level)
            smtp.ehlo()
            smtp.login(user, password)
            smtp.quit()
            return True
        except Exception as e:
            return e
