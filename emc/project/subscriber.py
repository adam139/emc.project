#-*- coding: UTF-8 -*-
from plone import api
from zope.event import notify
from zope.component import adapter
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from Acquisition import aq_parent
from zope.component import getMultiAdapter
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from emc.project.content.projectfolder import IProjectFolder
from emc.project.content.project import IProject
from emc.project.content.team import ITeam
from emc.project.content.document import IDocument
from emc.project.behaviors.localroles import Ilocalroles
from emc.project.behaviors.dynamic_role_users import IDynamicUsers
from emc.project.behaviors.users_sent import ISending

from emc.policy.portlets import navigation

from emc.memberArea.events import TodoitemWillCreateEvent
from zope.container.interfaces import IContainerModifiedEvent
#fire todoitemwillcreated event for every designer when add or modified product designer on project node
#@adapter(ITeam, IObjectAddedEvent)
def rolesAssianed(obj,event):
    "new create node,send the notify"
    filteAndSend(obj)
    
#@adapter(ITeam, IObjectModifiedEvent)
def roleModified(obj,event):
    """Project team has been modified subscriber's handler.
    obj: team instance,a project node
    event:objectModifiedevent
    todo:build a receivers list to avoid send repeat  """   

    if IContainerModifiedEvent.providedBy(event):
        return    
    filteAndSend(obj)

def filteAndSend(obj):
    "Those users been sent before this action should be filter"    
    nodeusers = getDesigners(obj)
#     import pdb
#     pdb.set_trace()
    saved = savedusers(obj)
    availabe = list(set(nodeusers) - set(saved))
    for user in availabe:
        sendTodoitem(obj,user)
        adapter = ISending(obj)
        if adapter != None:adapter.addSender(user) 

def sendTodoitem(obj,userid): 
    name = obj.title
    url = obj.absolute_url()
    sender = obj.creators[0]
   
    if ITeam.providedBy(obj):
        title = u"你已经被邀请加入%s项目组" % name
        title = title.encode("utf-8")
        text = u"""<p>详细情况请查看<a href="%s"><strong>%s项目组</strong></a></p>""" %(url,name)
    else:
        title = u"你已经被邀请加入%s项目" % name
        title = title.encode("utf-8")
        text = u"""<p>详细情况请查看<a href="%s"><strong>%s项目</strong></a></p>""" %(url,name)        
#     for id in getDesigners(obj):
    notify(TodoitemWillCreateEvent(title=title,userid=userid,sender=sender,text=text))
    #fetch product designer list
def savedusers(obj):
    "return obj's user list that user had been sent notify before this"
    adapter = ISending(obj)
    if adapter == None:return []
    return adapter.sent

