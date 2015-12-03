#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from emc.bokeh.testing import FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest as unittest
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

        portal.invokeFactory('emc.bokeh.fearture', 'fearture1',
                            title="fearture1",description="demo fearture")     
            
        self.portal = portal     

        
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/fearture1'        
        page = obj + '/@@fview'
#        import pdb
#        pdb.set_trace()
        browser.open(page)

        outstr = '<section class="plot">'

        
        self.assertTrue(outstr in browser.contents)
        
