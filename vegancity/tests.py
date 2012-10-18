from django.test.client import Client
from django.utils import unittest
import models

class VendorCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_best_vegan_dish(self):
        """Test to see if best_vegan_dish() returns a vegan dish where possible.
        Otherwise, it should return none."""

        for vendor in models.Vendor.objects.all():
            vegan_dishes = models.VeganDish.objects.filter(vendor=self.test_vendor)

            if vegan_dishes:
                assert (self.test_vendor.best_vegan_dish() in
                        models.VeganDish.objects.all())
            else:
                self.assertEqual(self.test_vendor.best_vegan_dish(), None)


def browser_tests():
    c = Client()

    reviews = models.Review.objects.all()
    vendors = models.Vendor.objects.all()
    vendor_count = vendors.count()
    

    ################################
    # Test Vendor IDs sequentially
    ################################
    for i in range(1, vendor_count + 1):
        # test the detail page for every vendor
        url = '/vendors/%d/' % i
        print "testing url:", url
        response = c.post(url)
        assert response.status_code == 200

        # test the review page for every vendor
        url = '/vendors/review/%d/' % i
        print "testing url:", url
        response = c.post(url)
        assert response.status_code == 302


    ################################
    # Test Vendors pages using ORM
    ################################
    for vendor in vendors:
        url = vendor.get_absolute_url()
        print "testing url:", url
        response = c.post(url)
        assert response.status_code == 200


    ################################
    # Test review pages using ORM
    ################################
    for review in reviews:
        url = review.get_absolute_url()
        print "testing url:", url
        response = c.post(url)
        assert response.status_code == 200

    ################################
    # Test other pages
    ################################

    # vendor summary page
    response = c.post('/vendors/')
    assert response.status_code == 200

    # new vendor page
    response = c.post('/vendors/add/')
    assert response.status_code == 302

    # blog page
    response = c.post('/blog/')
    assert response.status_code == 200

    # home page
    response = c.post('/')
    assert response.status_code == 200

    # about page
    response = c.post('/about/')
    assert response.status_code == 200

    # login page
    response = c.post('/accounts/login/')
    assert response.status_code == 200

    # logout page
    response = c.post('/accounts/logout/')
    assert response.status_code == 302

    # register page
    response = c.post('/accounts/register/')
    assert response.status_code == 200

    # admin portal
    response = c.post('/admin/')
    assert response.status_code == 200

    print
    print "#################################"
    print "# Tested every known url!"
    print "#################################"
    print

browser_tests()
