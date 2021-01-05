import datetime
import os.path
import inspect

from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.popup import Popup
Config.set('kivy', 'log_level', 'debug')


class LogMethods():
    filter = []
    def __initLog__(self, file_str='', class_str=''):
        '''Logging Levels:
            Debug:  Detailed information for debugging purposes
            Info:  Confirmation that things are working as expected
            Warning:  Indication that something unexpected happened or there is a potential
                      problem in the future: Disk space low
            Error:  Due to a serious problem, the software failed to complete a function
            Critical:  A problem likely to cause the program to stop working

        Formatting Parameters:
            name –
                The name of the logger used to log the event represented by this LogRecord.
                Note that this name will always have this value, even though it may be emitted
                by a handler attached to a different (ancestor) logger.
            level –
                The numeric level of the logging event (one of DEBUG, INFO etc.) Note that this
                is converted to two attributes of the LogRecord: levelno for the numeric value
                and levelname for the corresponding level name.
            pathname –
                The full pathname of the source file where the logging call was made.
            lineno –
                The line number in the source file where the logging call was made.
            msg –
                The event description message, possibly a format string with placeholders for
                variable data.
            args –
                Variable data to merge into the msg argument to obtain the event description.
            exc_info –
                An exception tuple with the current exception information, or None if no exception
                information is available.
            func –
                The name of the function or method from which the logging call was invoked.
            sinfo –
                A text string representing stack information from the base of the stack in the
                current thread, up to the logging call.'''

        self.file = file_str
        self.calling_class = class_str

    def logDebug(self, message):
        ''' message -> string'''
        caller = inspect.stack()[1]
        filename = self._getFileNameFromPath(caller[1])
        # Skip log if filtering is enabled
        if len(self.filter) > 0:
            if filename not in self.filter:
                return
        lineno = caller[2]
        function = caller[3]
        log_str = f'{filename}: [{self.calling_class}.{function}][{lineno}]'
        log_str += f' {message}\n'
        Logger.debug(log_str)

    def logInfo(self, message):
        ''' message -> string'''
        caller = inspect.stack()[1]
        filename = self._getFileNameFromPath(caller[1])
        # Skip log if filtering is enabled
        if len(self.filter) > 0:
            if filename not in self.filter:
                return
        lineno = caller[2]
        function = caller[3]
        log_str = f'{filename}: [{self.calling_class}.{function}][{lineno}]'
        log_str += f' {message}\n'
        Logger.info(log_str)

    def logWarning(self, message):
        ''' message -> string'''
        caller = inspect.stack()[1]
        filename = self._getFileNameFromPath(caller[1])
        # Skip log if filtering is enabled
        if len(self.filter) > 0:
            if filename not in self.filter:
                return
        lineno = caller[2]
        function = caller[3]
        log_str = f'{filename}: [{self.calling_class}.{function}][{lineno}]'
        log_str += f' {message}\n'
        Logger.warning(log_str)

    def logError(self, message):
        ''' message -> string'''
        caller = inspect.stack()[1]
        filename = self._getFileNameFromPath(caller[1])
        # Skip log if filtering is enabled
        if len(self.filter) > 0:
            if filename not in self.filter:
                return
        lineno = caller[2]
        function = caller[3]
        log_str = f'{filename}: [{self.calling_class}.{function}][{lineno}]'
        log_str += f' {message}\n'
        Logger.error(log_str)

    def logCritical(self, message):
        ''' message -> string'''
        caller = inspect.stack()[1]
        filename = self._getFileNameFromPath(caller[1])
        # Skip log if filtering is enabled
        if len(self.filter) > 0:
            if filename not in self.filter:
                return
        lineno = caller[2]
        function = caller[3]
        log_str = f'{filename}: [{self.calling_class}.{function}][{lineno}]'
        log_str += f' {message}\n'
        Logger.critical(log_str)

    def logTrace(self, message):
        ''' -> string
           message -> string'''
        caller = inspect.stack()[1]
        filename = self._getFileNameFromPath(caller[1])
        # Skip log if filtering is enabled
        if len(self.filter) > 0:
            if filename not in self.filter:
                return
        lineno = caller[2]
        function = caller[3]
        log_str = f'{filename}: [{self.calling_class}.{function}][{lineno}]'
        log_str += f' {message}\n'
        Logger.trace(log_str)

    def _getFileNameFromPath(self, file_path):
        end_folders = file_path.rfind('\\')
        file_name = file_path[end_folders + 1:]
        return file_name
