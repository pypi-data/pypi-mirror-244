# -*- coding: utf-8 -*-
from collective.resourcebooking.content.resources import IResources  # NOQA E501
from collective.resourcebooking.testing import (  # noqa
    COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING,
)
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ResourcesIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "ResourceBooking",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_resources_schema(self):
        fti = queryUtility(IDexterityFTI, name="Resources")
        schema = fti.lookupSchema()
        self.assertEqual(IResources, schema)

    def test_ct_resources_fti(self):
        fti = queryUtility(IDexterityFTI, name="Resources")
        self.assertTrue(fti)

    def test_ct_resources_factory(self):
        fti = queryUtility(IDexterityFTI, name="Resources")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IResources.providedBy(obj),
            "IResources not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_resources_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Resources",
            id="resources2",
        )

        self.assertTrue(
            IResources.providedBy(obj),
            "IResources not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("resources2", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("resources2", parent.objectIds())

    def test_ct_resources_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Resources")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))

    def test_ct_resources_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Resources")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "resources_id",
            title="Resources container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
