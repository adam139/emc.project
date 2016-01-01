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

# from plone.app.contenttypes.interfaces import IFolder,IDocument
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
    adapts(Interface)
#     adapts(IFolder)    
#     adapts(IProject)    
    enabled = [Ilocalroles]

    def __init__(self, context):
        self.context = context
    
    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerateBehaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)

  


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
        membership.addMember('member4', 'secret', ('Member',), ())
        membership.addMember('member5', 'secret', ('Member',), ())         
                
        provideAdapter(AssignRoles)
        portal.invokeFactory('emc.project.projectFolder','folder1')        
        portal['folder1'].invokeFactory('emc.project.project','project1')
        portal['folder1']['project1'].invokeFactory('emc.project.team','team1')
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.team','team1_1')                
 
         
         # 给元组赋值时，单个值要加","
        Ilocalroles(portal['folder1']['project1']).emc_designer = ('member1',)
        Ilocalroles(portal['folder1']['project1']).reader7 = ('member4',)
# the third members        
        Ilocalroles(portal['folder1']['project1']).reader8 = ('member5',)
         #child will  inherit parents sets.
        Ilocalroles(portal['folder1']['project1']['team1']).designer = ('member2',)
      
        Ilocalroles(portal['folder1']['project1']['team1']).reader1 = ('member3',)
        
       
         
        import transaction
        transaction.commit()                       
        acl_users = getToolByName(portal, 'acl_users')
        member1 = acl_users.getUserById('member1')
        member2 = acl_users.getUserById('member2')
        member3 = acl_users.getUserById('member3')
        member4 = acl_users.getUserById('member4')
        member5 = acl_users.getUserById('member5')        
        
# local roles will inherit parent object.        
# member1 is emc designer,it is Manager role in all child objects
        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['project1']))
        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['project1']['team1']))        
        self.assertTrue('Manager' in member1.getRolesInContext(portal['folder1']['project1']['team1']['team1_1']))                                                

# member2 is designer,it has Contributor role and Editor role in all child objects  
        self.assertFalse('Reader' in member2.getRolesInContext(portal['folder1']['project1']))    
        self.assertTrue('Contributor' in member2.getRolesInContext(portal['folder1']['project1']['team1']))   
        self.assertTrue('Editor' in member2.getRolesInContext(portal['folder1']['project1']['team1']))
        self.assertTrue('Contributor' in member2.getRolesInContext(portal['folder1']['project1']['team1']['team1_1']))        
        self.assertTrue('Editor' in member2.getRolesInContext(portal['folder1']['project1']['team1']['team1_1']))                  

# member3 is reader,it has Reader role in all child objects  
        self.assertFalse('Reader' in member3.getRolesInContext(portal['folder1']['project1']))    
        self.assertTrue('Reader' in member3.getRolesInContext(portal['folder1']['project1']['team1']))  
        self.assertTrue('Reader' in member3.getRolesInContext(portal['folder1']['project1']['team1']['team1_1']))
# member4 is the first members,it is Reader role in all child objects
        self.assertTrue('Reader' in member4.getRolesInContext(portal['folder1']['project1']))
        
# member5 is the third members,it is TempReader role in all child objects,not Reader role
        self.assertFalse('Reader' in member5.getRolesInContext(portal['folder1']['project1']))

        self.assertTrue('EMCExpert' in member5.getRolesInContext(portal['folder1']['project1']))                        
                
 