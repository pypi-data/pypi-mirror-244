# -*- coding: utf-8 -*-
from collective.resourcebooking.content.resource import IResource  # NOQA E501
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


class ResourceIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_RESOURCEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Resources",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_resource_schema(self):
        fti = queryUtility(IDexterityFTI, name="Resource")
        schema = fti.lookupSchema()
        self.assertEqual(IResource, schema)

    def test_ct_resource_fti(self):
        fti = queryUtility(IDexterityFTI, name="Resource")
        self.assertTrue(fti)

    def test_ct_resource_factory(self):
        fti = queryUtility(IDexterityFTI, name="Resource")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IResource.providedBy(obj),
            "IResource not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_resource_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Resource",
            id="resource",
        )

        self.assertTrue(
            IResource.providedBy(obj),
            "IResource not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("resource", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("resource", parent.objectIds())

    def test_ct_resource_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Resource")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))
