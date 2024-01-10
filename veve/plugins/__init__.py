from veve.manager import Manager

from veve.plugins.imap.login import Login as ImapLogin
from veve.plugins.smtp.login import Login as SmtpLogin

Manager.register("imap.login", ImapLogin())
Manager.register("smtp.login", SmtpLogin())
