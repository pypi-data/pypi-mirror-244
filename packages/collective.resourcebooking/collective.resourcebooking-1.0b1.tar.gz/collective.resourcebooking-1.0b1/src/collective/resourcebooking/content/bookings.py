# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
# from plone.namedfile import field as namedfile
from collective.resourcebooking.content.resource_booking import IResourceBooking
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import implementer


# from collective.resourcebooking import _


class IBookings(model.Schema):
    """Marker interface and Dexterity Python Schema for Bookings"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('bookings.xml')


@implementer(IBookings)
class Bookings(Container):
    """Content-type class for IBookings"""

    def get_resource_booking_container(self):
        def traverse_to_rb_container(obj):
            if ISiteRoot.providedBy(obj):
                return obj
            parent = obj.__parent__
            if not IResourceBooking.providedBy(parent):
                return traverse_to_rb_container(parent)
            return parent

        return traverse_to_rb_container(self)
