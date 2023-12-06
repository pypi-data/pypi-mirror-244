Powspec
=======

The powspec package provides functions to compute power and cross spectral density of 2D arrays. Units are properly taken into account


Quick start
-----------
Here's a simple script demonstrating the powspec package::

    >>> import astropy.units as u
    >>> from powspec import power_spectral_density, gen_pkfield

    >>> res = 1 * u.arcmin
    >>> img = gen_pkfield(npix=1024, fknee=0.1 / u.arcmin, res=res) * u.MJy
    >>> print(img.unit)
    MJy / arcmin2

    >>> powspec_k, k = power_spectral_density(img, res=res)
    >>> print(powspec_k.unit)
    MJy2 / arcmin2


Getting started
^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   ../auto_examples/index

Reference/API
=============

.. automodapi:: powspec
 
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
 
