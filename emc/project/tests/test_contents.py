import unittest as unittest

from emc.project.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
#from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('emc.project.projectFolder', 'folder1')
        portal['folder1'].invokeFactory('emc.project.project', 'project1')  
        portal['folder1']['project1'].invokeFactory('emc.project.team', 'team1')
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.doc', 'audit1') 
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.analysisDoc', 'analysis1') 
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.diagnoseDoc', 'dia1') 
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.designDoc', 'des1')                                                 

        self.portal = portal
    
    def test_item_types(self):
        self.assertEqual(self.portal['folder1'].id,'folder1')
        self.assertEqual(self.portal['folder1']['project1'].id,'project1')   
        self.assertEqual(self.portal['folder1']['project1']['team1'].id,'team1')
        self.assertEqual(self.portal['folder1']['project1']['team1']['audit1'].id,'audit1')
#         self.assertEqual(self.portal['folder1']['project1']['team1']['analysis1'].id,'analysis1') 
#         self.assertEqual(self.portal['folder1']['project1']['team1']['dia1'].id,'dia1') 
#         self.assertEqual(self.portal['folder1']['project1']['team1']['des1'].id,'des1')                                             
        
        
        