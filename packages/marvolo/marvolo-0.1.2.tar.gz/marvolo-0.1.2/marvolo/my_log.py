import logging
import colorlog
from datetime import datetime, timezone, timedelta

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

default_formats = {
    'color_format': '%(log_color)s%(asctime)s [%(levelname)s] : %(message)s',
}

class HandleLog:
    def __init__(self):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.INFO)

    @staticmethod
    def __init_console_handle():
        console_handle = colorlog.StreamHandler()
        return console_handle

    def __set_color_handle(self, console_handle):
        console_handle.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handle)

    @staticmethod
    def __set_color_formatter(console_handle, color_config):
        formatter = colorlog.ColoredFormatter(default_formats["color_format"], log_colors=color_config, datefmt='%m-%d %H:%M:%S')
        console_handle.setFormatter(formatter)

    def __console(self, level, message):
        console_handle = self.__init_console_handle()

        self.__set_color_formatter(console_handle, log_colors_config)
        self.__set_color_handle(console_handle)

        if level == 'info':
            self.__logger.info(message)
        elif level == 'debug':
            self.__logger.debug(message)
        elif level == 'warning':
            self.__logger.warning(message)
        elif level == 'error':
            self.__logger.error(message)
        elif level == 'critical':
            self.__logger.critical(message)

        self.__logger.removeHandler(console_handle)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def critical(self, message):
        self.__console('critical', message)

log = HandleLog()
