# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from django.test import TestCase
from django.test.client import RequestFactory

from djwkhtmltopdf.models import Html
from .views import example_view


class WKHTMLTestViews(TestCase):
    """
      Wkhtml Test View Cases
    """
    APP_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.pardir))
    fix_path = "{0}{1}".format(APP_DIR, '/fixtures/initial.json')
    fixtures = [fix_path]

    def setUp(self):
        self.factory = RequestFactory()
        html = Html.objects.get(id=1)
        #  mapping correct view if it is commented test must fail
        html.view = "djwkhtmltopdf.tests.views.example_view"
        html.name = 'test'  # giving pdf name dynamically
        html.save()
        self.request = self.factory.get('/')
        self.response = example_view(self.request)
        self.headers = dict(self.response._headers.itervalues())

    def test_view_response_status(self):
        """
            checking the status of pdf stream
        """
        self.assertEqual(self.response.status_code, 200)

    def test_view_response_content_type(self):
        """
           checking the type of response
        """
        self.assertEqual(self.headers['Content-Type'], "application/pdf")

    def test_view_pdf_dynamic_name(self):
        """
            checking the pdf file name mached with DATABASE records
        """
        self.assertRegexpMatches(
            self.headers['Content-Disposition'],
            '=test.',
            msg="file name is not mached")

    def test_view_pdf_static_name(self):
        """
            passing pdf name static without taking from DATABASE
        """
        self.request = self.factory.get('/?name=123')
        self.response = example_view(self.request)
        self.headers = dict(self.response._headers.itervalues())
        self.assertRegexpMatches(
            self.headers['Content-Disposition'],
            '=123.',
            msg="file name is not mached")

    def test_view_with_unicode(self):
        """
            test with unicode context
            number = u'20♥'
        """
        number = u'20♥'
        self.request = self.factory.get('/?number=' + number)
        self.response = example_view(self.request)
        self.assertEqual(self.response.status_code, 200)
        self.headers = dict(self.response._headers.itervalues())
