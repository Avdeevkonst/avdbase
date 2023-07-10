from django.test import TestCase, Client
from .utils import get_news
import json
from unittest.mock import patch, MagicMock

class UtilsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()


    # @patch('apicrypto.utils.requests.get')
    # def test_get_news(self, mock_get):
    #     mock_response = MagicMock()
    #     mock_response.json.return_value = {'articles': [{'title': 'Test news'}]}
    #     mock_get.return_value = mock_response
    #     request = self.client.get('/news/')
    #     response = get_news(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'news.html')
    #     self.assertEqual(response.context['news_data']['articles'][0]['title'], 'Test news')
    #     with open('news.txt') as news_file:
    #         news_data = json.load(news_file)
    #         self.assertEqual(news_data['articles'][0]['title'], 'Test news')


    def test_user_page(self):
        pass

