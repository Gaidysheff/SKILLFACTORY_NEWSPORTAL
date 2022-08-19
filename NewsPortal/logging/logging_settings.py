import logging

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/logging/email-messages'


class CustomHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    def emit(self, record):
        message = self.format(record)
        with open(self.filename, 'a') as file:
            file.write(message + '\n')


class NewFunctionFilter(logging.Filter):
    def filter(self, record):
        print(record.new_name)
        return record.funcName == 'new_function'


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose_1': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{'
        },
        'verbose_2': {
            'format': '{asctime} - {levelname} - {message} - {pathname}',
            'style': '{'
        },
        'verbose_3': {
            'format': '{asctime} - {levelname} - {message} - {pathname} - {exc_info}',
            'style': '{'
        },
        'verbose_4': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{'
        },
        'verbose_custome': {
            'format': '{asctime} - {levelname} - {module}  - {funcName} - {lineno} - {message} - {new_name}',
            'style': '{'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'custom_filter': {
            '()': NewFunctionFilter,
        },
    },
    'handlers': {
        'console_1': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true', ],
            'level': 'DEBUG',
            'formatter': 'verbose_1',
        },
        'console_2': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true', ],
            'level': 'WARNING',
            'formatter': 'verbose_2'
        },
        'console_3': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'filters': ['require_debug_true', ],
            'formatter': 'verbose_3'
        },
        'file_1': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'filename': 'general.log',
            'filters': ['require_debug_false', ],
            'formatter': 'verbose_4',
        },
        'file_2': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'filename': 'error.log',
            'formatter': 'verbose_3',
        },
        'file_3': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'filename': 'security.log',
            'formatter': 'verbose_4',
        },
        'file_custom': {
            '()': CustomHandler,
            'level': 'DEBUG',
            'filters': ['custom_filter', ],
            'filename': 'debug.log',
            'formatter': 'verbose_custome',
        },
        'file_custom_2': {
            '()': CustomHandler,
            'level': 'DEBUG',
            'filename': 'test2.log',
            'formatter': 'verbose_4',
        },
        # 'mail_admins': {
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     # 'class': 'logging.SMTPHandler',
        #     'level': 'ERROR',
        #     'filters': ['require_debug_false', ],
        #     'formatter': 'verbose_2',
        #     'email_backend': 'django.core.mail.backends.filebased.EmailBackend',
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console_1', 'console_2', 'console_3', 'file_1', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_2', ],  # 'mail_admins'
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_2', ],  # 'mail_admins'
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_2', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['file_2', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_3', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'custom_logger': {
            'handlers': ['file_custom', 'file_custom_2', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    },

    # 'incremental': True
}
