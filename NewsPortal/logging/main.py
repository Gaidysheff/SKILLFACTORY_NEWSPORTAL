import logging.config
from logging.handlers import RotatingFileHandler

from logging_settings import logger_config


logging.config.dictConfig(logger_config)


logger = logging.getLogger('django')
print('Level of logger ("django") =', logger.level)

logger_custom = logging.getLogger('custom_logger')
print('Level of logger ("django") =', logger_custom.level)


# logger_request = logging.getLogger('django.request')
# print('Level of logger_request =', logger_request.level)
# logger_server = logging.getLogger('django.server')
# print('Level of logger_server =', logger_server.level)
# logger_template = logging.getLogger('django.template')
# print('Level of logger_template =', logger_template.level)
# logger_db_backends = logging.getLogger('django.db_backends')
# print('Level of logger_db_backends =', logger_db_backends.level)
# logger_security = logging.getLogger('django.security')
# print('Level of logger_security =', logger_security.level)


# std_format = logging.Formatter(
#     fmt='{asctime} - {levelname} - {name} - {message}', style='{')

# logger.setLevel(10)
# handler_1 = logging.StreamHandler()
# handler_1.setLevel(10)
# logger.addHandler(handler_1)
# handler_1.setFormatter(std_format)


# handler_2 = logging.FileHandler('NewsPortal/logging/mylog.log', mode='a')
# handler_2.setLevel(10)
# logger.addHandler(handler_2)
# handler_2.setFormatter(std_format)


# logger.debug('print DEBUG message')
# logger.info('print INFO message')
# logger.warning('print WARNING message')
# logger.error('print ERROR message')
# logger.critical('print CRITICAL message')

# logger_request = logging.getLogger('django.request')

# print(logger)
# print(logger.parent)
# print()
# print(logger_request)
# print(logger_request.parent)
# print()


def new_function():
    name = 'eugene'
    logger_custom.info('test - Enter into the new_function() - This variable makes the PROBLEM', extra={
        'new_name': name}, exc_info=True)


def main():
    name = 'eugene'
    logger_custom.error(
        'test - Enter into the main()', extra={'new_name': name})

# -----------------------------Исключения в процессе логгирования----------------------------------------


words = ['new log', 'old logger', 'simple format', 33]


def function():
    for item in words:
        try:
            print(item.split(' '))
        except:
            logger_custom.error(
                f'test - Exception here, problem with item = {item}', exc_info=True)

# -----------------------------ротация файлов журнала----------------------------------------


def create_rotating_log(path):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(path, maxBytes=5, backupCount=3)
    logger.addHandler(handler)

    for i in range(100):
        logger.info("Это тестовая строка-запись в журнале %s" % i)

# -----------------------------------------------------------------------------------------------


if __name__ == '__main__':
    new_function()
    main()
    function()

    log_file = "test2.log"
    create_rotating_log(log_file)
