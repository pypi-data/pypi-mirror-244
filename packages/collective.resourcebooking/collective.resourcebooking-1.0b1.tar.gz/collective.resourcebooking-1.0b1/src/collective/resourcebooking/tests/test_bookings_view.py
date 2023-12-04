# -*- coding: utf-8 -*-
from collective.resourcebooking.testing import (
    COLLECTIVE_RESOURCEBOOKING_FUNCTIONAL_TESTING,
)
from collective.resourcebooking.testing import (
    COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING,
)
from collective.resourcebooking.views.bookings_view import IBookingsView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.roombookings = api.content.create(
            container=self.portal, type="ResourceBooking", title="roombookings"
        )
        self.booking = api.content.create(
            container=self.roombookings["bookings"],
            type="Booking",
            title="Test Booking 1",
        )
        api.content.create(self.portal, "Document", "front-page")

    def test_view_is_registered(self):
        view = getMultiAdapter((self.roombookings, self.portal.REQUEST), name="view")
        self.assertTrue(view.__name__ == "view")
        self.assertTrue(IBookingsView.providedBy(view))

    def test_view_not_matching_interface(self):
        view = getMultiAdapter(
            (self.portal["front-page"], self.portal.REQUEST), name="view"
        )
        self.assertFalse(IBookingsView.providedBy(view))


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
