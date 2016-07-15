from AccessControl.unauthorized import Unauthorized
from DateTime import DateTime
from plone.app.dexterity.behaviors.metadata import IPublication
from plone import api
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot
from zExceptions import NotFound
from zope.component.hooks import getSite


def InactiveProtector(event):
    """ Protect inactive content from unauthorized access. """

    site = getSite()
    if not site:
        return

    context = findContext(event.request)

    if api.user.has_permission('Modify portal content', obj=context):
        return

    # check expiration
    publication_date, expiration_date = getPublicationDates(context)

    if isUnreleased(publication_date) or isExpired(expiration_date):
        exception_type = api.portal.get_registry_record('ftw.protectinactive.registry.IProtectInactiveSettings.exception_type')
        exception = {
            'Unauthorized': Unauthorized,
            'NotFound': NotFound
        }.get(exception_type, NotImplementedError)

        raise exception()


def isUnreleased(publication_date):
    """ Checks if the publication date is in the future.
        If it is it checks if the user has access to unreleased content.
    """
    now = DateTime()
    return (publication_date and
            now < publication_date and
            not api.user.has_permission('Access inactive portal content'))


def isExpired(expiration_date):
    """ Checks if the expiration date has been exceeded.
        If it is it check if the user has access to expired content.
    """
    now = DateTime()
    return (expiration_date and
            now > expiration_date and
            not api.user.has_permission('Access future portal content'))


def getPublicationDates(context):
    """ Returns the publication and the expiration dates.
        This method supports both archetypes and dexterity content.
    """
    if IATContentType.providedBy(context):
        return getATPublicationDates(context)
    elif False:  # TODO: check for DX
        return getDXPublicationDates(context)

    return None, None


def getATPublicationDates(context):
    if not hasattr(context, 'Schema'):
        return None, None

    effective = context.Schema().getField('effectiveDate').get(context)
    expiration = context.Schema().getField('expirationDate').get(context)
    return effective, expiration


def getDXPublicationDates(context):
    # TODO: do
    pass


def findContext(request):
    """Find the context from the request
       copied from: https://github.com/plone/plone.app.theming/blob/master/src/plone/app/theming/utils.py#L171
    """
    published = request.get('PUBLISHED', None)
    context = getattr(published, '__parent__', None)
    if context is not None:
        return context

    for parent in request.PARENTS:
        if IContentish.providedBy(parent) or ISiteRoot.providedBy(parent):
            return parent

    return request.PARENTS[0]
