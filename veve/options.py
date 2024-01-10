import argparse
from veve.manager import Manager


def options():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--concurrency', help='Number of threads to use', required=False, default=10, type=int)
    parent_parser.add_argument('--output-format', help='Output format', required=False, default='txt')
    parent_parser.add_argument('--timeout', help='Timeout for each request', required=False, default=30, type=int)

    parser = argparse.ArgumentParser()
    parser.add_argument("--list-plugins", action="store_true", help="List all available plugins")
    parser.add_argument("--version", action="store_true", help="Show version and exit")

    registry = Manager.registry
    subparsers = parser.add_subparsers(dest="plugin", help="Select a plugin")

    for plugin_name, plugin in registry.items():
        plugin_parser = subparsers.add_parser(plugin_name, help=plugin.description(), parents=[parent_parser])
        plugin.options(plugin_parser)

    return parser.parse_args(), registry
