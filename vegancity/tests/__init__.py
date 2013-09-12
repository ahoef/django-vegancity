from optparse import make_option
from unittest import TestSuite
import logging

from django.conf import settings

from django.test.simple import DjangoTestSuiteRunner

from vegancity.tests.models import *  # NOQA

from vegancity.tests.views import *  # NOQA

from vegancity.tests.integration import *  # NOQA


class VegancityTestRunner(DjangoTestSuiteRunner):

    option_list = (
        make_option('-e', '--exclude-page-tests',
                    help=("Do not run the slow "
                          "page load tests, "
                          "run unnit tests only."),
                    action='store_const',
                    dest='exclude_page_tests',
                    const=True, default=False),
    )

    def __init__(self, *args, **kwargs):
        self.exclude_page_tests = kwargs['exclude_page_tests']
        return super(VegancityTestRunner, self).__init__(interactve=False,
                                                         *args, **kwargs)

    def run_tests(self, *args, **kwargs):
        logging.disable(logging.CRITICAL)
        return super(VegancityTestRunner, self).run_tests(*args, **kwargs)

    def build_suite(self, test_labels, *args, **kwargs):
        test_labels = test_labels or settings.MANAGED_APPS

        suite = super(VegancityTestRunner, self).build_suite(test_labels,
                                                             *args,
                                                             **kwargs)

        if self.exclude_page_tests:
            suite = TestSuite([test for test in suite
                               if not isinstance(test, PageLoadTest)])

        return suite
