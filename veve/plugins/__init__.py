from veve.manager import Manager

from veve.plugins.imap.login import Login

Manager.register("imap.login", Login())
