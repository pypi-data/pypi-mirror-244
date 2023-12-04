# -*- coding: utf-8 -*-
"""Init and utils."""
from logging import getLogger
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("collective.resourcebooking")


logger = getLogger("collective.resourcebooking")
