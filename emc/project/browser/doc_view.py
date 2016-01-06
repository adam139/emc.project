#-*- coding: UTF-8 -*-
from five import grok
from z3c.form import field
from plone.directives import dexterity
from plone.memoize.instance import memoize
from emc.project.content.AnalysisDoc import IAnalysisDoc
from emc.project.content.AuditDoc import IAuditDoc
from emc.project.content.DesignDoc import IDesignDoc
from emc.project.content.DiagnoseDoc import IDiagnoseDoc

from emc.project import _

grok.templatedir('templates')

class DocView(grok.View):
    "emc analysis doc view"
    grok.context(IAnalysisDoc)
    grok.template('analysis_view')
    grok.name('view')
    grok.require('emc.project.view_doc') 

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
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
    
    def getText(self):
        raw = self.context.text
        return raw
    
class AuditDocView(DocView):
    grok.context(IAuditDoc)
    grok.template('audit_view') 
class DesignDocView(DocView):
    grok.context(IDesignDoc)
    grok.template('design_view')
    
class DiagnoseDocView(DocView):
    grok.context(IDiagnoseDoc)
    grok.template('diagonose_view')                      


