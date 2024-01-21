import requests
import re
from veve.plugin import Plugin
from veve.response import Response

class Enum(Plugin):
    def __init__(self) -> None:
        self.args = None

    def description(self) -> str:
        return "HTTP Form email/usernames enumeration"

    def setup(self, args) -> None:
        self.args = args

    def run(self, credentials) -> dict:
        url = credentials.split("#")[1]
        payload = credentials.split("#")[0]

        result = self.__http_form_enumeration(payload, url)

        if result is True:
            return Response.ok(f'{url} - {payload}'), ""

        return Response.error(f'{url} - {payload}'), ""

    def options(self, parser) -> None:
        parser.add_argument('--target', help='File containing URL to use', required=False)
        parser.add_argument('--csrf-page', help='CSRF page to grab the CSRF Token', required=False)
        parser.add_argument('--csrf-regexp', help='CSRF token to use', required=False)
        parser.add_argument('--http-method', help='HTTP method to use', required=False, default='POST')
        parser.add_argument('--http-payload', help='HTTP payload to use', required=True)
        parser.add_argument('--http-success-string', help='HTTP Success Code', required=False, default='302')
        parser.add_argument('--payloads', help='Payloads file to use', required=True)

    def __http_form_enumeration(self, payload, url) -> bool:

        with requests.Session() as session:
            response = session.get(self.args.csrf_page)
            token = re.search(self.args.csrf_regexp, response.text).group(1)

            input_data = self.args.http_payload.replace('{PAYLOAD}', payload).replace('{TOKEN}', token)
            data = self.__payload_to_dict(input_data)

            if self.args.http_method == 'POST':
                response = session.post(url, data=data)

                success_string = self.args.http_success_string
                if success_string in response.text:
                    return True

        return False

    def __payload_to_dict(self, payload) -> dict:
        list_payload = payload.split('&')
        dict_payload = {}
        for item in list_payload:
            key, value = item.split('=')
            dict_payload[key] = value
        return dict_payload
