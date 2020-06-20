# -*- coding: utf-8 -*-

from json.decoder import JSONDecodeError
import logging
import logging.config

def initialize_logging(logfile_name):
    """
    Initialize logging defaults for Project.

    :param logfile_name: logfile used to the logfile
    :type logfile_name: string

    :Example from execution module, it will write out to mytest.log
        import logging
        import Loggerimport

        Logger.initialize_logging('mytest.log')
        log = logging.getLogger('root')
        log.debug("Logging is configured")
    """

    LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'long_format': {
                    'format': '%(asctime)s %(levelname)s %(filename)s:%(name)s:%(lineno)d %(message)s',
                    'datefmt': '%m/%d/%Y %H:%M:%S'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'long_format',
                    'level': 'DEBUG',
                    'stream': 'ext://sys.stdout'
                },
                'default_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'long_format',
                    "filename": logfile_name,
                    'maxBytes': 51200000,
                    'backupCount': 10,
                    'encoding': 'utf8'
                },
            },

            'loggers': {
                'root': {
                    'level': 'DEBUG',
                    'handlers': ['default_file_handler'],
                    'propagate': False
                }
            }
        }

    try:
        logging.config.dictConfig(LOGGING_CONFIG)
    except JSONDecodeError:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().error('malformed JSON config file for logging')
        raise
