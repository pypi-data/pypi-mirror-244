# -*- coding: utf-8 -*-
from collective.resourcebooking.content.booking import IBooking  # NOQA E501
from collective.resourcebooking.testing import (  # noqa
    COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class BookingIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Bookings",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_booking_schema(self):
        fti = queryUtility(IDexterityFTI, name="Booking")
        schema = fti.lookupSchema()
        self.assertEqual(IBooking, schema)

    def test_ct_booking_fti(self):
        fti = queryUtility(IDexterityFTI, name="Booking")
        self.assertTrue(fti)

    def test_ct_booking_factory(self):
        fti = queryUtility(IDexterityFTI, name="Booking")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IBooking.providedBy(obj),
            "IBooking not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_booking_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Booking",
            id="booking",
        )

        self.assertTrue(
            IBooking.providedBy(obj),
            "IBooking not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("booking", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("booking", parent.objectIds())

    def test_ct_booking_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Booking")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))
