#-*- coding: UTF-8 -*-
from plone import api

from zope.component import provideAdapter,adapts,queryUtility
from zope.event import notify
from emc.project.behaviors.localroles import Ilocalroles
from emc.project.testing import FUNCTIONAL_TESTING
from emc.project.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles,logout
from plone.testing.z2 import Browser
import unittest

from Products.CMFCore.utils import getToolByName
from emc.memberArea.events import BackMessageCreatedEvent
from emc.project.tests.test_localroles import AssignRoles,AssignUsers

class TestView(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('Folder', 'Members',
                             title=u"this is memberarea folder",
                             description=u"members folder")        
        pm = getToolByName(portal, 'portal_membership')
        pm.addMember('member1', 'secret', ('Member',), ())
        pm.addMember('member2', 'secret', ('Member',), ())
        pm.addMember('member3', 'secret', ('Member',), ()) 
        pm.addMember('member4', 'secret', ('Member',), ())
        pm.addMember('member5', 'secret', ('Member',), ())
        pm.memberareaCreationFlag = True
        for i in range(5):
            j = str(i + 1)
            username = 'member%s' % j            
            user = api.user.get(username=username)
            pm.createMemberarea(member_id= username)
            notify(BackMessageCreatedEvent(user))
        
        provideAdapter(AssignRoles)
        provideAdapter(AssignUsers)        
        

        portal.invokeFactory('emc.project.projectFolder', 'folder1',
                             title=u"this is project folder",
                             description=u"project folder")
        
                             
        portal['folder1'].invokeFactory('emc.project.project', 'project1',
                                        title=u"this is project",
                                        description=u"project")  
        portal['folder1']['project1'].invokeFactory('emc.project.team', 'team1',
                                                    title=u"this is team",
                                                    description="team is permission defense container")
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.doc', 'doc1',
                                                             text=u"here is rich text",
                                                             title="project document",
                                                             report="this is report")
        portal['folder1']['project1']['team1'].invokeFactory('Document', 'doc2',
                                                             text=u"here is rich text",
                                                             title="system document")            
     
        portal['folder1']['project1']['team1'].invokeFactory('emc.bokeh.fearture', 'fearture1',
                                                             text=u"here is rich text",
                                                             title="analysis document")
        portal['folder1']['project1']['team1'].invokeFactory('emc.bokeh.codefile', 'code2file1',
                                                             text=u"code to file",
                                                             title="code file")                     
        Ilocalroles(portal['folder1']['project1']).emc_designer = ('member1',)
        Ilocalroles(portal['folder1']['project1']).reader7 = ('member4',)
# the third members        
        Ilocalroles(portal['folder1']['project1']).reader8 = ('member5',)
         #child will  inherit parents sets.
        Ilocalroles(portal['folder1']['project1']['team1']).designer = ('member2',)
        portal['folder1']['project1']['team1']['doc1'].users = ('member2',)           
        
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
            
    def test_project_doc_workflow(self):
        # m/c1/c2/s1/s2/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_doc_workflow
        import pdb
        pdb.set_trace()
        dummy = portal['folder1']['project1']['team1']['doc1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_doc_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'draft')        
        wf.doActionFor(dummy, 'submit2designer4view', comment='submit to designer for view' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pendingview')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to designer for view')
        
        wf.doActionFor(dummy, 'submit2publish', comment='designer submit to public' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'public')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'designer submit to public')        

    def test_sys_doc_workflow(self):
        # m/c1/c2/s1/s2/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_doc_workflow
        dummy = portal['folder1']['project1']['team1']['doc2']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_doc_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'draft')
## test 'Document' work flow                  
        wf.doActionFor(dummy, 'submit2designer4feedback', comment='submit to designer for feedback')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pendingprocess')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to designer for feedback')
        wf.doActionFor(dummy, 'feedback', comment='designer submit to public')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'public')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'designer submit to public')            
        



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
        
    def test_code2file_doc_workflow(self):
        # m/c/z1/z2/d chain
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_project_workflow
        dummy = portal['folder1']['project1']['team1']['code2file1']

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
   