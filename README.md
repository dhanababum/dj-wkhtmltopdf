dj-wkhtmltopdf
--------------
--------------
It works on [wkhtmltopdf](http://wkhtmltopdf.org/) . ``dj-wkhtmltopdf`` will allow user to organize their own pdf generator through django admin without any deployment :).

Mainly I was inspired by [django-wkhtmltopdf](https://github.com/incuna/django-wkhtmltopdf) . When I am working on Eccomerce project we want to generate invoice for orders.So we preferred wkhtmltopdf for pdf generator using django-wkhtmltopdf wrapper. Every time we are doing some modifications in local server and pushing this modifications into production but we have faced different(I mean design) issues in production,then we resolved issues in local and pushed into production,but it is so painful then I came to this thought.
Requirements:
-------------
-------------
Install the [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html) .
Python 2.6+ and 3.3+ is supported.
Installation:
------------
------------
Run ``pip install django-wkhtmltopdf``.

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
