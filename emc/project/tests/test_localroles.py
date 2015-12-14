#-*- coding: UTF-8 -*-
import unittest
from borg.localrole.interfaces import ILocalRoleProvider

from emc.project.testing import FUNCTIONAL_TESTING
from emc.project.behavior.localroles import Ilocalroles,IlocalrolesMarker


from zope.component import createObject
from zope.interface import alsoProvides
from zope.component import provideUtility 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from Products.CMFCore.utils import getToolByName

from plone.app.contenttypes.interfaces import IFolder,IDocument
from plone.behavior.interfaces import IBehaviorAssignable,IBehavior
from five import grok

from zope.interface import implements,Interface
from zope.component import provideAdapter,adapts,queryUtility

# assign the behavior to content type
class AssignRoles(object):
    
    implements(IBehaviorAssignable)
#     adapts(Interface)
    adapts(IFolder)    
    
    enabled = [Ilocalroles]

    def __init__(self, context):
        self.context = context
    
    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerateBehaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)

class TestLocalRoles(unittest.TestCase):
    
    layer =  FUNCTIONAL_TESTING
      
    def test_LocalRoles(self):
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        membership = getToolByName(portal, 'portal_membership')
        membership.addMember('member7', 'secret', ('Member',), ())
        membership.addMember('member8', 'secret', ('Member',), ())
        
        provideAdapter(AssignRoles)
        portal.invokeFactory('Folder','folder1')        
        portal['folder1'].invokeFactory('Document','doc1')


        import transaction
        transaction.commit()

        membership.addMember('member1', 'secret', ('Member',), ())
        membership.addMember('member2', 'secret', ('Member',), ())
        membership.addMember('member3', 'secret', ('Member',), ())
        membership.addMember('member4', 'secret', ('Member',), ())
        membership.addMember('member5', 'secret', ('Member',), ())
        membership.addMember('member6', 'secret', ('Manager',), ())
        
        Ilocalroles(portal['folder1']).Manager = ('member1','member5')

              
        acl_users = getToolByName(portal, 'acl_users')
        member1 = acl_users.getUserById('member1')
        member2 = acl_users.getUserById('member2')
        member3 = acl_users.getUserById('member3')
        member4 = acl_users.getUserById('member4')
        member6 = acl_users.getUserById('member6')
        member7 = acl_users.getUserById('member7')
        member8 = acl_users.getUserById('member8')
                                        

        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']))
   
# local roles will inherit parent object.  
        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['doc1']))        


        
        