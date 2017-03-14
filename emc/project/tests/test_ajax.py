#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from emc.project.testing import FUNCTIONAL_TESTING  

from zope.component import getUtility
from zope.interface import alsoProvides
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('emc.project.projectFolder', 'folder1',
                             title=u"this is project folder",
                             description=u"project folder")
                             
        portal['folder1'].invokeFactory('emc.project.project', 'project1',
                                        title=u"this is project",
                                        description=u"project")  
        portal['folder1']['project1'].invokeFactory('emc.project.team', 'team1',
                                                    title=u"this is team",
                                                    description="team is permission defense container")
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.auditDoc', 'audit1',
#                                                              text=u"here is rich text",
#                                                              title="analysis document",
#                                                              report="this is report")  
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.analysisDoc', 'analysis1',
#                                                              text=u"here is rich text",
#                                                              title="analysis document",
#                                                              report="this is report") 
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.designDoc', 'design1',
#                                                              text=u"here is rich text",
#                                                              title="analysis document",
#                                                              report="this is report")  
#         portal['folder1']['project1']['team1'].invokeFactory('emc.project.diagnoseDoc', 'diagnose1',
#                                                              text=u"here is rich text",
#                                                              title="analysis document",
#                                                              report="this is report")       
        portal['folder1']['project1']['team1'].invokeFactory('emc.bokeh.fearture', 'fearture1',
                                                             text=u"here is rich text",
                                                             title="analysis document")            
        self.portal = portal   
        
    def test_ajax_search(self):
        request = self.layer['request']
        from emc.theme.interfaces import IThemeSpecific
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'subject': 'submit to chuyang',
                        'actionid':'chuyang' ,                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder1']['project1']
        view = box.restrictedTraverse('@@workflow_ajax')
        result = view()
        self.assertEqual(json.loads(result)['result'],True)
        self.assertEqual(json.loads(result)['status'],u"chuyang")
        wf = getToolByName(box, 'portal_workflow')
        review_state = wf.getInfoFor(box, 'review_state')
        self.assertEqual(review_state,"chuyang")
                
        
     


             

