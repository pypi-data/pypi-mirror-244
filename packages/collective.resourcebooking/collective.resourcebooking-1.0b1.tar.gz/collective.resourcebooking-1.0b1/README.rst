.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/collective/collective.resourcebooking/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.resourcebooking/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.resourcebooking/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.resourcebooking?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.resourcebooking/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.resourcebooking

.. image:: https://img.shields.io/pypi/v/collective.resourcebooking.svg
    :target: https://pypi.python.org/pypi/collective.resourcebooking/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.resourcebooking.svg
    :target: https://pypi.python.org/pypi/collective.resourcebooking
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.resourcebooking.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.resourcebooking.svg
    :target: https://pypi.python.org/pypi/collective.resourcebooking/
    :alt: License


================================
collective.resourcebooking (WIP)
================================

Allow users to book resources like rooms in Plone

Features
--------

- You can add multiple resource booking container in a Plone site, to manage different resources.
- Every resource booking container has a resources and a bookings container
- Create your resources you want to make bookable in the resources container
- Create bookings in the bookings container
- For now there are two time slots per day available "Morning", "Afternoon".




Translations
------------

This product has been translated into

- English



Installation
------------

Install collective.resourcebooking by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.resourcebooking


and then running ``bin/buildout``


Maintainers
-----------

- Maik Derstappen - MrTango <md@derico.de>


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.resourcebooking/issues
- Source Code: https://github.com/collective/collective.resourcebooking



Support
-------

If you are having issues, please let us know and open an issue.


License
-------

The project is licensed under the GPLv2.
