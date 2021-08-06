from django.http import request
from django.test import TestCase
from diawe.models import Teams, UserProfile
from django.urls import reverse
import importlib
from django.contrib.auth.models import User
from django.forms import fields as django_fields
# model test


class ModelTest(TestCase):
    def create_user_object(self):
        user  = User.objects.get_or_create(username='testAdmin')[0]
        user.set_password("adminPassword123")
        self.assertIsNotNone(user,"classcreate error")
        user.save()
        return user
    
    def create_super_user_object():
        return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

    

    def create_userprofile_object(self):
        user  = self.create_user_object()
        userprofile =UserProfile.objects.get_or_create(user =user)[0]
        self.assertIsInstance(userprofile,UserProfile,"classcreate error")
        userprofile.save()
        return userprofile

    def create_team_object(self):
        user  =self.create_user_object()
        userprofile = self.create_userprofile_object()
        team = Teams.objects.get_or_create(users =user,idT = 3, nameTeam = "TeamA")[0]
        
        team.save()
        self.assertIsInstance(team,Teams,"classcreate error")
        return team

    def test_login_functionality(self):
     
        user_object = self.create_user_object()
        userprofile_object = self.create_userprofile_object()
        response = self.client.post(reverse('diawe:login'), {'username': 'testAdmin', 'password': 'adminPassword123'})
     
        self.assertEqual(response.status_code,302 )
        
   



class ViewTest(TestCase):
    def test_view_exists(self):
        self.views_module = importlib.import_module('diawe.views')
        self.views_module_listing = dir(self.views_module)
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)
        
        self.assertTrue(name_exists, "name dont exist")
        self.assertTrue(is_callable, "index can't be called")

  

class TemplateTest(TestCase):
    
    def test_index_uses_template(self):
        self.response = self.client.get(reverse('diawe:index'))
        self.assertTemplateUsed(self.response, "diawe/index.html","index can't get reversed")
        request = self.client.get(reverse('diawe:register'))
        content = request.content.decode('utf-8')
        self.assertTrue('<h1 class="typeface1">register here!</h1><br />' in content)


class FormTest(TestCase):

       def test_category_form_class(self):

        import diawe.forms
        self.assertTrue('LogForm' in dir(diawe.forms))

        from diawe.forms import LogForm
        from diawe.models import LogPost
        log_form = LogForm()
        self.assertEqual(type(log_form.__dict__['instance']), LogPost)

        fields = log_form.fields

        expected_fields = {
            'title': django_fields.CharField,
            'body':django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys())
            self.assertEqual(expected_field, type(fields[expected_field_name]))

        
class URLTest(TestCase):
    def URLtest(self):
        try:
            url = reverse('diawe:register')
        except:
            pass
        self.assertEqual(url, '/diawe/register/')


    
 
