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
from emc.project.content.projectfolder import IProjectFolder
from emc.project.content.project import IProject
from emc.project.content.team import ITeam

from plone.behavior.interfaces import IBehaviorAssignable,IBehavior
from five import grok

from zope.interface import implements,Interface
from zope.component import provideAdapter,adapts,queryUtility

# assign the behavior to content type
class AssignRoles(object):
    
    implements(IBehaviorAssignable)
#     adapts(Interface)
    adapts(IFolder)    
#     adapts(IProject)    
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
        membership.addMember('member1', 'secret', ('Member',), ())
        membership.addMember('member2', 'secret', ('Member',), ())
        membership.addMember('member3', 'secret', ('Member',), ()) 
               
        provideAdapter(AssignRoles)
        portal.invokeFactory('Folder','folder1')        
        portal['folder1'].invokeFactory('Document','project1')
          

        
        
        Ilocalroles(portal['folder1']).Manager = ('member1','member3')


        import transaction
        transaction.commit()
                      
        acl_users = getToolByName(portal, 'acl_users')
        member1 = acl_users.getUserById('member1')
        member2 = acl_users.getUserById('member2')
        member3 = acl_users.getUserById('member3')

#         import pdb
#         pdb.set_trace()
                                        

        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']))
        self.assertFalse('Manager' in member2.getRolesInContext(portal['folder1']))        
   
# local roles will inherit parent object.  
        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['project1']))        


class TestProjectLocalRoles(unittest.TestCase):
    
    layer =  FUNCTIONAL_TESTING
        
    def test_project_LocalRoles(self):
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        membership = getToolByName(portal, 'portal_membership')
        membership.addMember('member1', 'secret', ('Member',), ())
        membership.addMember('member2', 'secret', ('Member',), ())
        membership.addMember('member3', 'secret', ('Member',), ()) 
                
        provideAdapter(AssignRoles)
        portal.invokeFactory('emc.project.projectFolder','folder1')        
        portal['folder1'].invokeFactory('emc.project.project','project1')
        portal['folder1']['project1'].invokeFactory('emc.project.team','team1')        
 
         
         
        Ilocalroles(portal['folder1']['project1']).Manager = ('member1','member3')
        Ilocalroles(portal['folder1']['project1']['team1']).Editor = ('member2')        
 
 
        import transaction
        transaction.commit()
                       
        acl_users = getToolByName(portal, 'acl_users')
        member1 = acl_users.getUserById('member1')
        member2 = acl_users.getUserById('member2')
        member3 = acl_users.getUserById('member3')
 

        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['project1']))                                          
    
# local roles will inherit parent object.
  
        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['project1']['team1']))   
        self.assertTrue('Editor' in member2.getRolesInContext(portal['folder1']['project1']['team1'])) 
#         
#         