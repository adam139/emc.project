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
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from borg.localrole.interfaces import ILocalRoleProvider
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog
#from eisoo.operation.areamanaged import Iareamanaged
#from eisoo.operation.area import Iarea
#from plone.app.vocabularies.users import UsersSource
from emc.project import MessageFactory as _

class Ilocalroles(form.Schema):
    """
    Description of the localroles
    source 字段不能有缺省值的
    """
    form.widget(Manager=AutocompleteMultiFieldWidget)
#    form.write_permission(Manager='iz.EditOfficialReviewers')
    Manager = schema.Tuple(
        title=_(u"Manager"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source="plone.principalsource.Users",),
        required=False
    )
    form.widget(Reviewer=AutocompleteMultiFieldWidget)
#    form.write_permission(Reviewer='iz.EditOfficialReviewers')
    Reviewer = schema.Tuple(
        title=_(u"Reviewer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source="plone.principalsource.Users",),
        required=False
    )
    form.widget(Editor=AutocompleteMultiFieldWidget)
#    form.write_permission(Editor='iz.EditOfficialReviewers')
    Editor = schema.Tuple(
        title=_(u"Editor"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source="plone.principalsource.Users",),
        required=False
    )
    form.widget(Reader=AutocompleteMultiFieldWidget)
#    form.write_permission(Reader='iz.EditOfficialReviewers')
    Reader = schema.Tuple(
        title=_(u"Reader"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source="plone.principalsource.Users",),
        required=False
    )
    
    form.fieldset(
                  'manager',
                  label=_(u'manage'),
                  fields=['Manager','Reviewer','Editor','Reader'],
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
    
    def getRoles(self, principal_id):
        """If the user is in the list of Reviewers for this item, grant
        the Reader, Editor and Contributor local roles.
        """
#        import pdb
#        pdb.set_trace()
        localrole = Ilocalroles(self.context, None)
        name = self.context.name
        catalog = getToolByName(self.context, 'portal_catalog')
        areaobject = catalog(id = name )

        if len(areaobject)==0:
            return set()

        else:
            area = areaobject[0].getObject()
        roles = set()
        if area.responsible_person is not None :
            if  principal_id in area.responsible_person :
                roles.add('area_manager')

        if area.bussiness_person is not None  :
            if  principal_id in area.bussiness_person:
                roles.add('bussiness_person')
        if area.channel_charger is not None:
            if principal_id in area.channel_charger:
                roles.add('channel manager')
        if area.product_manager is not None :
            if principal_id in area.product_manager :
                roles.add('product_manager')
        if area.support_charger is not None :
            if principal_id in area.support_charger :
                roles.add('product_manager')   
        if principal_id in localrole.Manager:
            roles.add('Manager') 
        if principal_id in localrole.Reviewer:         
            roles.add('Reviewer')
        if principal_id in localrole.Editor:
            roles.add('Editor')
        if principal_id in localrole.Reader :
            roles.add('Reader')
        return roles
        
    def getAllRoles(self):
        """Return a list of tuples (principal_id, roles), where roles is a
        list of roles for the given user id.
        """
#        import pdb
#        pdb.set_trace()
        localrole = Ilocalroles(self.context, None)
        name = self.context.name
        catalog = getToolByName(self.context, 'portal_catalog')
        areaobject = catalog(id = name )
        if len(areaobject)==0:
            return
        else:
            area = areaobject[0].getObject()

        if localrole is None and area is None or (not localrole.Manager and not localrole.Reviewer and not localrole.Editor \
                         and not localrole.Reader and not area.support_charger and not area.channel_charger  
                         and not area.product_manager and not area.bussiness_person and not area.responsible_person ):
            return
        
#        seen = set ()
#        for principal_id in localrole.Manager:
##            seen.add(principal_id)
#            yield (principal_id, ('area_manager'),)
        if area.responsible_person is not None:
            for principal_id in area.responsible_person:
                yield (principal_id,('area_manager',))                
        if area.bussiness_person is not None:
            for principal_id in area.bussiness_person:
                yield (principal_id, ('bussiness_person',),)
        if area.product_manager is not None:
            for principal_id in area.product_manager :
                yield (principal_id, ('product_manager',),)
        if area.support_charger is not None:
            for principal_id in area.support_charger :
                yield (principal_id, ('product_manager',),)
        if area.channel_charger is not None:
            for principal_id in area.channel_charger:
                yield (principal_id, ('channel manager',),)
        for principal_id in localrole.Manager:
            yield (principal_id, ('Manager',),)
        for principal_id in localrole.Reviewer:
            yield (principal_id, ('Reviewer',),)
        for principal_id in localrole.Editor:
            yield (principal_id, ('Editor',),)
        for principal_id in localrole.Reader:
            yield (principal_id, ('Reader',),)

            
class localrolesIndexer(grok.MultiAdapter):
    """Catalog indexer for the 'localroles' index.
    """
    grok.implements(IIndexer)
    grok.adapts(IlocalrolesMarker, IZCatalog)
    grok.name('localroles')
   
    def __init__(self, context, catalog):
        self.localroles = Ilocalroles(context)
   
    def __call__(self):
        Manager = self.localroles.Manager or ()
        Reviewer = self.localroles.Reviewer or ()
        Editor = self.localroles.Editor or ()
        Reader = self.localroles.Reader or ()
#        responsible_person = self.localroles.responsible_person or ()
#        bussiness_person = self.localroles.bussiness_person or ()
#        product_manager = self.localroles.product_manager or ()
#        channel_charger = self.localroles.channel_charger or ()
#        support_charger = self.localroles.support_charger or ()
        return tuple(set(Manager + Reviewer + Editor + Reader ))