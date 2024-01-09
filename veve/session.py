import logging
import os
import sys
from datetime import datetime
import json


class Session:
    output_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../output')

    def __init__(self, options):
        self.options = options
        self.file_formats = ['jsonl', 'txt']

        if self.options.output_format not in self.file_formats:
            print('Error: Invalid output format\n')
            print(f'Available formats: {", ".join(self.file_formats)}')
            sys.exit(1)

        if not self.options.target:
            print('Error: Target file not specified')
            sys.exit(1)

        logging.info("using file -> %s", f'{self.options.target}\n')

    def ok(self, plugin, data):
        logging.info("%s - %s", plugin, data)
        self.save(plugin, data, "success")

    def error(self, plugin, data):
        logging.error("%s - %s", plugin, data)
        self.save(plugin, data, "error")

    def save(self, plugin, data, saving_type):

        # jsonl format
        if self.options.output_format == self.file_formats[0]:
            self.to_jsonl(plugin, data, saving_type)

        # txt format
        elif self.options.output_format == self.file_formats[1]:
            self.to_txt(plugin, data, saving_type)

        # default format
        else:
            self.to_txt(plugin, data, saving_type)

    def found_at(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_jsonl(self, plugin, data, saving_type):
        with open(f'{self.output_directory}/{plugin}-{saving_type}.jsonl', 'a+', encoding='utf-8') as fp:
            json.dump({'date': self.found_at(), 'plugin': plugin, 'data': data}, fp)
            fp.write('\n')

    def to_txt(self, plugin, data, saving_type):
        with open(f'{self.output_directory}/{plugin}-{saving_type}.txt', 'a+', encoding='utf-8') as fp:
            fp.write(f'{self.found_at()} - {plugin} - {data}\n')
