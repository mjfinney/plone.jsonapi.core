# -*- coding: utf-8 -*-

import time
import traceback
import logging
import simplejson as json
from AccessControl import getSecurityManager
from zope.globalrequest import getRequest
try:
    # Plone < 4.3
    from zope.app.component.hooks import getSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSite

from werkzeug.exceptions import HTTPException, NotFound
from plone.jsonapi.core.exceptions import APIError

__author__ = 'Ramon Bartl <ramon.bartl@googlemail.com>'
__docformat__ = 'plaintext'

logger = logging.getLogger("plone.jsonapi.core.decorators")

def handle_errors(f):
    """ simple JSON error handler
    """

    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError, e: 
            request = getRequest()
            message = str(e)
            error=str(traceback.format_exc())

        except NotFound, e:
            message = str(e)
            error=str(traceback.format_exc())
            request = getRequest()
            request.response.setStatus(404)

        except Exception, e:
            request = getRequest()
            if request.response.getStatus() == 200:
                request.response.setStatus(500)
            message = str(request.response.getStatus()) + " There was an error with this request."
            error = str(e) + str(traceback.format_exc())

        site = getSite()
        status = request.response.getStatus()

        if status not in (200, 404, 410):
            logger.error("The following error has occured during an API response:\n %s\n %s", message, error)

        if not getSecurityManager().checkPermission("ManagePortal", site):
            if status == 404:
                error = "This resource does not seem to exist."
            else:
                error = "Please Contact a site administrator."

        result = {"success": False, "message": message, "error": error}
        #return error(str(e), error=str(traceback.format_exc()))
        return result

    return decorator


def runtime(func):
    """ simple runtime measurement of the called function
    """

    def decorator(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        result.update(dict(_runtime=end-start))
        return result

    return decorator


def returns_json(func):
    """ returns json output
    """

    def decorator(*args, **kwargs):
        instance = args[0]
        request = getattr(instance, 'request', None)
        request.response.setHeader("Content-Type", "application/json")
        result = func(*args, **kwargs)
        return json.dumps(result)

    return decorator


def supports_jsonp(func):
    """ suports jsonp output
    """

    def decorator(*args, **kwargs):
        instance = args[0]
        request = getattr(instance, 'request', None)

        c = request.form.get("c", None)
        if c is not None:
            return "%s(%s);" % (str(c), func(*args, **kwargs))
        return func(*args, **kwargs)

    return decorator
