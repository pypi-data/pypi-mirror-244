# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.resourcebooking import logger
from plone import api
from zope.component import createObject
from zope.component.hooks import getSite


def handler(obj, event):
    """Event handler"""
    container = aq_inner(event.object)
    portal = getSite()
    portal_types = portal.portal_types
    resources_id = portal_types.constructContent(
        "Resources",
        container,
        "resources",
        title="Resources",
    )
    bookings_id = portal_types.constructContent(
        "Bookings",
        container,
        "bookings",
        title="Bookings",
    )
    logger.info(
        f"Subscriber created bookings and resources containers in : {obj.absolute_url()}"
    )
