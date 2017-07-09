from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from django.db import connection


# connection.connection.text_factory = \
#     lambda x: unicode(x, "utf-8", "ignore")


import types
from django.db.backends.sqlite3.base import DatabaseWrapper


def to_unicode( s ):
    ''' Try a number of encodings in an attempt to convert the text to unicode. '''
    if isinstance( s, unicode ):
        return s
    if not isinstance( s, str ):
        return unicode(s)

    encodings = (
        'utf-8',
        'iso-8859-1', 'iso-8859-2', 'iso-8859-3',
        'iso-8859-4', 'iso-8859-5',
        'iso-8859-7', 'iso-8859-8', 'iso-8859-9',
        'iso-8859-10', 'iso-8859-11',
        'iso-8859-13', 'iso-8859-14', 'iso-8859-15',
        'windows-1250', 'windows-1251', 'windows-1252',
        'windows-1253', 'windows-1254', 'windows-1255',
        'windows-1257', 'windows-1258',
        'utf-8',     # Include utf8 again for the final exception.
    )
    for encoding in encodings:
        try:
            return unicode( s, encoding )
        except UnicodeDecodeError as e:
            pass
    raise e

if not hasattr(DatabaseWrapper, 'get_new_connection_is_patched'):
    _get_new_connection = DatabaseWrapper.get_new_connection
    def _get_new_connection_tolerant(self, conn_params):
        conn = _get_new_connection( self, conn_params )
        conn.text_factory = to_unicode
        return conn

    DatabaseWrapper.get_new_connection = types.MethodType( _get_new_connection_tolerant, None, DatabaseWrapper )
    DatabaseWrapper.get_new_connection_is_patched = True


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True,
                                      null=True)

    class Meta:
        abstract = True

@python_2_unicode_compatible
class BaseValue(Base):
    value = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.value)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class BaseName(Base):
    name = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        abstract = True


class DhcpVendor(BaseValue):

    class Meta:
        db_table = 'dhcp_vendor'


class UserAgent(BaseValue):

    class Meta:
        db_table = 'user_agent'


class DhcpFingerprint(BaseValue):
    # ignored = models.BooleanField(default=False)
    ignored = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'dhcp_fingerprint'


class Dhcp6Fingerprint(BaseValue):
    pass

    class Meta:
        db_table = 'dhcp6_fingerprint'


class Dhcp6Enterprise(BaseValue):
    organization = models.CharField(max_length=255, blank=True,
                                    null=True)

    class Meta:
        db_table = 'dhcp6_enterprise'


class MacVendor(BaseName):
    name = models.CharField(max_length=255, blank=True, null=True)
    mac = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = 'mac_vendor'


class Device(BaseName):
    name = models.CharField(max_length=255, blank=True, null=True)
    # mobile = models.NullBooleanField()
    mobile = models.PositiveSmallIntegerField(blank=True, null=True)
    # tablet = models.NullBooleanField()
    parent = models.PositiveSmallIntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    # inherit = models.NullBooleanField()
    inherit = models.PositiveSmallIntegerField(blank=True, null=True)
    submitter_id = models.PositiveIntegerField(
                            blank=True,
                            null=True,)
    # approved = models.models.NullBooleanField(default=True)
    approved = models.PositiveSmallIntegerField(default=1)
    devices_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'device'


@python_2_unicode_compatible
class Combination(Base):
    dhcp_fingerprint =  models.ForeignKey(DhcpFingerprint,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    user_agent = models.ForeignKey(UserAgent,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    device =  models.ForeignKey(Device,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    version = models.CharField(max_length=255, null=True, blank=True)
    dhcp_vendor = models.ForeignKey(DhcpVendor,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    score = models.PositiveSmallIntegerField(default=0)
    mac_vendor = models.ForeignKey(MacVendor,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    submitter_id = models.PositiveIntegerField(
                            blank=True,
                            null=True,)
    dhcp6_fingerprint = models.ForeignKey(Dhcp6Fingerprint,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    dhcp6_enterprise = models.ForeignKey(Dhcp6Enterprise,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,)
    fixed = models.PositiveSmallIntegerField(default=0)
    # fixed = models.NullBooleanField(default=False)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.dhcp_vendor,
                                    self.dhcp_fingerprint, self.score)

    class Meta:
        db_table = 'combination'
