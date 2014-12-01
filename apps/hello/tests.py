from django.core.urlresolvers import reverse
from django.test import TestCase

from models import HttpRequestLog, AboutUser


class IndexTest(TestCase):
    fixtures = [u'initial_data.json']

    def test_index_page_exists(self):
        response = self.client.get(reverse(u'index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_contains_first_name(self):
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'Artem')

    def test_index_shows_correct_user(self):
        AboutUser.objects.create(username=u'petryk', first_name=u'Petryk', last_name=u'Pyato4kin',
                                 birth_date='2000-01-01',
                                 bio='I was born with the wrong sign in the wrong house\nWith the wrong ascendancy',
                                 email='p.pyato4kin@example.com', jabber='p.pyato4kin@42cc.co', skype='p.pyato4kin',
                                 other_contacts='')
        response = self.client.get(reverse('index'))
        self.assertContains(response, u'Artem')
        self.assertNotContains(response, u'Petryk')


class TestHttpRequests(TestCase):
    def test_requests_page_exists(self):
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(response.status_code, 200)

    def test_requests_page_contains_header(self):
        response = self.client.get(reverse(u'requests'))
        self.assertContains(response, u'h1')

    def test_requests_middleware_works(self):
        http_requests = HttpRequestLog.objects.all()
        self.assertFalse(http_requests)
        self.client.get(reverse(u'index'))
        http_requests = HttpRequestLog.objects.all()
        self.assertEqual(http_requests.count(), 1)

    def test_only_ten_latest_requests_are_displayed(self):
        for i in range(10):
            self.client.get(reverse(u'index'))
            self.client.get(reverse(u'admin:index'))
        requests = HttpRequestLog.objects.all()
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(requests.count(), 21)
        self.assertEqual(response.context[u'requests'].count(), 10)
        latest_ten_requests = HttpRequestLog.objects.order_by(u'-date_time')[:10]
        for i in xrange(10):
            self.assertEqual(latest_ten_requests[i].path, response.context[u'requests'][i].path)
            self.assertEqual(latest_ten_requests[i].date_time, response.context[u'requests'][i].date_time)