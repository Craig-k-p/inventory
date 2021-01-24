import datetime
import inspect
import base64
import json
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.popup import Popup
Config.set('kivy', 'log_level', 'debug')

from resources.exceptions import PasswordAttemptsExceededError


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


class Security(LogMethods):
    '''Encrypt and decrypt user data with a password'''
    def __init__(self, app):
        self.__initLog__('utilities.py', 'Security')
        self._c = None
        # self._a = 0
        self._app = app

    def createPassword(self):
        self._getCypher(reset=True)

    def decryptFile(self, en_file_name):
        '''Load the encrypted file'''
        with open(self._app.settings['save file path'] + en_file_name, 'rb') as f:
            try:
                self._app.user_file_en = True
                return json.loads(self._getCypher(reset=True).decrypt(f.read()))
            except InvalidToken:
                # self._a += 1
                self._app.user_file_en = False
                self.logInfo('Invalid password attempt')
                return None

    def encryptFile(self, file_name, data):
        '''Encrypt the given contents and save to file_name'''
        with open(file_name, 'wb') as f:
            f.write(self._getCypher().encrypt(bytes(json.dumps(data).encode('utf-8'))))

    def reset(self):
        self._c = None

    def _getCypher(self, reset=False):
        '''Get cypher from user's password and return it'''
        if self._c != None and reset == False:
            return Fernet(self._c)
        else:
            # No _c... get it from the user's password
            self._c = self._getKDF().derive(self._app.pop.content.prompt.text.encode())
            self._c = base64.urlsafe_b64encode(self._c)
            return self._getCypher()

    def _getKDF(self):
        '''Return key derivation function'''
        return PBKDF2HMAC(
                    algorithm=hashes.SHA256,
                    length=32,
                    salt=self._loadSalt(),
                    iterations=146214,
                    backend=default_backend()
                )

    def _generateSalt(self):
        '''Make a salt if user doesn't have one already'''
        self.logWarning('Generating new SALT')
        path = os.path.join(os.getcwd(), 'save_data/.scrt/')
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print('Failure')

        with open(f'{path}/.file_salt', 'wb') as f:
            f.write(os.urandom(16))

    def _loadSalt(self):
        '''Return the saved salt or call for one to be created'''
        success = False
        i = 0
        while success == False:
            i += 1
            try:
                with open('save_data/.scrt/.file_salt', 'rb') as salt:
                    return salt.read()
            except FileNotFoundError:
                self._generateSalt()

            if i > 4:
                return None
