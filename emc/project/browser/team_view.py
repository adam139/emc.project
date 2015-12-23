#-*- coding: UTF-8 -*-
from five import grok
from z3c.form import field
from plone.directives import dexterity
from plone.memoize.instance import memoize
from emc.project.content.team import ITeam


from emc.project import _

grok.templatedir('templates')

class TeamView(grok.View):
    "emc analysis doc view"
    grok.context(ITeam)
    grok.template('team_view')
    grok.name('view')
    grok.require('zope2.View') 

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
    
                    


