from django.test import TestCase
from django.test import Client

from django.urls import reverse

from datetime import date
from bs4 import BeautifulSoup

from ..views import home

# Create your tests here.
class ViewsTest(TestCase):

    def setUp(self):
        client = Client()

    def test_home_page(self):
        """
            - Home page loads
            - Home is the title of the page
        """
        # Page loading
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

        # Checking title
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find("title") # uses html tag names
        title_text = title.get_text() # method for accessing text
        clean_title = title_text.strip() # getting rid of whitespace
        self.assertEquals(clean_title, "home")

    def test_income_page(self):
        pass

    def test_expenses_page(self):
        pass

    def test_loan_page(self):
        pass

    def test_cash_flow(self):
        pass
