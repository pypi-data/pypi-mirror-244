# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.supermodel.directives import fieldset
# from plone.namedfile import field as namedfile
# from z3c.form.browser.radio import RadioFieldWidget
from collective.resourcebooking import _
from datetime import datetime
from datetime import time
from dateutil.relativedelta import relativedelta
from plone import api
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IVocabularyFactory


def get_available_timeslots(context):
    timeslots_vocab_factory = getUtility(
        IVocabularyFactory, "collective.resourcebooking.AvailableTimeslots"
    )
    vocab = timeslots_vocab_factory(context)
    return vocab


def get_timeslots_count(context):
    """for external usage like in bookings view"""
    vocab = get_available_timeslots(context)
    timeslots_count = len(vocab) - 1
    return timeslots_count


def get_timeslot(context, timeslot=None, day=None):
    timeslots_vocab_factory = getUtility(
        IVocabularyFactory, "collective.resourcebooking.AvailableTimeslots"
    )
    vocab = timeslots_vocab_factory(context)
    timeslots_count = len(vocab) - 1
    DAY_MINUTES = 1440
    timeslot_minutes = DAY_MINUTES / timeslots_count
    day_begin = datetime.combine(day, time())
    i = vocab.by_value.get(timeslot).value - 1
    t1 = timeslot_minutes * i
    i += 1
    t2 = (timeslot_minutes * i) - 1
    return (
        day_begin + relativedelta(minutes=+t1),
        day_begin + relativedelta(minutes=+t2),
    )


def get_timeslot_start(context, timeslot=None, day=None):
    timeslots = get_timeslot(context, timeslot=timeslot, day=day)
    return timeslots[0]


def get_timeslot_end(context, timeslot=None, day=None):
    timeslots = get_timeslot(context, timeslot=timeslot, day=day)
    return timeslots[1]


@provider(IContextAwareDefaultFactory)
def resource_default_factory(parent):
    resource = parent.REQUEST.get("resource", "")
    print(f"resource: {resource}")
    return resource


class TimeslotUnavailable(Invalid):
    __doc__ = _("The choosen timeslot is not available on that day!")


class IBooking(model.Schema):
    """Marker interface and Dexterity Python Schema for Booking"""

    def get_resource_booking_container(self):
        return self.__parent__.get_resource_booking_container()

    directives.mode(title="hidden")
    title = schema.TextLine(
        title=_(
            "Computed Title",
        ),
        required=False,
        readonly=False,
    )

    resource = schema.Choice(
        title=_(
            "Resource",
        ),
        description=_(
            "Choose a resource to book",
        ),
        vocabulary="collective.resourcebooking.AvailableResources",
        # default="",
        defaultFactory=resource_default_factory,
        required=True,
        readonly=False,
    )

    day = schema.Date(
        title=_(
            "Day",
        ),
        # defaultFactory=get_default_,
        required=True,
        readonly=False,
    )

    timeslot = schema.Choice(
        title=_(
            "Timeslot",
        ),
        vocabulary="collective.resourcebooking.AvailableTimeslots",
        # default="",
        # defaultFactory=timeslot_default_factory,
        required=True,
        readonly=False,
    )

    directives.mode(start="hidden")
    start = schema.Datetime(
        title=_(
            "Start",
        ),
        required=False,
    )

    directives.mode(end="hidden")
    end = schema.Datetime(
        title=_(
            "End",
        ),
        required=False,
    )

    @invariant
    def validateTimeslotIsAvailable(data):
        if data.timeslot is not None:
            context = data.__context__
            resource_booking = context.get_resource_booking_container()
            timeslot_start = get_timeslot_start(
                context, timeslot=data.timeslot, day=data.day
            )
            timeslot_end = get_timeslot_end(
                context, timeslot=data.timeslot, day=data.day
            )
            res = api.content.find(
                context=resource_booking,
                resource=data.resource,
                start={"query": timeslot_start, "range": "min"},
                end={"query": timeslot_end, "range": "max"},
            )
            # import pdb; pdb.set_trace()  # NOQA: E702
            for booking in res:
                if booking.UID != context.UID():
                    raise TimeslotUnavailable(
                        _("The timeslot is not available on that day.")
                    )


@implementer(IBooking)
class Booking(Item):
    """Content-type class for IBooking"""

    @property
    def title(self):
        computed_title = ""
        if hasattr(self, "resource"):
            computed_title = self.resource
        if hasattr(self, "day") and hasattr(self, "timeslot"):
            computed_title += f": {self.day.isoformat()}-{self.timeslot}"
        return computed_title

    @title.setter
    def title(self, value):
        return None

    @property
    def start(self):
        if not self.timeslot:
            return datetime.today()
        timeslot = get_timeslot_start(self, timeslot=self.timeslot, day=self.day)
        return timeslot

    @start.setter
    def start(self, value):
        return None

    @property
    def end(self):
        if not self.timeslot:
            return datetime.today()
        timeslot = get_timeslot_end(self, timeslot=self.timeslot, day=self.day)
        return timeslot

    @end.setter
    def end(self, value):
        return None
