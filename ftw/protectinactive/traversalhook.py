from AccessControl.unauthorized import Unauthorized
from DateTime import DateTime
from plone.app.dexterity.behaviors.metadata import IPublication
from plone import api
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot
from zope.component.hooks import getSite


def InactiveProtector(event):
    """ Protect inactive content from unauthorized access. """

    context = findContext(event.request)

    site = getSite()
    if not site:
        return

    if not isInactive(context):
        return

    if api.user.has_permission('Modify portal content', obj=context):
        return

    if api.user.has_permission('Access inactive portal content'):
        return

    raise Unauthorized()


def isInactive(obj):
    publication_date, expiration_date = getPublicationDates(obj)
    now = DateTime()

    return publication_date and now < publication_date or \
        expiration_date and now > expiration_date


def getPublicationDates(obj):
    if IATContentType.providedBy(obj):
        return getATPublicationDates(obj)
    elif False:  # TODO: check for DX
        return getDXPublicationDates(obj)

    return None, None


def getATPublicationDates(obj):
    if not hasattr(obj, 'Schema'):
        return None, None

    effective = obj.Schema().getField('effectiveDate').get(obj)
    expiration = obj.Schema().getField('expirationDate').get(obj)
    return effective, expiration


def getDXPublicationDates(obj):
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
