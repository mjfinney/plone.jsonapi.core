from zope.interface import implements
from plone.jsonapi.core.exceptions import APIError
from plone.jsonapi.core.interfaces import IRouteProvider

class RouteProviderBase(object):
    implements(IRouteProvider)

    def initialize(self, context, request):
        """ get's called by the API Framework
        """
        pass

    def not_found_error(self, message="404: Not Found"):
        raise APIError(404, message)

    def gone_error(self, message="410: Gone"):
        raise APIError(410, message)
