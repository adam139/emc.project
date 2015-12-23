#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from emc.project.testing import FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest 
from plone.namedfile.file import NamedImage
import os
import datetime

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
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.auditDoc', 'audit1',
                                                             text=u"here is rich text",
                                                             title="analysis document",
                                                             report="this is report")  
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.analysisDoc', 'analysis1',
                                                             text=u"here is rich text",
                                                             title="analysis document",
                                                             report="this is report") 
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.designDoc', 'design1',
                                                             text=u"here is rich text",
                                                             title="analysis document",
                                                             report="this is report")  
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.diagnoseDoc', 'diagnose1',
                                                             text=u"here is rich text",
                                                             title="analysis document",
                                                             report="this is report")       
            
        self.portal = portal
             
    def test_projectfolderview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "this is project folder"
        outstr2 = "project folder"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)
        
    def test_projectview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "this is project"
        outstr2 = "project"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)        

    def test_teamview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1']['team1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "this is team"
        outstr2 = "team is permission defense container"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)
        
    def test_auditview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1']['team1']['audit1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "here is rich text"
        outstr2 = "this is report"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)
    def test_analysisview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1']['team1']['analysis1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "here is rich text"
        outstr2 = "this is report"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)
    def test_designview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1']['team1']['design1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "here is rich text"
        outstr2 = "this is report"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)
    def test_diagnoseview(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1']['team1']['diagnose1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "here is rich text"
        outstr2 = "this is report"       
        self.assertTrue(outstr in browser.contents)        
        self.assertTrue(outstr2 in browser.contents)                        
