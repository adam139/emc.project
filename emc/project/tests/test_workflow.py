#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from emc.project.testing import FUNCTIONAL_TESTING
from emc.project.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles,logout
from plone.testing.z2 import Browser
import unittest

from Products.CMFCore.utils import getToolByName

class TestView(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
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
        portal['folder1']['project1']['team1'].invokeFactory('emc.bokeh.fearture', 'fearture1',
                                                             text=u"here is rich text",
                                                             title="analysis document")            
        self.portal = portal                               
    
    def test_project_workflow(self):
        # m/c/s/d chain
        app = self.layer['app']
        portal = self.layer['portal']
      
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        page = portal['folder1']['project1'].absolute_url() + '/@@view'        

        browser.open(page)
        outstr = "submit to chuyang"
      
        self.assertTrue(outstr in browser.contents)            
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang', comment='submit to chu yang' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang')
        
        browser.open(page)
        outstr = "submit to shiyang"      
        self.assertTrue(outstr in browser.contents)         
                 
        wf.doActionFor(dummy, 'submit2shiyang', comment='submit to shiyang')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'shiyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to shiyang')
        
        browser.open(page)
        outstr = "submit to dingxing"      
        self.assertTrue(outstr in browser.contents)           
        
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing')               
 
    def test_team_workflow(self):
        # m/c/z/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang', comment='submit to chu yang' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang')
                 
        wf.doActionFor(dummy, 'submit2zhengyang', comment='submit to zhengyang')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'zhengyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to zhengyang')   
        
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing')         
            
    def test_design_doc_workflow(self):
        # m/c1/c2/s1/s2/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']['design1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang1', comment='submit to chu yang1' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang1')
        
        wf.doActionFor(dummy, 'submit2chuyang2', comment='submit to chu yang2' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang2')        
                 
        wf.doActionFor(dummy, 'submit2shiyang1', comment='submit to shiyang1')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'shiyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to shiyang1')
        wf.doActionFor(dummy, 'submit2shiyang2', comment='submit to shiyang2')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'shiyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to shiyang2')            
        
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing') 

    def test_analysis_doc_workflow(self):
        # m/c1/c2/z1/z2/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']['analysis1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang1', comment='submit to chu yang1' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang1')
        
        wf.doActionFor(dummy, 'submit2chuyang2', comment='submit to chu yang2' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang2')        
                 
        wf.doActionFor(dummy, 'submit2zhengyang1', comment='submit to zhengyang1')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'zhengyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to zhengyang1')
        wf.doActionFor(dummy, 'submit2zhengyang2', comment='submit to zhengyang2')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'zhengyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to zhengyang2')            
        
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing') 
     
    def test_audit_doc_workflow(self):
        # m/c1/c2/s/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']['audit1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang1', comment='submit to chu yang1' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang1')
        
        wf.doActionFor(dummy, 'submit2chuyang2', comment='submit to chu yang2' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang2')        
                 
        wf.doActionFor(dummy, 'submit2shiyang', comment='submit to shiyang')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'shiyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to shiyang')
                 
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing')       

    def test_diagnose_doc_workflow(self):
        # m/c1/c2/z/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']['diagnose1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang1', comment='submit to chu yang1' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang1')
        
        wf.doActionFor(dummy, 'submit2chuyang2', comment='submit to chu yang2' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang2')        
                 
        wf.doActionFor(dummy, 'submit2zhengyang', comment='submit to zhengyang')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'zhengyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to zhengyang')
                 
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing')

    def test_fearture_doc_workflow(self):
        # m/c/z1/z2/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']['fearture1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_project_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'fangan')        
        wf.doActionFor(dummy, 'submit2chuyang', comment='submit to chu yang' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'chuyang')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to chu yang')     
     
                 
        wf.doActionFor(dummy, 'submit2zhengyang1', comment='submit to zhengyang1')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'zhengyang1')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to zhengyang1')
        wf.doActionFor(dummy, 'submit2zhengyang2', comment='submit to zhengyang2')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'zhengyang2')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to zhengyang2')            
        
        wf.doActionFor(dummy, 'submit2dingxing', comment='submit to dingxing')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'dingxing')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to dingxing')       
   