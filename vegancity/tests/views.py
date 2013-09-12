from django.test import TestCase
from django.test.client import RequestFactory

from vegancity import views
from vegancity.models import Vendor
from vegancity.tests.utils import get_user


class VendorViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user()

    def test_valid_new_vendor_redirects(self):
        request = self.factory.post('/vendors/add',
                                    {'name': 'test123',
                                     'address': '123 Main st'})
        request.user = self.user

        response = views.new_vendor(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(1,
                         Vendor.objects.filter(name="test123").count())

    def test_invalid_new_vendor_does_not_save(self):
        request = self.factory.post('/vendors/add',
                                    {'name': 'test123'})
        request.user = self.user

        response = views.new_vendor(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0,
                         Vendor.objects.filter(name="test123").count())
