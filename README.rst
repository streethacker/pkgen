PkGen
=====

Introduction
------------

**PkGen** is a pk generator implemented using Python, who's core algorithm
derives from `Mongo's <https://docs.mongodb.com/>`_ generation of ``ObjectId``.

**Basic Concept of ObjectId**

   A BSON ObjectId is a 12-byte value consisting of a 4-byte timestamp
   (seconds since epoch), a 3-byte machine id, a 2-byte process id(PID)
   and a 3-byte counter. Note tha the timestamp and counter fields must
   be stored big endian unlike the rest of BSON.

   `More <https://docs.mongodb.com/manual/reference/method/ObjectId/>`_

Install
-------

2 ways to install **PkGen**:

1. clone the repo to your machine, run ``setup.py``

.. code:: bash

   $ cd ~ && git@github.com:streethacker/pkgen.git
   $ python setup.py install

2. using pip

.. code:: bash

   $ pip install -e git+https://github.com/streethacker/pkgen@0.1#egg=pkgen

Start
-----

.. code:: python

    >>> from pkgen import PkGen
    >>> pkg = PkGen()
    >>> pk = pkg.pkgen()
    >>> pk.pk
    '5735ae95c14e2435aa000000'
    >>>
