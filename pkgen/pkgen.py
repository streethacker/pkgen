# -*- coding: utf-8 -*-

import os
import md5
import binascii
import socket
import struct
import time
import datetime
import uuid
import logging

from threading import (
    Lock,
)

logger = logging.getLogger(__name__)


class Borg(object):
    _state = {}

    def __new__(cls, *args, **kw):
        ob = super(Borg, cls).__new__(cls, *args, **kw)
        ob.__dict__ = cls._state
        return ob


class Pk(object):
    """
    Pk Object.

    :param _id: Actual primary key send to the database.
    :param currtime: Byte stream represents the ts when `_id` was craeted.
    :param machine_signature: First 3 bytes of the machine
        fingerprints(i.e. md5 sig of hostname + mac address combination).
    :param proc_signature: PID of the process which generates `_id`.
    :param incr: Globally unique counter, represents the specific counter's
        value when `_id` was created.
    Returns an :py:class:`~Pk` object.
    """

    def __init__(
            self,
            _id,
            currtime,
            machine_signature,
            proc_signature,
            incr):
        self._id = _id
        self._currtime = currtime
        self._machine_signature = machine_signature
        self._proc_signature = proc_signature
        self._incr = incr

    @property
    def pk(self):
        return self._id

    @property
    def currtime(self):
        ts, = struct.unpack('>i', self._currtime)
        return self._utc2dt(ts)

    @property
    def machine_signature(self):
        return self._machine_signature

    @property
    def proc_signature(self):
        pid, = struct.unpack('>H', self._proc_signature)
        return pid

    @property
    def incr(self):
        incr, = struct.unpack('>I', self._incr)
        return incr

    def _utc2dt(self, ts):
        return datetime.datetime.fromtimestamp(ts)


class PkGen(Borg):
    """
    PkGen.

    A class that represents a pk generator.

    Inherited from :py:class:`~Borg`, this class is designed to be a singleton,
    i.e. all of its instances within the same process shares a class level
    primitive lock `_lock`, a global counter variable `_incr` and counter's
    maximum `_MAX_INCR`.

    e.g.

    .. code:: python

        >>> from pkgen import PkGen
        >>> pkg = PkGen()
        >>> pk = pkg.pkgen()
        >>> pk.pk
        '5735ae95c14e2435aa000000'
        >>>
    """

    _incr = 0
    _lock = Lock()

    _MAX_INCR = sum([pow(2, n) for n in xrange(24)]) + 1

    @classmethod
    def incrby(cls, incr=1):
        cls._incr += incr
        cls._incr %= cls._MAX_INCR
        return cls._incr

    @classmethod
    def pkgen(cls):
        currtime = struct.pack('>i', int(time.time()))
        machine_signature = md5.new(
            socket.gethostname() + hex(uuid.getnode())[2:]).digest()[0:3]
        proc_signature = struct.pack('>H', os.getpid())
        with cls._lock:
            incr = struct.pack('>I', cls._incr)
            cls.incrby()
        _id = binascii.hexlify(
            currtime +
            machine_signature +
            proc_signature +
            incr[1:])
        return Pk(
            _id,
            currtime,
            machine_signature,
            proc_signature,
            incr)
