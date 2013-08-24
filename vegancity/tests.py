from django.test import TestCase
from django.test.client import RequestFactory
from mock import MagicMock

from django.core.exceptions import ValidationError

from vegancity import models, views, email
from bs4 import BeautifulSoup

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


class VendorGeocodeTest(TestCase):
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

class VendorModelTest(TestCase):
    def setUp(self):
        self.user = get_user()

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

        review2.approved = True
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
                         models.Vendor.objects.filter(name="test123").count())

    def test_invalid_new_vendor_does_not_save(self):
        request = self.factory.post('/vendors/add',
                                    {'name': 'test123'})
        request.user = self.user

        response = views.new_vendor(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0,
                         models.Vendor.objects.filter(name="test123").count())


class VendorEmailTest(TestCase):

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


class VendorVeganDishValidationTest(TestCase):
    """
    Tests that trying to delete vegan dish relationships for
    vendors that have reviews will signal an error.
    """
    def setUp(self):
        self.user = get_user()

        self.vendor = models.Vendor(name="Test Vendor",
                                    address="123 Main St")
        self.vendor.save()

        self.vegan_dish1 = models.VeganDish(name="Tofu Scramble")
        self.vegan_dish1.save()

        self.vegan_dish2 = models.VeganDish(name="Tempeh Hash")
        self.vegan_dish2.save()

        self.review1 = models.Review(vendor=self.vendor,
                                     author=self.user,
                                     content="ahhhh")
        self.review1.save()

        self.vendor.vegan_dishes.add(self.vegan_dish1)
        self.vendor.vegan_dishes.add(self.vegan_dish2)

    def test_can_delete_relationship_without_any_reviews(self):
        self.assertEqual(self.vendor.vegan_dishes.count(), 2)

        self.vendor.vegan_dishes.remove(self.vegan_dish1)

        self.assertEqual(self.vendor.vegan_dishes.count(), 1)

    def test_can_delete_relationship_with_reviews_on_other_vegan_dish(self):
        self.review1.best_vegan_dish = self.vegan_dish1
        self.review1.save()

        self.assertEqual(self.vendor.vegan_dishes.count(), 2)

        self.vendor.vegan_dishes.remove(self.vegan_dish2)

        self.assertEqual(self.vendor.vegan_dishes.count(), 1)

    def test_can_clear_relationship_without_any_reviews(self):
        self.assertEqual(self.vendor.vegan_dishes.count(), 2)

        self.vendor.vegan_dishes.clear()

        self.assertEqual(self.vendor.vegan_dishes.count(), 0)

    def test_cant_clear_relationship_with_any_reviews(self):
        self.review1.best_vegan_dish = self.vegan_dish1
        self.review1.save()

        self.assertRaises(ValidationError, self.vendor.vegan_dishes.clear)

    def test_cant_delete_relationship_with_reviews(self):
        self.review1.best_vegan_dish = self.vegan_dish1
        self.review1.save()

        self.assertRaises(ValidationError,
                          self.vendor.vegan_dishes.remove,
                          self.vegan_dish1)

class SearchTest(TestCase):
    def setUp(self):
        self.v1 = models.Vendor.objects.create(name="Test Vendor Foo", approval_status='approved')
        self.v2 = models.Vendor.objects.create(name="Test Vendor Bar", approval_status='approved')
        self.v3 = models.Vendor.objects.create(name="Test Vendor Baz", approval_status='approved')
        self.v4 = models.Vendor.objects.create(name="Test Vendor Bart", approval_status='approved')
        self.factory = RequestFactory()

    def test_search_by_name_for_substring(self):
        request = self.factory.get('',
                                   {'current_query': 'Bar',})

        response = views.vendors(request)
        self.assertEqual(response.content.count("Results (2)"), 1)

        request = self.factory.get('',
                                   {'current_query': 'Vendor',})

        response = views.vendors(request)
        self.assertEqual(response.content.count("Results (4)"), 1)

    def test_search_by_name_approved_only(self):
        self.v4.approval_status = 'quarantined'
        self.v4.save()

        request = self.factory.get('',
                                   {'current_query': 'Vendor',})

        response = views.vendors(request)
        self.assertEqual(response.content.count("Results (3)"), 1)

    def test_neighborhoods_field_is_populated(self):
        """ This test was born out of an actual observed bug """

        def count_option_elements():
            request = self.factory.get('')
            response = views.vendors(request)
            content = BeautifulSoup(response.content)
            neighborhood_element = filter(lambda x: x['name'] == 'neighborhood',
                                          content.find_all('select'))[0]
            return len(neighborhood_element.find_all('option'))

        n1 = models.Neighborhood.objects.create(name="Foo")

        self.assertEqual(count_option_elements(), 1)

        self.v1.neighborhood = n1
        self.v1.save()

        self.assertEqual(count_option_elements(), 2)

