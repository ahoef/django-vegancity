from optparse import make_option
from unittest import TestSuite
import logging

from django.conf import settings

from django.test.simple import DjangoTestSuiteRunner

from vegancity.tests.models import *  # NOQA

from vegancity.tests.views import *  # NOQA

from vegancity.tests.integration import *  # NOQA

from vegancity.tests.admin_views import *  # NOQA

from vegancity.tests.validators import *  # NOQA

from vegancity.tests.template_tags import *  # NOQA


class VegancityTestRunner(DjangoTestSuiteRunner):

    option_list = (
        make_option('-e', '--exclude-integration-tests',
                    help=("Do not run the slow "
                          "page load tests, "
                          "run unnit tests only."),
                    action='store_const',
                    dest='exclude_integration_tests',
                    const=True, default=False),
    )

    def __init__(self, *args, **kwargs):
        self.exclude_integration_tests = kwargs['exclude_integration_tests']
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

        full_suite = TestSuite([test for test in suite if not
                                isinstance(test,
                                           (IntegrationTest,
                                            LiveServerTestCase))])

        # if running all tests, add the IntegrationTests and THEN
        # the LiveServerTestCases. This is a workaround because django
        # automatically fills the test database with ContentType data
        # as soon as you run the live test server. This wouldn't be
        # a problem, but the IntegrationTests are currently using
        # test fixtures (I know, I know) that have hardcoded ContentType
        # IDs in them. Even calling ContentType.objects.all().delete()
        # in the tearDown() method doesn't work, because the id_seq
        # would need to be reset, which is a bother. So, this'll do
        # for now.
        if not self.exclude_integration_tests:
            for test in suite:
                if isinstance(test, IntegrationTest):
                    full_suite.addTest(test)
            for test in suite:
                if isinstance(test, LiveServerTestCase):
                    full_suite.addTest(test)

        return full_suite
