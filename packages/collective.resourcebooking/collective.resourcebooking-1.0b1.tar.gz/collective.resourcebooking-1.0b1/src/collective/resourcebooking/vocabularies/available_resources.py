# -*- coding: utf-8 -*-

# from collective.resourcebooking import _
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class AvailableResources(object):
    """ """

    def __call__(self, context):
        terms = []
        if not context:
            return SimpleVocabulary(terms)
        resource_booking = context.get_resource_booking_container()
        items = [
            VocabItem(item.id, item.Title)
            for item in api.content.find(
                context=resource_booking,
                portal_type="Resource",
                sort_on="sortable_title",
            )
            if item
        ]
        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


AvailableResourcesFactory = AvailableResources()
