#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides, Interface

from plone.directives import form
from zope import schema

from plone.formwidget.autocomplete.widget import AutocompleteMultiFieldWidget

from borg.localrole.interfaces import ILocalRoleProvider
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog

from emc.project import  _

class Ilocalroles(form.Schema):
    """
    Description of the localroles
    source 字段不能有缺省值的
    """
    form.widget(Manager=AutocompleteMultiFieldWidget)
#    form.write_permission(Manager='iz.EditOfficialReviewers')
    Editor = schema.Tuple(
        title=_(u"Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    Reader1 = schema.Tuple(
        title=_(u"Commander"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    Reader2 = schema.Tuple(
        title=_(u"Deputy Commander"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    Reader3 = schema.Tuple(
        title=_(u"Chief Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )     
    Reader4 = schema.Tuple(
        title=_(u"Deputy Chief Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )    
    Reader5 = schema.Tuple(
        title=_(u"Chief quality engineer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    ) 
    Reader6 = schema.Tuple(
        title=_(u"Deputy Chief quality engineer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    Reader7 = schema.Tuple(
        title=_(u"process staff"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )   
    Reader8 = schema.Tuple(
        title=_(u"quality manage staff"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )   
    Reader9 = schema.Tuple(
        title=_(u"dispatch staff"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )                               
    Manager = schema.Tuple(
        title=_(u"Manager"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    Reviewer = schema.Tuple(
        title=_(u"Reviewer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )    
    Reader10 = schema.Tuple(
        title=_(u"EMC expert"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )        
    form.fieldset(
                  'permission',
                  label=_(u'permissions'),
                  fields=['Editor','Reader1','Reader2','Reader3','Reader4','Reader5','Reader6'],
                  )
    form.fieldset(
                  'other permissions',
                  label=_(u'the third user permission'),
                  fields=['Manager','Reviewer','Reader7','Reader8','Reader9','Reader10'],
                  )    

alsoProvides(Ilocalroles, form.IFormFieldProvider)
       
class IlocalrolesMarker(Interface):
    """Marker interface that will be provided by instances using the
    Ilocalroles behavior. The ILocalRoleProvider adapter is registered for
    this marker.
    """
    
class AddLocalRoles(grok.Adapter):
    
    grok.implements(ILocalRoleProvider)
    grok.context(IlocalrolesMarker)
    
    
    def __init__(self, context):
        self.context = context
        self.readers = set()
    
    def getReaders(self):
        if self.readers != set(): return self.readers
        localrole = Ilocalroles(self.context, None)
        if localrole == None:return set()
        tp = set()
        for i in xrange(1,11):

            attrname = 'Reader%s' % i
#             import pdb
#             pdb.set_trace()
            item = getattr(localrole , attrname, ())
            if type(item) == type(''):
                tp.add(item)
            else:
            # set join set
                tp = set(getattr(localrole , attrname, ())) | tp 

        self.readers = tp
        return tp         
        
        
    def getRoles(self, principal_id):
        """If the user is in the list of Reviewers for this item, grant
        the Reader, Editor and Contributor local roles.
        """
#        import pdb
#        pdb.set_trace()
        localrole = Ilocalroles(self.context, None)

        roles = set()
  
        if principal_id in localrole.Manager:
            roles.add('Manager')

        if principal_id in localrole.Editor:
            roles.add('Editor')
          
            
        if principal_id in self.getReaders():
            roles.add('Reader')
        return roles
        
    def getAllRoles(self):
        """Return a list of tuples (principal_id, roles), where roles is a
        list of roles for the given user id.
        """

        localrole = Ilocalroles(self.context, None)

        if localrole is None  or (not localrole.Manager and not localrole.Reviewer \
                                   and not localrole.Editor and not self.getReaders()):
            return       


        for principal_id in localrole.Manager:
            yield (principal_id, ('Manager',),)

        for principal_id in localrole.Reviewer:
            yield (principal_id, ('Reviewer',),)
        for principal_id in localrole.Editor:
            yield (principal_id, ('Editor',),)
        for principal_id in self.getReaders():
            yield (principal_id, ('Reader',),)

            
class localrolesIndexer(grok.MultiAdapter):
    """Catalog indexer for the 'localroles' index.
    """
    grok.implements(IIndexer)
    grok.adapts(IlocalrolesMarker, IZCatalog)
    grok.name('localManager')
   
    def __init__(self, context, catalog):
        self.localroles = Ilocalroles(context)
   
    def __call__(self):
        Manager = self.localroles.Manager or ()
        return tuple(set(Manager))