from django.http import request
from django.test import TestCase
from diawe.models import Teams, UserProfile
from django.urls import reverse
import importlib
from django.contrib.auth.models import User
# model test


class ModelTest(TestCase):
    def team_test(self):
        user  = User.objects.create('testAdmin', 'email@email.com', 'adminPassword123')
        team = Teams(user = user,idT = 3, nameTeam = "TeamA")
        team.save()
        self.assertIsInstance(team,Teams,"classcreate error")





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
            'title': log_form.CharField,
            'body':log_form.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys())
            self.assertEqual(expected_field, type(fields[expected_field_name]))

