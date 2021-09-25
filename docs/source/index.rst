Welcome to jiml's documentation!
================================

|downloads| |license| |wheel| |pyversions| |build-status-image| |pypi-version| |codecov| |docs|

.. include:: ../../README.rst

--------------
The User Guide
--------------

This part of the documentation, which is mostly prose, begins with some
background information about Jiml, then focuses on step-by-step
instructions for getting the most out of Jiml.

This library is an attempt to make easier and standartize an approach to
conversion json to json. Under the hood, Jiml uses Jinja and PyYAML libraries.
jsonschema is used for validation. If you are not familiar with their syntax,
there are some links for five-minute tutorials for each of these tools.

Table of contents:

.. toctree::
   :maxdepth: 2

   Welcome <self>
   guide/install
   guide/quickstart
   guide/validation
   guide/performance

.. guide/tests experimental
.. tutorials
.. classes documentation



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |downloads| image:: https://pepy.tech/badge/jiml/month
    :target: https://pepy.tech/project/jiml
    :alt: Requests Downloads Per Month Badge
.. |license| image:: https://img.shields.io/pypi/l/jiml.svg
    :target: https://pypi.org/project/jiml/
    :alt: License Badge
.. |wheel| image:: https://img.shields.io/pypi/wheel/jiml.svg
    :target: https://pypi.org/project/jiml/
    :alt: Wheel Support Badge
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/jiml.svg
    :target: https://pypi.org/project/jiml/
    :alt: Python Version Support Badge
.. |build-status-image| image:: https://app.travis-ci.com/vmstarchenko/jiml.svg?branch=main
      :target: https://travis-ci.com/vmstarchenko/jiml?branch=main
.. |pypi-version| image:: https://img.shields.io/pypi/v/jiml.svg
   :target: https://pypi.python.org/pypi/jiml
.. |codecov| image:: https://codecov.io/gh/tfranzel/jiml/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/vmstarchenko/jiml
.. |docs| image:: https://readthedocs.org/projects/jiml/badge/
   :target: https://jiml.readthedocs.io/
