#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.template import Context, Template
from django.core.urlresolvers import resolve
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse

from .models import Html

import tempfile
import time
import os
import subprocess


class InstanceError(Exception):
    pass


class WkHtmlToPdfError(Exception):
    pass


class WKHtmlToPDFGenerator(object):
    """
        Wkhtmltopdf generator, it will take context and html converts to pdf.
    """
    def __init__(self, **kwargs):
        """
        By default it will search django core settings,
        if wkhtmltopdf not found there it will add that command.
        :param kwargs:
        It may contains the html and context,
        html object is model and context of view
        :type kwargs: Dictionary
        :returns: None
        """
        tempfile.tempdir = '/tmp/'
        self.tmp_dir = tempfile.gettempdir()
        self.html = kwargs.get('html')
        self.context = kwargs.get('context')
        self.command = []
        self.code_format = "utf-8"
        if hasattr(settings, "WKHTML_TO_PDF_CMD") and isinstance(settings.WKHTML_TO_PDF_CMD, str):
            self.command = [settings.WKHTML_TO_PDF_CMD]

    @property
    def _get_options(self):
        """ Providing external options for wkhtmltopdf from settings
            and HtmlHeaderFooter model
        """
        if self.html.htmlheader.quiet:
            self.command.append('--quiet')
        if self.html.htmlheader.zoom:
            self.command.extend(['--zoom', str(self.html.htmlheader.zoom)])
        # default to UTF-8 encoding.  Use <meta charset="latin-1"> to override.
        self.command.extend(['--encoding', self.html.htmlheader.encode_type])

        options = getattr(settings, 'WKHTML_OPTIONS', None)
        if options is not None:
            if not isinstance(options, dict):
                raise InstanceError("WKHTML_OPTIONS not a dictionary")
            for key, value in options.iteritems():
                if value is None:
                    self.command.append(str(key))
                else:
                    self.command.extend([str(key), str(value)])

    def _write_data_into_file(self, content, name, file_to_del, css=False):
        """It will creates the temp file in temporary folder
        :param: content: context of view
        :type: content: Dictionary
        :param: name:
        html or css file suffix
        :type: name: str or unicode
        :param: file_to_del:
        it will holds the temp files for after delete those
        files from temp folder when pdf generate complete.
        :type: file_to_del: list
        :param: css:
        By default it is False, If it provides then this suffix is css.
        :type: css: bool
        :returns: temp file object
        """
        encoded_content = content.encode(self.code_format)
        if not css:
            _sanitize_string = self._sanitize_html(encoded_content)
        else:
            _sanitize_string = encoded_content
        render_str = self._render_string(_sanitize_string)
        com_file = file(
            os.path.join(self.tmp_dir, str(time.time()) + name), 'w'
        )
        com_file.write(render_str.encode(self.code_format))
        file_to_del.append(com_file.name)
        return com_file

    @property
    def generate_pdf_file(self):
        """This method will generates the Pdf object from html

        :return: pdf object
        :raise: RuntimeError: run time
        :raise: WkHtmlToPdfError: html error
        :raise: OSError, IOError: none
        """
        out_filename = tempfile.mktemp(suffix=".pdf", prefix="webkit.tmp.")
        file_to_del = [out_filename]
        if not self.command:
            self.command = ['wkhtmltopdf']
        self._get_options
        if self.html.htmlheader.header:
            head_file = self._write_data_into_file(
                str(self.html.htmlheader.header),
                '.head.html',
                file_to_del
            )
            file_to_del.append(head_file.name)
            self.command.extend(['--header-html', head_file.name])
            head_file.close()
        if self.html.htmlheader.footer:
            foot_file = self._write_data_into_file(
                self.html.htmlheader.footer,
                '.foot.html',
                file_to_del
            )
            self.command.extend(['--footer-html', foot_file.name])
            file_to_del.append(foot_file.name)
            foot_file.close()
        if self.html.htmlheader.css:
            css_file = self._write_data_into_file(
                self.html.htmlheader.footer,
                '.style.css',
                file_to_del,
                css=True
            )
            file_to_del.append(css_file.name)
            self.command.extend(['--user-style-sheet', css_file.name])
            css_file.close()
        if self.html.htmlheader.margin_top:
            self.command.extend([
                '--margin-top',
                str(self.html.htmlheader.margin_top).replace(',', '.')
            ])
        if self.html.htmlheader.margin_bottom:
            self.command.extend([
                '--margin-bottom',
                str(self.html.htmlheader.margin_bottom).replace(',', '.')
            ])
        if self.html.htmlheader.margin_left:
            self.command.extend([
                '--margin-left',
                str(self.html.htmlheader.margin_left).replace(',', '.')
            ])
        if self.html.htmlheader.margin_right:
            self.command.extend([
                '--margin-right',
                str(self.html.htmlheader.margin_right).replace(',', '.')
            ])
        if self.html.htmlheader.orientation:
            self.command.extend([
                '--orientation',
                str(self.html.htmlheader.orientation).replace(',', '.')
            ])
        if self.html.htmlheader.page_size:
            self.command.extend([
                '--page-size',
                str(self.html.htmlheader.page_size).replace(',', '.')
            ])
        count = 0
        for body in self.html.htmlbody.all():
            html_file = self._write_data_into_file(
                body.body,
                '.%s.body.html' % body.id,
                file_to_del
            )
            self.command.append(html_file.name)
            count += 1
            html_file.close()
        self.command.append(out_filename)
        seder_fd, seder_path = tempfile.mkstemp(text=True)
        file_to_del.append(seder_path)
        try:
            status = subprocess.call(self.command, stderr=seder_fd)
            os.close(seder_fd)  # ensure flush before reading
            seder_fd = None  # avoid closing again in finally block
            file_obj = open(seder_path, 'r')
            message = file_obj.read()
            file_obj.close()
            if not message:
                error_message = 'No diagnosis message was provided'
            else:
                error_message = '''The following diagnosis message was provided:\n''' + message
            if status:
                raise RuntimeError("""
                                   Webkit error The command 'wkhtmltopdf'
                                   failed with error
                                   code = %s. Message: %s""" %
                                   (status, error_message))
            pdf_file = open(out_filename, 'rb')
            pdf = pdf_file.read()
            pdf_file.close()
        except Exception as e:
            if subprocess.call(['which', self.command[0]]):
                raise WkHtmlToPdfError("make sure wkhtmltopdf installed in your instance \
                or check wkhtmltopdf path is given correctly")
            if "does not support more then one input document" in (e.message):
                raise WkHtmlToPdfError("""This Wkhtmltopdf doesn't support please follow this link
                http://stackoverflow.com/questions/18758589/wkhtmltopdf-installation-error-on-ubuntu""")
        finally:
            if seder_fd is not None:
                os.close(seder_fd)
            for f_to_del in file_to_del:
                try:
                    os.unlink(f_to_del)
                except (OSError, IOError):
                    #  print("cannot remove file %s: %s" % (f_to_del, exc))
                    pass
        return pdf

    def _render_string(self, html):
        """Render the context in html
        :param html: html data
        :type html: str or unicode
        :returns Sends the Render the Context html
        """
        temp = Template(html)
        return temp.render(Context(self.context))

    @staticmethod
    def _sanitize_html(html):
        """wkhtmltopdf expects the html page to declare a doctype.
        :param html: html document
        :type html: str or unicode
        :returns: html document
        """
        input_html = html
        if input_html and input_html[:9].upper() != "<!DOCTYPE":
            html = "<!DOCTYPE html>\n" + input_html
        return html


