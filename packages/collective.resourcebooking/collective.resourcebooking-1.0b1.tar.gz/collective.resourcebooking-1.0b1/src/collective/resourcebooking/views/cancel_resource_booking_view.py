# -*- coding: utf-8 -*-

from plone import api
from plone.protect.utils import safeWrite
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


class ICancelResourceBookingView(Interface):
    """Marker Interface for ICancelResourceBookingView"""


@implementer(ICancelResourceBookingView)
class CancelResourceBookingView(BrowserView):
    def __call__(self):
        safeWrite(self.context, self.request)
        # print(f"Cancel booking {self.context.title}")
        api.content.delete(obj=self.context)
        rb_container = self.context.get_resource_booking_container()
        self.request.response.setHeader("Cache-Control", "max-age=0, must-revalidate, private")
        return self.request.response.redirect(rb_container.absolute_url(), status=301)
