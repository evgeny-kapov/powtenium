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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By

class ChildrenFindingTests(unittest.TestCase):

    def test_should_find_element_by_xpath(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        child = element.find_element_by_xpath("select")
        self.assertEqual(child.get_attribute("id"), "2")

    def test_should_not_find_element_by_xpath(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
            element.find_element_by_xpath("select/x")
            self.fail("Expected NoSuchElementException to have been thrown")
        except NoSuchElementException as e:
            pass

    def test_finding_dot_slash_elements_on_element_by_xpath_should_find_not_top_level_elements(self):
        self._load_simple_page()
        parent = self.driver.find_element_by_id("multiline")
        children = parent.find_elements_by_xpath("./p")
        self.assertEqual(1, len(children))
        self.assertEqual("A div containing", children[0].text)

    def test_should_find_elements_by_xpath(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        children = element.find_elements_by_xpath("select/option")
        self.assertEqual(len(children), 8);
        self.assertEqual(children[0].text, "One")
        self.assertEqual(children[1].text, "Two")

    def test_should_not_find_elements_by_xpath(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        children = element.find_elements_by_xpath("select/x")
        self.assertEqual(len(children), 0)

    def test_finding_elements_on_element_by_xpath_should_find_top_level_elements(self):
        self._load_simple_page()
        parent = self.driver.find_element_by_id("multiline")
        all_para_elements = self.driver.find_elements_by_xpath("//p")
        children = parent.find_elements_by_xpath("//p")
        self.assertEqual(len(all_para_elements), len(children))

    def test_should_find_element_by_name(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        child = element.find_element_by_name("selectomatic")
        self.assertEqual(child.get_attribute("id"), "2")

    def test_should_find_elements_by_name(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        children = element.find_elements_by_name("selectomatic")
        self.assertEqual(len(children), 2)

    def test_should_find_element_by_id(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        child = element.find_element_by_id("2")
        self.assertEqual(child.get_attribute("name"), "selectomatic")

    def test_should_find_elements_by_id(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        child = element.find_elements_by_id("2")
        self.assertEqual(len(child), 2)

    def test_should_find_element_by_id_when_multiple_matches_exist(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_id("test_id_div")
        child = element.find_element_by_id("test_id")
        self.assertEqual(child.text, "inside")

    def test_should_find_element_by_id_when_no_match_in_context(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_id("test_id_div")
        try:
            element.find_element_by_id("test_id_out")
            self.fail("Expected NoSuchElementException to have been thrown")
        except NoSuchElementException as e:
            pass

    def test_should_find_element_by_link_text(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("div1")
        child = element.find_element_by_link_text("hello world")
        self.assertEqual(child.get_attribute("name"), "link1")

    def test_should_find_elements_by_link_text(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("div1")
        children = element.find_elements_by_link_text("hello world")
        self.assertEqual(len(children), 2)
        self.assertEqual("link1", children[0].get_attribute("name"))
        self.assertEqual("link2", children[1].get_attribute("name"))

    def test_should_find_element_by_class_name(self):
        self._load_page("nestedElements")
        parent = self.driver.find_element_by_name("classes")
        element = parent.find_element_by_class_name("one")
        self.assertEqual("Find me", element.text)

    def test_should_find_elements_by_class_name(self):
        self._load_page("nestedElements")
        parent = self.driver.find_element_by_name("classes")
        elements = parent.find_elements_by_class_name("one")
        self.assertEqual(2, len(elements))

    def test_should_find_element_by_tag_name(self):
        self._load_page("nestedElements")
        parent = self.driver.find_element_by_name("div1")
        element = parent.find_element_by_tag_name("a")
        self.assertEqual("link1", element.get_attribute("name"))

    def test_should_find_elements_by_tag_name(self):
        self._load_page("nestedElements")
        parent = self.driver.find_element_by_name("div1")
        elements = parent.find_elements_by_tag_name("a")
        self.assertEqual(2, len(elements))

    def test_should_be_able_to_find_an_element_by_css_selector(self):
        self._load_page("nestedElements")
        parent = self.driver.find_element_by_name("form2")
        element = parent.find_element_by_css_selector('*[name="selectomatic"]')
        self.assertEqual("2", element.get_attribute("id"))

    def test_should_be_able_to_find_multiple_elements_by_css_selector(self):
        self._load_page("nestedElements")
        parent = self.driver.find_element_by_name("form2")
        elements = parent.find_elements_by_css_selector(
            '*[name="selectomatic"]')
        self.assertEqual(2, len(elements))

    def test_should_throw_an_error_if_user_passes_in_integer(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_element(By.ID, 333333)
           self.fail("_should have thrown _web_driver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_in_tuple(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_element((By.ID, 333333))
           self.fail("_should have thrown _web_driver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_inNone(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_element(By.ID, None)
           self.fail("_should have thrown _web_driver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_in_invalid_by(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_element("css", "body")
           self.fail("_should have thrown _web_driver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_in_integer_when_find_elements(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_elements(By.ID, 333333)
           self.fail("_should have thrown _web_driver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_in_tuple_when_find_elements(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_elements((By.ID, 333333))
           self.fail("_should have thrown _web_driver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_inNone_when_find_elements(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_elements(By.ID, None)
           self.fail("should have thrown webdriver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def test_should_throw_an_error_if_user_passes_in_invalid_by_when_find_elements(self):
        self._load_page("nestedElements")
        element = self.driver.find_element_by_name("form2")
        try:
           element.find_elements("css", "body")
           self.fail("Should have thrown WebDriver Exception")
        except InvalidSelectorException:
            pass #_this is expected

    def _page_url(self, name):
        return self.webserver.where_is(name + '.html')

    def _load_simple_page(self):
        self._load_page("simpleTest")

    def _load_page(self, name):
        self.driver.get(self._page_url(name))
