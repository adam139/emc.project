#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from emc.project import _

try:
    from plone.app.dexterity import _ as _p
except:
    from plone.app.dexterity import PloneMessageFactory as _p


class IUsersrolesProvider(Interface):
    """Marker interface which specifies that the view  will provide Usersroles viewlet.
    """

class IProjectContent(form.Schema,IBasic):
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
    
class IMaking(Interface):
    """复制文档类型设置
    """
    types = schema.Set(
            title=_(u"zhi ding yu xia fa"),
            description=_(u"List project folder allow add zhi ding yu xia fa."),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u"zhi ding")),
        )        