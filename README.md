[![PyPI version](https://badge.fury.io/py/dj-wkhtmltopdf.svg)](http://badge.fury.io/py/dj-wkhtmltopdf)
dj-wkhtmltopdf
--------------
--------------
It works on [wkhtmltopdf](http://wkhtmltopdf.org/) . ``dj-wkhtmltopdf`` will allow user to organize their own pdf generator through django admin without any deployment :).

Mainly I was inspired by [django-wkhtmltopdf](https://github.com/incuna/django-wkhtmltopdf) . When I was working on Eccomerce project we generated invoice for orders using wkhtmltopdf ( pdf generator using django-wkhtmltopdf wrapper ). Every time we did some modifications on local server and push it to production we faced different design issues on production, then we resolve those issues on local and pushed it to production, but it's a painful and time consuming process so I thought of buliding this package.
Requirements:
-------------
-------------
Install the [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html) .
Python 2.6+ and 3.3+ is supported.
Installation:
------------
------------
Run ``pip install dj-wkhtmltopdf``.

Add 'djwkhtmltopdf' to ``INSTALLED_APPS`` in your ``settings.py`` .

Then run the ``python manage.py syncdb`` .

By default it will execute the first wkhtmltopdf command found on your ``PATH`` .

If you can't add wkhtmltopdf to your ``PATH`` you can set ``WKHTMLTOPDF_CMD`` to a specific execuatable:

e.g. in ``settings.py``:

``WKHTML_TO_PDF_CMD = '/path/to/my/wkhtmltopdf' ``

You may also set wkhtmltopdf options through django admin or ``WKHTML_OPTIONS`` in settings.py to a dictionary of default command-line options.

Like this is:
``
WKHTML_OPTIONS = {
    '--quiet': True,
}
``
Important Note:
---------------
---------------
I've tested it only on Ubuntu but haven't tested it on Mac and Windows.
License:
--------
--------
MIT licensed. See the bundled [LICENSE](https://github.com/dhanababum/dj-wkhtmltopdf/blob/master/LICENSE) file for more details.
