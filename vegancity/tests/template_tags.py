from django.test import TestCase

import hashlib

from django.template.loader import get_template_from_string
from django.template.base import Context
from vegancity.templatetags.vegancity_template_tags import gravatar_urlify, strip_http, DEFAULT_USER_ICON

class TemplateTagTest(TestCase):
    
    def assertSimpleTemplate(self, template_string, expected_value):
        template = get_template_from_string(template_string)
        template_value = template.render(Context({}))
        self.assertEqual(template_value, expected_value)

    
    def test_gravatar_urlify_with_email(self):
        hash = hashlib.md5('ex@example.com').hexdigest()

        self.assertSimpleTemplate(
            "{% load vegancity_template_tags %}"
            "{{ 'ex@example.com'|gravatar_urlify }}",
            "http://gravatar.com/avatar/%s?s=72&d=%s"
            % (hash, DEFAULT_USER_ICON))

    def test_gravatar_urlify_with_empty_email(self):
        self.assertSimpleTemplate(
            "{% load vegancity_template_tags %}"
            "{{ ''|gravatar_urlify }}",
            DEFAULT_USER_ICON)

    def test_gravatar_urlify_without_email(self):
        self.assertSimpleTemplate(
            "{% load vegancity_template_tags %}"
            "{{ None|gravatar_urlify }}",
            DEFAULT_USER_ICON)

    def test_strip_http_empty(self):
        self.assertEqual(strip_http(None), '')

    def test_strip_http(self):
        self.assertEqual(strip_http('http://www.example.com'),
                         'www.example.com')

    def test_strip_http_with_ssl(self):
        self.assertEqual(strip_http('https://www.example.com'),
                         'www.example.com')

    def test_strip_http_with_long_domain(self):
        self.assertEqual(strip_http('http://www.example.co.uk'),
                         'www.example.co.uk')

    def test_strip_http_with_trailing_slash(self):
        self.assertEqual(strip_http('http://www.example.com/'),
                         'www.example.com')

    def test_strip_http_with_trailing_slash_no_strip(self):
        self.assertEqual(strip_http('www.example.com/'),
                         'www.example.com')

        

