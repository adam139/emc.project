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
from plone.app.dexterity import _ as _p


@provider(IFormFieldProvider)
class IDynamicUsers(model.Schema):
    
    model.fieldset(
        'settings',
        label=_p(u"Settings"),
        fields=['users']
    )    
    
    form.order_before(users='ITableOfContents.table_of_contents')
    form.write_permission(users='emc.project.add_team')
    users = schema.Tuple(
        title=_(u"Workflow setting"),
        description=_(u"Workflow next processor"),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(), # important!
    )

    form.widget('users',AjaxSelectFieldWidget,vocabulary='plone.principalsource.Users')


@implementer(IDynamicUsers)
@adapter(IDexterityContent)
class DynamicUsers(object):

    def __init__(self, context):
        self.context = context



