import logging
import os
from django.conf import settings


LOG_PATH = os.path.dirname(os.path.dirname(__file__)) + '/logs/'


class LogHandler(object):
    """Log Handler class.

    Generates log handling objects to modules and makes it easier to
    add methods and events to them

    Args:
        module (str): Calling module name
        level (str): Min log level
    """

    def __init__(self, module, level='DEBUG'):
        # Initialize logger
        self.logger = logging.getLogger(module)
        self.logger.setLevel(getattr(logging, level, 'DEBUG'))

        # Formatter
        formatter_full = logging.Formatter('%(asctime)-15s %(levelname)-8s %(name)-15s: %(message)s', '%d/%m/%Y %H:%M:%S')
        formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s: %(message)s', '%d/%m/%Y %H:%M:%S')

        # Stream Handler
        st = logging.StreamHandler()
        st.setLevel(getattr(logging, level, 'DEBUG'))
        st.setFormatter(formatter_full)
        self.logger.addHandler(st)

        # Module File Handler
        # fl = logging.FileHandler(LOG_PATH + module + '.log')
        # fl.setLevel(getattr(logging, level, 'DEBUG'))
        # fl.setFormatter(formatter)
        # self.logger.addHandler(fl)

        # Full File Handler
        # fu = logging.FileHandler(LOG_PATH + 'full.log')
        # fu.setLevel(getattr(logging, level, 'DEBUG'))
        # fu.setFormatter(formatter_full)
        # self.logger.addHandler(fu)

        # SMTP Handler
        sm = logging.handlers.SMTPHandler(
            mailhost=('smtp.gmail.com', 587),
            fromaddr=settings.DEFAULT_FROM_EMAIL,
            toaddrs=settings.ADMINS[0][1],
            subject="[Django] Manual Error",
            credentials=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD),
            secure=())
        sm.setLevel(getattr(logging, level, 'DEBUG'))
        sm.setFormatter(formatter_full)
        self.logger.addHandler(sm)

        """Uncomment to allow HTTP handling
        # HTTP Handler
        ht = logging.handlers.HTTPHandler()
        ht.setLevel(getattr(logging, level, 'DEBUG'))
        ht.setFormatter(formatter_full)
        self.logger.addHandler(ht)
        """
