from django.test import TestCase

from vegancity.forms import VegUserCreationForm
from vegancity.models import User

class VegUserCreationFormTest(TestCase):
    def test_save_required_only(self):
        form = VegUserCreationForm({'username': 'test1235',
                                    'password1': 'test123',
                                    'password2': 'test123',
                                    'email': 'a@b.com' })
        
        form.save()
        user = User.objects.get(username='test1235')
        self.assertEqual(user.email, 'a@b.com')
        self.assertEqual(user.get_profile().mailing_list, False)
        self.assertEqual(user.get_profile().bio, '')

    def test_save_all(self):
        form = VegUserCreationForm({'username': 'test1235',
                                    'password1': 'test123',
                                    'password2': 'test123',
                                    'email': 'a@b.com',
                                    'bio': "Big veggie lover.",
                                    'mailing_list': 'on' })
        
        form.save()
        user = User.objects.get(username='test1235')
        self.assertEqual(user.get_profile().mailing_list, True)
        self.assertEqual(user.get_profile().bio, 'Big veggie lover.')

    def test_save_no_email(self):
        form = VegUserCreationForm({'username': 'test1235',
                                    'password1': 'test123',
                                    'password2': 'test123', })
        
        self.assertRaises(ValueError, form.save)

 
    def test_save_short_username(self):
        form = VegUserCreationForm({'username': 'te',
                                    'password1': 'test123',
                                    'password2': 'test123',
                                    'email': 'a@b.com' })
        
        self.assertRaises(ValueError, form.save)
 
    def test_save_username_case_sensitivity(self):
        form = VegUserCreationForm({'username': 'teSter',
                                    'password1': 'test123',
                                    'password2': 'test123',
                                    'email': 'a@b.com' })
        
        self.assertRaises(ValueError, form.save)
 
