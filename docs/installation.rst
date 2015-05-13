Installation of dj-wkhtmltopdf
==============================

.. toctree::
   :maxdepth: 2

Requirements
-------------

   Install the wkhtmltopdf in your local/server going through this link `wkhtmltopdf download <http://wkhtmltopdf.org/downloads.html>`_ .

   Python 2.6+ and 3.3+ is supported.

dj-wkhtmltopdf Installation
---------------------------

From PyPI
~~~~~~~~~

.. code-block:: bash

    pip install dj-wkhtmltopdf

From source
~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/dhanababum/dj-wkhtmltopdf.git
    cd dj-wkhtmltopdf
    python setup.py install

Setting up dj-wkhtmltopdf in Django
-----------------------------------

Add ``wkhtmltopdf`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'djwkhtmltopdf',
        # ...
    )

Then run the below django command,

.. code-block:: bash

    python manage.py syncdb

By default it will try to execute the ``wkhtmltopdf`` command from your ``PATH``.

If you can't add wkhtmltopdf to your ``PATH`` or you want to use some other
version, you can use the ``WKHTMLTOPDF_CMD`` setting:

.. code-block:: python

    WKHTMLTOPDF_CMD = '/path/to/my/wkhtmltopdf'
