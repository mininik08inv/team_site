from django.test import SimpleTestCase, Client
from django.views.generic import TemplateView
from . import views


class HomePageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_name(self):
        self.assertEqual(self.response.resolver_match.url_name, 'team_detail')


    def test_view_name(self):
        self.assertEqual(self.response.resolver_match.func, views.team_detail)


class PlayerDetailPageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/player/<int:player_id>/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_name(self):
        self.assertEqual(self.response.resolver_match.url_name, 'about')

    def test_url_namespace(self):
        self.assertEqual(self.response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertIs(self.response.resolver_match.func.view_class, TemplateView)


