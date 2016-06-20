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

import unittest
import base64
import imghdr


class ScreenshotTests(unittest.TestCase):

    def test_get_screenshot_as_base64(self):
        self._loadSimplePage()
        result = base64.b64decode(self.driver.get_screenshot_as_base64())
        self.assertEqual(imghdr.what('', result), 'png')

    def test_get_screenshot_as_png(self):
        self._loadSimplePage()
        result = self.driver.get_screenshot_as_png()
        self.assertEqual(imghdr.what('', result), 'png')

    def _pageURL(self, name):
        return self.webserver.where_is(name + '.html')

    def _loadSimplePage(self):
        self._loadPage("simpleTest")

    def _loadPage(self, name):
        self.driver.get(self._pageURL(name))
