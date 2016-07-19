#-*- coding: UTF-8 -*-
from plone import api
from zope.event import notify
from zope.component import adapter
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from Acquisition import aq_parent
from zope.component import getMultiAdapter
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from emc.project.content.team import ITeam
from emc.project.content.document import IDocument
from emc.project.behaviors.localroles import Ilocalroles

from emc.memberArea.events import TodoitemWillCreateEvent
#fire todoitemwillcreated event for every designer when add or modified product designer on project node
@adapter(ITeam, IObjectModifiedEvent)
def roleModified(obj,event):
    """Project team has been modified subscriber's handler.
    obj: team instance,a project node
    event:objectModifiedevent """  

    #fetch product designer list 
    name = obj.title
    url = obj.absolute_url()
    import pdb
    pdb.set_trace()    
    if ITeam.providedBy(obj):
        title = u"你已经被邀请加入%s项目组" % name
        title = title.encode("utf-8")
        text = u"""<p>详细情况请查看<a href="%s"><strong>%s项目组</strong></a></p>""" %(url,name)
    else:
        title = u"你已经被邀请加入%s项目" % name
        title = title.encode("utf-8")
        text = u"""<p>详细情况请查看<a href="%s"><strong>%s项目</strong></a></p>""" %(url,name)        
    for id in getDesigners(obj):
        notify(TodoitemWillCreateEvent(title=title,userid=id,text=text))

def getDesigners(node):
    """fetch the current node's product designer list.
    if the current node has been set product designer,
    then fetch from the parent node"""
    
    dl = Ilocalroles(node).designer
    portal = api.portal.get()
#     import pdb
#     pdb.set_trace()
    while dl == None:
        node = aq_parent(node)
        if node == portal:return ()
        dl = node.designer
    return dl

## workflow event handler
@adapter(IDocument, IAfterTransitionEvent)
def createTodoitem(doc, event):
    "generate todoitem when switch document workflow status "
    
    state = event.new_state.getId()  
    # notify designer to view the doc
    node = aq_parent(doc)
    name = doc.title
    url = doc.absolute_url()

    text = u"""<p>详细情况请点击查看：<a href="%s"><strong>%s</strong></a></p>""" %(url,name) 
    if state == "pendingview":        
        title = u"请查阅下发的文档资料：%s" % name
        title = title.encode("utf-8")

        for id in getDesigners(node):
#             import pdb
#             pdb.set_trace()            
            notify(TodoitemWillCreateEvent(title=title,userid=id,text=text))
            
    elif state == "pendingprocess":
        title = u"请查阅下发的文档资料：%s，并反馈" % name
        title = title.encode("utf-8")
        for id in self.getDesigner(obj):

            notify(TodoitemWillCreateEvent(title=title,userid=id,text=text))
    else:
        pass                
        