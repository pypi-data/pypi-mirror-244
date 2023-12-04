# -*- coding: utf-8 -*-

from ..content.booking import IBooking
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IBooking)  # ADJUST THIS!
def resource(obj):
    """Calculate and return the value for the indexer"""
    return obj.resource
