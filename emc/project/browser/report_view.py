#-*- coding: UTF-8 -*-
# from five import grok
from Acquisition import aq_inner
from Acquisition import aq_base
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
from plone.app.contenttypes.browser.folder import FolderView

from emc.project import _
from Products.CMFPlone import PloneMessageFactory as _p

# grok.templatedir('templates')

class ReportView(FolderView):
    "emc report view"

    def report(self,obj):
        textfield = getattr(aq_base(obj), 'report', None)
        text = getattr(textfield, 'output', None)
        if text:
            self.text_class = 'stx' if textfield.mimeType in (
                'text/structured', 'text/x-rst', 'text/restructured'
            ) else 'plain'
        return text
      
    
  
