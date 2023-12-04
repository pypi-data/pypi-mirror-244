# from collective.resourcebooking import _
from plone.dexterity.browser import add
from zope.interface import implementer
from zope.interface import Interface


ADDFORM_FIELDS = [
    "title",
    "resource",
]


class BookingDefaultAddForm(add.DefaultAddForm):
    autoGroups = False
    portal_type = "Booking"
    addform_fields = ADDFORM_FIELDS

    def updateFieldsFromSchemata(self):
        super().updateFieldsFromSchemata()

        # we do not want the extra groups...
        self.groups = ()
        # filter out fields which are not in addform_fields
        for field_name in self.fields:
            if field_name not in self.addform_fields:
                self.fields = self.fields.omit(field_name)

    # def updateWidgets(self, prefix=None):
    #     resource = self.request.get("resource")
    #     if resource:
    #         import pdb; pdb.set_trace()  # NOQA: E702
    #         self.fields["resource"]
    #     return super().updateWidgets(prefix)

    def nextURL(self):
        if self.immediate_view is not None:
            return "{:s}/@@edit".format(
                "/".join(self.immediate_view.split("/")[:-1]),
            )
        else:
            return self.context.absolute_url()


class IBookingDefaultAddView(Interface):
    """ """


@implementer(IBookingDefaultAddView)
class BookingDefaultAddView(add.DefaultAddView):
    form = BookingDefaultAddForm
