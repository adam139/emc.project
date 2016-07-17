#-*- coding: UTF-8 -*-
from plone import api
from zope import event
from Acquisition import aq_parent
from zope.component import getMultiAdapter
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from emc.project.content.team import ITeam

from emc.memberArea.events import TodoitemWillCreateEvent
#fire todoitemwillcreated event for every designer when add or modified product designer on project node
def roleModified(obj,event):
    """Project team has been modified subscriber's handler.
    obj: team instance,a project node
    event:objectModifiedevent """  

    #fetch product designer list 
    name = obj.title
    url = obj.absolute_url()
    if ITeam.providedBy(obj):
        title = u"你已经被邀请加入%s项目组" % name
        title = title.encode("utf-8")
        text = u"""<p>详细情况请查看<a href="%s"><strong>%s项目组</strong></a></p>""" %(url,name)
    else:
        title = u"你已经被邀请加入%s项目" % name
        title = title.encode("utf-8")
        text = u"""<p>详细情况请查看<a href="%s"><strong>%s项目</strong></a></p>""" %(url,name)        
    for id in self.getDesigner(obj):
        event.notify(TodoitemWillCreateEvent(title=title,userid=id,text=text))
    

    
    # admin by pass

def getDesigners(node):
    """fetch the current node's product designer list.
    if the current node has been set product designer,
    then fetch from the parent node"""
    
    dl = node.designer
    portal = api.portal.get()
    while dl == ():
        node = aq_parent(node)
        if node == portal:return ()
        dl = node.designer
    return dl
        