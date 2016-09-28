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


import pytest

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


@pytest.yield_fixture
def driver(capabilities):
    options = Options()
    driver = Firefox(
        capabilities=capabilities,
        firefox_options=options)
    yield driver
    driver.quit()


class TestOptions(object):

    def test_we_can_pass_options(self, driver, pages):
        pages.load('formPage.html')
        driver.find_element_by_id("cheese")
