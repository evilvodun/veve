import time
import sys
import toml
from veve.log import Log
from veve.manager import Manager
from veve.session import Session
from veve import options as Options


def setup():
    config = toml.load("config.toml")


    log = Log()
    log.setup_logging()

    options, registry = Options.options()

    if options.list_plugins:
        print("Available plugins:")
        for plugin_name, plugin in registry.items():
            print(f"\t{plugin_name} - {plugin.description()}")
        sys.exit(0)

    if options.version:
        print(f"{config['name']} v{config['version']}")
        sys.exit(0)

    print(f"{config['name']} v{config['version']}\n")

    return options


def main():
    opts = setup()
    session = Session(opts)
    manager = Manager(session)

    manager.setup()

    print(f"Running {opts.plugin} plugin...\n")
    print(f"Loaded Targets: {manager.targets}\n")

    start = time.perf_counter()

    try:
        manager.start()
    except KeyboardInterrupt:
        print("\n\nStopping...")
        sys.exit(1)

    finish = time.perf_counter()

    print(f"\nFinished in {round(finish - start, 2)} second(s)")


if __name__ == "__main__":
    main()
