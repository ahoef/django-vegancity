from django.test import TestCase
from django.utils import unittest
from django.test.client import RequestFactory
from mock import MagicMock

from vegancity import  models, views, email

def get_user():
    user = models.User(username="Moby")
    user.save()
    return user

class PageLoadTest(TestCase):
    fixtures = ['public_data.json']
    def setUp(self):
        self.reviews = models.Review.approved_objects.all()
        self.vendors = models.Vendor.approved_objects.all()
        self.vendor_count = self.vendors.count()

    def assertNoBrokenTemplates(self, url):
        response = self.client.post(url)
        self.assertEqual(response.content.count("{{"), 0)
        self.assertEqual(response.content.count("}}"), 0)

    def assertCorrectStatusCode(self, url, desired_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, desired_code)

    def test_orm_links(self):
        "Test Vendors pages using ORM"
        for vendor in self.vendors:
            url = vendor.get_absolute_url()
            self.assertNoBrokenTemplates(url)
            self.assertCorrectStatusCode(url, 200)

    def test_review_links(self):
        "Test review pages using ORM"
        for review in self.reviews:
            url = review.get_absolute_url()
            self.assertNoBrokenTemplates(url)
            self.assertCorrectStatusCode(url, 200)

    def test_other_pages(self):
        PAGES_RETURNING_302 = [
            '/vendors/add/',
            '/accounts/logout/',
            ]

        PAGES_RETURNING_200 = [
            '/',
            '/vendors/',
            '/about/',
            '/accounts/login/',
            '/accounts/register/',
            '/admin/',
            ]

        for url in PAGES_RETURNING_302:
            self.assertNoBrokenTemplates(url)
            self.assertCorrectStatusCode(url, 302)

        for url in PAGES_RETURNING_200:
            self.assertNoBrokenTemplates(url)
            self.assertCorrectStatusCode(url, 200)

class VendorTest(TestCase):
    def setUp(self):
        self.user = get_user()
        
    def test_no_address_no_geocode(self):
        vendor = models.Vendor(name="Test Vendor")
        vendor.save()

        self.assertEqual(vendor.location, None)
        self.assertEqual(vendor.neighborhood, None)
        self.assertFalse(vendor.needs_geocoding())

    def test_address_causes_geocode(self):
        vendor = models.Vendor(
            name="Test Vendor",
            address="300 Christian St, Philadelphia, PA, 19147")

        vendor.save()

        self.assertNotEqual(vendor.location, None)
        self.assertNotEqual(vendor.neighborhood, None)
        
    def test_needs_geocoding(self):
        vendor = models.Vendor(name="Test Vendor")
        self.assertFalse(vendor.needs_geocoding())

        vendor.address = "300 Christian St, Philadelphia, PA, 19147"
        self.assertTrue(vendor.needs_geocoding())
        
        vendor.save()
        self.assertFalse(vendor.needs_geocoding())

    def test_food_and_atmosphere_rating(self):
        vendor = models.Vendor(name="Test Vendor")
        vendor.save()

        self.assertEqual(vendor.food_rating(), None)
        self.assertEqual(vendor.atmosphere_rating(), None)

        models.Review(vendor=vendor, 
                      approved=True,
                      food_rating=1,
                      atmosphere_rating=1,
                      author=self.user).save()

        self.assertEqual(vendor.food_rating(), 1)
        self.assertEqual(vendor.atmosphere_rating(), 1)

        review2 = models.Review(vendor=vendor, 
                      approved=False,
                      food_rating=4,
                      atmosphere_rating=4,
                      author=self.user)
        review2.save()

        self.assertEqual(vendor.food_rating(), 1)
        self.assertEqual(vendor.atmosphere_rating(), 1)

        review2.approved=True
        review2.save()

        # Floored Average
        self.assertEqual(vendor.food_rating(), 2)
        self.assertEqual(vendor.atmosphere_rating(), 2)

        review3 = models.Review(vendor=vendor, 
                      approved=True,
                      food_rating=4,
                      atmosphere_rating=4,
                      author=self.user)
        review3.save()

        # Floored Average
        self.assertEqual(vendor.food_rating(), 3)
        self.assertEqual(vendor.atmosphere_rating(), 3)

class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user()

    def test_valid_new_vendor_redirects(self):
        request = self.factory.post('/vendors/add',
                                    { 'name': 'test123',
                                      'address': '123 Main st'})
        request.user = self.user

        response = views.new_vendor(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vendor.objects.filter(name="test123").count(), 1)

    def test_invalid_new_vendor_does_not_save(self):
        request = self.factory.post('/vendors/add',
                                    { 'name': 'test123' })
        request.user = self.user

        response = views.new_vendor(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Vendor.objects.filter(name="test123").count(), 0)

class EmailTest(TestCase):

    def setUp(self):
        # mock the email function so that we can just see if it's called
        email.send_new_vendor_approval = MagicMock()
        self.user = get_user()
        self.user.email = "test@test.com"
        self.user.save()

    def test_newly_approved_vendor_gets_emailed(self):
        """
        Test that the email function is called once when a vendor is approved
        and then not again if its approval status changes, even if to approved.
        """

        # not called because it is not yet approved
        vendor = models.Vendor(name="The Test Vendor",
                               address="123 Main St",
                               submitted_by=self.user)
        vendor.save()
        email.send_new_vendor_approval.assert_not_called()
        
        # called now because it was approved
        vendor.approval_status = "approved"
        vendor.save()
        email.send_new_vendor_approval.assert_called_with(vendor)

        # reset mock function to test it doesn't get called again
        email.send_new_vendor_approval.reset_mock()

        # not called when approval status changes away from approved
        vendor.approval_status = "quarantined"
        vendor.save()
        email.send_new_vendor_approval.assert_not_called()

        # not called when approval status is changed back to approved
        vendor.approval_status = "approved"
        vendor.save()
        email.send_new_vendor_approval.assert_not_called()

