# -*- coding: utf-8 -*-
"""Init and utils."""
from Products.PythonScripts.Utility import allow_module
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plomino.captchacore')

allow_module("plomino.captchacore.utility")
