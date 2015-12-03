#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides, Interface

from plone.directives import form
from zope import schema

from plone.formwidget.autocomplete.widget import AutocompleteMultiFieldWidget
from plone.z3cform.textlines import TextLinesFieldWidget
from plone.dexterity.interfaces import IDexterityContent
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from borg.localrole.interfaces import ILocalRoleProvider
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog

from eisoo.behaviors import MessageFactory as _

class IReviewers(form.Schema):
    """pass"""
#    form.mode(next_reviewer='hidden')
    next_reviewer = schema.TextLine(
        title=_(u"next_reviewer"),
#        value_type=schema.TextLine(),
#        value_type=schema.Choice(title=_(u"User id"),
#                                  source="plone.principalsource.Users",),
        required=False
    )
    next_obj= schema.Int(
                     title=_(u"next_obj"),
                     default = -1,
                     required=False
                     )

alsoProvides(IReviewers, form.IFormFieldProvider)

class IReviewersMarker(Interface):
    """Marker interface that will be provided by instances using the
    Ilocalroles behavior. The ILocalRoleProvider adapter is registered for
    this marker.
    """

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name,value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)

class Reviewers(object):
    """
       Adapter for IReviewers
    """
    implements(IReviewers)
    adapts(IReviewersMarker)

    def __init__(self,context):
        self.context = context

    def getnext(self):
        value = getattr(self.context, "next_reviewer")
        if value is None:
            return ''
        if isinstance(value,list):
            return value
        else:
            return value.split(",")
    def setnext(self,value):
        if isinstance(value,list):
            value = ",".join(value)
        else:
            pass
        setattr(self.context, "next_reviewer", value)
    def delnext(self):
        delattr(self.context, "next_reviewer")
    
    next_reviewer = property(getnext,setnext,delnext)
    next_obj = context_property('next_obj') 
          

    
class ReviewersLocalRoles(grok.Adapter):
    
    grok.implements(ILocalRoleProvider)
    grok.context(IReviewersMarker)
    
    def __init__(self, context):
        self.context = context
    
    def getRoles(self, principal_id):
        """If the user is in the list of Reviewers for this item, grant
        the Reader, Editor and Contributor local roles.
        """
        reviewer = IReviewers(self.context, None)
        roles = set()
        if principal_id in reviewer.next_reviewer:         
            roles.add('Reviewer')
        return roles
        
    def getAllRoles(self):
        """Return a list of tuples (principal_id, roles), where roles is a
        list of roles for the given user id.
        """
        reviewer = IReviewers(self.context, None)
        if reviewer is None or ( not reviewer.next_reviewer ):
            return
        
        seen = set ()

        for principal_id in reviewer.next_reviewer:
            seen.add(principal_id)
            yield (principal_id, ('Reviewer',),)


            
class localrolesIndexer(grok.MultiAdapter):
    """Catalog indexer for the 'localroles' index.
    """
    grok.implements(IIndexer)
    grok.adapts(IReviewersMarker, IZCatalog)
    grok.name('reviewers')
   
    def __init__(self, context, catalog):
        self.reviewers = IReviewers(context)
   
    def __call__(self):
        Reviewer = self.reviewer.next_reviewer or ()       
        return tuple(set(Reviewer))