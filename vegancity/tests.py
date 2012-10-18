from django.test.client import Client
from django.utils import unittest
import models

class VendorCase(unittest.TestCase):
    def setUp(self):
        pass
        #self.test_vendor = models.Vendor.objects.create(name="Test Vendor")

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

    vendor_count = models.Vendor.objects.count()
    
    for i in range(1, vendor_count + 1):

        # test the detail page for every vendor
        url = '/vendors/%d/' % i
        response = c.post(url)
        assert response.status_code == 200

        # test the review page for every vendor
        url = '/vendors/review/%d/' % i
        response = c.post(url)
        assert response.status_code == 302

    response = c.post('/vendors/')
    assert response.status_code == 200

    response = c.post('/vendors/add/')
    assert response.status_code == 302

    response = c.post('/blog/')
    assert response.status_code == 200

    response = c.post('/')
    assert response.status_code == 200

    response = c.post('/about/')
    assert response.status_code == 200

    response = c.post('/accounts/login/')
    assert response.status_code == 200

    response = c.post('/accounts/logout/')
    assert response.status_code == 302

    response = c.post('/accounts/register/')
    assert response.status_code == 200

    response = c.post('/admin/')
    assert response.status_code == 200

    print
    print "#################################"
    print "Tested every known url!"
    print "#################################"
    print

browser_tests()