def convert_html_to_pdf(**kwargs):
    """It is Api call for converting Html to Pdf.
    It Creates the WKHtmlToPDFGenerator instance.

    :param request: view client request
    :type request: WSGIRequest
    :param context: rendering template with this context --> optional
    :type context: Dictionary
    :param name: pdf name --> optional
    :type name: str or unicode or int
    :returns: Sends the HttpResponse to view
    :raises: DoesNotExist
    :raises: InstanceError
    """
    if 'request' not in kwargs:
        raise KeyError('request param not in kwargs')
    request = kwargs.get('request')
    if not isinstance(request, WSGIRequest):
        raise InstanceError("request is not instance of WSGIRequest")
    url_match = resolve(request.path)
    view = url_match.func.__module__ + "." + url_match.func.__name__
    try:
        html = Html.objects.get(view=view)
    except Html.DoesNotExist:
        raise Html.DoesNotExist("The provided view does not match in the Html model, view={}\
                           ".format(view))
    webkit = WKHtmlToPDFGenerator(context=kwargs.get('context'), html=html)
    disposition = 'attachment;'
    if not html.attachment:
        disposition = ''
    if 'name' in kwargs and len(str(kwargs.get('name'))) > 0:
        disposition += " filename={}.pdf".format(str(kwargs.get('name')))
    else:
        disposition += " filename={}.pdf".format(html.name)
    response = HttpResponse(
        webkit.generate_pdf_file,
        content_type='application/pdf')
    response['Content-Disposition'] = disposition
    webkit.command = []
    return response
