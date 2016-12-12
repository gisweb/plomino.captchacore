# -*- coding: utf-8 -*-
#
# File: attachment.py
#
# Copyright (c) 2009 by ['Eric BREHAULT']
#
# Zope Public License (ZPL)
#

__author__ = """Eric BREHAULT <eric.brehault@makina-corpus.com>"""
__docformat__ = 'plaintext'

# Zope
from zope.formlib import form
from zope.interface import implements
from zope import component
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

# Plomino
from Products.CMFPlomino.fields.base import IBaseField, BaseField, BaseForm
from Products.CMFPlomino.interfaces import IPlominoField
from Products.CMFPlomino.fields.dictionaryproperty import DictionaryProperty
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName


class ICaptchaCoreField(IBaseField):
    """ Captcha core field schema
    """

class CaptchaCoreField(BaseField):
    """
    """

    implements(ICaptchaCoreField)

    plomino_field_parameters = {'interface': ICaptchaCoreField,
                                'label':"Captcha",
                                'index_type':"ZCTextIndex"}

    read_template = PageTemplateFile('templates/CAPTCHAFieldRead.pt')
    edit_template = PageTemplateFile('templates/CAPTCHAFieldEdit.pt')    

    def validate(self, submittedValue):
        """
        """
        errors=[]
        fieldname = self.context.id
        # Verify the user input against the captcha.
        # Get captcha type (static or dynamic)
        try:
            from quintagroup.captcha.core.utils import decrypt, parseKey, encrypt1, getWord
        except ImportError:
            return ["manca il prodotto quintagroup.captcha.core"]

        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()
        captcha_type = portal.getCaptchaType()

        request = self.context.REQUEST

        test_key = submittedValue
        hashkey = request.get('hash-%s'%fieldname, '')
        decrypted_key = decrypt(portal.captcha_key, hashkey)
        parsed_key = parseKey(decrypted_key)

        index = parsed_key['key']
        date = parsed_key['date']

        if captcha_type == 'static':
            img = getattr(portal, '%s.jpg' % index)
            solution = img.title
            enc = encrypt1(test_key)
        else:
            enc = test_key
            solution = getWord(int(index))

        captcha_tool = getToolByName(portal, 'portal_captchas')
        if (enc != solution) or (decrypted_key in captcha_tool.keys()) or \
           (DateTime().timeTime() - float(date) > 3600):
            errors.append('Il testo immesso non corrisponde. Riprova')

        return errors


component.provideUtility(CaptchaCoreField, IPlominoField, 'CAPTCHA')

for f in getFields(ICaptchaCoreField).values():
    setattr(CaptchaCoreField,
            f.getName(),
            DictionaryProperty(f, 'parameters'))

class SettingForm(BaseForm):
    """
    """
    form_fields = form.Fields(ICaptchaCoreField)

