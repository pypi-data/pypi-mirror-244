# -*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta
from plone import api
from plone.protect.utils import safeWrite
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


class IBookResourceView(Interface):
    """Marker Interface for IBookResourceView"""


@implementer(IBookResourceView)
class BookResourceView(BrowserView):
    def __call__(self):
        safeWrite(self.context, self.request)
        wday = self.request.get("wday")
        target_date_str = self.request.get("date")
        target_date = (target_date_str and date.fromisoformat(target_date_str)) or date.today()
        day = target_date + timedelta(days=(int(wday) - target_date.weekday()))
        booking = api.content.create(
            container=self.context,
            type="Booking",
            title=self.request.get("resource"),
            resource=self.request.get("resource"),
            day=day,
            timeslot=int(self.request.get("timeslot")),
        )
        # print(f"Booked {booking.title}")
        rb_container = self.context.get_resource_booking_container()
        url = rb_container.absolute_url()
        if target_date_str:
            url += f"?date={target_date_str}"
        self.request.response.setHeader("Cache-Control", "max-age=0, must-revalidate, private")
        return self.request.response.redirect(url, status=301)