def getDesigners(node):
    """fetch the current node's product designer list.
    if the current node has been not set product designer,
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

def getProject(obj):
    "obj is a object of the project path"
    while not IProject.providedBy(obj):
        obj = aq_parent(obj)
    return obj

## workflow event handler from status:pendingview to published  or pendingprocess to review
@adapter(IDocument, IAfterTransitionEvent)
def Review(doc, event):
    "handler from status:pendingview to published(owner action) or pendingprocess to review"

    state = event.new_state.getId()
#     import pdb
#     pdb.set_trace()   
    if state == "pendingview":
        old = event.old_state.getId()
        id = doc.creators[0]
        sender = api.user.get_current().id
        name = safe_unicode(doc.title)
        url = doc.absolute_url()
        text = u"""<p>详细情况请点击查看：<a href="%s"><strong>%s</strong></a></p>""" %(url,name)                
        if old =="pendingview":
            name = u"我已阅读了文档：%s" % name
            title = name.encode("utf-8")
            notify(TodoitemWillCreateEvent(title=title,userid=id,sender=sender,text=text))
    if state == "review":
        old = event.old_state.getId()
        id = doc.creators[0]
        sender = api.user.get_current().id
        name = safe_unicode(doc.title)
        url = doc.absolute_url()
        text = u"""<p>详细情况请点击查看：<a href="%s"><strong>%s</strong></a></p>""" %(url,name)
        if old =="pendingprocess":       
            name = u"我已编辑了文档：%s" % name
            title = name.encode("utf-8")
            notify(TodoitemWillCreateEvent(title=title,userid=id,sender=sender,text=text))
                        
            

## workflow event handler receive front end select next processor 
#handler for draft to pendingview or draft to pendingprocess
@adapter(IDocument, IAfterTransitionEvent)
def AssignCreate(doc, event):
    "assign the selected user to a local roles and send todoitem notify"

    state = event.new_state.getId()  
    # notify designer to view the doc

    if state == "pendingview":
        users = doc.users
        creator = doc.creators[0]
        name = doc.title
        url = doc.absolute_url()
        text = u"""<p>详细情况请点击查看：<a href="%s"><strong>%s</strong></a></p>""" %(url,name)         
        title = u"请查阅下发的文档资料：%s" % name
        title = title.encode("utf-8")
        pjt = getProject(doc) 
        for id in users:
            # assign Reader to users
            pjt.manage_setLocalRoles(id, ['ProjectReader'])
#             doc.manage_setLocalRoles(id, ['ProjectReader'])
            # send create todoitem event
            notify(TodoitemWillCreateEvent(title=title,userid=id,sender=creator,text=text))
        doc.reindexObject()        
                           
    elif state == "pendingprocess":
        old = event.old_state.getId()
        users = doc.users
        creator = doc.creators[0]
        name = safe_unicode(doc.title)
        url = doc.absolute_url()
        text = u"""<p>详细情况请点击查看：<a href="%s"><strong>%s</strong></a></p>""" %(url,name)        
        if old != "review":        
            title = u"请查阅下发的文档资料：%s，及时填写并反馈" % name
        else:
            title = u"请再次查阅下发的文档资料：%s，参考审阅意见，及时完善并反馈" % name
        title = title.encode("utf-8")
        pjt = getProject(doc)
        for id in users:
            # assign Reader to users
            pjt.manage_setLocalRoles(id, ['Editor','ProjectReader'])
#             doc.manage_setLocalRoles(id, ['Editor','ProjectReader'])
            api.user.grant_roles(username=id,roles=['Reader'])
            # send create todoitem event
            notify(TodoitemWillCreateEvent(title=title,userid=id,sender=creator,text=text))
    else:
        pass     


## workflow event handler binding to container node
@adapter(IDocument, IAfterTransitionEvent)
def createTodoitem(doc, event):
    "generate todoitem when switch document workflow status "
    
    state = event.new_state.getId()  
    # notify designer to view the doc
    node = aq_parent(doc)
    name = doc.title
    sender = doc.creators[0]
    url = doc.absolute_url()

    text = u"""<p>详细情况请点击查看：<a href="%s"><strong>%s</strong></a></p>""" %(url,name) 
    if state == "pendingview":        
        title = u"请查阅下发的文档资料：%s" % name
        title = title.encode("utf-8")

        for id in getDesigners(node):
#             import pdb
#             pdb.set_trace()            
            notify(TodoitemWillCreateEvent(title=title,userid=id,sender=sender,text=text))
            
    elif state == "pendingprocess":
        title = u"请查阅下发的文档资料：%s，并反馈" % name
        title = title.encode("utf-8")
        for id in self.getDesigner(obj):

            notify(TodoitemWillCreateEvent(title=title,userid=id,sender=sender,text=text))
    else:
        pass                


# @grok.subscribe(IProject, IObjectAddedEvent)
def addProjectNavPortlet(obj, event):
    """Event handler triggered when adding a project folder. This will add
    the project navigator portlet automatically.
    """
     
    parent = aq_parent(obj)
    if IProjectFolder.providedBy(parent):
        return
    
    # A portlet manager is akin to a column
    column = getUtility(IPortletManager, name=u"plone.leftcolumn")
    
    # We multi-adapt the object and the column to an assignment mapping,
    # which acts like a dict where we can put portlet assignments
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    
    # We then create the assignment and put it in the assignment manager,
    # using the default name-chooser to pick a suitable name for us.
    assignment = navigation.Assignment()
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment        