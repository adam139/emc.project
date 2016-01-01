# -*- coding: utf-8 -*-
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
# from plone.autoform.view import WidgetsView
# from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from emc.project import _


@provider(IFormFieldProvider)
class ISecurityLevel(model.Schema):

    security_level = schema.Choice(
        title=_(u"task type"),
        vocabulary="emc.project.vocabulary.securitylevel",
        default ="public"
    )
#     form.widget('report', RichTextFieldWidget)
#     model.primary('text')


@implementer(ISecurityLevel)
@adapter(IDexterityContent)
class SecurityLevel(object):

    def __init__(self, context):
        self.context = context



