#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from Acquisition import aq_inner
from five import grok
from DateTime import DateTime
from emc.project import viewReport

class Macros(BrowserView):

    template = ViewPageTemplateFile('templates/macros.pt')

    @property
    def macros(self):
        return self.template.macros

    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm

    def canbeRead(self):
#        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission(viewReport,self.context)
        return canbe

    def hasSummaryView(self):
        try:
            sview = getMultiAdapter((self.context, self.request),name=u"summary_view")
        except:
            sview = None
        return  (sview is not None)
    
    def hasListingView(self):
        try:
            sview = getMultiAdapter((self.context, self.request),name=u"listing_view")
        except:
            sview = None
        return  (sview is not None)    
    
    def text_to_html(self, text):
        text = text or ''
        pt = getToolByName(self.context, 'portal_transforms')
        return pt.convertTo('text/html', text, mimetype='text/plain').getData()

    def timedelta(self, start, end):
        if isinstance(start, DateTime):
            start=start.asdatetime()
        if isinstance(end, DateTime):
            end=end.asdatetime()
        return start-end


