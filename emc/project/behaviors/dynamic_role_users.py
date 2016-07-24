# -*- coding: utf-8 -*-
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.view import WidgetsView
from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from emc.project import _


@provider(IFormFieldProvider)
class IDynamicUsers(model.Schema):
    form.order_after(users='description')
    users = schema.Tuple(
        title=_(u"Workflow next processor"),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(), # important!
    )
#     form.widget('report', RichTextFieldWidget)
    form.widget('users',AjaxSelectFieldWidget,vocabulary='plone.principalsource.Users')


@implementer(IDynamicUsers)
@adapter(IDexterityContent)
class DynamicUsers(object):

    def __init__(self, context):
        self.context = context



