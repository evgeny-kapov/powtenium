# Copyright 2008-2010 WebDriver committers
# Copyright 2008-2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import socket
import logging
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.remote_connection import RemoteConnection


LOGGER = logging.getLogger(__name__)
PORT = 0 #
HOST = None 
_URL = ""
class ExtensionConnection(RemoteConnection):
    def __init__(self, host, firefox_profile, firefox_binary=None, timeout=30):
        self.profile = firefox_profile
        self.binary = firefox_binary
        HOST = host
        if self.binary is None:
            self.binary = FirefoxBinary()

        if HOST is None:
            HOST = "127.0.0.1"

        PORT = self._free_port()
        self.profile.port = PORT 
        self.profile.update_preferences()
        
        self.profile.add_extension()

        self.binary.launch_browser(self.profile)
        _URL = "http://%s:%d/hub" % (HOST, PORT)
        RemoteConnection.__init__(
            self, _URL)

    def quit(self, sessionId=None):
        self.execute(Command.QUIT, {'sessionId':sessionId})
        while self.is_connectable():
            LOGGER.info("waiting to quit")
            time.sleep(1)

    def connect(self):
        """Connects to the extension and retrieves the session id."""
        return self.execute(Command.NEW_SESSION, {'desiredCapabilities': DesiredCapabilities.FIREFOX})
    
    @classmethod
    def connect_and_quit(cls):
        """Connects to an running browser and quit immediately."""
        self._request('%s/extensions/firefox/quit' % _URL)
    
    @classmethod
    def is_connectable(cls):
        """Trys to connect to the extension but do not retrieve context."""
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.settimeout(1)
            socket_.connect((HOST, PORT))
            socket_.close()
            return True
        except socket.error:
            return False

    def _free_port(self):
        free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        free_socket.bind((socket.gethostname(), 0))
        port = free_socket.getsockname()[1]
        free_socket.close()
        return port

class ExtensionConnectionError(Exception):
    """An internal error occurred int the extension.

    Might be caused by bad input or bugs in webdriver
    """
    pass

