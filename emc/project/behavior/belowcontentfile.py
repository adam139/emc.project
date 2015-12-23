# -*- coding: utf-8 -*-
from plone.app.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IAttachFile(model.Schema):

    attach = namedfile.NamedBlobFile(
        title=_(u'label_attachfile', default=u'attach file below content body'),
        description=_(u'help_attachfile', default=u''),
        required=False,
    )




@implementer(IAttachFile)
@adapter(IDexterityContent)
class AttachFile(object):

    def __init__(self, context):
        self.context = context
