"""
File-based storage
"""

from config import FILESTORAGE_DIR
import os
import re
import anyjson

class FileStorage():
    """
    Store hosts and guests on the filesystem
    """

    _base_path = None

    _host_file_re = re.compile(r'^host_(.+)\.json$')
    _guest_file_re = re.compile(r'^host_.+_guest_(.+)\.json$')

    def __init__(self):
        """
        base_path - base abs FS path to storage dir
        """
        self._base_path = FILESTORAGE_DIR

    def list_hosts(self):
        """
        Return a list of all KVM host names.
        """
        ret = []
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            hm = self._host_file_re.match(f)
            gm = self._guest_file_re.match(f)
            if hm is not None and gm is None:
                ret.append(hm.group(1))
        return ret

    def get_host(self, name):
        """
        Return the hash of information about a host.

        Return None if not found.
        """
        fname = "host_%s.json" % name
        path = os.path.join(self._base_path, fname)
        if not os.path.exists(path):
            return None
        if not os.path.isfile(path):
            return None
        ret = None
        raw = ""
        with open(path, 'r') as fh:
            raw = fh.read()
        ret = anyjson.deserialize(raw)
        return ret

    def get_all_hosts(self):
        """
        Return a dict of all KVM host information,
        hostname -> dict of data
        """
        ret = {}
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            hm = self._host_file_re.match(f)
            gm = self._guest_file_re.match(f)
            if gm is not None or hm is None:
                continue
            foo = None
            raw = None
            with open(p, 'r') as fh:
                raw = fh.read()
                foo = anyjson.deserialize(raw)
            ret[hm.group(1)] = foo
        return ret

    def store_host(self, hostname, data):
        """
        Store a host's data, from the client script.

        :param hostname: the hostname
        :type hostname: string
        :param data: the dict of data to store
        :type data: dict
        :rtype: boolean
        :returns: True on success, False on failure
        """
        fname = "host_%s.json" % hostname
        path = os.path.join(self._base_path, fname)
        j = anyjson.serialize(data)
        with open(path, 'w') as fh:
            fh.write(j)
        return True

    def list_guests(self):
        """
        Return a list of all KVM guest names.
        """
        ret = []
        file_re = re.compile(r'guest_(.+).json')
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            gm = self._guest_file_re.match(f)
            if gm is not None:
                ret.append(gm.group(1))
        return ret

    def get_guest(self, domname):
        """
        Return the hash of information about a specific guest,
        by libvirt domain name

        Return None if not found.
        """
        fname = "guest_%s.json" % name
        path = os.path.join(self._base_path, fname)
        if not os.path.exists(path):
            return None
        if not os.path.isfile(path):
            return None
        ret = None
        raw = ""
        with open(path, 'r') as fh:
            raw = fh.read()
        ret = anyjson.deserialize(raw)
        return ret

    def get_all_guests(self):
        """
        Return a dict of all KVM guest information,
        libvirt domain name -> dict of data
        """
        ret = {}
        file_re = re.compile(r'guest_(.+).json')
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            gm = self._guest_file_re.match(f)
            if gm is None:
                continue
            foo = None
            with open(p, 'r') as fh:
                raw = fh.read()
            foo = anyjson.deserialize(raw)
            ret[gm.group(1)] = foo
        return ret
