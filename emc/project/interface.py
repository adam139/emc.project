#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema
from plone.directives import form
from emc.project import _


class IUsersrolesProvider(Interface):
    """Marker interface which specifies that the view  will provide Usersroles viewlet.
    """

class IProjectContent(form.Schema):
    """
    emc project  content type base interface
    """

class IDocTypeSettings(Interface):
    """设置各种类型项目文档，分析文档/测试文档等，用于构建项目文档的标题词汇
    """    
    types = schema.Set(
            title=_(u"document types"),
            description=_(u"List project folder allow add document types."),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u"Type")),
        )    