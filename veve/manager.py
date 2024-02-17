import gevent

from gevent.queue import Queue
from gevent.monkey import patch_all
patch_all()


class Manager:
    registry = {}
    tasks = Queue()
    plugin = None
    targets = None

    def __init__(self, session):
        self.session = session
        self.options = session.options
        self.plugin_name = self.options.plugin
        self.targets = self.options.target

        self.__load_tasks()

    @staticmethod
    def register(plugin_name, plugin):
        Manager.registry[plugin_name] = plugin

    def setup(self):
        plugin = self.__get_plugin(self.plugin_name)
        plugin.setup(self.options)
        self.plugin = plugin

    def start(self):
        workers = [gevent.spawn(self.__worker) for _ in range(self.options.concurrency)]
        gevent.joinall(workers)

    def __get_plugin(self, plugin_name):
        return self.registry[plugin_name]

    def __worker(self):
        while not self.tasks.empty():
            creds = self.tasks.get()

            result, message = gevent.with_timeout(self.options.timeout, self.plugin.run, creds, timeout_value=(False, "timeout occured"))

            if message == "timeout occured":
                self.session.error(self.plugin_name, message)
            else:
                self.session.append(self.plugin_name, result)


    def __load_tasks(self,):
        # TODO: refactor to handle without payloads
        if self.options.single:
            payloads = self.__load_payloads(self.options.payloads)

            for _, payload in enumerate(payloads):
                self.tasks.put_nowait(f"{payload}#{self.options.target}")

        elif self.options.multiple:
            targets = self.__load_targets(self.options.target)

            for _, target in enumerate(targets):
                self.tasks.put_nowait(target)

    def __load_payloads(self, payloads) -> list:
        with open(payloads, 'r', encoding='utf-8') as fp:
            lines = fp.read().splitlines()

        return lines

    def __load_targets(self, targets) -> list:
        with open(targets, 'r', encoding='utf-8') as fp:
            lines = fp.read().splitlines()

        return lines
    