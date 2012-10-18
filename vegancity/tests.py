from django.test import client
from django.utils import unittest
import models

####################################
# UNIT TESTS
####################################

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


#####################################
# INTEGRATED TESTS
#####################################

def test_url(url, desired_code):
    """Tests a url using the built-in django browser.

    See if the url returns a reasonable status code.
    Check if the response has any double-moustaches in
    it, implying a template misfired.

    [Add description of upcoming test here]"""
    c = client.Client()
    response = c.post(url)
    response_string = str(response)
    assert not response_string.count("{{")
    assert not response_string.count("}}")
    assert response.status_code == desired_code
    return "tested url: '%s' for code '%d'" % (url, desired_code)

def browser_tests():
    """Test every known url on the site."""

    reviews = models.Review.objects.all()
    vendors = models.Vendor.objects.all()
    vendor_count = vendors.count()
    
    ################################
    # Test Vendor IDs sequentially
    ################################
    for i in range(1, vendor_count + 1):
        # test the detail page for every vendor
        url = '/vendors/%d/' % i
        print test_url(url, 200)

        # test the review page for every vendor
        url = '/vendors/review/%d/' % i
        print test_url(url, 302)

    ################################
    # Test Vendors pages using ORM
    ################################
    for vendor in vendors:
        url = vendor.get_absolute_url()
        print test_url(url, 200)

    ################################
    # Test review pages using ORM
    ################################
    for review in reviews:
        url = review.get_absolute_url()
        print test_url(url, 200)

    ################################
    # Test other pages
    ################################

    PAGES_RETURNING_302 = [
        '/vendors/add/',
        '/accounts/logout/',
        ]

    PAGES_RETURNING_200 = [
        '/',
        '/vendors/',
        '/blog/',
        '/about/',
        '/accounts/login/',
        '/accounts/register/',
        '/admin/',
        ]

    for url in PAGES_RETURNING_302:
        print test_url(url, 302)

    for url in PAGES_RETURNING_200:
        print test_url(url, 200)

    print
    print "#################################"
    print "# Tested every known url!"
    print "#################################"
    print

    

browser_tests()
