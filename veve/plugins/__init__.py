from veve.manager import Manager

from veve.plugins.imap.login import Login as ImapLogin
from veve.plugins.smtp.login import Login as SmtpLogin
from veve.plugins.pop3.login import Login as Pop3Login
from veve.plugins.http.enum import Enum as HttpEnum

Manager.register("imap.login", ImapLogin())
Manager.register("smtp.login", SmtpLogin())
Manager.register("pop3.login", Pop3Login())
Manager.register("http.enum", HttpEnum())
