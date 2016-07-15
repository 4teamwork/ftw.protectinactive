from zope.interface import Interface
from zope import schema


class IProtectInactiveSettings(Interface):
    exception_type = schema.Choice(
        title=u"Exception Type",
        description=u"The exception raised when a user tries to access "
                    u"inactive content without permission.",
        values=['Unauthorized', 'NotFound'],
        default='Unauthorized'
    )
