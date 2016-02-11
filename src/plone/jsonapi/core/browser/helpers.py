# -*- coding: utf-8 -*-

__author__ = 'Ramon Bartl <ramon.bartl@googlemail.com>'
__docformat__ = 'plaintext'


def success(message, **kw):
    result = {"success": True, "message": message}
    result.update(kw)
    return result
