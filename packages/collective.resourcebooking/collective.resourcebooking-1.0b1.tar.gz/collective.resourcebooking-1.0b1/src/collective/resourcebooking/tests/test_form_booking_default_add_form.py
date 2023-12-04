# -*- coding: utf-8 -*-
from collective.resourcebooking.forms.booking_default_add_form import (
    IBookingDefaultAddView,
)
from collective.resourcebooking.testing import (
    COLLECTIVE_RESOURCEBOOKING_FUNCTIONAL_TESTING,
)
from collective.resourcebooking.testing import (
    COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        roombookings = api.content.create(
            self.portal, "ResourceBooking", "roombookings", "Room bookings"
        )
        # self.bookings = api.content.create(
        #     roombookings, "Bookings", "bookings", "Bookings"
        # )
        # resources = api.content.create(
        #     roombookings, "Resources", "resources", "Resources"
        # )
        self.bookings = roombookings["bookings"]
        resources = roombookings["resources"]
        api.content.create(resources, "Resource", "resource1", "Resource 1")

    def test_booking_default_add_form_is_registered(self):
        view = self.bookings.unrestrictedTraverse("++add++Booking")
        self.assertTrue(view.__name__ == "Booking")
        self.assertTrue(IBookingDefaultAddView.providedBy(view))


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
