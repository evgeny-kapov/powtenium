# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import socket
import subprocess
import time
import urllib

import pytest
from _pytest.skipping import MarkEvaluator

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from test.selenium.webdriver.common.webserver import SimpleWebServer
from test.selenium.webdriver.common.network import get_lan_ip

drivers = (
    'BlackBerry',
    'Chrome',
    'Edge',
    'Firefox',
    'Ie',
    'Marionette',
    'PhantomJS',
    'Remote',
    'Safari',
)


def pytest_addoption(parser):
    parser.addoption(
        '--driver',
        action='append',
        choices=drivers,
        dest='drivers',
        metavar='DRIVER',
        help='driver to run tests against ({0})'.format(', '.join(drivers)))


def pytest_ignore_collect(path, config):
    _drivers = set(drivers).difference(config.getoption('drivers') or drivers)
    parts = path.dirname.split(os.path.sep)
    return len([d for d in _drivers if d.lower() in parts]) > 0


@pytest.fixture(scope='function')
def driver(request):
    kwargs = {}

    try:
        driver_class = request.param
    except AttributeError:
        raise Exception('This test requires a --driver to be specified.')

    # conditionally mark tests as expected to fail based on driver
    request.node._evalxfail = request.node._evalxfail or MarkEvaluator(
        request.node, 'xfail_{0}'.format(driver_class.lower()))

    # skip driver instantiation if xfail(run=False)
    if not request.config.getoption('runxfail'):
        if request.node._evalxfail.istrue():
            if request.node._evalxfail.get('run') is False:
                yield
                return

    if driver_class == 'BlackBerry':
        kwargs.update({'device_password': 'password'})
    if driver_class == 'Firefox':
        kwargs.update({'capabilities': {'marionette': False}})
    if driver_class == 'Marionette':
        driver_class = 'Firefox'
    if driver_class == 'Remote':
        capabilities = DesiredCapabilities.FIREFOX.copy()
        kwargs.update({'desired_capabilities': capabilities})
    driver = getattr(webdriver, driver_class)(**kwargs)
    yield driver
    try:
        driver.quit()
    except:
        pass


@pytest.fixture
def pages(driver, webserver):
    class Pages(object):
        def url(self, name):
            return webserver.where_is(name)

        def load(self, name):
            driver.get(self.url(name))
    return Pages()


@pytest.fixture(autouse=True, scope='session')
def server(request):
    drivers = request.config.getoption('drivers')
    if drivers is None or 'Remote' not in drivers:
        yield None
        return

    _host = 'localhost'
    _port = 4444
    _path = 'buck-out/gen/java/server/src/org/openqa/grid/selenium/selenium.jar'

    def wait_for_server(url, timeout):
        start = time.time()
        while time.time() - start < timeout:
            try:
                urllib.urlopen(url)
                return 1
            except IOError:
                time.sleep(0.2)
        return 0

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    url = 'http://{}:{}/wd/hub'.format(_host, _port)
    try:
        _socket.connect((_host, _port))
        print('The remote driver server is already running or something else'
              'is using port {}, continuing...'.format(_port))
    except Exception:
        print('Starting the Selenium server')
        process = subprocess.Popen(['java', '-jar', _path])
        print('Selenium server running as process: {}'.format(process.pid))
        assert wait_for_server(url, 10), 'Timed out waiting for Selenium server at {}'.format(url)
        print('Selenium server is ready')
        yield process
        process.terminate()
        process.wait()
        print('Selenium server has been terminated')


@pytest.fixture(autouse=True, scope='session')
def webserver():
    webserver = SimpleWebServer(host=get_lan_ip())
    webserver.start()
    yield webserver
    webserver.stop()
