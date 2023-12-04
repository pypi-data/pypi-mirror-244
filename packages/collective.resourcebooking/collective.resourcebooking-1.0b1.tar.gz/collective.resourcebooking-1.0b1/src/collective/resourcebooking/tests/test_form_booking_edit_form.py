# -*- coding: utf-8 -*-
from collective.resourcebooking.forms.booking_edit_form import IBookingEditForm
from collective.resourcebooking.testing import (
    COLLECTIVE_RESOURCEBOOKING_FUNCTIONAL_TESTING,
)
from collective.resourcebooking.testing import (
    COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        roombookings = api.content.create(
            self.portal, "ResourceBooking", "roombookings", "Room bookings"
        )
        # bookings = api.content.create(roombookings, "Bookings", "bookings", "Bookings")
        # resources = api.content.create(
        #     roombookings, "Resources", "resources", "Resources"
        # )
        bookings = roombookings["bookings"]
        resources = roombookings["resources"]
        api.content.create(resources, "Resource", "resource1", "Resource 1")
        api.content.create(bookings, "Booking", "booking1", "Booking 1")

    def test_booking_edit_form_is_registered(self):
        view = getMultiAdapter(
            (self.portal["roombookings"]["bookings"]["booking1"], self.portal.REQUEST),
            name="edit",
        )
        self.assertTrue(view.__name__ == "edit")
        self.assertTrue(IBookingEditForm.providedBy(view))


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
