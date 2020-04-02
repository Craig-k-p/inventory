import datetime
import os.path
import inspect

from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.popup import Popup
Config.set('kivy', 'log_level', 'debug')


class UtilityMethods():
    '''Used to extend the Kivy Screen widgets found in kv_screens.py and main_widgets.kv'''

    def resetTextInputs(self):
        '''Reset the text input fields for this screen'''
        for widget in self.widgets['TextInputs']:
            self.widgets['TextInputs'][widget].text = ''

    def isEmail(self, email):
        '''Work on this'''

        if '@' not in email:
            return False
        elif '.' not in email:
            return False
        elif len(email) < 5:
            return False

        else:
            return True

    def checkPw(self, pw, pw2):
        '''Check passwords for length and matching'''
        if len(pw) < self.manager.app.settings['password min length']:
            return False
        elif pw != pw2:
            return False
        else:
            return True


class LogMethods():
    filter = []
    def __initLog__(self, file_str='', class_str=''):
        ''' It looksl like Kivy has it's own implementation of logging.  Instead of creating a custom
            logger, scroll to the bottom of this doc string.

        Resources:
            https://docs.python.org/3/library/logging.html
            Log to a terminal and file:
                https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
            DictConfig dictionary example:
                https://stackoverflow.com/questions/7507825/...
                ...where-is-a-complete-example-of-logging-config-dictconfig

        Logging Levels:
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
                current thread, up to the logging call.

        ---------- SAMPLE CODE -----------
        # Get the absolute path to the current file
        # Resource:
        # https://stackoverflow.com/questions/17249701/...
        #     ...how-can-i-find-the-currently-executing-script-file-and-path-in-python
        file_path = os.path.dirname(os.path.abspath(__file__))

        # Set formatting for the Formatter instances
        log_format = '%(levelname)s:%(filename)s:%(name)s:%(funcName)s:%(lineno)s'
        log_format += f'\n\t{now.hour}:{now.minute}:{now.second}    >>>    %(message)s\n'

        # See resource above
        log_dict_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': log_format
                }
            },
            #    - the corresponding value will be a dict in which each key is a formatter id
            #      and each value is a dict describing how to configure the corresponding Formatter
            #      instance.
            # 'filters': {},
            #    - the corresponding value will be a dict in which each key is a filter id and each
            #      value is a dict describing how to configure the corresponding Filter instance.
            'handlers': {
                'default': {
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout'
                },
                'log_filer': {
                    'level': 'WARNING',
                    'formatter': 'standard',
                    'class': 'logging.FileHandler',
                    'filename': file_path
                }
            },
            #    - the corresponding value will be a dict in which each key is a handler id and each
            #      value is a dict describing how to configure the corresponding Handler instance.
            #      The configuring dict is searched for the following keys:
            # class (mandatory). This is the fully qualified name of the handler class.
            # level (optional). The level of the handler.
            # formatter (optional). The id of the formatter for this handler.
            # filters (optional). A list of ids of the filters for this handler.
            'loggers': {
                '': {  # Root logger. Additional loggers inherit from this instance.
                    'handlers': ['default', 'log_filer'],
                    'level': 'INFO',
                    'propogate': True
                }
            }

        # Tried this from the following resource, but it didn't work
        # https://stackoverflow.com/questions/36785002/basic-logging-dictconfig-in-python?noredirect=1
        # ...It looks like Kivy overrides the Python logging module with it's own custome implementation
        # Using the Python implementation is beyond my skill at this point.
        logging.config.dictConfig(log_dict_config)
        '''

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


# class WindowKeyboard():
#     def __init__(self):
#         '''Essentially this allows the init method of both inherited classes by LoginWindow
#            to execute.  If we didn't call this, Screen's init method would be the only init
#            method to execute on top of LoginWindow's init method.  This ensures that all
#            three execute.
#            https://stackoverflow.com/questions/
#            3277367/how-does-pythons-super-work-with-multiple-inheritance'''
#         super(WindowKeyboard, self).__init__()

#     def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
#         ''' Check if a popup is open so we don't keep opening popups.
#             -- Need to fix:
#                 - enter only executes buttonPressLogin().  Need to make it handle
#                   executing different functions.'''

#         if keycode == 40:  # 40 - Enter key pressed
#             self.logDebug('kvLogic', f'The enter key was pressed (keycode 40)..')
#             # Check if a popup is open already.  If so, close it.

#             if isinstance(App.get_running_app().sm.current_screen.children[0], Popup):
#                 App.get_running_app().root_window.children[0].dismiss()
#                 self.logDebug('kv_ops', '  ..and the popup was dismissed')

#             # Otherwise, execute the following function
#             else:
#                 self.logDebug('kvLogic', '  ..and self.buttonPress was called')
#                 self.buttonPress()
