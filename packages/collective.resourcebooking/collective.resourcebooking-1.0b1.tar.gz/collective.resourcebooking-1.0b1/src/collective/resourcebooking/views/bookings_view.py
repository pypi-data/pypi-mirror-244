# -*- coding: utf-8 -*-

# from collective.resourcebooking import _
from ..content.booking import get_available_timeslots
from ..content.booking import IBooking
from ..vocabularies.utils import get_vocab_term
from collections import defaultdict
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import MO
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import SU
from plone import api
from plone.protect.utils import addTokenToUrl
from pprint import pprint
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

import zope.schema


class IBookingsView(Interface):
    """Marker Interface for IBookingsView"""


@implementer(IBookingsView)
class BookingsView(BrowserView):
    def __call__(self):
        today = date.today()
        self.date = today
        self.target_date = self.request.get("date", "")
        if self.target_date:
            self.date = date.fromisoformat(self.target_date)
        self.calendar_week = self.date.isocalendar().week
        self.next_target_date = self.date + timedelta(weeks=1)
        self.prev_target_date = self.date + timedelta(weeks=-1)
        self.week_start, self.week_end = self.get_week_dates()
        current_week_bookings = self.find_bookings(self.week_start, self.week_end)
        self.weekdays = (0, 1, 2, 3, 4, 5, 6)
        self.available_ressources = api.content.find(context=self.context, portal_type="Resource", sort_on="sortable_title")
        self.dates_of_week = self.generate_dates_of_week(self.date, self.weekdays)
        self.available_timeslots = get_available_timeslots(self.context)
        self.timeslots_count = len(self.available_timeslots) - 1
        self.current_week_bookings = self.resolve_vocabularies(
            current_week_bookings
        )
        self.bookings_by_resource = self.get_bookings_by_resource(
            self.current_week_bookings
        )
        self.resource_ids = sorted(self.bookings_by_resource.keys())
        return self.index()

    def generate_dates_of_week(self, rdate, weekdays):
        dates_of_week = []
        for wday in weekdays:
            wdate = rdate + timedelta(days=(wday - rdate.weekday()))
            dates_of_week.append(wdate)
        return dates_of_week

    def add_token_to_url(self, url):
        return addTokenToUrl(url)

    def find_bookings(self, week_start, week_end):
        bookings = api.content.find(
            context=self.context,
            portal_type="Booking",
            start={
                "query": week_end,
                "range": "max",
            },
            end={
                "query": week_start,
                "range": "min",
            },
            order_by=["resource", "day", "timeslot"],
        )
        return bookings

    def resolve_vocabularies(self, bookings):
        resolved_bookings = []
        fields = zope.schema.getFields(IBooking)
        for brain in bookings:
            # this might be a booking without day and timeslot, we ignore it
            if not brain.day:
                continue
            booking = brain.getObject()
            booking_info = {}
            resource_term = get_vocab_term(
                booking, fields["resource"], booking.resource
            )
            booking_info["resource"] = resource_term["token"]
            booking_info["resource_title"] = resource_term["title"]
            timeslot_term = get_vocab_term(
                booking, fields["timeslot"], booking.timeslot
            )
            booking_info["timeslot"] = timeslot_term["token"]
            booking_info["timeslot_title"] = timeslot_term["title"]
            booking_info["day"] = booking.day.isoformat()
            booking_info["url"] = booking.absolute_url()
            booking_info["obj"] = booking
            resolved_bookings.append(booking_info)
        return resolved_bookings

    def get_bookings_by_resource(self, bookings):
        def rec_dd():
            return defaultdict(rec_dd)

        bookings_by_resource = rec_dd()
        for booking in bookings:
            booking_day = date.fromisoformat(booking["day"])
            booking_weekday = booking_day.weekday()
            bookings_by_resource[booking["resource"]]["name"] = booking["resource_title"]
            # bookings_by_resource[booking["resource"]][booking_weekday][booking["timeslot"]]["name"] = booking["timeslot_title"]
            bookings_by_resource[booking["resource"]][booking_weekday][
                booking["timeslot"]
            ] = booking
        # pprint(bookings_by_resource)
        return bookings_by_resource

    def get_booking_by_resource_id(self, resource_id):
        return self.bookings_by_resource.get(resource_id, None)

    def get_week_dates(self):
        day = self.date
        current_week_start = day + relativedelta(weekday=MO(-1))
        current_week_end = day + relativedelta(weekday=SU)
        # next_week_start = day + relativedelta(weekday=MO(+1))
        # next_week_end = day + relativedelta(weekday=SU(+2))
        # nextnext_week_start = day + relativedelta(weekday=MO(+2))
        # nextnext_week_end = day + relativedelta(weekday=SU(+3))
        # return {
        #     "current_week": (current_week_start, current_week_end),
        #     "next_week": (next_week_start, next_week_end),
        #     "nextnext_week": (nextnext_week_start, nextnext_week_end),
        # }
        return (current_week_start, current_week_end)
