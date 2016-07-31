#-*- coding: UTF-8 -*-
# from five import grok
from Acquisition import aq_inner
from z3c.form import field
from plone.directives import dexterity
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from plone.app.customerize import registration
from emc.project.content.project import IProject
from emc.project.content.team import ITeam
from Products.Five.browser import BrowserView
# from plone.app.contenttypes.browser.folder import FolderView

from emc.project import _
from Products.CMFPlone import PloneMessageFactory as _p

# grok.templatedir('templates')

class ProjectView(BrowserView):
    "emc analysis doc view"
#     grok.context(IProject)
#     grok.template('project_view')
#     grok.name('view')
#     grok.require('emc.project.view_project') 

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm
    
    def wf(self):
        context = aq_inner(self.context)
        wf = getToolByName(context, 'portal_workflow')
        return wf    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission("emc.project.add_project",self.context)
    
    def getText(self):
        raw = self.context.text
        return raw
    
    def workflow_state(self):
        "workflow status"
        review_state = self.wf().getInfoFor(self.context, 'review_state')
        return review_state        
    
    @memoize       
    def getAllTeams(self):
#         import pdb
#         pdb.set_trace()
        query = {"object_provides":ITeam.__identifier__,
                 'path': '/'.join(self.context.getPhysicalPath())}
        brains = self.catalog()(query)
        return self.output(brains)
        
    def output(self,braindata):
        "根据参数total,braindata,返回jason 输出"
        outhtml = ""      
        k = 0
        for i in braindata:

            status =  self.context.translate(_p(i.review_state))         
            out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-3 text-left"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-6 text-left">%(description)s</td>
                                <td class="col-md-1 text-center">%(status)s</td>
                                <td class="col-md-1 text-center">%(date)s</td>                                
                            </tr> """% dict(objurl="%s/@@view" % i.getURL(),
                                            num=str(k + 1),
                                            title=i.Title,
                                            description= i.Description,
                                            status = status.encode('utf-8'),
                                            date = i.created.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1           
       
        return outhtml         
    
### load viewlet
    def __getitem__(self,name):
        viewlet = self.setUpViewletByName(name)
        if viewlet is None:
            active_layers = [ str(x) for x in self.request.__provides__.__iro__]
            active_layers = tuple(active_layers)
            raise RuntimeError("Viewlet does not exist by name %s for the active theme "% name)
        viewlet.update()
        return viewlet.render()
    
    def getViewletByName(self,name):
        views = registration.getViews(IBrowserRequest)
        for v in views:
            if v.provided == IViewlet:
                if v.name == name:
#                    if str(v.required[1]) == '<InterfaceClass plone.app.discussion.interfaces.IDiscussionLayer>':
                        return v
        return None
    
    def setUpViewletByName(self,name):
        context = aq_inner(self.context)
        request = self.request
        reg = self.getViewletByName(name)
        if reg == None:
            return None
        factory = reg.factory
        try:
            viewlet = factory(context,request,self,None).__of__(context)
        except TypeError:
            raise RuntimeError("Unable to initialize viewlet %s. Factory method %s call failed."% name)
        return viewlet    
